/**
 * @param {HTMLElement} section 
 */
export function importerDMSPage(section) {
  const accountID = document.head.querySelector('meta[name="account_id"]').content;
  /**
   * @type {HTMLFormElement}
   */
  const form = document.forms["dm-approval"];

  form.addEventListener("submit", handleDMApproval(accountID));
}

/**
 * @param {Event} event 
 */
function handleDMApproval(event) {

}
