import { kemonoAPI } from "@wp/api";
import { ImageLink } from "@wp/components";
import { paysites, freesites } from "@wp/utils";

/**
 * @type {KemonoAPI.Artist[]}
 */
let creators;
/**
 * @type {KemonoAPI.Artist[]}
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

  section.addEventListener("click", (event) => {
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
      loadCards();
    }
  });

  searchForm.addEventListener("submit", (event) => event.preventDefault());
  queryInput.addEventListener("change", (event) => {
    filterCards(
      orderSelect.value, 
      serviceSelect.value, 
      sortSelect.value, 
      queryInput.value
    );
    loadCards();
  });
  serviceSelect.addEventListener("change", (event) => {
    filterCards(
      orderSelect.value, 
      serviceSelect.value, 
      sortSelect.value, 
      queryInput.value
    );
    loadCards();
  });
  sortSelect.addEventListener("change", (event) => {
    filterCards(
      orderSelect.value, 
      serviceSelect.value, 
      sortSelect.value, 
      queryInput.value
    );
    loadCards();
  });
  orderSelect.addEventListener("change", (event) => {
    filterCards(
      orderSelect.value, 
      serviceSelect.value, 
      sortSelect.value, 
      queryInput.value
    );
    loadCards();
  });

  await retrieveArtists(loadingStatus);
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

function loadCards() {
  document.getElementById('display-status').innerHTML = 'Displaying search results';
  document.getElementById('vertical-views').innerHTML = `
    <div class="paginator" id="paginator-top">
      ${createPaginator()}
    </div>
    <table class="search-results" width="100%">
      <thead>
        <tr>
          <th width="50px">Icon</th>
          <th>Name</th>
          <th>Service</th>
        </tr>
      </thead>
      <tbody>
        ${filteredCreators.length ? '' : `
          <tr>
            <td></td>
            <td class="subtitle">No artists found for your query.</td>
            <td></td>
          </tr>
        `}
        ${filteredCreators.slice(skip, skip + 25).map(artist => `
          <tr class="artist-row">
            <td>
              ${ImageLink(
                null,
                freesites.kemono.user.profile(artist.service, artist.id),
                freesites.kemono.user.icon(artist.service, artist.id),
                "",
                "",
                true,
                true,
                "user-icon"
              ).outerHTML}
            </td>
            <td>
              <a href="${ freesites.kemono.user.profile(artist.service, artist.id)}">
                ${ artist.name }
              </a>
            </td>
            <td>
              ${ paysites[artist.service].title}
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    <div class="paginator" id="paginator-bottom">
      ${createPaginator()}
    </div>
  `;
}

/**
 * @param {HTMLHeadingElement} displayStatus 
 * @param {HTMLDivElement} loadingStatus 
 */
async function retrieveArtists(loadingStatus) {
  try {
    const artists = await kemonoAPI.api.creators();

    if (!artists) {
      alert(error);
      return null;
    }

    loadingStatus.innerHTML = '';
    creators = artists;
    filteredCreators = artists;

  } catch (error) {
    alert(error);
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
