import { createComponent } from "@wp/js/component-factory";

export function LoadingIcon() {
  /**
   * @type {HTMLSpanElement}
   */
  const icon = createComponent("loading-icon");
  return icon;
}
