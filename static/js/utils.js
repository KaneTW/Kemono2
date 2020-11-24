/* eslint-disable no-unused-vars */

function getParameterByName (name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[[]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)');
  var results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function debounce (func, wait, immediate) {
  var timeout;
  return function () {
    var context = this; var args = arguments;
    var later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}

function thumbHTML (data) {
  return `
    <a href="${data.href}" class="thumb-link">
      ${data.src ? `
        <div class="thumb thumb-with-image ${data.class || 'thumb-standard'}">
          <img src="${data.src.replace('https://kemono.party', '')}?size=500">
        </div>
      ` : `
        <div class="thumb thumb-with-text ${data.class || 'thumb-standard'}">
          <h3>${data.title}</h3>
          <p>${data.content}</p>
        </div>
      `}
    </a>
  `;
}

let contentView;
function renderPost (post) {
  if (!contentView) contentView = document.getElementById('content');
  let parent = false;
  // if you couldn't tell, i'm very bad at regex
  const inline = post.content.match(/(((http|https|ftp):\/\/([\w-\d]+\.)+[\w-\d]+){0,1}(\/[\w~,;\-./?%&+#=]*))/ig) || [];
  inline.reverse();
  const href = `/${post.service}/user/${post.user}/post/${post.id}`;
  inline.forEach(function (url) {
    if ((/\.(gif|jpe?g|png|webp)$/i).test(url) && (/\/inline\//i).test(url)) {
      parent = true;
      contentView.innerHTML += thumbHTML({
        src: url,
        href: href,
        class: 'thumb-child'
      });
    }
  });
  const attachments = post.attachments;
  attachments.reverse();
  attachments.forEach(function (attachment) {
    if ((/\.(gif|jpe?g|png|webp)$/i).test(attachment.path)) {
      parent = true;
      contentView.innerHTML += thumbHTML({
        src: attachment.path,
        href: href,
        class: 'thumb-child'
      });
    }
  });
  contentView.innerHTML += thumbHTML({
    src: (/\.(gif|jpe?g|png|webp)$/i).test(post.file.path) ? post.file.path : undefined,
    title: post.title,
    content: post.content.replace(/(&nbsp;|<([^>]+)>)/ig, ''),
    class: post.shared_file ? 'thumb-shared' : (parent ? 'thumb-parent' : undefined),
    href: href
  });
}

/* eslint-enable no-unused-vars */
