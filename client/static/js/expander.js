var Expand = function (c, t) {
  if (!c.naturalWidth) {
    return setTimeout(Expand, 10, c, t);
  }
  c.style.maxWidth = '100%';
  c.style.display = '';
  t.style.display = 'none';
  t.style.opacity = '';
};

var Expander = function (e) {
  var t = e.target;
  if (t.parentNode.classList.contains('fileThumb')) {
    e.preventDefault();
    if (t.hasAttribute('data-src')) {
      var c = document.createElement('img');
      c.setAttribute('src', t.parentNode.getAttribute('href'));
      c.style.display = 'none';
      t.parentNode.insertBefore(c, t.nextElementSibling);
      t.style.opacity = '0.75';
      setTimeout(Expand, 10, c, t);
    } else {
      var a = t.parentNode;
      a.firstChild.style.display = '';
      a.removeChild(t);
      a.offsetTop < window.pageYOffset && a.scrollIntoView({ top: 0, behavior: 'smooth' });
    }
  }
};

document.addEventListener('click', Expander);
