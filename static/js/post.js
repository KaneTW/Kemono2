function attemptFlag (api) {
  if (confirm('Are you sure you want to flag this post for reimport?')) {
    fetch(api, { method: 'post' })
      .then(function (res) {
        window.alert(res.ok ? 'Successfully flagged.' : 'Error. There might already be a flag here.');
      });
  }
}

Array.prototype.forEach.call(document.getElementsByClassName('flag'), function (flag) {
  flag.addEventListener('click', function (_) {
    attemptFlag(
      '/api/' + 
      flag.getAttribute('data-service') +
      '/user/' +
      flag.getAttribute('data-user') +
      '/post/' +
      flag.getAttribute('data-post') +
      '/flag'
    );
  });
})