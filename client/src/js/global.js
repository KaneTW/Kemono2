import "./global.scss";
import { initSections } from "@wp/pages";
import { initFavorites } from "@wp/js/favorites";
import { fixImageLinks } from "@wp/utils";

const isLoggedIn = localStorage.getItem('logged_in') === "yes";

if (isLoggedIn) {
  initFavorites()
}
fixImageLinks(document.images);
initSections(isLoggedIn);

// function isStorageAvailable() {
//   try {
//     localStorage.setItem("__storage_test__", "__storage_test__");
//     localStorage.removeItem("__storage_test__");
//     return true;
//   } catch (error) {
//     return false;
//   }
// }
