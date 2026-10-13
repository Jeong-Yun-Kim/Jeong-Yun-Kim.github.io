import { readdir, readFile, stat } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { parseHTML } from 'linkedom';

const root = resolve('dist');
const origin = 'https://jeong-yun-kim.github.io';
const errors = [];
async function walk(dir) {
  const entries = await readdir(dir, {withFileTypes:true});
  const lists = await Promise.all(entries.map(e => e.isDirectory() ? walk(join(dir,e.name)) : [join(dir,e.name)]));
  return lists.flat();
}
const files = await walk(root);
const htmlFiles = files.filter(f=>f.endsWith('.html'));
const pages = new Map();
for (const file of htmlFiles) {
  const text = await readFile(file,'utf8');
  const {document} = parseHTML(text);
  pages.set(file,document);
  const label = file.slice(root.length);
  if(document.documentElement.lang!=='ko') errors.push(`${label}: missing lang=ko`);
  if(document.querySelectorAll('h1').length!==1) errors.push(`${label}: expected exactly one h1`);
  if(!document.querySelector('main')) errors.push(`${label}: missing main`);
  if(!document.querySelector('title')?.textContent.trim()) errors.push(`${label}: missing title`);
  if(!document.querySelector('meta[name="description"]')?.getAttribute('content')) errors.push(`${label}: missing description`);
  if(!document.querySelector('meta[property="og:image"]')) errors.push(`${label}: missing Open Graph image`);
  if(!document.querySelector('link[rel="canonical"]')?.getAttribute('href')?.startsWith(origin+'/')) errors.push(`${label}: wrong canonical`);
  if(/Lorem ipsum|TODO|TBD|PLACEHOLDER/i.test(document.body.textContent)) errors.push(`${label}: unfinished text`);
  if(/010[- ]?\d{4}[- ]?\d{4}|학번\s*[:：]?\s*\d{8,}|notion-file-block:|X-Amz-(Credential|Signature)/i.test(text)) errors.push(`${label}: private data or temporary asset URL`);
  for(const img of document.querySelectorAll('img')){
    if(!img.hasAttribute('alt')) errors.push(`${label}: image missing alt`);
    if(!img.hasAttribute('width')||!img.hasAttribute('height')) errors.push(`${label}: image dimensions missing`);
    if(img.getAttribute('loading')!=='lazy') errors.push(`${label}: image is not lazy loaded`);
  }
  let previous=0;
  for(const h of document.querySelectorAll('h1,h2,h3,h4,h5,h6')) {
    const current=Number(h.tagName[1]);
    if(current>previous+1) errors.push(`${label}: heading level jump to ${h.tagName}`);
    previous=current;
  }
  const ids=[...document.querySelectorAll('[id]')].map(el=>el.id);
  if(new Set(ids).size!==ids.length) errors.push(`${label}: duplicate element id`);
  for(const a of document.querySelectorAll('a[target="_blank"]')) {
    const rel=a.getAttribute('rel')||'';
    if(!rel.includes('noopener')||!rel.includes('noreferrer')) errors.push(`${label}: unsafe external link`);
  }
}
let internalLinks=0,assets=0;
const external=new Set();
async function findTarget(pathname){
  const decoded=decodeURIComponent(pathname);
  let file=resolve(root,'.'+decoded);
  if(!file.startsWith(root)) return null;
  try {if((await stat(file)).isDirectory()) file=join(file,'index.html'); await stat(file); return file;} catch {return null;}
}
for(const [file,document] of pages){
  const route=file.slice(root.length).replace(/index\.html$/,'');
  for(const el of document.querySelectorAll('a[href],img[src],script[src],link[href]')){
    const raw=el.getAttribute('href')||el.getAttribute('src');
    if(!raw||/^(mailto:|tel:|data:)/.test(raw)) continue;
    const url=new URL(raw,origin+route);
    if(url.origin!==origin){external.add(url.href);continue;}
    const target=await findTarget(url.pathname);
    if(!target){errors.push(`${route}: missing ${raw}`);continue;}
    if(el.tagName==='A'){
      internalLinks++;
      if(url.hash && pages.has(target) && !pages.get(target).getElementById(decodeURIComponent(url.hash.slice(1)))) errors.push(`${route}: missing anchor ${raw}`);
    }else assets++;
  }
}
const mandatory=['index.html','404.html','about/index.html','projects/index.html','resume/index.html','projects/carla-autonomous-driving/index.html','projects/ai-rescue-box/index.html','robots.txt','sitemap-index.xml','sitemap-0.xml','favicon.svg','images/og-cover.png'];
for(const file of mandatory){if(!files.includes(join(root,file)))errors.push(`missing required file ${file}`);}
const projects=JSON.parse(await readFile('src/data/projects.json','utf8'));
if(projects.filter(p=>p.featured).length<4||projects.filter(p=>p.featured).length>6)errors.push('featured project count outside 4–6');
const slugs=projects.map(p=>p.slug);
if(new Set(slugs).size!==slugs.length)errors.push('duplicate project slug');
if(errors.length){console.error(errors.join('\n'));process.exit(1);}
const bytes=(await Promise.all(files.map(async f=>(await stat(f)).size))).reduce((a,b)=>a+b,0);
console.log(JSON.stringify({status:'passed',pages:htmlFiles.length,internalLinks,assets,externalLinks:external.size,totalBytes:bytes,external:[...external].sort()},null,2));
