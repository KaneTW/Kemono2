document.getElementById('specific_id').style.display = 'none';

/* eslint-disable no-unused-vars */
function handleClick (radio) {
  if (radio.value === 'specific') {
    document.getElementById('specific_id').style.display = 'block';
  } else {
    document.getElementById('specific_id').style.display = 'none';
  }
}
/* eslint-enable no-unused-vars */
