import { kemonoFetch, errorList } from "./kemono-fetch";

/**
 * @type {KemonoAPI.Favorites}
 */
export const favorites = {
  retrieveFavoriteArtists,
  favoriteArtist,
  unfavoriteArtist,
  retrieveFavoritePosts,
  favoritePost,
  unfavoritePost
};

async function retrieveFavoriteArtists() {
  const params = new URLSearchParams([
    ["type", "artist"]
  ]).toString();

  try {
    const response = await kemonoFetch(`/api/favorites?${params}`);

    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    /**
     * @type {string}
     */
    const favs = await response.text();
    return favs;
    
  } catch (error) {
    alert(error);
  }

}

/**
 * @param {string} service 
 * @param {string} userID 
 */
async function favoriteArtist(service, userID) {
  try {
    const response = await kemonoFetch(
      `/favorites/artist/${service}/${userID}`, 
      { method: "POST" }
    );

    if (!response.ok) {
      alert(`Error 003 - ${errorList.get("003")}`);
      return false;
    }
    
    return true;

  } catch (error) {
    alert(error);
  }
}

/**
 * @param {string} service 
 * @param {string} userID 
 */
async function unfavoriteArtist(service, userID) {
  try {
    const response = await kemonoFetch(
      `/favorites/artist/${service}/${userID}`, 
      { method: "DELETE" }
    );

    if (!response.ok) {
      alert(`Error 004 - ${errorList.get("004")}`);
      return false;
    }
    
    return true;

  } catch (error) {
    alert(error);
  }
}

async function retrieveFavoritePosts() {
  const params = new URLSearchParams([
    ["type", "post"]
  ]).toString();

  try {
    const response = await kemonoFetch(`/api/favorites?${params}`);

    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    /**
     * @type {string}
     */
    const favs = await response.text();
    return favs;
    
  } catch (error) {
    alert(error);
  }
}

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} post_id 
 */
async function favoritePost(service, user, post_id) {
  try {
    const response = await kemonoFetch(
      `/favorites/post/${service}/${user}/${post_id}`,
      { method: 'POST' }
    );

    if (!response.ok) {
      alert(`Error 001 - ${errorList.get("001")}`);
      return false;
    }

    return true;

  } catch (error) {
    alert(error);
  }
}

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} post_id 
 */
async function unfavoritePost(service, user, post_id) {
  try {
    const response = await kemonoFetch(
      `/favorites/post/${service}/${user}/${post_id}`, 
      { method: "DELETE" }
    );

    if (!response.ok) {
      alert(`Error 002 - ${errorList.get("002")}`);
      return false;
    }

    return true;

  } catch (error) {
    alert(error);
  }
}
