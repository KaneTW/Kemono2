import { KemonoError } from "@wp/utils";
import { validateImportKey } from "@wp/lib";
import { showTooltip, registerMessage } from "@wp/components";

/**
 * @param {HTMLElement} section
 */
export function importerPage(section) {
  const isLoggedIn = localStorage.getItem("logged_in") === "yes";
  /**
   * @type {HTMLFormElement}
   */
  const form = document.forms["import-list"];
  const discordSection = form.querySelector("#discord-section");
  const dmConsentSection = form.querySelector("#dm-consent");

  form.addEventListener("change", switchDiscordSection(discordSection));
  form.addEventListener("change", switchConsentSection(dmConsentSection));
  form.addEventListener("submit", handleSubmit(isLoggedIn));
}

/**
 * @param {HTMLElement} discordSection
 * @returns {(event: Event) => void}
 */
function switchDiscordSection(discordSection) {
  return (event) => {
    if (event.target.id === "service") {
      event.stopPropagation();

      /**
       * @type {HTMLSelectElement}
       */
      const select = event.target;

      if (select.value === "discord") {
        discordSection.classList.remove("form__section--hidden");
      } else {
        discordSection.classList.add("form__section--hidden");
      }
    }
  }

}

/**
 * @param {HTMLElement} dmConsentSection
 * @returns {(event: Event) => void}
 */
function switchConsentSection(dmConsentSection) {
  return (event) => {
    if (event.target.id === "service") {
      event.stopPropagation();

      /**
       * @type {HTMLSelectElement}
       */
      const select = event.target;

      // the dm importer is currently patreon only
      if (select.value === "patreon") {
        dmConsentSection.classList.remove("form__section--hidden");
      } else {
        dmConsentSection.classList.add("form__section--hidden");
      }
    }
  }

}

/**
 * @param {boolean} isLoggedIn
 * @returns {(event: Event) => void}
 */
function handleSubmit(isLoggedIn) {
  return (event) => {
    /**
     * @type {HTMLFormElement}
     */
    const form = event.target;
    /**
     * @type {HTMLInputElement}
     */
    const dmConsent = form.elements["save-dms"];

    if (dmConsent.checked && !isLoggedIn) {
      event.preventDefault();
      showTooltip(dmConsent, registerMessage(null));
      return;
    }

    /**
     * @type {string}
     */
    const service = form.elements["service"].value;
    /**
     * @type {HTMLInputElement}
     */
    const importKeyInput = form.elements["session-key"];
    /**
     * @type {string}
     */
    const importKey = importKeyInput.value;

    if (!importKey.length) {
      event.preventDefault();
      const paragraph = document.createElement("p");
      paragraph.textContent = "Session key missing.";
      showTooltip(importKeyInput, paragraph);
      return;
    }

    const validatedKey = validateImportKey(importKey, service);

    if (validatedKey instanceof KemonoError) {
      event.preventDefault();
      const paragraph = document.createElement("p");
      paragraph.textContent = validatedKey.message;
      showTooltip(importKeyInput, paragraph);
      return;
    }

    importKeyInput.value = validatedKey;
  }
}
