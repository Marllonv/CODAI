// Mostra o modal de sucesso ao enviar o formulário de cadastro
(function () {
  const form = document.querySelector('.cad-form');
  const modal = document.getElementById('cad-success');
  const dismissers = modal?.querySelectorAll('[data-dismiss]');

  if (!form || !modal) return;

  form.addEventListener('submit', function (e) {
    // se você já tiver backend, remova o preventDefault
    e.preventDefault();
    modal.classList.remove('is-hidden');
    document.body.classList.add('no-scroll');
  });

  // fechar modal por backdrop/botão
  dismissers.forEach(el => {
    el.addEventListener('click', () => {
      modal.classList.add('is-hidden');
      document.body.classList.remove('no-scroll');
    });
  });

  // fechar com ESC
  window.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape' && !modal.classList.contains('is-hidden')) {
      modal.classList.add('is-hidden');
      document.body.classList.remove('no-scroll');
    }
  });
})();

 // Navegação do carrossel
    (function(){
      const track = document.getElementById('pfTrack');
      const prev = document.querySelector('.pf-prev');
      const next = document.querySelector('.pf-next');
      if(!track) return;

      const step = () => Math.max(320, track.clientWidth * 0.6);
      prev.addEventListener('click', () => track.scrollBy({left: -step(), behavior: 'smooth'}));
      next.addEventListener('click', () => track.scrollBy({left:  step(), behavior: 'smooth'}));
    })();

// Dynamic category colors for forum and blog
(function() {
  // Apply colors to filter buttons (both forum and blog)
  const filterButtons = document.querySelectorAll('.filter-btn[data-color]');
  filterButtons.forEach(button => {
    const color = button.getAttribute('data-color');
    if (color) {
      button.style.setProperty('--category-color', color);
    }
  });

  // Apply colors to forum tags
  const forumTags = document.querySelectorAll('.forum-tag[data-color]');
  forumTags.forEach(tag => {
    const color = tag.getAttribute('data-color');
    if (color) {
      tag.style.setProperty('--category-color', color);
    }
  });

  // Apply colors to blog tags
  const blogTags = document.querySelectorAll('.blog-tag[data-color]');
  blogTags.forEach(tag => {
    const color = tag.getAttribute('data-color');
    if (color) {
      tag.style.setProperty('--category-color', color);
    }
  });
})();


