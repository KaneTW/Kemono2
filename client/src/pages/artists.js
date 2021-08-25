import { kemonoAPI } from "@wp/api";
import { CardList } from "@wp/components";
import { isLoggedIn } from "@wp/js/account";
import { findFavouriteArtist } from "@wp/js/favorites";
import { UserCard } from "./components/cards";

/**
 * @type {KemonoAPI.User[]}
 */
let creators;
/**
 * @type {KemonoAPI.User[]}
 */
let filteredCreators;
let skip = 0;
let limit = 25;

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

    if (
      button.classList.contains("paginator-button")
      && button.dataset
      && button.dataset.value
    ) {
      skip = Number(button.dataset.value);
      filterCards(
        orderSelect.value,
        serviceSelect.value,
        sortSelect.value,
        queryInput.value
      );
      await loadCards(displayStatus, cardContainer, pagination);
    }
  });

  searchForm.addEventListener("submit", (event) => event.preventDefault());
  queryInput.addEventListener("change", handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination));
  serviceSelect.addEventListener("change", handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination));
  sortSelect.addEventListener("change", handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination));
  orderSelect.addEventListener("change", handleSearch(orderSelect, serviceSelect, sortSelect, queryInput, displayStatus, cardContainer, pagination));

  await retrieveArtists(loadingStatus);
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
    await loadCards(displayStatus, cardContainer, pagination);
  }
}

/**
 * @param {string} order
 * @param {string} service
 * @param {string} sortBy
 * @param {string} query
 */
function filterCards(order, service, sortBy, query) {
  filteredCreators = creators;

  if (order === 'desc') {
    filteredCreators.reverse()
  }

  filteredCreators = filteredCreators.filter(
    creator => creator.service === (service || creator.service)
  ).sort((a, b) => {

    if (order === 'desc') {
      return sortBy === 'indexed'
        ? Date.parse(a.indexed) - Date.parse(b.indexed)
        : a[sortBy].localeCompare(b[sortBy]);

    } else {
      return sortBy === 'indexed'
        ? Date.parse(b.indexed) - Date.parse(a.indexed)
        : b[sortBy].localeCompare(a[sortBy]);
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

function createPaginator() {
  let currentPage = Math.ceil(skip / limit);
  let maxPages = Math.ceil(filteredCreators.length / limit);
  const range = skip >= 100
    ? createRange(currentPage - 2, currentPage + 3)
    : createRange(0, 7);

  const paginator = `
    <small>Showing ${ skip + 1 } - ${ skip + limit } of ${ filteredCreators.length }</small>
    <menu>
      ${skip >= limit
        ? `<li>
            <a href="#" class="paginator-button" data-value="${skip - limit}" title="Previous page">
              &lt;
            </a>
          </li>`
        : '<li class="subtitle">&lt;</li>'
      }
      ${skip >= 100
        ? `
        <li>
          <a href="#" class="paginator-button" data-value="0">
            1
          </a>
        </li>
        <li>...</li>
      ` : ''
      }
      ${range.map(page => {
        if (filteredCreators.length > page * limit) {
          if (page * limit == skip) {
            return `<li>${page + 1}</li>`
          } else {
            return `
              <li>
                <a href="#" class="paginator-button" data-value="${page * limit}">
                  ${page + 1}
                </a>
              </li>
            `
          }
        }
      }).join('')}
      ${createRange(0, maxPages).map((page, index, arr) => {
        if (index === arr.length - 1 && filteredCreators.length - skip >= 100 && filteredCreators.length > 175) {
          return `
            <li>...</li>
            <li>
              <a href="#" class="paginator-button" data-value="${page * limit}">
                ${maxPages}
              </a>
            </li>
          `
        }
      }).join('')}
      ${filteredCreators.length - skip > limit ? `
        <li><a href="#" class="paginator-button" data-value="${skip + limit}" title="Next page">&gt;</a></li>
      ` : `
        <li class="subtitle">&gt;</li>
      `}
    </menu>`

  return paginator;
}

/**
 * @param {HTMLDivElement} displayStatus
 * @param {HTMLDivElement} cardContainer
 * @param {{ top: HTMLElement, bottom: HTMLElement }} pagination
 */
async function loadCards(displayStatus, cardContainer, pagination) {
  displayStatus.textContent = 'Displaying search results';
  pagination.top.innerHTML = createPaginator();
  pagination.bottom.innerHTML = createPaginator();
  /**
   * @type {[ HTMLDivElement, HTMLElement ]}
   */
  const [header, ...cards] = cardContainer.children;
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

    for await (const user of filteredCreators.slice(skip, skip + 25)) {
      const userCard = UserCard(null, user, true);
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