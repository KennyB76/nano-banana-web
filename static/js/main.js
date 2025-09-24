document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');

    let uploadedFiles = [];

    // Click to upload
    dropZone.addEventListener('click', function() {
        fileInput.click();
    });

    // Drag and drop events
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');

        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    // File input change event
    fileInput.addEventListener('change', function(e) {
        handleFiles(e.target.files);
    });

    // Handle files function
    function handleFiles(files) {
        for (let i = 0; i < files.length; i++) {
            const file = files[i];

            // Check if file is an image
            if (!file.type.match('image.*')) {
                showError('이미지 파일만 업로드 가능합니다.');
                continue;
            }

            // Check file size (16MB max)
            if (file.size > 16 * 1024 * 1024) {
                showError('파일 크기는 16MB 이하여야 합니다.');
                continue;
            }

            uploadedFiles.push(file);
            createPreview(file);
        }

        // Update file input
        updateFileInput();
    }

    // Create preview function
    function createPreview(file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';

            const img = document.createElement('img');
            img.src = e.target.result;
            img.alt = file.name;

            const removeBtn = document.createElement('button');
            removeBtn.className = 'preview-remove';
            removeBtn.innerHTML = '×';
            removeBtn.onclick = function() {
                removeFile(file);
                previewItem.remove();
            };

            previewItem.appendChild(img);
            previewItem.appendChild(removeBtn);
            previewContainer.appendChild(previewItem);
        };

        reader.readAsDataURL(file);
    }

    // Remove file function
    function removeFile(file) {
        const index = uploadedFiles.indexOf(file);
        if (index > -1) {
            uploadedFiles.splice(index, 1);
        }
        updateFileInput();
    }

    // Update file input with current files
    function updateFileInput() {
        const dataTransfer = new DataTransfer();
        uploadedFiles.forEach(file => {
            dataTransfer.items.add(file);
        });
        fileInput.files = dataTransfer.files;
    }

    // Show error message
    function showError(message) {
        const errorMessage = document.getElementById('errorMessage');
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 5000);
        }
    }

    // Prevent default drag behavior for the entire document
    document.addEventListener('dragover', function(e) {
        e.preventDefault();
    });

    document.addEventListener('drop', function(e) {
        e.preventDefault();
    });
});

// Service worker for PWA (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.serviceWorker.register('/sw.js');
    });
}