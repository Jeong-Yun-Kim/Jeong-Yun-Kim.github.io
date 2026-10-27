(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const menu = $('#siteNav');
  const toggle = $('#navToggle');
  function closeMenu() {
    menu?.classList.remove('is-open');
    toggle?.setAttribute('aria-expanded', 'false');
    toggle?.setAttribute('aria-label', '탐색 메뉴 열기');
    if ($('#navToggleLabel')) $('#navToggleLabel').textContent = '메뉴';
  }
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? '탐색 메뉴 닫기' : '탐색 메뉴 열기');
    $('#navToggleLabel').textContent = open ? '닫기' : '메뉴';
  });
  $$('#siteNav a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      toggle.focus();
    }
  });
  const mobile = window.matchMedia('(max-width: 768px)');
  mobile.addEventListener('change', closeMenu);
  const cards = $$('.project-card[data-categories]');
  const filters = $$('.filter-button');
  if (filters.length) $('.filter-bar').hidden = false;
  filters.forEach(button => button.addEventListener('click', () => {
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    const filter = button.dataset.filter;
    cards.forEach(card => {
      card.hidden = filter !== 'all' && !card.dataset.categories.split(' ').includes(filter);
    });
    $('#projectCount').textContent = `${cards.filter(card => !card.hidden).length} / ${cards.length} PROJECTS`;
  }));
  const dialog = $('#projectDialog');
  let activeProject = '';
  let opener = null;
  const visibleProjects = () => cards.filter(card => !card.hidden).map(card => card.dataset.slug);
  function renderProject(slug) {
    const template = document.getElementById(`detail-${slug}`);
    if (!template || !dialog) return;
    activeProject = slug;
    $('#dialogContent').replaceChildren(template.content.cloneNode(true));
    const list = visibleProjects();
    const index = list.indexOf(slug);
    $('#dialogCode').textContent = `PROJECT ${String(index + 1).padStart(2, '0')} / ${String(list.length).padStart(2, '0')}`;
    $('#dialogPrev').disabled = index <= 0;
    $('#dialogNext').disabled = index >= list.length - 1;
    dialog.scrollTop = 0;
  }
  $$('.project-open-btn').forEach(link => link.addEventListener('click', event => {
    if (!dialog || typeof dialog.showModal !== 'function' || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = link;
    renderProject(link.dataset.project);
    dialog.showModal();
    document.body.classList.add('modal-open');
    $('#dialogClose').focus();
  }));
  $('#dialogClose')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog?.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    opener?.focus();
  });
  function navigateProject(direction) {
    const list = visibleProjects();
    const target = list[list.indexOf(activeProject) + direction];
    if (target) {
      renderProject(target);
      $('#dialogTitle').focus();
    }
  }
  $('#dialogPrev')?.addEventListener('click', () => navigateProject(-1));
  $('#dialogNext')?.addEventListener('click', () => navigateProject(1));
  let toastTimer;
  function notify(message) {
    const toast = $('#toast');
    toast.textContent = message;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toast.textContent = ''; }, 5000);
  }
  $$('.copy-button').forEach(button => button.addEventListener('click', async () => {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(button.dataset.copy);
      notify('이메일 주소를 복사했습니다.');
    } catch {
      const address = $('#emailAddress');
      const range = document.createRange();
      range.selectNodeContents(address);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      notify('주소를 선택했습니다. Ctrl+C 또는 길게 눌러 복사해 주세요.');
    }
  }));
  $('#printResume')?.addEventListener('click', () => window.print());
  if ('IntersectionObserver' in window) {
    const navLinks = $$('.nav-link[href^="#"]');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        navLinks.forEach(link => {
          if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-15% 0px -65% 0px', threshold: 0 });
    $$('main>section[id]').forEach(section => observer.observe(section));
  }
})();
