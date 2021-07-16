import { errorList, kemonoFetch } from "./kemono-fetch";

export const api = {
  bans,
  bannedArtist,
  creators
};

async function bans() {
  try {
    const response = await kemonoFetch('/api/bans', { method: "GET" });

    if (!response.ok) {
      alert(`Error 006 - ${errorList.get("006")}`);
      return null;
    }

    /**
     * @type {KemonoAPI.API.BanItem[]}
     */
    const banItems = await response.json();
    
    return banItems;

  } catch (error) {
    alert(error);
  }
}

/**
 * @param {string} id 
 * @param {string} service 
 */
async function bannedArtist(id, service) {
  const params = new URLSearchParams([
    ["service", service ],
  ]).toString();

  try {
    const response = await kemonoFetch(`/api/lookup/cache/${id}?${params}`);

    if (!response.ok) {
      alert(`Error 007 - ${errorList.get("007")}`);
      return null;
    }

    /**
     * @type {KemonoAPI.API.BannedArtist}
     */
    const artist = await response.json();

    return artist;

  } catch (error) {
    alert(error);
  }
}

async function creators() {
  try {
    const response = await kemonoFetch('/api/creators', { method: "GET" });

    if (!response.ok) {
      alert(`Error 008 - ${errorList.get("008")}`);
      return null;
    }

    /**
     * @type {KemonoAPI.Artist[]}
     */
    const artists = await response.json();
    
    return artists;

  } catch (error) {
    alert(error);
  }
}
