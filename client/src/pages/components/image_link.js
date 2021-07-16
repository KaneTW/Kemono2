import { createComponent } from "./_index";

/**
 * @param {HTMLAnchorElement} element 
 * @param {string} url 
 * @param {string} src 
 * @param {string} alt 
 * @param {string} srcset 
 * @param {boolean} isLazy 
 * @param {boolean} isNoop 
 * @param {string} className 
 */
export function ImageLink(
  element = null, 
  url, 
  src = url, 
  alt = "", 
  srcset = src, 
  isLazy = true,
  isNoop = true,
  className = null
  ) {
  
  const imageLink = element
    ? initFromElement(element)
    : initFromScratch(url, src, alt, srcset, isLazy, isNoop, className);
  
  return imageLink;
}

/**
 * @param {HTMLAnchorElement} element 
 */
function initFromElement(element) {
  return element;
}

/**
 * @param {string} url 
 * @param {string} src 
 * @param {string} alt 
 * @param {string} srcset 
 * @param {boolean} isLazy 
 * @param {boolean} isNoop 
 * @param {string} className 
 */
function initFromScratch(url, src, alt, srcset, isLazy, isNoop, className) {
  /**
   * @type {HTMLAnchorElement}
   */
  const imageLink = createComponent("fancy-link image-link");
  /**
   * @type {HTMLImageElement}
   */
  const image = imageLink.querySelector(".fancy-image__image");

  imageLink.href = url;
  imageLink.alt = alt;
  image.src = src;
  image.srcset = srcset; 

  if (isNoop) {
    imageLink.target = "_blank";
    imageLink.rel = "noopener noreferrer"
  }

  if (isLazy) {
    image.loading = "lazy";
  } else {
    image.loading = "eager";
  }

  if (className) {
    imageLink.classList.add(className);
  }

  return imageLink;
}
