import { kemonoAPI } from "@wp/api";
import { addFavouritePost, removeFavouritePost, findFavouritePost } from "@wp/js/favorites";
import { createComponent, LoadingIcon } from "./components/_index";

const meta = {
  service: null,
  user: null,
  postID: null,
};

/** 
 * @param {HTMLElement} section
 */
export function postPage(section) {
  /**
   * @type {HTMLElement}
   */
  const buttonPanel = section.querySelector(".post__actions");

  meta.service = document.head.querySelector("[name='service']").content;
  meta.user = document.head.querySelector("[name='user']").content;
  meta.postID = document.head.querySelector("[name='id']").content;
  section.addEventListener('click', Expander);

  initButtons(buttonPanel);
}

/**
 * @param {HTMLElement} buttonPanel 
 */
function initButtons(buttonPanel) {
  /**
   * @type {HTMLButtonElement}
   */
  const flagButton = buttonPanel.querySelector(".post__flag");
  /**
   * @type {HTMLButtonElement}
   */
  const favButton = createComponent("post__fav");
  const isFavorited = findFavouritePost(meta.service, meta.user, meta.postID);

  if (isFavorited) {
    const [icon, text] = favButton.children;
    favButton.classList.add("post__fav--unfav");
    icon.textContent = "★";
    text.textContent = "Unfavorite";
  }

  if (!flagButton.classList.contains("post__flag--flagged")) {
    flagButton.addEventListener(
      "click", 
      handleFlagging(
        meta.service,
        meta.user,
        meta.postID
      )
    );
  }

  favButton.addEventListener(
    "click", 
    handleFavouriting(
      meta.service,
      meta.user,
      meta.postID
    )
  );

  buttonPanel.appendChild(favButton);
}

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} postID 
 * @returns {(event: MouseEvent) => Promise<void>}
 */
function handleFlagging(service, user, postID) {
  return async (event) => {
    /**
     * @type {HTMLButtonElement}
     */
    const button = event.target;
    const [icon, text] = button.children;
    const loadingIcon = LoadingIcon();
    const isConfirmed = confirm('Are you sure you want to flag this post for reimport?');

    button.classList.add("post__flag--loading");
    button.disabled = true;
    button.insertBefore(loadingIcon, text);


    try {
      if (isConfirmed) {
        const isFlagged = await kemonoAPI.posts.attemptFlag(service, user, postID);

        if (isFlagged) {
          const parent = button.parentElement;
          const newButton = createComponent("post__flag post__flag--flagged");

          parent.insertBefore(newButton, button);
          button.remove();
        }
      }
      
    } catch (error) {
      alert(error);

    } finally {
      loadingIcon.remove();
      button.disabled = false;
      button.classList.remove("post__flag--loading");
    }
  }
}

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} postID 
 * @returns {(event: MouseEvent) => Promise<void>}
 */
function handleFavouriting(service, user, postID) {
  return async (event) => {
    /**
     * @type {HTMLButtonElement}
     */
    const button = event.currentTarget;

    const [icon, text] = button.children;
    const loadingIcon = LoadingIcon();

    button.disabled = true;
    button.classList.add("post__fav--loading");
    button.insertBefore(loadingIcon, text);

    try {
      if ( button.classList.contains("post__fav--unfav") ) {
        const isUnfavorited = await removeFavouritePost(service, user, postID);

        if (isUnfavorited) {
          button.classList.remove("post__fav--unfav");
          icon.textContent = "☆";
          text.textContent = "Favorite";
        }

      } else {
        const isFavorited = await addFavouritePost(service, user, postID);

        if (isFavorited) {
          button.classList.add("user-header__favourite--unfav");
          icon.textContent = "★";
          text.textContent = "Unfavorite";
        }
      }

    } catch (error) {
      alert(error);

    } finally {
      loadingIcon.remove();
      button.disabled = false;
      button.classList.remove("post__fav--loading");
    }
  }
}

// expander.js
function Expand(c, t) {
  if (!c.naturalWidth) {
    return setTimeout(Expand, 10, c, t);
  }
  c.style.maxWidth = '100%';
  c.style.display = '';
  t.style.display = 'none';
  t.style.opacity = '';
};

/**
 * @param {MouseEvent} e 
 */
function Expander(e) {
  /**
   * @type {HTMLElement}
   */
  var t = e.target;
  if (t.parentNode.classList.contains('fileThumb')) {
    e.preventDefault();
    if (t.hasAttribute('data-src')) {
      var c = document.createElement('img');
      c.setAttribute('src', t.parentNode.getAttribute('href'));
      c.style.display = 'none';
      t.parentNode.insertBefore(c, t.nextElementSibling);
      t.style.opacity = '0.75';
      setTimeout(Expand, 10, c, t);
    } else {
      var a = t.parentNode;
      a.firstChild.style.display = '';
      a.removeChild(t);
      a.offsetTop < window.pageYOffset && a.scrollIntoView({ top: 0, behavior: 'smooth' });
    }
  }
};
