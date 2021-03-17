const contentGrid = document.getElementById('content-grid');
for (i = 0; i < _posts.length; i++) {
  post = _posts[i];
  flagged = _flagged[i];
  previews = _previews[i];
  attachments = _attachments[i];
  after_kitsune = _after_kitsune[i];
  is_image = _is_image[i];

  contentGrid.innerHTML += `
    <div class="pure-u-1 pure-u-sm-1-2 pure-u-md-1-2 pure-u-lg-1-2 pure-u-xl-1-3 card-container">
      ${is_image ? `
        <div class="card">
          <style>
            #toggle-${post.id}:checked ~ .card-reveal {
              display: block;
              animation-name: fadeInOpacity;
	            animation-iteration-count: 1;
	            animation-timing-function: ease-in;
	            animation-duration: 100ms;
            }
          </style>
          <div class="card-image">
            <label for="toggle-${ post.id }">
              <img src="/thumbnail${ post.file.path }" loading="lazy">
            </label>
          </div>
          <input type="checkbox" class="visually-hidden" id="toggle-${ post.id }">
          <div class="card-content">
            <label for="toggle-${ post.id }" class="card-title" style="cursor:pointer;">${ post.title }</label>
            <br>
            ${post.published ? `
              <label for="toggle-${ post.id }" class="subtitle" style="cursor:pointer;">${ post.published }</label>
            `: ''}
          </div>
          <div class="card-reveal">
            <div class="card-reveal-content">
              ${post.shared_file ? `
                <p class="subtitle">This post is user-shared, and cannot be verified for integrity. Exercise caution.</p>
              `: ''}
              ${post.service == 'dlsite' && post.attachments.length > 1 ? `
                <p class="subtitle">
                  This DLsite post was received as a split set of multiple files due to file size. Download all the files, then open the .exe file to compile them into a single one.
                </p>
              `: ''}
              ${post.service !== 'subscribestar' ? `
                <label for="toggle-${ post.id }" class="card-title">${ post.title }</label>
              ` : ''}
              ${post.published ? `
                <label for="toggle-${ post.id }" class="subtitle" style="cursor:pointer;">${ post.published }</label>
              `: ''}
              ${flagged ? `
                <span class="flag-disabled" title="This post has been flagged.">⚑</span>
              ` : `
                <span class="flag" title="Flag post" id="flag-button" data-service="${ post.service }" data-user="${ post.user }" data-post="${ post.id }">⚑</span>
              `}
              ${attachments.map(attachment => `
                <a href="${ attachment.path }" target="_blank">
                  Download ${ attachment.name }
                </a>
                <br>
              `).join('')}
              <p>
                ${post.service == "subscribestar" && after_kitsune ? '<div>' : ''}
                ${post.content}
              </p>
              ${previews.map(preview => `
                ${preview.type == 'thumbnail' ? `
                  <a class="fileThumb" href="${ preview.path }">
                    <img
                      data-src="/thumbnail${ preview.path }"
                      src="/thumbnail${ preview.path }"
                      loading="lazy"
                    >
                  </a>
                  <br>
                ` : `
                  <a href="${ preview.url }" target="_blank">
                    <div class="embed-view">
                      ${preview.subject ? `
                        ${'<h3>' + preview.subject + '</h3>'}
                      ` : '<h3 class="subtitle">(No title)</h3>'}
                      ${preview.description ? `
                        ${'<p>' + preview.description + '</p>'}
                      ` : ''}
                    </div>
                  </a>
                  <br>
                `}
              `).join('')}
            </div>
          </div>
          <div class="card-action">
            <a target="_blank" href="${ post.file.path }">POST IMAGE</a>
            <a target="_blank" href="/${ post.service }/user/${ post.user }/post/${ post.id }">VIEW POST</a>
          </div>
        </div>
      ` : `
        <div class="text-card">
          <div class="card-reveal-content">
          </div>
        <div>
      `}
    </div>
  `
}