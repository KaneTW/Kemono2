/**
 * @type {Record<string, { minLength: number, maxLength: number }}
 */
export const serviceConstraints = {
  patreon: KeyConstraints(),
  fanbox: KeyConstraints(),
  gumroad: KeyConstraints(),
  subscribestar: KeyConstraints(),
  dlsite: KeyConstraints(),
  discord: KeyConstraints(),
  fantia: KeyConstraints(),
}

function KeyConstraints(minLength = 1, maxLength = 1024) {
  return {
    minLength,
    maxLength
  }
}
