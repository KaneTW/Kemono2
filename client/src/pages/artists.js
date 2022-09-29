import { kemonoAPI } from "@wp/api";
import { CardList, UserCard } from "@wp/components";
import { isLoggedIn } from "@wp/js/account";
import { findFavouriteArtist } from "@wp/js/favorites";

/**
 * @type {KemonoAPI.User[]}
 */
let creators;
/**
 * @type {KemonoAPI.User[]}
 */
let filteredCreators;
let skip = parseInt(window.location.hash.substring(1).split('&').find(e => e.split('=')[0] === 'o')?.split('=')[1]) || 0;
let limit = 50;
const TOTAL_BUTTONS = 5;
const OPTIONAL_BUTTONS = TOTAL_BUTTONS - 2;
const MANDATORY_BUTTONS = TOTAL_BUTTONS - OPTIONAL_BUTTONS;

// generic debounce function, idk jsdoc, figure it out :)
function debounce(func, timeout = 300){
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => { func.apply(this, args); }, timeout);
  };
}

/**
 * @param {HTMLElement} section
 */
export async function artistsPage(section) {
  /**
   * @type {HTMLHeadingElement}
   */
  const displayStatus = document.getElementById("display-status");
  /**
   * @type {HTMLDivElement}
   */
  const loadingStatus = document.getElementById("loading");
  /**
   * @type {HTMLFormElement}
   */
  const searchForm = document.forms["search-form"];
  /**
   * @type {HTMLSelectElement}
   */
  const orderSelect = searchForm.elements["order"];
  /**
   * @type {HTMLSelectElement}
   */
  const serviceSelect = searchForm.elements["service"];
  /**
   * @type {HTMLSelectElement}
   */
  const sortSelect = searchForm.elements["sort_by"];
  /**
   * @type {HTMLInputElement}
   */
  const queryInput = searchForm.elements["q"];
  /**
   * @type {HTMLDivElement}
   */
  const cardListElement = section.querySelector(".card-list");
  const { cardList, cardContainer } = CardList(cardListElement);
  const pagination = {
    top: document.getElementById("paginator-top"),
    bottom: document.getElementById("paginator-bottom")
  }

  Array.from(cardContainer.children).forEach(async (userCard) => {
    const { id, service } = userCard.dataset;
    const isFav = isLoggedIn && await findFavouriteArtist(id, service);

    if (isFav) {
      userCard.classList.add("user-card--fav");
    }
  })
  section.addEventListener("click", async (event) => {
    /**
     * @type {HTMLAnchorElement}
     */
    const button = event.target;
    const isB = button.parentElement.classList.contains('paginator-button-ident');
    if (
      (button.classList.contains('paginator-button-ident')
      && button.dataset
      && button.dataset.value)
      ||
      (isB
      && button.parentElement.dataset
      && button.parentElement.dataset.value)
    ) {
      event.preventDefault();
      skip = Number(isB ? button.parentElement.dataset.value : button.dataset.value);
      window.location.hash = 'o=' + skip;
      filterCards(
        orderSelect.value,
        serviceSelect.value,
        sortSelect.value,
        queryInput.value
      );
      await loadCards(displayStatus, cardContainer, pagination, sortSelect.value);
    }
  });

  searchForm.addEventListener("submit", (event) => event.preventDefault());
  queryInput.addEventListener("change", handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination));
  // 300 ms delay between each keystroke, trigger a new search on each new letter added or removed
  // debounce lets you do this by waiting for the user to stop typing first
  queryInput.addEventListener("keydown", debounce(handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination), 300));
  serviceSelect.addEventListener("change", handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination));
  sortSelect.addEventListener("change", handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination));
  orderSelect.addEventListener("change", handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination));

  await retrieveArtists(loadingStatus);
  handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination)(null);
}

/**
 * @param {HTMLSelectElement} orderSelect
 * @param {HTMLSelectElement} serviceSelect
 * @param {HTMLSelectElement} sortSelect
 * @param {HTMLInputElement} queryInput
 * @param {HTMLDivElement} displayStatus
 * @param {HTMLDivElement} cardContainer
 * @param {{ top: HTMLElement, bottom: HTMLElement }} pagination
 * @return {(event: Event) => void}
 */
function handleSearch(
  orderSelect,
  serviceSelect,
  sortSelect,
  queryInput,
  displayStatus,
  cardContainer,
  pagination
) {
  return async (event) => {
    filterCards(
      orderSelect.value,
      serviceSelect.value,
      sortSelect.value,
      queryInput.value
    );
    await loadCards(displayStatus, cardContainer, pagination, sortSelect.value);
  }
}

