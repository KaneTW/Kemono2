import { KemonoError, KemonoValidationError, isASCIIString } from "@wp/utils";
import { serviceConstraints } from "./type.js";

/**
 * Validates the key according to these rules:
 * - Trim spaces from both sides.
 * - Minimum and maximum length of the key (depending on service).
 * - ASCII characters only.
 * @param {string} key
 * @param {string} service
 * @returns {string | KemonoError}
 */
export function validate_import_key(key, service) {
  const formattedKey = key.trim();
  const keyLength = formattedKey.length;
  const { minLength, maxLength } = serviceConstraints[service];
  const isValidLength = keyLength > minLength && keyLength < maxLength;

  // key is within length constraints
  if (!isValidLength) {
    return new KemonoValidationError(`The key \"${key}\" of service \"${service}\" and length \"${keyLength}\" is outside of \"${minLength} - ${maxLength}\" range. You should let the administrator know about this.`)
  }

  // key is ascii
  if (!isASCIIString(formattedKey)) {
    return new KemonoValidationError(`The key \"${key}\" is of invalid encoding.`)
  }

  return formattedKey;
}
