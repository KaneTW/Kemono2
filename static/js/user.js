require.config({
  paths: {
    oboe: 'https://unpkg.com/oboe@2.1.5/dist/oboe-browser.min'
  }
});

/* eslint-disable no-unused-vars */
function favorite_artist(service, user) {
  fetch(`/favorites/artist/${service}/${user}`, {
    method: 'POST'
  }).then(res => {
    if (res.redirected) {
      window.location =  add_url_param(res.url, 'redir', window.location.pathname);;
    } else if (res.ok) {
      location.reload();
    } else {
      alert('Error 003 - could not save favorite');
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
      location.reload();
    } else {
      alert('Error 004 - could not remove favorite');
    }
  });
}
/* eslint-enable no-unused-vars */

function loadQuery () {
  const query = document.getElementById('search-input').value;
  const pathname = window.location.pathname.split('/');
  const contentView = document.getElementById('content');
  contentView.innerHTML = '';
  const api = ({
    patreon: `/api/patreon/user/${pathname[3]}/lookup?q=${query}`,
    fanbox: `/api/fanbox/user/${pathname[3]}/lookup?q=${query}`,
    gumroad: `/api/gumroad/user/${pathname[3]}/lookup?q=${query}`,
    subscribestar: `/api/subscribestar/user/${pathname[3]}/lookup?q=${query}`,
    dlsite: `/api/dlsite/user/${pathname[3]}/lookup?q=${query}`
  })[document.getElementsByName('service')[0].content];
  require(['oboe'], function (oboe) {
    oboe(api)
      .node('!.*', function (post) {
        return renderPost(post);
      });
  });
}

document.getElementById('search-input').addEventListener('keyup', debounce(() => loadQuery(), 350));