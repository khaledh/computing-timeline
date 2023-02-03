function setAllEntries(display) {
  els = document.querySelectorAll('dd, dt, .year, h2');
  for (el of els) {
    el.style.display = display;
  }
}

andColors = [
  '#FFE5CC', // light orange
  '#CCFFFF', // light blue
  '#E5CCFF', // light purple
  '#CCFFE5', // light green
  '#E0E0E0', // light grey
]
lastColorIndex = 0;

// represent filters as "conjunction of disjunctions"; i.e. one AND of a group of ORs
// e.g. (a | b | c) & (m | n) & (x)
var andClause = JSON.parse(localStorage.getItem('andClause'));
if (!andClause) {
  andClause = [[]];
}

window.onload = function() {
  setFilters();
  showSelectedEntries();
};

function setFilters() {
  var buttons = document.querySelectorAll('.buttons > span');
  var buttonsHash = {};
  for (el of buttons) {
    buttonsHash[el.id] = el;
    el.classList.remove('shadow-inner');
    el.style.backgroundColor = null;
  }

  currentColorIndex = 0;
  for (orClause of andClause) {
    for (id of orClause) {
      var el = buttonsHash[id];
      el.classList.add('shadow-inner');
      el.style.backgroundColor = andColors[currentColorIndex];
    }
    currentColorIndex++;
  }
}

function showSelectedEntries() {
  setAllEntries('none');

  var orSelectors = [];
  for (orClause of andClause) {
    orSelectors.push(orClause.map(id => `.${id}`).join(', '));
  }
  var selectorClasses = orSelectors.map(s => `has(> ${s})`).join(':');
  var selector = `dd:${selectorClasses}`
  console.log(selector);

  var els = document.querySelectorAll(selector);
  for (el of els) {
    var display = '';
    el.style.display = display;
    el.previousElementSibling.style.display = display;
    el.parentNode.previousElementSibling.style.display = display;
    el.parentNode.previousElementSibling.parentNode.previousElementSibling.style.display = display;
  }
}

function toggleDef(event) {
  if (event.target.tagName != 'SPAN' && event.target.tagName != 'ABBR') {
    return;
  }

  id = event.target.id;
  if (id == '') {
    // node is <abbr>, get parent <span> id
    id = event.target.parentNode.id;
  }

  // if id is already selected, remove it
  removed = false;
  for (let [i, orClause] of andClause.entries()) {
    if (orClause.indexOf(id) != -1) {
      andClause[i] = orClause.filter(x => x !== id);
      if (andClause[i].length == 0 && andClause.length > 1) {
        andClause.splice(i, 1);
        if (lastColorIndex > 0) {
          lastColorIndex = lastColorIndex - 1;
        }
      }
      removed = true;
      break;
    }
  }

  if (!removed) {
    if (!event.shiftKey) {
      andClause[andClause.length - 1].push(id);
    } else {
      andClause.push([id]);
      lastColorIndex = (lastColorIndex + 1) % andColors.length;
    }
  }

  setFilters();

  localStorage.setItem('andClause', JSON.stringify(andClause));

  console.log('AND=', JSON.stringify(andClause));
  console.log('lastColorIndex=', lastColorIndex);

  if (andClause.length == 1 && andClause[0].length == 0) {
    setAllEntries('');
    return;
  }

  showSelectedEntries();
}

function clearFilters(evt) {
  andClause = [[]];
  localStorage.removeItem('andClause');
  var buttons = document
    .querySelectorAll('.buttons > span')
    .forEach(b => {
      b.classList.remove('shadow-inner');
      b.style.backgroundColor = null;
  });
  setAllEntries('');
  evt.preventDefault();
}
