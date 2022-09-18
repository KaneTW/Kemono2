import { createComponent } from "@wp/js/component-factory";
import { ImageLink, Timestamp, FancyImage } from "@wp/components";
import { freesites, paysites } from "@wp/utils";

/**
 * @param {HTMLElement} element 
 * @param {KemonoAPI.Post} post
 */
export function PostCard(element = null, post = {}) {
  const postCard = element
    ? initFromElement(element)
    : initFromScratch(post);

  const view = postCard.postCardElement.querySelector(".post-card__view");

  if (view) {
    /**
     * @type {HTMLButtonElement}
     */
    const button = view.querySelector(".post-card__button");
    /**
     * @type {HTMLAnchorElement}
     */
    const link = postCard.postCardElement.querySelector(".post-card__link");

    button.addEventListener("click", handlePostView(link));
  }

  return postCard;
};

/**
 * @param {HTMLElement} element 
 */
function initFromElement(element) {
  const { id, service, user } = element.dataset;
  return {
    postCardElement: element,
    postID: id,
    service,
    userID: user
  }
}

/**
 * @param {KemonoAPI.Post} post 
 */
function initFromScratch(post) {
  /**
   * @type {HTMLElement}
   */
  const postCardElement = createComponent("post-card");

  return {
    postCardElement,
    postID: post.id,
    service: post.service,
    userID: post.user
  }
}

/**
 * @param {HTMLAnchorElement} link
 * @returns {(event: MouseEvent) => void}
 */
function handlePostView(link) {
  return (event) => {
    link.focus();
  }
}

/**
 * @param {HTMLElement} element 
 * @param {KemonoAPI.User} user 
 * @param {boolean} isCount 
 * @param {boolean} isDate 
 * @param {string} className 
 */
export function UserCard(
  element, 
  user = {}, 
  isCount = false, 
  isUpdated = false, 
  isIndexed = false, 
  className=null
) {
  const userCard = element
    ? initUserCardFromElement(element)
    : initUserCardFromScratch(user, isCount, isUpdated, isIndexed, className);

  return userCard;
}

/**
 * @param {HTMLElement} element 
 */
function initUserCardFromElement(element) {
  const userCard = element;

  return userCard;
}

/**
 * @param {KemonoAPI.User} user 
 * @param {boolean} isCount 
 * @param {boolean} isDate 
 * @param {string} className 
 */
function initUserCardFromScratch(user, isCount, isUpdated, isIndexed, className) {
  const profileIcon = freesites.kemono.user.icon(user.service, user.id);
  const profileBanner = freesites.kemono.user.banner(user.service, user.id);
  const profileLink = freesites.kemono.user.profile(user.service, user.id);
  /**
   * @type {HTMLElement}
   */
  const userCard = createComponent("user-card");
  userCard.href = profileLink;
  userCard.style.backgroundImage = `linear-gradient(rgb(0 0 0 / 50%), rgb(0 0 0 / 80%)), url(${profileBanner})`;

  const imageLink = FancyImage(null,
    profileIcon,
    profileIcon,
    true,
    "",
    'user-card__user-icon'
  );

  const userIcon = userCard.querySelector(".user-card__icon");
  const userName = userCard.querySelector(".user-card__name");
  const userService = userCard.querySelector(".user-card__service");
  const userCount = userCard.querySelector(".user-card__count");
  const userUpdated = userCard.querySelector(".user-card__updated");

  userIcon.appendChild(imageLink);
  userName.textContent = user.name;
  userService.textContent = paysites[user.service].title;
  userService.style.backgroundColor = paysites[user.service].color;

  if (className) {
    userCard.classList.add(className);
  }

  if (isCount) {
    userCount.innerHTML = `<b>${user.favorited}</b> favorites`;
  } else {
    userCount.remove();
  }

  if (isUpdated || isIndexed) {
    const timestamp = Timestamp(null, isUpdated ? user.updated : user.indexed);
    userUpdated.appendChild(timestamp);
  } else {
    userUpdated.remove();
  }

  return userCard;
}
