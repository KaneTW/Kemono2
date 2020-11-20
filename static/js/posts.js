require.config({
  paths: {
    oboe: 'https://unpkg.com/oboe@2.1.5/dist/oboe-browser.min'
  }
});

const rowHTML = data => `
  <li>
    <a href="${data.href}">
      ${data.title} <span class="subtitle">${data.subtitle}</span>
    </a>
  </li>
`;

function renderPatreonQuery (query = '', limit = 10) {
  const resultsView = document.getElementById('results');
  require(['oboe'], oboe => {
    oboe(`/api/lookup?q=${encodeURIComponent(query)}&service=patreon&limit=${limit}`)
      .node('!.*', userId => {
        fetch(`/api/lookup/cache/${userId}?service=patreon`)
          .then(res => res.json())
          .then(cache => {
            resultsView.innerHTML += rowHTML({
              id: `patreon-user-${userId}`,
              href: '/user/' + userId,
              avatar: '',
              title: cache.name,
              subtitle: 'Patreon'
            });
          });
      });
  });
}

function renderGumroadQuery (query = '', limit = 10) {
  const resultsView = document.getElementById('results');
  require(['oboe'], oboe => {
    oboe(`/api/lookup?q=${encodeURIComponent(query)}&service=gumroad&limit=${limit}`)
      .node('!.*', userId => {
        fetch(`/api/lookup/cache/${userId}?service=gumroad`)
          .then(res => res.json())
          .then(cache => {
            resultsView.innerHTML += rowHTML({
              id: `gumroad-user-${userId}`,
              href: '/gumroad/user/' + userId,
              avatar: '',
              title: cache.name,
              subtitle: 'Gumroad'
            });
          });
      });
  });
}

function renderFanboxQuery (query = '', limit = 10) {
  const resultsView = document.getElementById('results');
  require(['oboe'], oboe => {
    oboe(`/api/lookup?q=${encodeURIComponent(query)}&service=fanbox&limit=${limit}`)
      .node('!.*', userId => {
        fetch(`/api/lookup/cache/${userId}?service=fanbox`)
          .then(res => res.json())
          .then(cache => {
            resultsView.innerHTML += rowHTML({
              id: `fanbox-user-${userId}`,
              href: '/fanbox/user/' + userId,
              avatar: '',
              title: cache.name,
              subtitle: 'Pixiv Fanbox'
            });
          });
      });
  });
}

function renderDiscordQuery (query = '', limit = 10) {
  const resultsView = document.getElementById('results');
  require(['oboe'], oboe => {
    oboe(`/api/lookup?q=${encodeURIComponent(query)}&service=discord&limit=${limit}`)
      .node('!.*', userId => {
        fetch(`/api/lookup/cache/${userId}?service=discord`)
          .then(res => res.json())
          .then(cache => {
            resultsView.innerHTML += rowHTML({
              id: `discord-server-${userId}`,
              href: '/discord/server/' + userId,
              avatar: '',
              title: cache.name,
              subtitle: 'Discord'
            });
          });
      });
  });
}

function renderSubscribestarQuery (query = '', limit = 10) {
  const resultsView = document.getElementById('results');
  require(['oboe'], oboe => {
    oboe(`/api/lookup?q=${encodeURIComponent(query)}&service=subscribestar&limit=${limit}`)
      .node('!.*', userId => {
        fetch(`/api/lookup/cache/${userId}?service=subscribestar`)
          .then(res => res.json())
          .then(cache => {
            resultsView.innerHTML += rowHTML({
              id: `subscribestar-user-${userId}`,
              href: '/subscribestar/user/' + userId,
              avatar: '',
              title: cache.name,
              subtitle: 'SubscribeStar'
            });
          });
      });
  });
}

function renderDlsiteQuery (query = '', limit = 10) {
  const resultsView = document.getElementById('results');
  require(['oboe'], oboe => {
    oboe(`/api/lookup?q=${encodeURIComponent(query)}&service=dlsite&limit=${limit}`)
      .node('!.*', userId => {
        fetch(`/api/lookup/cache/${userId}?service=dlsite`)
          .then(res => res.json())
          .then(cache => {
            resultsView.innerHTML += rowHTML({
              id: `dlsite-user-${userId}`,
              href: '/dlsite/user/' + userId,
              avatar: '',
              title: cache.name,
              subtitle: 'DLsite'
            });
          });
      });
  });
}

function queryUpdate (num) {
  const resultsView = document.getElementById('results');
  resultsView.innerHTML = '';
  const service = document.getElementById('service-input').value;
  const query = document.getElementById('search-input').value;
  switch (service) {
    case 'patreon': {
      renderPatreonQuery(query, num);
      break;
    }
    case 'fanbox': {
      renderFanboxQuery(query, num);
      break;
    }
    case 'gumroad': {
      renderGumroadQuery(query, num);
      break;
    }
    case 'discord': {
      renderDiscordQuery(query, num);
      break;
    }
    case 'subscribestar': {
      renderSubscribestarQuery(query, num);
      break;
    }
    case 'dlsite': {
      renderDlsiteQuery(query, num);
      break;
    }
    default: {
      renderPatreonQuery(query);
      renderFanboxQuery(query);
      renderGumroadQuery(query);
      renderDiscordQuery(query);
      renderSubscribestarQuery(query);
      renderDlsiteQuery(query);
    }
  }
}

window.onload = () => {
  document.getElementById('search-input').addEventListener('keyup', debounce(() => queryUpdate(150), 350));
  document.getElementById('service-input').addEventListener('change', () => queryUpdate(150));
};
