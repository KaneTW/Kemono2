import { favoriteArtist, retrieveFavorites, unfavoriteArtist } from "@wp/api/_index";

/**
 * @type {Map<string, FavoriteItem}
 */
const favourites = new Map();

// save into localStorage upon closing the page
window.addEventListener("beforeunload", saveFavourites);

export async function initFavorites() {
  let isLoggedIn = localStorage.getItem('logged_in');

  if (isLoggedIn) {
    let storageFavs = localStorage.getItem('favs');
    /**
     * @type {FavoriteItem[]}
     */
    let favList;

    if (!storageFavs) {
      favList = await retrieveFavorites();
    } else {
      favList = JSON.parse(storageFavs);
    }
  
    favList.forEach(favItem => {
      favourites.set(uniqueID(favItem), favItem);
    });  
  }
  
}

export function saveFavourites() {
  /**
   * @type {FavoriteItem[]}
   */
  let localFavs = [];
  favourites.forEach(favItem => {
    localFavs.push(favItem);
  })

  localStorage.setItem("favs", JSON.stringify(localFavs));
}

/**
 * @param {string} id 
 * @param {string} service
 */
export function findFavouriteArtist(id, service) {
  return favourites.get(uniqueID({ id, service }));
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
  newFavs.forEach(favItem => {
    if ( !favourites.has( uniqueID(favItem) ) ) {
      favourites.set( uniqueID(favItem), favItem )
    }
  })

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

  const isDeleted = favourites.delete( uniqueID({ id, service }) );
  return isDeleted;
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
