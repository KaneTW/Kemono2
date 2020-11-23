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
