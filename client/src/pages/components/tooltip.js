import { createComponent } from "@wp/js/component-factory";

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
 * @param {string} actionName 
 */
export function registerMessage(element, actionName="") {
  /**
   * @type {HTMLParagraphElement}
   */
  const messageElement = element
    ? element
    : initFromScratch(actionName);

  return messageElement;
}

/**
 * @param {HTMLElement} element
 */
function initFromElement(element) {}

/**
 * @param {string} actionName
 */
function initFromScratch(actionName) {
  /**
   * @type {HTMLParagraphElement}
   */
  const message = createComponent("tooltip__message tooltip__message--register");
  /**
   * @type {HTMLSpanElement}
   */
  const action = message.querySelector(".tooltip__action");

  action.textContent = actionName;
  
  return message;
}
