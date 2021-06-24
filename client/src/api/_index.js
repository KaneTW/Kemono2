/**
 * The map of error names and their messages.
 */
export const errorList = new Map([
  ["001", "Could not save favorite post."],
  ["002", "Could not remove favorite post."],
  ["003", "Could not save favorite artist."],
  ["004", "Could not remove favorite artist."],
]);

export async function retrieveFavorites() {
  try {
    const response = await kemonoFetch("/api/favorites");

    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    /**
     * @type {string}
     */
    const favs = await response.text();
    return favs;
    
  } catch (error) {
    console.log(error);
    alert(error);
  }

}

/**
 * @param {string} service 
 * @param {string} userID 
 */
export async function favoriteArtist(service, userID) {
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
export async function unfavoriteArtist(service, userID) {
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

/**
 * Generic request for Kemono API.
 * @param {RequestInfo} endpoint 
 * @param {RequestInit} options 
 * @returns {Promise<Response>}
 */
async function kemonoFetch(endpoint, options) {
  const url = new URL(endpoint, location.origin).toString();

  try {
    const response = await fetch(url, options);

    if (response.redirected) {
      location = addURLParam(response.url, "redir", location.pathname);
    }

    return response;

  } catch (error) {
    alert(`Kemono request error: ${error}`);
  }
}

/**
 * @param {string} url 
 * @param {string} paramName 
 * @param {string} paramValue 
 * @returns {string}
 */
function addURLParam(url, paramName, paramValue) {
  var newURL = new URL(url);
  newURL.searchParams.set(paramName, paramValue);
  return newURL.toString();
}
