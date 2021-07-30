import { initComponentFactory } from "@wp/components";
import { initShell } from "./components/shell";
import { bansPage } from "./bans";
import { userPage } from "./user";
import { registerPage } from "./register";
import { postPage } from "./post";
import { importerPage } from "./importer_list";
import { importerStatusPage } from "./importer_status";
import { importerDMSPage } from "./importer_dms";
import { postsPage } from "./posts";
import { artistsPage } from "./artists";

/**
 * The map of page names and their callbacks.
 */
const pages = new Map([
  ["user", userPage],
  ["register", registerPage],
  ["post", postPage],
  ["importer", importerPage],
  ["bans", bansPage],
  ["importer-status", importerStatusPage],
  ["importer-dms", importerDMSPage],
  ["posts", postsPage],
  ["artists", artistsPage],
]);

/**
 * Initialises the scripts on the page.
 * @param {boolean} isLoggedIn
 */
export function initSections(isLoggedIn) {
  const header = document.querySelector(".global-header");
  const main = document.querySelector("main");
  /**
   * @type {HTMLElement}
   */
  const footer = document.querySelector(".global-footer");
  /**
   * @type {NodeListOf<HTMLElement>}
   */
  const sections = main.querySelectorAll("main > .site-section");
  
  initShell(header, isLoggedIn);
  initComponentFactory(footer);
  sections.forEach(section => {
    const sectionName = /site-section--([a-z\-]+)/i.exec(section.className)[1];

    if (pages.has(sectionName)) {
      const sectionCallback = pages.get(sectionName);
      sectionCallback(section);
    }
  });

  
}
