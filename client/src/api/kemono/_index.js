import { errorList } from "./kemono-fetch";
import { favorites } from "./favorites";
import { posts } from "./posts";
import { api } from "./api";

/**
 * @type {KemonoAPI}
 */
export const kemonoAPI = {
  errors: errorList,
  favorites,
  posts,
  api
}
