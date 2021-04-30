(function() {
  "use strict";

  /**
   * @type {HTMLFormElement}
   */
  const form = document.querySelector(".form");
  const discordSection = form.querySelector("#discord-section");

  form.addEventListener("change", switchDiscordSection);

  /**
   * @param {Event} event
   */
  function switchDiscordSection(event) {

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
})();
