import { kemonoAPI } from "@wp/api";
import { createComponent } from "@wp/js/component-factory";
import { waitAsync } from "@wp/utils";

/**
 * @typedef Stats
 * @property {string} importID
 * @property {HTMLSpanElement} status
 * @property {HTMLSpanElement} count
 * @property {number} cooldown
 * @property {number} retries
 */

/**
 * TODOs: 
 * - service heuristics
 * - error handling
 * @param {HTMLElement} section 
 */
export async function importerStatusPage(section) {
  /**
   * @type {HTMLDivElement}
   */
  const importInfo = section.querySelector(".import__info");
  /**
   * @type {[HTMLDivElement, HTMLDivElement]}
   */
  const [importStats, buttonPanel] = importInfo.children;
  const [status, count] = importStats.children;
  /**
   * @type {Stats}
   */
  const stats = {
    importID: document.head.querySelector("meta[name='import_id']").content,
    status: status.children[1],
    count: count.children[1],
    cooldown: 5000,
    retries: 0,
  }
  /**
   * @type {HTMLParagraphElement}
   */
  const loadingPlaceholder = section.querySelector(".loading-placeholder");
  /**
   * @type {HTMLOListElement}
   */
  const logList = section.querySelector(".log-list");
  
  initButtons(buttonPanel, logList);
  const logs = await kemonoAPI.api.logs(stats.importID);

  if (logs) {
    populateLogList(logs, logList, loadingPlaceholder);
    stats.status.textContent = "In Progress";
    stats.count.textContent = logs.length;
    count.classList.remove("import__count--invisible");

    await waitAsync(stats.cooldown);
    await updateLogList(logs, logList, stats);
  } else {
    loadingPlaceholder.classList.add("loading-placeholder--complete");
    alert("Failed to fetch the logs, try reloading the page.");
  }
}

/**
 * @param {HTMLDivElement} buttonPanel
 * @param {HTMLOListElement} logList
 */
function initButtons(buttonPanel, logList) {
  /**
   * @type {HTMLButtonElement[]}
   */
  const [reverseButton] = buttonPanel.children;

  reverseButton.addEventListener("click", reverseList(logList));
}

/**
 * @param {HTMLOListElement} logList 
 * @returns {(event: MouseEvent) => void}
 */
function reverseList(logList) {
  return (event) => {
    logList.classList.toggle("log-list--reversed");
  }
}

/**
 * @param {string[]} logs 
 * @param {HTMLOListElement} logList 
 * @param {HTMLParagraphElement} loadingItem
 */
function populateLogList(logs, logList, loadingItem){
  const fragment = document.createDocumentFragment();

  logs.forEach((log) => {
    const logItem = LogItem(log);
    fragment.appendChild(logItem);
  });

  loadingItem.classList.add("loading-placeholder--complete")
  logList.appendChild(fragment);
  logList.classList.add("log-list--loaded");
}

/**
 * TODO: finishing condition.
 * @param {string[]} logs 
 * @param {HTMLOListElement} logList 
 * @param {Stats} stats
 */
async function updateLogList(logs, logList, stats) {
  let newLogs = await kemonoAPI.api.logs(stats.importID);

  if (!newLogs) {

    if (stats.retries === 5) {
      stats.status.textContent = "Fatal Error";
      return;
    }

    await waitAsync(stats.cooldown);
    stats.retries++
    return await updateLogList(logs, logList, stats);
  }

  const diff = newLogs.length - logs.length;

  if (diff === 0) {
    stats.cooldown = stats.cooldown * 2;
    await waitAsync(stats.cooldown);
    return await updateLogList(logs, logList, stats);
  }

  const diffLogs = newLogs.slice(newLogs.length - diff);
  const fragment = document.createDocumentFragment();
  diffLogs.forEach((log) => {
    const logItem = LogItem(log);
    fragment.appendChild(logItem);
  });
  logs.push(...diffLogs);
  logList.appendChild(fragment);
  stats.count.textContent = logs.length;

  await waitAsync(stats.cooldown);
  return await updateLogList(logs, logList, stats);
}

/**
 * @param {string} message 
 */
function LogItem(message) {
  /**
   * @type {HTMLLIElement}
   */
  const item = createComponent("log-list__item");
  
  item.textContent = message;

  return item;
}
