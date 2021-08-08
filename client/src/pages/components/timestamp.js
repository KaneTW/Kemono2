import { createComponent } from "./_index";

/**
 * TODO: make it work with `Date` objects.
 * @param {HTMLTimeElement} element 
 * @param {string} date 
 * @param {string} className 
 */
export function Timestamp(
  element, 
  date, 
  isRelative = false, 
  className = null
) {
  const timestamp = element
    ? element
    : initFromScratch(date, isRelative, className)
  
  return timestamp;
}

/**
 * @param {string} date 
 * @param {boolean} isRelative 
 * @param {string} className 
 */
function initFromScratch(date, isRelative, className) {
  /**
   * @type {HTMLTimeElement}
   */
  const timestamp = createComponent("timestamp");

  timestamp.dateTime = date;
  
  if (className) {
    timestamp.classList.add(className);
  }

  if (isRelative) {
    timestamp.textContent = date;
  } else {
    timestamp.textContent = date;
  }

  return timestamp;
}
