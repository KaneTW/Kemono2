document.addEventListener('DOMContentLoaded', function() {
  const elements = [].slice.call(document.querySelectorAll('[data-style]'));
  if ('IntersectionObserver' in window && elements.length) {
    let lazyObserver = new IntersectionObserver(function(entries, _) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          let lazyElement = entry.target;
          lazyElement.style.cssText = lazyElement.dataset.style;
          lazyObserver.unobserve(lazyElement);
        }
      });
    });
  
    elements.forEach(function(element) {
      lazyObserver.observe(element)
    });
  } else if (elements.length) {
    elements.forEach(function(element) {
      element.style.cssText = element.dataset.style;
    });
  }
});
