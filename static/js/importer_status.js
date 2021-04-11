var logs = [];

window.addEventListener('load', async function() {
    await fetchAndShowLogs();
});

async function fetchAndShowLogs() {
    await fetchNewLogs();
    var logContainer = document.getElementById('logs');
    var lastChild = logContainer.lastChild;
    var shouldScrollToBottom = true;
    if (lastChild) {
        shouldScrollToBottom = isScrolledIntoView(logContainer.lastChild);
    }

    var currentChildCount = logContainer.childElementCount;
    var newLastChild;
    logs.forEach((msg, idx) => {
        if (idx < currentChildCount) { return; }

        var node = document.createElement('p');
        node.appendChild(document.createTextNode(msg));
        logContainer.appendChild(node);
        newLastChild = node;
    });

    if (newLastChild && shouldScrollToBottom) {
        newLastChild.scrollIntoView();
    }

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

function isScrolledIntoView(el) {
    var parent = document.getElementsByClassName('info')[0];
    var height = parent.scrollTop;
    return el.offsetTop >= height && (el.offsetTop <= height + parent.offsetHeight + 10 + el.offsetHeight)
}
