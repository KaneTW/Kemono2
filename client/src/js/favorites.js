import { kemonoAPI } from "@wp/api";

export async function initFavorites() {
  let artistFavs = localStorage.getItem('favs');
  let postFavs = localStorage.getItem('post_favs');

  if (!artistFavs || artistFavs === "undefined") {
    /**
     * @type {string}
     */
    const favs = await kemonoAPI.favorites.retrieveFavoriteArtists();

    if (favs) {
      localStorage.setItem("favs", favs);
    }
  }

  if (!postFavs || postFavs === "undefined") {
    /**
     * @type {string}
     */
    const favs = await kemonoAPI.favorites.retrieveFavoritePosts();

    if (favs) {
      localStorage.setItem("post_favs", favs);
    }
  }
}

async function saveFavouriteArtists() {
  try {
    const favs = await kemonoAPI.favorites.retrieveFavoriteArtists();
    
    if (!favs) {
      alert("Could not retrieve favorite artists");
      return false;
    }

    localStorage.setItem("favs", favs);
    return true;

  } catch (error) {
    console.error(error);
  }
}

async function saveFavouritePosts() {
  try {
    const favs = await kemonoAPI.favorites.retrieveFavoritePosts();
    
    if (!favs) {
      alert("Could not retrieve favorite posts");
      return false;
    }

    localStorage.setItem("post_favs", favs);
    return true;

  } catch (error) {
    console.error(error);
  }
}

/**
 * @param {string} id 
 * @param {string} service
 * @returns {Promise<KemonoAPI.Favorites.User> | undefined}
 */
export async function findFavouriteArtist(id, service) {
  /**
   * @type {KemonoAPI.Favorites.User[]}
   */
  let favList;

  try {
    favList = JSON.parse(localStorage.getItem("favs"));

  } catch (error) {
    // corrupted entry
    if (error instanceof SyntaxError) {
      const isSaved = await saveFavouriteArtists();

      if (!isSaved) {
        return undefined;
      }

      return await findFavouriteArtist(id, service);
    }
  }

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
 * @returns {Promise<KemonoAPI.Favorites.Post> | undefined}
 */
export async function findFavouritePost(service, user, postID) {
  /**
   * @type {KemonoAPI.Favorites.Post[]}
   */
  let favList;
 
  try {
    favList = JSON.parse(localStorage.getItem("post_favs"));
    
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

  } catch (error) {
    // corrupted entry
    if (error instanceof SyntaxError) {
      const isSaved = await saveFavouritePosts();

      if (!isSaved) {
        return undefined;
      }

      return await findFavouritePost(service, user, postID);
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
