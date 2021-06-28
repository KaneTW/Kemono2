/**
 * The map of error names and their messages.
 */
export const errorList = new Map([
  ["001", "Could not favorite post."],
  ["002", "Could not unfavorite post."],
  ["003", "Could not favorite artist."],
  ["004", "Could not unfavorite artist."],
  ["005", "There might already be a flag here."],
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
