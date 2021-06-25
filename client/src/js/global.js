import "./global.scss";
import { initSections } from "@wp/pages/_index";
import { initFavorites } from "@wp/js/favorites";

const isLoggedIn = localStorage.getItem('logged_in') === "yes";

isLoggedIn && initFavorites();
initSections();

// function isStorageAvailable() {
//   try {
//     localStorage.setItem("__storage_test__", "__storage_test__");
//     localStorage.removeItem("__storage_test__");
//     return true;
//   } catch (error) {
//     return false;
//   }
// }
