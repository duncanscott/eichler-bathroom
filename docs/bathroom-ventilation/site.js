document.documentElement.classList.add('has-js');

const openingToggle = document.querySelector('#show-opening');
openingToggle.addEventListener('change', () => {
  document.querySelector('#grille-comparison').classList.toggle('show-openings', openingToggle.checked);
});
