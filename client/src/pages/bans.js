import { kemonoAPI } from "@wp/api";
import { createComponent } from "@wp/components";

/**
 * @type {{[key: string]: { href: (id: string) => string, title: string }}}
 */
const paysites = {
  patreon: {
    title: "Patreon",
    href: (id) => `https://www.patreon.com/user?u=${id}`
  },
  fanbox: {
    title: "Pixiv Fanbox",
    href: (id) => `https://www.pixiv.net/fanbox/creator/${id}`
  },
  gumroad: {
    title: "Gumroad",
    href: (id) => `https://gumroad.com/${id}`
  },
  subscribestar: {
    title: "SubscribeStar",
    href: (id) => `https://subscribestar.adult/${id}`
  },
  dlsite: {
    title: "DLsite",
    href: (id) => `https://www.dlsite.com/eng/circle/profile/=/maker_id/${id}`
  },
  fantia: {
    title: "Fantia",
    href: (id) => `https://fantia.jp/fanclubs/${id}`
  }
};

/**
 * @param {HTMLElement} section 
 */
export async function bansPage(section) {
  const banList = section.querySelector("#bans");
  const fragment = document.createDocumentFragment();
  
  try {
    const banItems = await kemonoAPI.api.bans();

    if (!banItems) {
      alert("Could not retrieve the list of banned creators.");
      return;
    }

    for await (const banItem of banItems) {
      const banEntry = await retrieveBannedArtist(banItem);

      if (!banEntry) {
        continue;
      }

      const paysite = paysites[banItem.service];
      const banElement = BanItem(
        paysite.href(banItem.id), 
        banEntry.name, 
        paysite.title
      );

      fragment.appendChild(banElement);
    }

  } catch (error) {
    alert(error);
  }

  banList.appendChild(fragment);
}

/**
 * @param {KemonoAPI.API.BanItem} banItem
 */
async function retrieveBannedArtist(banItem) {
  try {
    const banEntry = await kemonoAPI.api.bannedArtist(banItem.id, banItem.service);

    if (!banEntry) {
      console.warn(`Failed to retrieve an artist by the id "${banItem.id}" and service "${banItem.service}"`);
    }

    return banEntry;
  } catch (error) {
    alert(error);
  }
}

/**
 * @param {string} paysiteProfile 
 * @param {string} artistName 
 * @param {string} serviceTitle 
 */
function BanItem(paysiteProfile, artistName, serviceTitle) {
  /**
   * @type {HTMLLIElement}
   */
  const item = createComponent("bans__item");
  const link = item.querySelector("a");
  const [ nameElement, serviceElement ] = link.children;

  link.href = paysiteProfile;
  nameElement.textContent = artistName;
  serviceElement.textContent = serviceTitle;

  return item;
}

// window.onload = async () => {
//   const bansData = await fetch('/api/bans');
//   const bans = await bansData.json();
//   bans.forEach(async (ban) => {
//     let cache, href, service;
//     switch (ban.service) {
//       case 'patreon': {
//         service = 'Patreon';
//         const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=patreon`);
//         cache = await cacheData.json();
//         href = `https://www.patreon.com/user?u=${ban.id}`;
//         break;
//       }
//       case 'fanbox': {
//         service = 'Pixiv Fanbox';
//         const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=fanbox`);
//         cache = await cacheData.json();
//         href = `https://www.pixiv.net/fanbox/creator/${ban.id}`;
//         break;
//       }
//       case 'gumroad': {
//         service = 'Gumroad';
//         const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=gumroad`);
//         cache = await cacheData.json();
//         href = `https://gumroad.com/${ban.id}`;
//         break;
//       }
//       case 'subscribestar': {
//         service = 'SubscribeStar';
//         const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=subscribestar`);
//         cache = await cacheData.json();
//         href = `https://subscribestar.adult/${ban.id}`;
//         break;
//       }
//       case 'dlsite': {
//         service = 'DLsite';
//         const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=dlsite`);
//         cache = await cacheData.json();
//         href = `https://www.dlsite.com/eng/circle/profile/=/maker_id/${ban.id}`;
//         break;
//       }
//       case 'fantia': {
//         service = 'Fantia';
//         const cacheData = await fetch(`/api/lookup/cache/${ban.id}?service=fantia`);
//         cache = await cacheData.json();
//         href = `https://fantia.jp/fanclubs/${ban.id}`;
//         break;
//       }
//     }

//     document.getElementById('bans').innerHTML += `
//       <li>
//         <a href="${href}">
//           ${cache.name} <span class="subtitle">${service}</span>
//         </a>
//       </li>
//     `;
//   });
// };
