const navbar = document.getElementById('navbar');
const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');

function setMenuOpen(open) {
  if (!navLinks) return;
  navLinks.classList.toggle('open', open);
  document.body.style.overflow = open ? 'hidden' : '';
}

if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);
  });
}

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    setMenuOpen(!navLinks.classList.contains('open'));
  });

  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setMenuOpen(false));
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 768) setMenuOpen(false);
  });
}

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  },
  { threshold: 0.1 }
);

document.querySelectorAll('.project-card, .skill-card, .experience-card').forEach((el) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

document.querySelectorAll('.gallery-thumb').forEach((thumb) => {
  thumb.addEventListener('click', () => {
    const gallery = thumb.closest('.project-gallery');
    const main = gallery?.querySelector('.project-gallery-main img');
    if (!main) return;

    gallery.querySelectorAll('.gallery-thumb').forEach((t) => t.classList.remove('active'));
    thumb.classList.add('active');
    main.style.opacity = '0';
    setTimeout(() => {
      main.src = thumb.dataset.src;
      main.alt = thumb.dataset.alt;
      main.style.opacity = '1';
    }, 150);
  });
});
