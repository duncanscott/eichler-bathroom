document.documentElement.classList.add('has-js');

const openingToggle = document.querySelector('#show-opening');
openingToggle.addEventListener('change', () => {
  document.querySelector('#grille-comparison').classList.toggle('show-openings', openingToggle.checked);
});

const search = document.querySelector('#document-search');
const category = document.querySelector('#document-category');
const documents = [...document.querySelectorAll('.document')];
function filterDocuments() {
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  documents.forEach(item => {
    const matches = item.textContent.toLocaleLowerCase().includes(query)
      && (category.value === 'all' || item.dataset.category === category.value);
    item.hidden = !matches;
    if (matches) visible++;
  });
  document.querySelectorAll('.document-group').forEach(group => {
    group.hidden = ![...group.querySelectorAll('.document')].some(item => !item.hidden);
  });
  document.querySelector('#document-count').textContent = `${visible} of ${documents.length} documents shown`;
  document.querySelector('#no-documents').hidden = visible !== 0;
}
search.addEventListener('input', filterDocuments);
category.addEventListener('change', filterDocuments);
filterDocuments();

document.querySelector('#print-brief').addEventListener('click', () => {
  document.body.classList.add('print-brief');
  window.print();
});
window.addEventListener('afterprint', () => document.body.classList.remove('print-brief'));
