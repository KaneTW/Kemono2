export const features = {
  localStorage: isLocalStorageAvailable()
}

function isLocalStorageAvailable() {
  try {
    localStorage.setItem("__storage_test__", "__storage_test__");
    localStorage.removeItem("__storage_test__");
    return true;
  } catch (error) {
    return false;
  }
}
