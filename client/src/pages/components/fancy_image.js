import { createComponent } from "./_index";

/**
 * @param {HTMLSpanElement} element 
 * @param {string} src 
 * @param {string} srcset 
 * @param {boolean} isLazy 
 * @param {string} alt 
 * @param {string} className 
 */
export function FancyImage(
  element = null, 
  src,
  srcset = src,
  isLazy = true,
  alt = "",
  className = null
) {
  /**
   * @type {HTMLSpanElement}
   */
  const fancyImage = element
    ? initFromElement(element)
    : initFromScratch(src, srcset, isLazy, alt, className);
  
  return fancyImage;
}

/**
 * @param {HTMLSpanElement} element 
 */
function initFromElement(element) {
  return element;
}

/**
 * @param {string} src 
 * @param {string} srcset 
 * @param {boolean} isLazy 
 * @param {string} alt 
 * @param {string} className 
 */
function initFromScratch(src, srcset, isLazy, alt, className) {
  /**
   * @type {HTMLSpanElement}
   */
  const fancyImage = createComponent("fancy-image");
  /**
   * @type {HTMLImageElement}
   */
  const img = fancyImage.querySelector(".fancy-image__image");

  img.src = src;
  img.srcset = srcset;
  img.alt = alt;
  
  if (className) { fancyImage.classList.add(className) };
  
  if (isLazy) {
    img.loading = "lazy"
  } else {
    img.loading = "eager"
  }

  return fancyImage;
}
