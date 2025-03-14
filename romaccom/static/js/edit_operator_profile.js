document.addEventListener('DOMContentLoaded', function() {
    // Hide Django's file field completely
    const djangoFileField = document.querySelector('.form-group input[type="file"]');
    if (djangoFileField) {
        djangoFileField.parentElement.style.display = 'none';
    }
    
    // Set up custom file input
    const customFileInput = document.createElement('input');
    customFileInput.type = 'file';
    customFileInput.id = 'custom-logo-upload';
    customFileInput.accept = 'image/*';
    customFileInput.style.display = 'none';
    document.body.appendChild(customFileInput);
    
    // Connect custom button to custom file input
    const customButton = document.querySelector('.custom-file-upload');
    customButton.addEventListener('click', function(e) {
        e.preventDefault();
        customFileInput.click();
    });
    
    // Handle file selection
    customFileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            // Update file name display
            const fileNameDisplay = document.getElementById('file-name-display');
            const fileName = document.getElementById('file-name');
            fileNameDisplay.style.display = 'flex';
            fileName.textContent = this.files[0].name;
            
            // Update the hidden Django input
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(this.files[0]);
            djangoFileField.files = dataTransfer.files;
            
            // Add a "remove" button option
            const clearContainer = document.createElement('div');
            clearContainer.className = 'custom-clear-option';
            clearContainer.innerHTML = `
                <label>
                    <input type="checkbox" id="clear-logo">
                    Clear selected file
                </label>
            `;
            
            // Replace any existing clear option
            const existingClear = document.querySelector('.custom-clear-option');
            if (existingClear) {
                existingClear.remove();
            }
            fileNameDisplay.insertAdjacentElement('afterend', clearContainer);
            
            // Handle clear checkbox
            document.getElementById('clear-logo').addEventListener('change', function() {
                if (this.checked) {
                    customFileInput.value = '';
                    djangoFileField.value = '';
                    fileNameDisplay.style.display = 'none';
                    
                    // Set Django's clear checkbox if it exists
                    const djangoClear = document.querySelector('input[name="logo-clear"]');
                    if (djangoClear) {
                        djangoClear.checked = true;
                    }
                }
            });
        }
    });
});