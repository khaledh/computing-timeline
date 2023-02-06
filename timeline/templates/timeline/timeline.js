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

var andClause = [[]];

window.addEventListener('DOMContentLoaded', (event) => {
  var savedState = JSON.parse(localStorage.getItem('andClause'));
  if (savedState && savedState.length > 0 && savedState[0].length > 0) {
    andClause = savedState;
    setFilters();
    showSelectedEntries();
  }
});

var esc = 0;

document.addEventListener('keydown', function(e) {
    if (e.keyCode == 27) {
      esc++;
      if (esc == 2) {
        esc = 0;
        clearFilters();
      }
    }
});

function setFilters() {
  document.querySelector('#current-filters').replaceChildren();

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
      document.querySelector('#current-filters').append(el.cloneNode(true));
    }
    currentColorIndex++;
  }
}

function setAllEntries(display) {
  els = document.querySelectorAll('dd, dt, .year, .month, h2');
  for (el of els) {
    el.style.display = display;
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
    if (parseInt(el.dataset.weight) >= 0) {
      el.style.display = display;
    }
    el.previousElementSibling.style.display = display; // <dt>
    if (el.previousElementSibling.previousElementSibling && el.previousElementSibling.previousElementSibling.classList.contains('month')) {
      el.previousElementSibling.previousElementSibling.style.display = display; // month
    }
    el.parentNode.previousElementSibling.style.display = display; // year
//    console.log(el.parentNode.previousElementSibling);
//    if (el.parentNode.previousElementSibling.previousElementSibling) {
//      el.parentNode.previousElementSibling.previousElementSibling.style.display = display; // month
//    }
    el.parentNode.previousElementSibling.parentNode.previousElementSibling.style.display = display; // decade
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

//  console.log('AND=', JSON.stringify(andClause));
//  console.log('lastColorIndex=', lastColorIndex);

  if (andClause.length == 1 && andClause[0].length == 0) {
    setAllEntries('');
    return;
  }

  showSelectedEntries();
}

function clearFilters(evt) {
  andClause = [[]];
  localStorage.removeItem('andClause');
  setFilters();
  setAllEntries('');
  evt.preventDefault();
}
