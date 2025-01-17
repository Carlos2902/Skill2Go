document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.getElementById('drop-area');
  const fileInput = document.getElementById('id_image');

  


  if (!dropArea || !fileInput) {
    console.error('Drop area or file input not found in the DOM.');
    return;
  }


  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
  });

  dropArea.addEventListener('drop', handleDrop, false);

  fileInput.addEventListener('change', () => {
    const files = fileInput.files;
    const fileNames = Array.from(files).map(file => file.name).join(', ');
    displayFileNames(fileNames);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  function handleFiles(files) {
    fileInput.files = files;
    const fileNames = Array.from(files).map(file => file.name).join(', ');
    displayFileNames(fileNames);
  }

  function displayFileNames(fileNames) {
    const fileNameDisplay = document.createElement('p');
    fileNameDisplay.textContent = `Selected Image: ${fileNames}`;

    const existingDisplay = dropArea.querySelector('.file-name-display');
    if (existingDisplay) {
      existingDisplay.remove();
    }

    fileNameDisplay.classList.add('file-name-display');
    dropArea.appendChild(fileNameDisplay);
  }
});
