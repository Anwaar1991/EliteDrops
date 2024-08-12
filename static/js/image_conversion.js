
  // Function to display image preview and progress bar
  function showImagePreview(file, fileSizeKB) {
    const imageContainer = document.createElement('div');
    imageContainer.classList.add('image-container');

    const image = document.createElement('img');
    image.src = URL.createObjectURL(file);
    image.alt = file.name;

    const fileSizeLabel = document.createElement('span');
    fileSizeLabel.innerText = `(${fileSizeKB} KB)`;

    const progressContainer = document.createElement('div');
    progressContainer.classList.add('progress');

    const progressBar = document.createElement('div');
    progressBar.classList.add('progress-bar');

    progressContainer.appendChild(progressBar);
    imageContainer.appendChild(image);
    imageContainer.appendChild(fileSizeLabel);
    imageContainer.appendChild(progressContainer);

    document.getElementById('imagePreview').appendChild(imageContainer);

    return { progressBar, imageContainer };
  }

  // Function to update progress bar
  function updateProgressBar(progressBar) {
    let width = 0;
    const animationInterval = setInterval(() => {
      width += 1;
      progressBar.style.width = width + '%';
      if (width >= 100) {
        clearInterval(animationInterval);
      }
    }, 20);
  }

  // Handle file input change
  document.getElementById('file').addEventListener('change', () => {
    const files = document.getElementById('file').files;

    // Clear the previous image previews
    document.getElementById('imagePreview').innerHTML = '';

    // Iterate through each selected file and show preview
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const fileSizeKB = (file.size / 1024).toFixed(2);
      const { progressBar } = showImagePreview(file, fileSizeKB);
      updateProgressBar(progressBar);
    }
  });
