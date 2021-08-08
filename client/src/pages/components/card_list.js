import { createComponent } from "./_index";

/**
 * TODO: layout switch button.
 * @param {HTMLElement} element 
 * @param {string} layout 
 */
export function CardList(element=null, layout="feature") {
  const cardList = element
    ? initFromElement(element)
    : initFromScratch();
  let currentLayout = layout;

  return cardList;
}

/**
 * @param {HTMLElement} element 
 */
function initFromElement(element) {
  /**
   * @type {HTMLDivElement}
   */
  const cardContainer = element.querySelector(".card-list__items");
  /**
   * @type {NodeListOf<HTMLElement>}
   */
  const itemListElements = element.querySelectorAll(".card-list__items > *");

  return {
    cardList: element,
    cardContainer,
    cardItems: Array.from(itemListElements)
  };
}

function initFromScratch() {
  /**
   * @type {HTMLElement}
   */
  const cardList = createComponent("card-list");
  /**
   * @type {HTMLDivElement}
   */
  const cardContainer = cardList.querySelector(".card-list__items");
  /**
   * @type {HTMLElement[]}
   */
  const cardItems = [];

  return {
    cardList,
    cardContainer,
    cardItems
  };
}
