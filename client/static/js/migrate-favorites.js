if (localStorage.getItem("favorites")) {
  var migrations_div = document.getElementById("migrations");
  migrations_div.innerHTML = '<span class="subtitle">Old favorites found. Now migrating... (do not refresh)</span>';

  var old_favs = localStorage.getItem("favorites").split(',');
  old_favs.map(function (fav) {
    var fmd = new FormData();
    fmd.append('favorites', fav);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/config/add", false);
    xhr.send(fmd)
  });

  migrations_div.innerHTML = '<span class="subtitle">Done migrating. Please refresh the page.</span>';
}