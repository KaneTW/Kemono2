window.onload = () => {
  document.getElementById('channel_ids').style.display = 'none';
  document.getElementById('service').addEventListener('change', () => {
    switch (document.getElementById('service').value) {
      case 'discord':
        document.getElementById('channel_ids').style.display = 'block';
        break;
      default:
        document.getElementById('channel_ids').style.display = 'none';
    }
  });
};
