/**
 * The map of error names and their messages.
 */
export const errorList = new Map([
  ["001", "Could not favorite the post."],
  ["002", "Could not unfavorite the post."],
  ["003", "Could not favorite the artist."],
  ["004", "Could not unfavorite the artist."],
  ["005", "There might already be a flag here."],
  ["006", "Could not retrieve the list of bans."],
  ["007", "Could not retrieve a banned artist."],
  ["008", "Could not retrieve artists."],
  ["009", "Could not retrieve import logs."],
]);

/**
 * Generic request for Kemono API.
 * @param {RequestInfo} endpoint 
 * @param {RequestInit} options 
 * @returns {Promise<Response>}
 */
export async function kemonoFetch(endpoint, options) {
  try {
    const response = await fetch(endpoint, options);

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