// localeCompare isn't slow itself, but this is still faster and we're processing a LOT of data here!
// better get any speed gains we can
function fastCompare(a, b) {
  return a < b ? -1 : (a > b ? 1 : 0);
}

/**
 * @param {string} order
 * @param {string} service
 * @param {string} sortBy
 * @param {string} query
 */
function filterCards(order, service, sortBy, query) {
  filteredCreators = creators.slice(0);

  if (order === 'desc') {
    filteredCreators.reverse();
  }

  filteredCreators = filteredCreators.filter(
    creator => creator.service === (service || creator.service)
  ).sort((a, b) => {

    if (order === 'asc') {
      return sortBy === 'indexed'
        ? a.parsedIndexed - b.parsedIndexed
        : (sortBy === 'updated'
            ? a.parsedUpdated - b.parsedUpdated
            : fastCompare(a[sortBy], b[sortBy])
          );
    } else {
      return sortBy === 'indexed'
        ? b.parsedIndexed - a.parsedIndexed
        : (sortBy === 'updated'
            ? b.parsedUpdated - a.parsedUpdated
            : fastCompare(b[sortBy], a[sortBy])
          );
    }
  }).filter(creator => {
    return creator.name.match(
      new RegExp(
        query.replace(
          /[-\/\\^$*+?.()|[\]{}]/g,
          '\\$&'
        ),
        'i'
      )
    )
  })
}

function _paginatorButton(content, skip, className = '') {
  if (typeof skip === 'string') {
    className = skip;
    skip = null;
  }
  if (typeof skip === 'number') return `<a href="#" class="${className ? className : ''} paginator-button-ident" data-value="${skip}"><b>${content}</b></a>`;
  return `<li class="${className ? className : ''} paginator-button-ident"><b>${content}</b></li>`;
}

function createPaginator() {
  const count = filteredCreators.length;

  const currentCeilingOfRange = (skip + limit) < count ? skip + limit : count

  const currPageNum = Math.ceil((skip + limit) / limit);
  const totalPages = Math.ceil(count / limit);
  const numBeforeCurrPage = ((totalPages < TOTAL_BUTTONS) || (currPageNum < TOTAL_BUTTONS)) ? currPageNum - 1 : ((totalPages - currPageNum) < TOTAL_BUTTONS ? ((TOTAL_BUTTONS - 1) + ((TOTAL_BUTTONS) - (totalPages - currPageNum))) : (TOTAL_BUTTONS - 1))
  const basePageNum = Math.max(currPageNum - numBeforeCurrPage - 1, 1);
  const showFirstPostsButton = basePageNum > 1;
  const showLastPostsButton = totalPages - currPageNum > (TOTAL_BUTTONS + (currPageNum - basePageNum < TOTAL_BUTTONS ? (TOTAL_BUTTONS - (currPageNum - basePageNum)) : 0));
  const optionalBeforeButtons = currPageNum - MANDATORY_BUTTONS - (totalPages - currPageNum < MANDATORY_BUTTONS ? (MANDATORY_BUTTONS - (totalPages - currPageNum)) : 0);
  const optionalAfterButtons = currPageNum + MANDATORY_BUTTONS + (currPageNum - basePageNum < MANDATORY_BUTTONS ? (MANDATORY_BUTTONS - (currPageNum - basePageNum)) : 0);

  const range = createRange(0, (TOTAL_BUTTONS * 2) + 1);

  const paginator = (count > limit) ? `
    <small>Showing ${ skip + 1 } - ${ currentCeilingOfRange } of ${ count }</small>
    <menu>

    ${
      (showFirstPostsButton || showLastPostsButton) ? 
      showFirstPostsButton ? _paginatorButton('<<', 0) : _paginatorButton('<<', `pagination-button-disabled${ currPageNum - MANDATORY_BUTTONS - 1 ? ' pagination-desktop' : '' }`)
      : ``
    }
    ${
      showFirstPostsButton ? '' :
      currPageNum - MANDATORY_BUTTONS - 1 ? 
      _paginatorButton('<<', 0, 'pagination-mobile') :
      ((totalPages - currPageNum > MANDATORY_BUTTONS) && !showLastPostsButton) ? 
      _paginatorButton('<<', 'pagination-button-disabled pagination-mobile') : ''
    }
    ${
      currPageNum > 1 ? 
      _paginatorButton('<', (currPageNum - 2) * limit) :
      _paginatorButton('<', 'pagination-button-disabled')
    }
    ${
      range.map(page => (
        (page + basePageNum) && ((page + basePageNum) <= totalPages) ? 
        _paginatorButton((page + basePageNum), (page + basePageNum) != currPageNum ? (page + basePageNum - 1) * limit : null, 
        (((page + basePageNum) < optionalBeforeButtons || (page + basePageNum) > optionalAfterButtons) && ((page + basePageNum) != currPageNum)) ? 'pagination-button-optional' :
        ((page + basePageNum) == currPageNum) ? 'pagination-button-disabled pagination-button-current' : 
        ((page + basePageNum) == (currPageNum + 1)) ? 'pagination-button-after-current' : ''
        )
        : ''
      )).join('\n')
    }
    ${
      currPageNum < totalPages ? _paginatorButton('>', currPageNum * limit) : _paginatorButton('>', `pagination-button-disabled${totalPages ? ' pagination-button-after-current' : ''}`)
    }
    ${
      showFirstPostsButton || showLastPostsButton ?
      showLastPostsButton ? 
      _paginatorButton('>>', (totalPages - 1) * limit) :
      _paginatorButton('>>', `pagination-button-disabled${totalPages - currPageNum > MANDATORY_BUTTONS ? ' pagination-desktop' : ''}`) : ''
    }
    ${
      showLastPostsButton ? '' : 
      totalPages - currPageNum > MANDATORY_BUTTONS ? 
      _paginatorButton('>>', (totalPages - 1) * limit, 'pagination-mobile') :
      ((currPageNum > OPTIONAL_BUTTONS) && !showFirstPostsButton) ? 
      _paginatorButton('>>', 'pagination-button-disabled pagination-mobile') : ''
    }
    </menu>
  ` : '';

  return paginator;
}

