import { favoriteArtist, retrieveFavorites, unfavoriteArtist } from "@wp/api/_index";

/**
 * @type {Map<string, FavoriteItem}
 */
const favourites = new Map();

// save into localStorage upon closing the page
window.addEventListener("beforeunload", saveFavourites);

export async function initFavorites() {
  let storageFavs = localStorage.getItem('favs');
  /**
   * @type {FavoriteItem[]}
   */
  let parsedFavs;

  if (!storageFavs) {
    const favs = await retrieveFavorites();

    if (favs) {
      localStorage.setItem("favs", favs);
    }
    
  }

  parsedFavs = JSON.parse(storageFavs);

  if (parsedFavs.length !== 0) {
    parsedFavs.forEach(favItem => {
      favourites.set(uniqueID(favItem), favItem);
    });  
  }
}

export function saveFavourites() {
  if (localStorage.getItem("favs")) {
    localStorage.setItem(
      "favs", 
      JSON.stringify( favourites.values() )
    );
  }  
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
    // querying on fail because the server returns error even on success
    const favItems = await retrieveFavorites();
    localStorage.setItem("favs", favItems);
    return true
  }

  const isDeleted = favourites.delete( uniqueID({ id, service }) );

  if (!isDeleted) {
    return false;
  }

  localStorage.setItem("favs", JSON.stringify(favourites.values()));

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
