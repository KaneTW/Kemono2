import { CardList, PostCard, registerPaginatorKeybinds } from "@wp/components";
import { isLoggedIn } from "@wp/js/account";
import { findFavouritePost, findFavouriteArtist } from "@wp/js/favorites";

/**
 * @param {HTMLElement} section 
 */
export function postsPage(section) {
  const cardListElement = section.querySelector(".card-list");
  const { cardList, cardItems } = CardList(cardListElement);

  cardItems.forEach(async (card) => {
    registerPaginatorKeybinds();
    
    const { postID, userID, service } = PostCard(card);
    const favPost = isLoggedIn && await findFavouritePost(service, userID, postID);
    const favUser = isLoggedIn && await findFavouriteArtist(userID, service);

    if (favPost) {
      card.classList.add("post-card--fav");
    };

    if (favUser) {
      const postHeader = card.querySelector(".post-card__header");
      const postFooter = card.querySelector(".post-card__footer");

      postHeader.classList.add("post-card__header--fav");
      postFooter.classList.add("post-card__footer--fav");
      userName.textContent = favUser.name;
    };

  });
}
