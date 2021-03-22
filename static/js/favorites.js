const favorites = localStorage.getItem('favorites').split(',');
const favoritesList = document.getElementById('favorites-list');
favorites.forEach(favorite => {
  const [service, user] = favorite.split(':');
  fetch(`/api/lookup/cache/${user}?service=${service}`)
    .then(data => data.json())
    .then(cache => {
      favoritesList.innerHTML += `
        <tr class="artist-row">
          <td>
            <a href="/${service}/user/${user}">${cache.name}</a>
          </td>
          <td>
            ${({
              patreon: 'Patreon',
              fanbox: 'Pixiv Fanbox',
              subscribestar: 'SubscribeStar',
              gumroad: 'Gumroad',
              discord: 'Discord',
              dlsite: 'DLsite'
            })[service]}
          </td>
        </tr>
      `;
    });
});

function on_change_favorite_type(target) {
  if (target) {
    var new_type = target.value;
    if (new_type) {
      window.location = '/favorites?type=' + new_type;
    }
  }
}

function on_change_filters(field, target) {
  if (target) {
    var value = target.value;
    var query_string = window.location.search;
    var url_params = new URLSearchParams(query_string);
    url_params.set(field, value);
    window.location.search = url_params.toString();
  }
}
