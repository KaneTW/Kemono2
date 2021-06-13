; (() => {
  // select registration section
  const sectionRegister = document.querySelector(".site-section--register");

  // if it's present run its script
  sectionRegister && initSectionRegister();

  function initSectionRegister() {
    populate_favorites();
  }

  function populate_favorites() {
    var input = document.getElementById('serialized-favorites');
    var favorites = localStorage.favorites;
    var to_serialize = [];
    if (input && favorites) {
      var artists = favorites.split(',');
      artists.forEach(function (artist) {
        var split = artist.split(':');
        if (split.length != 2) { return; }
        var elem = {
          'service': split[0],
          'artist_id': split[1]
        };
        to_serialize.push(elem);
      });
      var serialized = JSON.stringify(to_serialize);
      input.value = serialized;
    }
  }

  if (localStorage.getItem('logged_in')) {
    document.getElementById('account-buttons').innerHTML += `
      <li><a href="/favorites">[Favorites]</a></li>
      <li><a id="logout" href="/account/logout">[Logout]</a></li>
    `
    document.getElementById('logout').addEventListener('click', e => {
      e.preventDefault();
      localStorage.removeItem('logged_in');
      localStorage.removeItem('favs');
      location.href = '/account/logout';
    })
  } else {
    document.getElementById('account-buttons').innerHTML += `
      <li><a href="/account/login">[Login]</a></li>
    `
  }
})();

/**
 * @param {string} url 
 * @param {string} param_name 
 * @param {string} param_value 
 * @returns {string}
 */
function add_url_param(url, param_name, param_value) {
  var newURL = new URL(url);
  newURL.searchParams.set(param_name, param_value);
  return newURL.toString();
}