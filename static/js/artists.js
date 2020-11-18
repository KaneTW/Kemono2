window.onload = () => {
  Array.from(document.querySelectorAll('.user-icon')).forEach(icon => {
    switch (icon.getAttribute('data-service')) {
      case 'patreon': {
        fetch(`/proxy/patreon/user/${icon.getAttribute('data-user')}`)
          .then(res => res.json())
          .then(user => {
            const avatar = user.included ? user.included[0].attributes.avatar_photo_url : user.data.attributes.image_url;
            icon.setAttribute('style', `background-image: url('${avatar}');`);
          });
        break;
      }
      case 'fanbox': {
        require(['https://unpkg.com/unraw@1.2.5/dist/index.min.js'], unraw => {
          fetch(`/proxy/fanbox/user/${icon.getAttribute('data-user')}`)
            .then(res => res.json())
            .then(user => {
              const avatar = unraw.unraw(user.body.user.iconUrl);
              icon.setAttribute('style', `background-image: url('${avatar}');`);
            });
        });
        break;
      }
      case 'subscribestar': {
        fetch(`/proxy/subscribestar/user/${icon.getAttribute('data-user')}`)
          .then(res => res.json())
          .then(user => {
            const avatar = user.avatar;
            icon.setAttribute('style', `background-image: url('${avatar}');`);
          });
        break;
      }
      case 'gumroad': {
        fetch(`/proxy/gumroad/user/${icon.getAttribute('data-user')}`)
          .then(res => res.json())
          .then(user => {
            const avatar = user.avatar;
            icon.setAttribute('style', `background-image: url('${avatar}');`);
          });
        break;
      }
      case 'discord': {
        fetch(`/proxy/discord/server/${icon.getAttribute('data-user')}`)
          .then(res => res.json())
          .then(user => {
            const avatar = `https://cdn.discordapp.com/icons/${icon.getAttribute('data-user')}/${user[0].icon}?size=256`;
            icon.setAttribute('style', `background-image: url('${avatar}');`);
          });
        break;
      }
    }
  });
};
