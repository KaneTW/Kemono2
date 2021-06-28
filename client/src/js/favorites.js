import { kemonoAPI } from "@wp/api";

export async function initFavorites() {
  let artistFavs = localStorage.getItem('favs');
  let postFavs = localStorage.getItem('post_favs');

  if (!artistFavs) {
    /**
     * @type {string}
     */
    const favs = await kemonoAPI.favorites.retrieveFavoriteArtists();

    if (favs) {
      localStorage.setItem("favs", favs);
    }
  }

  if (!postFavs) {
    /**
     * @type {string}
     */
    const favs = await kemonoAPI.favorites.retrieveFavoritePosts();

    if (favs) {
      localStorage.setItem("post_favs", favs);
    }
  }
}

/**
 * @param {string} id 
 * @param {string} service 
 */
export async function addFavouriteArtist(id, service) {
  const isFavorited = await kemonoAPI.favorites.favoriteArtist(service, id);

  if (!isFavorited) {
    return false;
  }

  const newFavs = await kemonoAPI.favorites.retrieveFavoriteArtists();
  localStorage.setItem("favs", newFavs);

  return true;
}

/**
 * @param {string} id 
 * @param {string} service 
 */
export async function removeFavouriteArtist(id, service) {
  const isUnfavorited = await kemonoAPI.favorites.unfavoriteArtist(service, id);

  if (!isUnfavorited) {
    return false
  }

  const favItems = await kemonoAPI.favorites.retrieveFavoriteArtists();
  localStorage.setItem("favs", favItems);

  return true;
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
 * @param {string} service 
 * @param {string} user 
 * @param {string} postID 
 */
export async function addFavouritePost(service, user, postID) {
  const isFavorited = await kemonoAPI.favorites.favoritePost(service, user, postID);

  if (!isFavorited) {
    return false;
  }

  const newFavs = await kemonoAPI.favorites.retrieveFavoritePosts();
  localStorage.setItem("post_favs", newFavs);

  return true;
};

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} postID 
 * @returns 
 */
export async function removeFavouritePost(service, user, postID) {
  const isUnfavorited = await kemonoAPI.favorites.unfavoritePost(service, user, postID);

  if (!isUnfavorited) {
    return false
  }

  const favItems = await kemonoAPI.favorites.retrieveFavoritePosts();
  localStorage.setItem("post_favs", favItems);

  return true;
};

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} postID 
 */
export function findFavouritePost(service, user, postID) {
  /**
   * @type {KemonoAPI.Favorites.Post[]}
   */
  const favList = JSON.parse(localStorage.getItem("post_favs"));

  if (!favList) {
    return undefined;
  }
  const favPost = favList.find((favItem) => {
    const isMatch = favItem.id === postID 
      && favItem.service === service
      && favItem.user === user;
    return isMatch;
  });

  return favPost;
}
