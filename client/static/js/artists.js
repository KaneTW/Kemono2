var creators;
var filtered_creators;
var skip = 0;
var limit = 25;

const range = (start, end) => {
  const length = end - start;
  return Array.from({ length }, (_, i) => start + i);
}

const paginator = () => {
  var rng; // range
  rng = skip >= 100 ? range(Math.ceil((skip / limit)) - 2, Math.ceil((skip / limit)) + 3) : range(0, 7)
  return `
    <small>Showing ${ skip + 1 } - ${ skip + limit } of ${ filtered_creators.length }</small>
    <menu>
      ${skip >= limit ? `<li><a href="#" class="paginator-button" data-value="${skip - limit}" title="Previous page">&lt;</a></li>` : '<li class="subtitle">&lt;</li>'}
      ${skip >= 100 ? `
        <li>
          <a href="#" class="paginator-button" data-value="0">
            1
          </a>
        </li>
        <li>...</li>
      ` : ''}
      ${rng.map(page => {
        if (filtered_creators.length > page * limit) {
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
      ${range(0, Math.ceil((filtered_creators.length / limit))).map((page, i, arr) => {
        if (i === arr.length - 1 && filtered_creators.length - skip >= 100 && filtered_creators.length > 175) {
          return `
            <li>...</li>
            <li>
              <a href="#" class="paginator-button" data-value="${page * limit}">
                ${Math.ceil((filtered_creators.length / limit))}
              </a>
            </li>
          `
        }
      }).join('')}
      ${filtered_creators.length - skip > limit ? `
        <li><a href="#" class="paginator-button" data-value="${skip + limit}" title="Next page">&gt;</a></li>
      ` : `
        <li class="subtitle">&gt;</li>
      `}
    </menu>
  `
}

function filter() {
  filtered_creators = creators;
  if (document.getElementById('order').value === 'desc') {
    filtered_creators.reverse()
  }
  filtered_creators = filtered_creators
    .filter(creator => creator.service === (document.getElementById('service').value || creator.service))
    .sort((a, b) => {
      if (document.getElementById('order').value === 'desc') {
        return document.getElementById('sort_by') === 'indexed' ? Date.parse(a.indexed) - Date.parse(b.indexed) : a[document.getElementById('sort_by').value].localeCompare(b[document.getElementById('sort_by').value])
      } else {
        return document.getElementById('sort_by') === 'indexed' ? Date.parse(b.indexed) - Date.parse(a.indexed) : b[document.getElementById('sort_by').value].localeCompare(a[document.getElementById('sort_by').value])
      }
    })
    .filter(creator => creator.name.match(new RegExp(document.getElementById('q').value.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&'), 'i')))
}

function load() {
  document.getElementById('display-status').innerHTML = 'Displaying search results';
  document.getElementById('vertical-views').innerHTML = `
    <div class="paginator" id="paginator-top">
      ${paginator()}
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
        ${filtered_creators.length ? '' : `
          <tr>
            <td></td>
            <td class="subtitle">No artists found for your query.</td>
            <td></td>
          </tr>
        `}
        ${filtered_creators.slice(skip, skip + 25).map(artist => `
          <tr class="artist-row">
            <td>
              <a href="/${ artist.service }/${ artist.service === 'discord' ? 'server' : 'user' }/${artist.id}">
                <div class="user-icon" style="background-image: url('/icons/${ artist.service }/${ artist.id }');"></div>
              </a>
            </td>
            <td>
              <a href="/${ artist.service }/${ artist.service === 'discord' ? 'server' : 'user' }/${artist.id}">${ artist.name }</a>
            </td>
            <td>
              ${
                ({
                  'patreon': 'Patreon',
                  'fanbox': 'Pixiv Fanbox',
                  'subscribestar': 'SubscribeStar',
                  'gumroad': 'Gumroad',
                  'discord': 'Discord',
                  'dlsite': 'DLsite',
                  'fantia': 'Fantia'
                })[artist.service]
              }
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    <div class="paginator" id="paginator-bottom">
      ${paginator()}
    </div>
  `;

  Array.prototype.forEach.call(document.getElementsByClassName('paginator-button'), btn => {
    btn.addEventListener('click', e => {
      skip = Number(e.target.getAttribute('data-value'))
      filter();
      load();
    })
  });
}

document.getElementById('search-form').addEventListener('submit', e => e.preventDefault())

fetch('/api/creators')
  .then(data => data.json())
  .then(data => {
    document.getElementById('loading').innerHTML = '';
    creators = data;
    filtered_creators = data;
    document.getElementById('q').addEventListener('input', e => {
      filter();
      load();
    })
    document.getElementById('service').addEventListener('change', () => {
      filter();
      load();
    });
    document.getElementById('sort_by').addEventListener('change', () => {
      filter();
      load();
    })
    document.getElementById('order').addEventListener('change', () => {
      filter();
      load();
    })
  })