import "./global.scss";
import { initSections } from "@wp/pages/_index";
import { initFavorites } from "@wp/js/favorites";

const context = {
  isLoggedIn: localStorage.getItem('logged_in') === "yes"
}

context.isLoggedIn && initFavorites();
initSections();
