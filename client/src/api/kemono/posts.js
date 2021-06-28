import { kemonoFetch, errorList } from "./kemono-fetch";

export const posts = {
  attemptFlag
};

/**
 * @param {string} service 
 * @param {string} user 
 * @param {string} post_id 
 */
async function attemptFlag(service, user, post_id) {
  try {
    const response = await kemonoFetch(`/api/${service}/user/${user}/post/${post_id}/flag`, { method: "POST" });

    if (!response.ok) {
      alert(`Error 005 - ${errorList.get("005")}`)
      return false;
    }

    return true;

  } catch (error) {
    alert(error);
  }
}
