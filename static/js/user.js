/* eslint-disable no-unused-vars */
function favorite_artist(service, user) {
  fetch(`/favorites/artist/${service}/${user}`, {
    method: 'POST'
  }).then(res => {
    if (res.redirected) {
      window.location =  add_url_param(res.url, 'redir', window.location.pathname);;
    } else if (res.ok) {
      fetch('/api/favorites')
        .then(resp => resp.text())
        .then(favs => localStorage.setItem('favs', favs))
        .then(() => {
          location.reload();
        })
    } else {
      fetch('/api/favorites')
        .then(resp => resp.text())
        .then(favs => localStorage.setItem('favs', favs))
        .then(() => {
          alert('Error 003 - could not save favorite');
        })
    }
  });
}

function unfavorite_artist(service, user) {
  fetch(`/favorites/artist/${service}/${user}`, {
    method: "DELETE"
  }).then(res => {
    if (res.redirected) {
      window.location =  add_url_param(res.url, 'redir', window.location.pathname);;
    } else if (res.ok) {
      fetch('/api/favorites')
        .then(resp => resp.text())
        .then(favs => localStorage.setItem('favs', favs))
        .then(() => {
          location.reload();
        })
    } else {
      fetch('/api/favorites')
        .then(resp => resp.text())
        .then(favs => localStorage.setItem('favs', favs))
        .then(() => {
          alert('Error 004 - could not remove favorite');
        })
    }
  });
}

(async () => {
  if (localStorage.getItem('logged_in')) {
    var favs = localStorage.getItem('favs');
    if (!favs) {
      var fetched_favs = await fetch('/api/favorites');
      favs = await fetched_favs.text();
      localStorage.setItem('favs', favs)
    }
    if (JSON.parse(favs).filter(fav => fav.id === document.getElementsByName('id')[0].content && fav.service === document.getElementsByName('service')[0].content).length > 0) {
      document.getElementById('user-header-info-top').innerHTML += `
        <a href="javascript:unfavorite_artist('${ document.getElementsByName('service')[0].content }', '${document.getElementsByName('id')[0].content}');" class="user-header-favorite">
          <span style="color: #FFD700;">★</span>
        </a>
      `
    } else {
      document.getElementById('user-header-info-top').innerHTML += `
        <a href="javascript:favorite_artist('${ document.getElementsByName('service')[0].content }', '${document.getElementsByName('id')[0].content}');" class="user-header-favorite">
          ☆
        </a>
      `
    }
  } else {
    document.getElementById('user-header-info-top').innerHTML += `
      <a href="javascript:favorite_artist('${ document.getElementsByName('service')[0].content }', '${document.getElementsByName('id')[0].content}');" class="user-header-favorite">
        ☆
      </a>
    `
  }
})();
/* eslint-enable no-unused-vars */