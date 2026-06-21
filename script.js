const navbar = document.getElementById('navbar');
const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
});

navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

navLinks.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

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
    const main = document.getElementById('bzone-main');
    if (!main) return;

    document.querySelectorAll('.gallery-thumb').forEach((t) => t.classList.remove('active'));
    thumb.classList.add('active');
    main.style.opacity = '0';
    setTimeout(() => {
      main.src = thumb.dataset.src;
      main.alt = thumb.dataset.alt;
      main.style.opacity = '1';
    }, 150);
  });
});
