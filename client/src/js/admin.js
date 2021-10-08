import "./admin.scss";
import { fixImageLinks } from "@wp/utils";
import { initSections } from "./page-loader";
import { adminPageScripts } from "@wp/pages";

fixImageLinks(document.images);
initSections(adminPageScripts);
