var logs = ['Import started'];

window.addEventListener('load', async function() {
    await fetchAndShowLogs();
});

async function fetchAndShowLogs() {
    await fetchNewLogs();
    var logElem = document.getElementById('logs');
    logElem.innerHTML = '';
    logs.forEach((msg, idx) => {
        var node = document.createElement('p');
        node.appendChild(document.createTextNode(msg));
        logElem.appendChild(node);
    });

    setTimeout(async () => {
        await fetchAndShowLogs()
    }, 5000);
}

async function fetchNewLogs() {
    await fetch(`/api/logs/${log_id}`)
    .then(resp => resp.json())
    .then(data => logs = data)
    .catch(() => logs.push('Error fetching log. Trying again.'));
}
