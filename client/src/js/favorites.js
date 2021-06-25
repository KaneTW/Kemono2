import { favoriteArtist, retrieveFavorites, unfavoriteArtist } from "@wp/api/_index";

export async function initFavorites() {
  let storageFavs = localStorage.getItem('favs');

  if (!storageFavs) {
    /**
     * @type {string}
     */
    const favs = await retrieveFavorites();

    if (favs) {
      localStorage.setItem("favs", favs);
    }
  }
}

/**
 * @param {string} id 
 * @param {string} service
 */
export function findFavouriteArtist(id, service) {
  /**
   * @type {FavoriteItem[]}
   */
  const favList = JSON.parse(localStorage.getItem("favs"));

  if (!favList) {
    return undefined;
  }
  
  const favArtist = favList.find((favItem) => {
    return favItem.id === id && favItem.service === service;
  });

  return favArtist;
}

/**
 * @param {string} id 
 * @param {string} service 
 */
export async function addFavourite(id, service) {
  const isFavorited = await favoriteArtist(service, id);

  if (!isFavorited) {
    return false;
  }

  const newFavs = await retrieveFavorites();
  localStorage.setItem("favs", newFavs);

  return true;
}

/**
 * @param {string} id 
 * @param {string} service 
 */
export async function removeFavourite(id, service) {
  const isUnfavorited = await unfavoriteArtist(service, id);

  if (!isUnfavorited) {
    return false
  }

  const favItems = await retrieveFavorites();
  localStorage.setItem("favs", favItems);

  return true;
}

/**
 * Combines `id` and `service` into a single entry
 * for the memory storage purposes.
 * Because IDs by themselves are only guarantied
 * to be unique within a service.
 * @param {FavoriteItem} fav
 */
function uniqueID(fav) {
  return `${fav.id}-${fav.service}`;
}
