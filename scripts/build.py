"""Build framework-free HTML pages using only the Python standard library."""
from pathlib import Path
from html import escape
import json
import shutil
import re
import base64
import mimetypes

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
ORIGIN = 'https://jeong-yun-kim.github.io'
data = json.loads((ROOT / 'src/data/profile.json').read_text())
profile, activities, awards, skills = (data[k] for k in ('profile', 'activities', 'awards', 'skills'))
archive_data = json.loads((ROOT / 'src/data/archive.json').read_text())
archive, studies = archive_data['archive'], archive_data['studies']
projects = json.loads((ROOT / 'src/data/projects.json').read_text())
CSS = '\n'.join((ROOT / f'src/styles/{f}').read_text() for f in ('site.css', 'enhancements.css'))
JS = (ROOT / 'src/site.js').read_text()

def e(value):
    return escape(str(value), quote=True)

def link(url, label, cls='text-link'):
    external = url.startswith('https:')
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    arrow = '↗' if external else '→'
    return f'<a class="{cls}" href="{e(url)}"{attrs}>{e(label)} <span aria-hidden="true">{arrow}</span></a>'

def bullets(items):
    return '<ul class="bullet-list">' + ''.join(f'<li>{e(x)}</li>' for x in items) + '</ul>'

def tags(items):
    return '<div class="tags">' + ''.join(f'<span class="tag">{e(x)}</span>' for x in items) + '</div>'

def heading(number, english, title, description=''):
    return f'<div class="section-header"><span class="section-index">{number} / {english}</span><div class="section-title-row"><h2 class="section-title">{e(title)}</h2><p class="section-subtitle">{e(description)}</p></div></div>'

def section(id, contents, alt=False):
    return f'<section id="{id}" class="section{" section-alt" if alt else ""}"><div class="container">{contents}</div></section>'

def picture(p, cls='', lazy=True):
    return f'<img class="{cls}" src="{p["image"]}" alt="{e(p["imageAlt"])}" width="960" height="540" loading="{"lazy" if lazy else "eager"}" decoding="async">'

def nav(home=False):
    prefix = '' if home else '/'
    items = [('about','소개'),('projects','프로젝트'),('skills','기술'),('experience','활동·수상'),('contact','연락처')]
    links = ''.join(f'<li><a class="nav-link" href="{prefix}#{id}">{label}</a></li>' for id,label in items)
    return f'''<a class="skip-link" href="#main-content">본문으로 건너뛰기</a>
    <header class="site-header"><div class="container header-inner">
    <a class="site-brand" href="{'#top' if home else '/'}" aria-label="김정윤 포트폴리오 첫 화면"><span>PORTFOLIO</span><span class="brand-divider" aria-hidden="true"></span><span class="brand-name">김정윤</span></a>
    <button class="nav-toggle" id="navToggle" type="button" aria-controls="siteNav" aria-expanded="false" aria-label="탐색 메뉴 열기"><span id="navToggleLabel">메뉴</span><span aria-hidden="true">☰</span></button>
    <nav class="site-nav" id="siteNav" aria-label="주요 메뉴"><ul class="nav-list">{links}<li><a class="nav-link header-resume" href="/resume/">이력서 ↗</a></li></ul></nav></div></header>'''

def footer():
    return '<footer class="site-footer"><div class="container footer-inner"><p class="footer-copy">© 2026 김정윤 · Jeong-Yun Kim</p><span class="footer-date">ROBOTICS / AUTONOMOUS DRIVING / BACKEND</span><a href="#top" class="top-link">맨 위로 ↑</a></div></footer><div class="toast" id="toast" role="status" aria-live="polite"></div>'

def page(title, description, content, route='/', home=False, body_class='', extra=''):
    full_title = '김정윤 | Robotics · Autonomous Driving · Backend' if home else f'{title} | 김정윤 포트폴리오'
    structured = json.dumps({'@context':'https://schema.org','@type':'Person','name':profile['name'],'alternateName':profile['englishName'],'url':ORIGIN+'/', 'sameAs':[profile['github']],'email':profile['email']},ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(full_title)}</title>
