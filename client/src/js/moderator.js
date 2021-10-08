import "./moderator.scss";
import { fixImageLinks } from "@wp/utils";
import { initSections } from "./page-loader";
import { moderatorPageScripts } from "@wp/pages";

fixImageLinks(document.images);
initSections(moderatorPageScripts);
