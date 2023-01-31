import Dashboard from "@uppy/dashboard";
import Form from "@uppy/form";
import Uppy from "@uppy/core";
import Tus from "@uppy/tus";

import '@uppy/dashboard/dist/style.min.css';
import '@uppy/core/dist/style.min.css';

// import "@wp/js/resumable";

/**
 * @param {HTMLElement} section 
 */
export async function uploadPage(section) {
  Array.from(document.getElementsByTagName('textarea')).forEach(tx => {
    function onTextareaInput() {
      this.style.height = 'auto';
      this.style.height = this.scrollHeight + 'px';
    }
    tx.setAttribute('style', 'height:' + tx.scrollHeight + 'px;overflow-y:hidden;');
    tx.addEventListener('input', onTextareaInput, false);
  });

  const uppy = new Uppy({
    restrictions: {
      maxTotalFileSize: 2 * 1024 * 1024 * 1024,
      maxNumberOfFiles: 10,
      minNumberOfFiles: 1
    }
  })
    .use(Dashboard, {
      note: 'Up to 10 files permitted.',
      fileManagerSelectionType: 'both',
      target: '#upload',
      // inline: true,
      inline: false,
      trigger: '#upload-button',
      theme: 'dark'
    })
    .use(Tus, {
      // endpoint: 'https://tusd.tusdemo.net/files/',
      endpoint: 'http://localhost:1080/files/',
      retryDelays: [0, 1000, 3000, 5000]
    })
    .use(Form, {
      resultName: 'uppyResult',
      target: '#upload-form',
      submitOnSuccess: false
    })

  uppy.on('complete', ({ successful }) => {
    successful.forEach(file => {
      const fileList = document.getElementById('file-list');
      fileList.innerHTML += `<li>${file.meta.name}</li>`;
    })
  })
}
