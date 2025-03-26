function showError(message) {
        const errorDiv = document.getElementById('error-message');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 3000);
    }

    function validateAndSubmit(event) {
        event.preventDefault();
        
        const fileInput = document.getElementById('single-upload');
        const form = document.getElementById('upload-form');
        
        if (!fileInput.files || fileInput.files.length === 0) {
            showError('Please select an image file first❗️');
            return false;
        }

        const file = fileInput.files[0];
        if (!file.type.match('image.*')) {
            showError('Please select a valid image file❗️');
            return false;
        }

        document.getElementById('loading').style.display = 'block';
        const formData = new FormData(form);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Upload failed');
            }
            return response.text();
        })
        .then(html => {
            document.documentElement.innerHTML = html;
        })
        .catch(error => {
            showError('Upload failed: ' + error.message);
            document.getElementById('loading').style.display = 'none';
        });

        return false;
    }

    function previewImage(event) {
        const file = event.target.files[0];
        const filenameDisplay = document.getElementById('selected-filename');
        const preview = document.getElementById('preview');
        const previewText = document.getElementById('preview-text');
        
        if (file) {
            filenameDisplay.textContent = 'Selected: ' + file.name;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
                previewText.style.display = 'none';
            };
            reader.readAsDataURL(file);
        } else {
            filenameDisplay.textContent = '';
            preview.style.display = 'none';
            previewText.style.display = 'block';
        }
    }