<meta name="description" content="{e(description)}"><meta name="theme-color" content="#ffffff"><meta name="color-scheme" content="light"><meta name="author" content="김정윤">
<link rel="canonical" href="{ORIGIN}{route}"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{ORIGIN}{route}"><meta property="og:image" content="{ORIGIN}/images/og-cover.png"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{structured}</script>
<style>{CSS}</style><noscript><style>.site-nav{{display:block;position:static;padding:0;border:0}}.site-header{{height:auto;position:static}}.header-inner{{flex-wrap:wrap;padding-block:16px}}.nav-list{{flex-direction:row;flex-wrap:wrap;gap:16px}}.nav-toggle{{display:none}}.copy-button{{display:none}}</style></noscript>
</head><body id="top" class="{body_class}">{nav(home)}<main id="main-content">{content}</main>{footer()}{extra}<script>{JS}</script></body></html>'''

def robot_graphic():
    # An original vector illustration, not a screenshot or measured system diagram.
    return '''<div class="hero-visual" role="img" aria-label="로봇팔과 센서·제어·데이터 연결을 표현한 개념 일러스트">
    <div class="diagram-top"><span>ROBOTICS / SYSTEM INTEGRATION</span><span>FIG. 01</span></div>
    <svg viewBox="0 0 500 420" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M25 0H0V25" fill="none" stroke="#e8e8e8" stroke-width=".7"/></pattern></defs>
    <rect width="500" height="420" fill="url(#grid)"/><ellipse cx="250" cy="332" rx="148" ry="35" fill="none" stroke="#d0d0d0"/><path d="M70 332H430M250 88V370" stroke="#d0d0d0" stroke-dasharray="4 5" fill="none"/>
    <g stroke="#171717" stroke-width="1.5" fill="none"><path d="M160 325L208 350L280 318L232 296Z" fill="#fff"/><path d="M160 325V337L208 362L280 330V318M208 350V362"/><path d="M185 319V283L218 268L250 284V320L218 334Z" fill="#e5e5e5"/><path d="M218 334V298L250 284M185 283L218 298"/>
    <path d="M202 281L165 219L184 190L206 203L240 263Z" fill="#d4d4d4"/><path d="M202 281L220 269L183 207L165 219" fill="#171717"/><circle cx="181" cy="210" r="22" fill="#fff"/><circle cx="181" cy="210" r="10" fill="#171717"/>
    <path d="M171 192L254 120L283 144L200 216" fill="#fafafa"/><path d="M200 216L281 147L281 129L254 120L171 192"/><path d="M183 200L265 130" stroke="#a3a3a3"/><circle cx="270" cy="133" r="21" fill="#171717"/><circle cx="270" cy="133" r="9" fill="#fff"/>
    <path d="M283 125L346 170L328 194L265 149" fill="#d4d4d4"/><path d="M282 142L337 181" stroke="#737373"/><circle cx="338" cy="182" r="16" fill="#fff"/><circle cx="338" cy="182" r="6" fill="#171717"/>
    <path d="M344 193V218L327 229M354 186L369 210L359 229" stroke-width="5"/><path d="M335 242L352 233L369 243L351 253Z" fill="#171717"/><path d="M335 242V264L351 274L369 264V243M351 253V274"/>
    <path d="M102 148H138L162 178M379 135H413M379 134L354 164M104 285H144L175 298" stroke="#737373" stroke-width=".8"/>
    </g><g font-family="monospace" font-size="9" fill="#626262"><text x="58" y="144">CONTROL</text><text x="390" y="128">VISION</text><text x="63" y="281">HARDWARE</text><text x="315" y="307">DATA → API</text></g>
    <rect x="60" y="70" width="7" height="7" fill="#171717"/><path d="M420 70h12m-6-6v12" stroke="#171717"/>
    </svg><div class="diagram-bottom"><span>SENSE → CONTROL → CONNECT</span><span>CONCEPT ILLUSTRATION</span></div></div>'''

def hero():
    return f'''<section class="hero" aria-labelledby="hero-title"><div class="container"><div class="hero-grid"><div class="hero-content"><div><span class="hero-eyebrow">ROBOTICS · AUTONOMOUS DRIVING · BACKEND</span><h1 class="hero-title" id="hero-title">김정윤<span class="name-en">Jeong-Yun Kim</span></h1><p class="hero-lead">로봇 제어부터 서버까지,<br>하나의 시스템으로 연결합니다.</p><p class="hero-desc">ROS2 기반 로봇 제어, 자율주행 시뮬레이션과 서버 개발 프로젝트를 기록합니다.</p></div><div class="hero-actions"><a class="btn btn-primary" href="#projects">프로젝트 보기 <span aria-hidden="true">↘</span></a><a class="btn btn-secondary" href="/resume/">이력서 보기 <span aria-hidden="true">↗</span></a></div></div>{robot_graphic()}</div><div class="hero-summary" aria-label="주요 정보"><div class="summary-item"><span class="summary-label">01 / EDUCATION</span><p class="summary-value">충북대학교 지능로봇공학과</p></div><div class="summary-item"><span class="summary-label">02 / FOCUS</span><p class="summary-value">로보틱스 · 자율주행 · Backend</p></div><div class="summary-item"><span class="summary-label">03 / CURRENT</span><p class="summary-value"><span class="status-dot" aria-hidden="true"></span>모두의 창업 2차 진행 중</p></div></div></div></section>'''

def about_content():
    rows = [('학력',profile['education']+'<br><span class="small-note">'+profile['educationPeriod']+'</span>'),('주요 활동','Double Click 로봇 프로젝트'),('개발 환경','Linux · ROS2 · Raspberry Pi'),('관심 분야','로봇 제어 · 자동화 · 서버 개발')]
    return f'''<div class="about-grid"><div class="about-statement"><p class="about-headline">하드웨어의 동작을 소프트웨어와 연결하는 개발을 합니다.</p><p class="about-paragraph">{e(profile['about'])}</p><div class="about-links">{link('/resume/','이력서')}{link(profile['github'],'GitHub')}</div></div><dl class="about-details">{''.join(f'<div class="detail-row"><dt class="detail-term">{k}</dt><dd class="detail-desc">{v}</dd></div>' for k,v in rows)}</dl></div>'''

CATEGORIES = {'causalroboqc':'robotics backend vision','carla-autonomous-driving':'driving','mirobot-ros2':'robotics vision','smart-factory-server':'backend robotics'}

def project_card(p, i):
    repo = next((x for x in p['links'] if x['label'].startswith('GitHub')), None)
    repo_html = link(repo['url'], 'GitHub', 'repo-link') if repo else ''
    image_type = '실제 시연 이미지' if p['image'].endswith('.webp') else '시스템 구성도'
    return f'''<article class="project-card" data-slug="{p['slug']}" data-categories="{CATEGORIES[p['slug']]}"><a href="/projects/{p['slug']}/" class="project-thumb" aria-label="{e(p['title'])} 상세 페이지"><span class="project-badge">PROJECT / {i+1:02}</span>{picture(p,'diagram' if p['image'].endswith('.svg') else '')}<span class="project-image-caption">{image_type}</span></a><div class="project-body"><span class="project-category">{e(p['category'].upper())}</span><h3 class="project-title"><a href="/projects/{p['slug']}/">{e(p['title'])}</a></h3><p class="project-desc">{e(p['summary'])}</p>{tags(p['technologies'])}<dl class="project-meta"><div class="project-meta-item"><dt class="project-meta-label">역할</dt><dd class="project-meta-value">{e(p['role'])}</dd></div><div class="project-meta-item"><dt class="project-meta-label">진행</dt><dd class="project-meta-value">{e(p['status'])}</dd></div></dl></div><div class="project-footer"><a class="project-open-btn" href="/projects/{p['slug']}/" data-project="{p['slug']}" aria-haspopup="dialog"><span>상세 보기</span><span aria-hidden="true">+</span></a>{repo_html}</div></article>'''

def project_listing():
    filters = [('all','전체'),('robotics','로보틱스'),('driving','자율주행'),('backend','서버'),('vision','비전')]
    buttons = ''.join(f'<button type="button" class="filter-button" data-filter="{key}" aria-pressed="{str(key=="all").lower()}">{name}</button>' for key,name in filters)
    return f'<div class="project-tools"><div class="filter-bar" role="group" aria-label="프로젝트 분야 선택" hidden>{buttons}</div><span class="project-count" id="projectCount" role="status" aria-live="polite">4 / 4 PROJECTS</span></div><div class="project-grid">'+''.join(project_card(p,i) for i,p in enumerate(projects))+'</div>'

def skill_content():
    return '<div class="skill-grid">'+''.join(f'<article class="skill-item"><span class="skill-index">{i+1:02}</span><h3>{e(s["category"])}</h3>{tags(s["names"])}<p>{e(s["evidence"])}</p>{link(s["href"],"적용 프로젝트")}</article>' for i,s in enumerate(skills))+'</div>'

def experience_content():
    activity_html=''.join(f'<article class="timeline-item"><span class="timeline-year">{e(a["period"])}</span><div><h4>{e(a["title"])}</h4><p>{e(a["description"])}</p></div></article>' for a in activities[:3])
    award_html=''.join(f'<article class="timeline-item"><span class="timeline-year">{e(a["year"] or a["scope"])}</span><div><h4>{e(a["name"])}</h4><span class="award-result">{e(a["result"])}</span></div></article>' for a in awards)
    return f'<div class="experience-grid"><div><h3 class="column-title">주요 활동 <span>EXPERIENCE</span></h3>{activity_html}</div><div><h3 class="column-title">수상 내역 <span>AWARDS</span></h3>{award_html}</div></div>'

def archive_content():
    return '<div class="archive-grid">'+''.join(f'<article class="archive-item"><span class="project-category">{e(a["category"])}</span><h3>{e(a["title"])}</h3><p>{e(a["summary"])}</p><p class="archive-note">{e(a["note"])}</p>{link(a["href"],a["linkLabel"])}</article>' for a in archive)+'</div>'

def research_content():
    return '<article class="research-row"><div><span class="research-label">2026.10 / 기획 단계</span><h3>리니어 이송 보관대 기반 자동 피킹</h3></div><div><p>Mirobot과 주문 박스를 고정하고 보관대를 이동하는 Double Click 팀 프로젝트. Raspberry Pi 주문 관리, Arduino 리니어 모터 제어, QR 확인과 Pick & Place를 연결하는 구조를 설계했습니다.</p><p class="small-note">설계·역할 분담·3주 개발 계획 기록 기준.</p></div></article><div class="study-links">'+''.join(f'<div>{link(s["url"],s["title"])}<p>{e(s["description"])}</p></div>' for s in studies)+'</div>'

def contact_content():
    return f'''<div class="contact-grid"><div class="contact-intro"><p class="contact-lead">프로젝트와 개발에 관한<br>이야기를 기다립니다.</p><p class="contact-note">로봇 제어, 자동화, 자율주행과 서버 개발에 관심이 있습니다.<br>프로젝트 문의는 이메일로 연락해 주세요.</p><div class="about-links">{link('/resume/','이력서 확인')}</div></div><div class="contact-box"><h3 class="contact-group-title">DIRECT CONTACT</h3><dl class="contact-list"><div class="contact-item"><dt class="contact-label">Email</dt><dd class="contact-value email-row"><a id="emailAddress" href="mailto:{profile['email']}">{profile['email']}</a><button type="button" class="copy-button" data-copy="{profile['email']}">주소 복사</button></dd></div></dl><h3 class="contact-group-title">ELSEWHERE</h3><dl class="contact-list"><div class="contact-item"><dt class="contact-label">GitHub</dt><dd class="contact-value">{link(profile['github'],'Jeong-Yun-Kim')}</dd></div></dl></div></div>'''

def modal():
    templates=[]
    for p in projects:
        templates.append(f'''<template id="detail-{p['slug']}"><span class="hero-eyebrow">{e(p['category'])}</span><h2 id="dialogTitle" tabindex="-1">{e(p['title'])}</h2><p>{e(p['overview'])}</p><dl class="info-grid"><div><dt>역할</dt><dd>{e(p['role'])}</dd></div><div><dt>기간 · 상태</dt><dd>{e(p['period'])}<br>{e(p['status'])}</dd></div></dl>{tags(p['technologies'])}<section><h3>구현 내용</h3>{bullets(p['features'])}</section><section><h3>결과</h3>{bullets(p['results'])}</section><section><h3>검증 범위와 후속 과제</h3>{bullets(p['limits'])}</section><p class="source-note">{e(p['sourceNote'])}</p><div class="dialog-actions">{link('/projects/'+p['slug']+'/','전체 프로젝트 기록','btn btn-primary')}{''.join(link(x['url'],x['label'],'btn btn-secondary') for x in p['links'][:1])}</div></template>''')
    return '<dialog class="project-dialog" id="projectDialog" aria-labelledby="dialogTitle"><div class="dialog-header"><span id="dialogCode">PROJECT</span><button type="button" id="dialogClose" class="dialog-close" aria-label="프로젝트 상세 창 닫기">닫기 ×</button></div><div class="dialog-content" id="dialogContent"></div><div class="dialog-footer"><button id="dialogPrev" type="button">← 이전 프로젝트</button><button id="dialogNext" type="button">다음 프로젝트 →</button></div></dialog>'+''.join(templates)

def project_detail(p, i):
    head=f'''<div class="page-heading"><div class="container"><a class="back-link" href="/projects/">← 프로젝트 목록</a><div class="hero-eyebrow">PROJECT / {i+1:02} · {e(p['category'].upper())}</div><h1>{e(p['title'])}</h1><p class="page-lead">{e(p['summary'])}</p><div class="page-meta"><span>{e(p['period'])}</span><span>{e(p['status'])}</span><span>{e(p['team'])}</span></div></div></div>'''
    navigation=[('overview','개요·역할'),('architecture','시스템 구성'),('implementation','구현 과정'),('evaluation','평가 결과'),('scope','검증 범위'),('resources','관련 자료')]
    sidebar='<nav class="case-nav" aria-label="프로젝트 목차">'+''.join(f'<a href="#{id}">{label}</a>' for id,label in navigation)+'</nav>'
    overview=f'<section id="overview"><h2>개요와 담당 역할</h2><p>{e(p["overview"])}</p><div class="info-grid"><div><h3>개발 배경</h3><p>{e(p["background"])}</p></div><div><h3>담당 역할</h3>{bullets(p["responsibility"])}</div></div><h3>개발 목표</h3>{bullets(p["goals"])}</section>'
    architecture='<section id="architecture"><h2>시스템 구성</h2><figure>'+picture(p)+f'<figcaption>{e(p["imageCaption"])}</figcaption></figure><div class="architecture-grid">'+''.join(f'<div class="architecture-card"><span>{j+1:02}</span><h3>{e(a["title"])}</h3><p>{e(a["description"])}</p></div>' for j,a in enumerate(p['architecture']))+'</div></section>'
    implementation='<section id="implementation"><h2>구현 과정</h2>'+''.join(f'<article class="case-entry"><h3>{e(a["title"])}</h3><p>{e(a["description"])}</p></article>' for a in p['implementation'])+'<h3>주요 기능</h3>'+bullets(p['features'])+'</section>'
    challenges='<section id="challenges"><h2>문제 해결</h2>'+''.join(f'<article class="case-entry"><h3>{e(c["problem"])}</h3><p>{e(c["solution"])}</p><p class="verification">{e(c["verification"])}</p></article>' for c in p['challenges'])+'</section>'
    metrics='<div class="metric-grid">'+''.join(f'<div class="metric-item"><div class="metric-value">{e(m["value"])}</div><div class="metric-label">{e(m["label"])}</div><p class="metric-context">{e(m["context"])}</p></div>' for m in p['metrics'])+'</div>' if p['metrics'] else ''
    evaluation='<section id="evaluation"><h2>평가 결과</h2>'+metrics+'<h3>검증 방법</h3>'+bullets(p['evaluation'])+'<h3 style="margin-top:24px">주요 결과</h3>'+bullets(p['results'])
    if p.get('extraImage'):
        image=p['extraImage']
        evaluation+=f'<figure><img src="{image["src"]}" alt="{e(image["alt"])}" width="960" height="540" loading="lazy"><figcaption>{e(image["caption"])}</figcaption></figure>'
    evaluation+='</section>'
    scope='<section id="scope"><h2>검증 범위와 후속 과제</h2>'+bullets(p['limits'])+'</section>'
    resources='<section id="resources"><h2>관련 자료</h2><div class="case-links">'+(''.join(link(a['url'],a['label']) for a in p['links']) or '<p>현재 공개된 외부 자료 링크가 없습니다. 이 페이지에 구현과 평가 기록을 정리했습니다.</p>')+f'</div><p class="source-note">{e(p["sourceNote"])}</p></section>'
    prev=projects[(i-1)%len(projects)]
    nex=projects[(i+1)%len(projects)]
    bottom=f'<div class="case-bottom">{link("/projects/"+prev["slug"]+"/",prev["title"])}{link("/projects/"+nex["slug"]+"/",nex["title"])}</div>'
    return head+f'<div class="container case-layout">{sidebar}<div class="case-main">{overview}{architecture}{implementation}{challenges}{evaluation}{scope}{resources}{bottom}</div></div>'

def resume():
    project_html=''
    for p in projects:
        note={'causalroboqc':'합성 데이터 시험 모델. 실제 제조 불량 예측 성능을 의미하지 않음.','carla-autonomous-driving':'2026.10.02 시뮬레이션 기록. 전진 주차 검증, NMPC는 설계 단계.','mirobot-ros2':'기존 시연과 분리본 검증 범위를 구분. 최신 분리본 실기기 재검증 필요.','smart-factory-server':'주문 상태는 메모리 기반이며 재시작 시 초기화됨.'}[p['slug']]
        project_html+=f'<article class="resume-project"><div class="resume-project-heading"><h3><a href="/projects/{p["slug"]}/">{e(p["title"])}</a></h3><span>{e(p["period"])}</span></div><p class="resume-role">{e(p["role"])}</p><p>{e(p["summary"])}</p><p class="resume-result">{e(p["highlight"])}</p><p class="small-note">{note}</p></article>'
    activity_html=''.join(f'<p><strong>{e(a["period"])} · {e(a["title"])}</strong><br>{e(a["description"])}</p>' for a in activities if a.get('resume'))
    award_html='<ul class="resume-awards">'+''.join(f'<li>{e(a["year"]+" · " if a["year"] else "")}{e(a["name"])} — <strong>{e(a["result"])}</strong></li>' for a in awards)+'</ul>'
    skill_html=''.join(f'<p><strong>{e(s["category"])}</strong><span>{e(" · ".join(s["names"]))}</span></p>' for s in skills)
    return f'''<div class="container resume-toolbar"><p>브라우저 인쇄에서 PDF로 저장할 수 있습니다.</p><button type="button" class="btn btn-primary" id="printResume">인쇄 / PDF 저장 ↗</button></div><article class="resume-sheet container"><header class="resume-header"><div><span class="hero-eyebrow">RESUME / 2026</span><h1>김정윤 <span>Jeong-Yun Kim</span></h1><p>{e(profile['focus'])}</p></div><address><a href="mailto:{profile['email']}">{profile['email']}</a><a href="{profile['github']}">github.com/Jeong-Yun-Kim</a><a href="{ORIGIN}/">jeong-yun-kim.github.io</a></address></header><section class="resume-section"><h2>소개·학력</h2><div><p>{e(profile['intro'])}</p><p><strong>{e(profile['education'])}</strong> · {e(profile['educationPeriod'])}</p></div></section><section class="resume-section"><h2>주요 프로젝트</h2><div>{project_html}</div></section><section class="resume-section"><h2>활동·수상</h2><div>{activity_html}{award_html}</div></section><section class="resume-section"><h2>기술</h2><div class="resume-skills">{skill_html}</div></section><p class="resume-updated">프로젝트·활동 자료 기준: {profile['updated']} · 세부 평가 조건은 프로젝트 상세 페이지 참조</p></article>'''

def write(path, content):
    target=OUT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(content,encoding='utf-8')

def build():
    OUT.mkdir(exist_ok=True)
    for stale in OUT.iterdir():
        if stale.is_dir(): shutil.rmtree(stale)
        else: stale.unlink()
    shutil.copytree(ROOT/'public', OUT, dirs_exist_ok=True)
    home=hero()+section('about',heading('01','ABOUT','소개','장비와 소프트웨어를 연결하는 개발')+about_content())
    home+=section('projects',heading('02','SELECTED PROJECTS','대표 프로젝트','구현 내용과 검증 결과를 중심으로')+project_listing(),True)
    home+=section('skills',heading('03','SKILLS','기술과 개발 범위','프로젝트에서 실제로 사용한 기술')+skill_content())
    home+=section('experience',heading('04','EXPERIENCE & AWARDS','활동 및 수상','프로젝트 밖의 경험과 기록')+experience_content(),True)
    home+=section('archive',heading('05','MORE WORK','개발 아카이브','실험·통신·공간정보와 학습 기록')+archive_content()+research_content())
    home+=section('contact',heading('06','CONTACT','연락처')+contact_content(),True)
    write('index.html',page('포트폴리오',profile['intro'],home,home=True,extra=modal()))
    project_page='<div class="page-heading"><div class="container"><span class="hero-eyebrow">PROJECT ARCHIVE</span><h1>프로젝트</h1><p class="page-lead">구현 내용, 문제 해결과 검증 범위를 정리한 개발 기록.</p></div></div>'
    project_page+=section('selected',heading('01','SELECTED PROJECTS','대표 프로젝트')+project_listing())
    project_page+=section('archive',heading('02','MORE WORK','개발 아카이브')+archive_content(),True)
    project_page+=section('research',heading('03','PLANNING & STUDY','기획·학습')+research_content())
    write('projects/index.html',page('프로젝트','로봇 제어·비전·자율주행·서버 프로젝트와 개발 기록.',project_page,'/projects/',extra=modal()))
    for i,p in enumerate(projects):
        write(f'projects/{p["slug"]}/index.html',page(p['title'],p['summary'],project_detail(p,i),'/projects/'+p['slug']+'/'))
    about_page='<div class="page-heading"><div class="container"><span class="hero-eyebrow">ABOUT</span><h1>소개</h1><p class="page-lead">'+e(profile['intro'])+'</p></div></div>'
    about_page+=section('about',heading('01','PROFILE','김정윤')+about_content())+section('experience',heading('02','EXPERIENCE','활동 및 수상')+experience_content(),True)+section('skills',heading('03','SKILLS','기술과 개발 범위')+skill_content())
    write('about/index.html',page('소개',profile['intro'],about_page,'/about/'))
    write('resume/index.html',page('이력서','김정윤의 학력, 주요 프로젝트, 기술 및 수상 내역을 정리한 이력서.',resume(),'/resume/',body_class='resume-page'))
    ai_content='''<div class="page-heading"><div class="container"><a class="back-link" href="/projects/">← 프로젝트 아카이브</a><div class="hero-eyebrow">SPATIAL INFORMATION / ARCHIVE</div><h1>AI Rescue Box</h1><p class="page-lead">사고 전 도면과 재난 후 공간지도를 연결하는 공간정보 모듈.</p><div class="page-meta"><span>2026.08 개발 기록</span><span>개발 중</span></div></div></div><div class="container case-layout"><nav class="case-nav" aria-label="프로젝트 목차"><a href="#overview">개요</a><a href="#architecture">시스템 구성</a><a href="#scope">검증 범위</a></nav><div class="case-main"><section id="overview"><h2>프로젝트 개요</h2><p>RGB-D와 Depth SLAM으로 얻은 공간정보를 기존 도면과 비교하여 구조에 필요한 정보를 제공하는 프로젝트입니다. 제13회 전국 ICT융합 AI 공모전 프로젝트 기록으로 정리되어 있습니다.</p><h3 style="margin-top:24px">담당 역할</h3><p>시스템 구성과 코드 개발. RTAB-Map·nvblox 기반 SLAM과 도면 투영 시연을 연결했습니다.</p></section><section id="architecture"><h2>시스템 구성</h2><dl class="info-grid"><div><dt>센싱</dt><dd>RGB-D · Depth SLAM</dd></div><div><dt>컴퓨팅</dt><dd>Jetson Orin Nano · Host</dd></div><div><dt>연계 모듈</dt><dd>UWB · 도면 비교 및 공간정보 처리</dd></div></dl></section><section id="scope"><h2>검증 범위</h2><p>개발 중인 프로젝트로, 정합 정확도와 실제 재난 환경의 성능, 반복 시험 결과는 확인되지 않았습니다. 소스는 비공개입니다.</p></section><section><h2>관련 자료</h2>'''+link('https://www.youtube.com/watch?v=GDBDBAFVDPM','기존 프로젝트 시연')+'''<p class="source-note">기존 프로젝트 개요와 시연 기록 기준.</p></section></div></div>'''
    write('projects/ai-rescue-box/index.html',page('AI Rescue Box','재난 전후 공간정보를 비교하는 AI Rescue Box 프로젝트.',ai_content,'/projects/ai-rescue-box/'))
    error_content='<section class="section"><div class="container"><span class="hero-eyebrow">404 / PAGE NOT FOUND</span><h1 class="hero-title">페이지를 찾을 수 없습니다.</h1><p class="hero-desc">주소를 확인하거나 포트폴리오 첫 화면으로 이동해 주세요.</p><div class="hero-actions"><a class="btn btn-primary" href="/">첫 화면으로 →</a><a class="btn btn-secondary" href="/projects/">프로젝트 보기</a></div></div></section>'
    write('404.html',page('페이지를 찾을 수 없습니다','포트폴리오 첫 화면과 프로젝트 목록으로 이동합니다.',error_content,'/404.html'))
    routes=['/','/about/','/projects/','/resume/','/projects/ai-rescue-box/']+['/projects/'+p['slug']+'/' for p in projects]
    write('sitemap-0.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{r}</loc></url>' for r in routes)+'</urlset>')
    write('sitemap-index.xml',f'<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>{ORIGIN}/sitemap-0.xml</loc></sitemap></sitemapindex>')
    write('robots.txt',f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap-index.xml\n')
    write('.nojekyll','')
    # A standalone HTML download: images embedded, subpages link to the live site.
    portable=(OUT/'index.html').read_text()
    def embed(match):
        path=OUT/match.group(1).lstrip('/')
        mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'
        return 'src="data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()+'"'
    portable=re.sub(r'src="(/images/[^"]+)"',embed,portable)
    portable=re.sub(r'href="(/[^\"]*)"',lambda m:'href="'+ORIGIN+m.group(1)+'"',portable)
    write('portfolio.html',portable)
    print(f'Built {len(list(OUT.rglob("*.html")))} HTML files in {OUT}')

if __name__ == '__main__':
    build()
