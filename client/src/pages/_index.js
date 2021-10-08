import { bansPage } from "./bans";
import { userPage } from "./user";
import { registerPage } from "./account/_index.js";
import { postPage } from "./post";
import { importerPage } from "./importer_list";
import { importerStatusPage } from "./importer_status";
import { importerDMSPage } from "./importer_dms";
import { postsPage } from "./posts";
import { artistsPage } from "./artists";
import { updatedPage } from "./updated";
import { uploadPage } from "./upload";

export { adminPageScripts } from "./account/administrator/_index.js";
export { moderatorPageScripts } from "./account/moderator/_index.js";
/**
 * The map of page names and their callbacks.
 */
export const globalPageScripts = new Map([
  ["user", userPage],
  ["register", registerPage],
  ["post", postPage],
  ["importer", importerPage],
  ["bans", bansPage],
  ["importer-status", importerStatusPage],
  ["importer-dms", importerDMSPage],
  ["posts", postsPage],
  ["artists", artistsPage],
  ["updated", updatedPage],
  ["upload", uploadPage],
]);
