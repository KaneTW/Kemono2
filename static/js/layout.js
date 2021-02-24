function setCookie(name, value, days) {
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days*24*60*60*1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

var select = document.getElementById("posts_layout");
select.addEventListener('change', function () {
  setCookie('layout', select.value, 99999)
  window.location.reload()
})