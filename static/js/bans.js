window.onload = async () => {
  const bansData = await fetch('/api/bans');
  const bans = await bansData.json();
  bans.forEach(async (ban) => {
    let cache, href, service;
    switch (ban.service) {
      case 'patreon': {
        service = 'Patreon';
        const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=patreon`);
        cache = await cacheData.json();
        href = `https://www.patreon.com/user?u=${ban.id}`;
        break;
      }
      case 'fanbox': {
        service = 'Pixiv Fanbox';
        const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=fanbox`);
        cache = await cacheData.json();
        href = `https://www.pixiv.net/fanbox/creator/${ban.id}`;
        break;
      }
      case 'gumroad': {
        service = 'Gumroad';
        const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=gumroad`);
        cache = await cacheData.json();
        href = `https://gumroad.com/${ban.id}`;
        break;
      }
      case 'subscribestar': {
        service = 'SubscribeStar';
        const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=subscribestar`);
        cache = await cacheData.json();
        href = `https://subscribestar.adult/${ban.id}`;
        break;
      }
      case 'dlsite': {
        service = 'DLsite';
        const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=dlsite`);
        cache = await cacheData.json();
        href = `https://www.dlsite.com/eng/circle/profile/=/maker_id/${ban.id}`;
        break;
      }
    }
    document.getElementById('bans').innerHTML += `
      <li>
        <a href="${href}">
          ${cache.name} <span class="subtitle">${service}</span>
        </a>
      </li>
    `;
  });
};
