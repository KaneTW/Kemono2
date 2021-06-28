import { initComponentFactory } from "@wp/pages/components/_index";
import { userPage } from "./user";
import { registerPage } from "./register";
import { postPage } from "./post";

const main = document.querySelector("main");
/**
 * @type {HTMLElement}
 */
const footer = document.querySelector(".global-footer");
/**
 * The map of page names and their callbacks.
 */
const pages = new Map([
  ["user", userPage],
  ["register", registerPage],
  ["post", postPage]
]);

initComponentFactory(footer);

/**
 * Initialises the scripts on the page..
 */
export function initSections() {
  /**
   * @type {NodeListOf<HTMLElement>}
   */
  const sections = main.querySelectorAll("main > .site-section");
  const accButtons = document.querySelector("#account-buttons");
  let isLoggedIn = localStorage.getItem('logged_in');

  sections.forEach(section => {
    const sectionName = /site-section--([a-z]+)/i.exec(section.className)[1];

    if (pages.has(sectionName)) {
      pages.get(sectionName)(section);
    }
  });

  if (isLoggedIn) {
    accButtons.innerHTML += `
      <li><a href="/favorites">[Favorites]</a></li>
      <li><a id="logout" href="/account/logout">[Logout]</a></li>
    `
    document.getElementById('logout').addEventListener('click', e => {
      e.preventDefault();
      localStorage.removeItem('logged_in');
      localStorage.removeItem('favs');
      localStorage.removeItem('post_favs');
      location.href = '/account/logout';
    })
  } else {
    accButtons.innerHTML += `
      <li><a href="/account/login">[Login]</a></li>
    `
  }
}
