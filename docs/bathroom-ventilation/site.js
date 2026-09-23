document.documentElement.classList.add('has-js');

const openingToggle = document.querySelector('#show-opening');
openingToggle.addEventListener('change', () => {
  document.querySelector('#grille-comparison').classList.toggle('show-openings', openingToggle.checked);
});

document.querySelector('#print-brief').addEventListener('click', () => {
  document.body.classList.add('print-brief');
  window.print();
});
window.addEventListener('afterprint', () => document.body.classList.remove('print-brief'));