/**
 * @param {HTMLDivElement} displayStatus
 * @param {HTMLDivElement} cardContainer
 * @param {{ top: HTMLElement, bottom: HTMLElement }} pagination
 * @param {String} sortBy
 */
async function loadCards(displayStatus, cardContainer, pagination, sortBy) {
  displayStatus.textContent = 'Displaying search results';
  pagination.top.innerHTML = createPaginator();
  pagination.bottom.innerHTML = createPaginator();
  /**
   * @type {[ HTMLDivElement, HTMLElement ]}
   */
  const [...cards] = cardContainer.children;
  cards.forEach((card) => {
    card.remove();
  });

  if (filteredCreators.length === 0) {
    const paragraph = document.createElement("p");

    paragraph.classList.add("subtitle", "card-list__item--no-results");
    paragraph.textContent = "No artists found for your query.";
    cardContainer.appendChild(paragraph);
    return;
  } else {
    const fragment = document.createDocumentFragment();

    for await (const user of filteredCreators.slice(skip, skip + limit)) {
      const userIsCount = sortBy === 'favorited';
      const userIsIndexed = sortBy === 'indexed';
      const userIsUpdated = sortBy === 'updated';
      const userCard = UserCard(null, user, userIsCount, userIsUpdated, userIsIndexed);
      const isFaved = isLoggedIn && await findFavouriteArtist(user.id, user.service);

      if (isFaved) {
        userCard.classList.add("user-card--fav");
      }

      fragment.appendChild(userCard);
    };

    cardContainer.appendChild(fragment);
  }
}

/**
 * @param {HTMLDivElement} loadingStatus
 */
async function retrieveArtists(loadingStatus) {
  try {
    const artists = await kemonoAPI.api.creators();

    if (!artists) {
      return null;
    }

    for (const artist of artists) {
      // preemptively do it here, it's taxing to parse a date string then convert it to a unix timestamp in milliseconds
      // this way we only have to do it once after fetching and none for sorting
      artist.parsedIndexed = artist.indexed * 1000;
      artist.parsedUpdated = artist.updated * 1000;
      artist.indexed = new Date(artist.parsedIndexed).toISOString();
      artist.updated = new Date(artist.parsedUpdated).toISOString();
    }

    loadingStatus.innerHTML = '';
    creators = artists;
    filteredCreators = artists;

  } catch (error) {
    console.error(error);
  }
}

/**
 * @param {number} start
 * @param {number} end
 */
function createRange(start, end) {
  const length = end - start;
  const range = Array.from({ length }, (_, index) => start + index);

  return range;
}