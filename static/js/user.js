fetch('/artists/favorites')
  .then(async (res) => {
    var favorites = document.createElement('html');
    favorites.innerHTML = await res.text();

    var service = document.getElementsByName('service')[0].content;
    var user = document.getElementsByName('id')[0].content;
    if (favorites.getElementsByClassName(service + '-' + user).length) {
      document.getElementById('user-header-info-top').innerHTML += `
        <form
          action="/config/remove"
          method="POST"
          enctype="multipart/form-data"
          style="display: inline;"
        >
          <input type="hidden" name="favorites" value="${service}:${user}">
          <label for="submit-favorite" class="user-header-favorite"><span style="color: #FFD700;">★</span></label>
          <input id="submit-favorite" type="submit" style="display: none;">
        </form>
      `;
    } else {
      document.getElementById('user-header-info-top').innerHTML += `
        <form
          action="/config/add"
          method="POST"
          enctype="multipart/form-data"
          style="display: inline;"
        >
          <input type="hidden" name="favorites" value="${service}:${user}">
          <label for="submit-favorite" class="user-header-favorite">☆</label>
          <input id="submit-favorite" type="submit" style="display: none;">
        </form>
      `;
    }
  });