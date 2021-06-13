document.getElementById('login_form').addEventListener('submit', e => {
  e.preventDefault();
  localStorage.setItem('logged_in', 'yes');
  e.target.submit();
})