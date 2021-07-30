import { createComponent } from "./_index";

/**
 * @type {HTMLDivElement}
 */
const tooltip = document.getElementById("flying-tooltip");
/**
 * @type {[HTMLButtonElement, HTMLSpanElement]}
 */
const [closeButton, messageContainer] = tooltip.children;

closeButton.addEventListener("click", (event) => {
  tooltip.classList.remove("tooltip--shown");
});

/**
 * @param {HTMLElement} element 
 * @param {HTMLParagraphElement} messageElement 
 */
export function showTooltip(element, messageElement) {
  const { left, bottom } = element.getBoundingClientRect();

  tooltip.classList.remove("tooltip--shown");
  messageContainer.replaceWith(messageElement);
  tooltip.style.setProperty("--local-x", `${left}px`);
  tooltip.style.setProperty("--local-y", `${bottom}px`);
  tooltip.classList.add("tooltip--shown");
}

/**
 * TODO: init from `action_name`
 * @param {HTMLElement} element 
 * @param {string} action_name 
 */
export function registerMessage(element, action_name="") {
  /**
   * @type {HTMLParagraphElement}
   */
  const messageElement = element
    ? element
    : createComponent("tooltip__message tooltip__message--register");

  return messageElement;
}
