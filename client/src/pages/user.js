import { addFavourite, removeFavourite } from "@wp/js/favorites";
import { createComponent } from "./components/_index";

/** 
 * @param {HTMLElement} section
 */
export async function userPage(section) {
  const artistID = document.head.querySelector("[name='id']").content;
  const artistService = document.head.querySelector("[name='service']").content;
  /**
   * @type {HTMLButtonElement}
   */
  const favoriteButton = section.querySelector(".user-header__favourite");

  favoriteButton.addEventListener("click", handleFavouriting(artistID, artistService));
}

/**
 * @param {string} id
 * @param {string} service
 * @returns {(event: MouseEvent) => Promise<void>}
 */
function handleFavouriting(id, service) {
  return async (event) => {
    /**
     * @type {HTMLButtonElement}
     */
    const button = event.target;
    const [icon, text] = button.children;
    /**
     * @type {HTMLElement}
     */
    const loadingIcon = createComponent("loading-icon");
    const oldIcon = icon.textContent;

    button.classList.add("user-header__favourite--loading");
    icon.textContent = null;
    icon.appendChild(loadingIcon);
    button.disabled = true;

    try {

      if (button.classList.contains("user-header__favourite--unfav")) {
        const isRemoved = await removeFavourite(id, service);

        if (isRemoved) {
          button.classList.remove("user-header__favourite--unfav");
          loadingIcon.remove();
          icon.textContent = "☆";
          text.textContent = "Favorite";
        }
        
      } else {
        const isAdded = await addFavourite(id, service);

        if (isAdded) {
          button.classList.add("user-header__favourite--unfav");
          loadingIcon.remove();
          icon.textContent = "★";
          text.textContent = "Unfavorite";
        }
        
      }

    } catch (error) {
      alert(error)
      

    } finally {
      loadingIcon.remove();
      icon.textContent = oldIcon;
      button.disabled = false;
      button.classList.remove("user-header__favourite--loading");
    }
    
  }
}

function favorite_artist(service, user) {
  fetch(`/favorites/artist/${service}/${user}`, {
    method: 'POST'
  }).then(res => {
    if (res.ok) {
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
    if (res.ok) {
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
