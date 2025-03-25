document.addEventListener('DOMContentLoaded', function() {
    // Hide Django's file field completely
    const djangoFileField = document.querySelector('.form-group input[type="file"]');
    if (djangoFileField) {
        djangoFileField.parentElement.style.display = 'none';
    }
    
    /**
     * Creates a custom file input element
     */
    const customFileInput = document.createElement('input');
    customFileInput.type = 'file';
    customFileInput.id = 'custom-logo-upload';
    customFileInput.accept = 'image/*';
    customFileInput.style.display = 'none';
    document.body.appendChild(customFileInput);
    
    /**
     * Creates a custom file input element
     */
    const customButton = document.querySelector('.custom-file-upload');
    customButton.addEventListener('click', function(e) {
        e.preventDefault();
        customFileInput.click();
    });
    
    /**
     * Handles file selection and updates the UI accordingly
     */
    customFileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            const fileNameDisplay = document.getElementById('file-name-display');
            const fileName = document.getElementById('file-name');
            fileNameDisplay.style.display = 'flex';
            fileName.textContent = this.files[0].name;
            
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(this.files[0]);
            djangoFileField.files = dataTransfer.files;
            
            /**
             * Creates a clear option to remove the selected file
             */
            const clearContainer = document.createElement('div');
            clearContainer.className = 'custom-clear-option';
            clearContainer.innerHTML = `
                <label>
                    <input type="checkbox" id="clear-logo">
                    Clear selected file
                </label>
            `;
            
            const existingClear = document.querySelector('.custom-clear-option');
            if (existingClear) {
                existingClear.remove();
            }
            fileNameDisplay.insertAdjacentElement('afterend', clearContainer);
            
            /**
             * Handles the clear option checkbox functionality
             */
            document.getElementById('clear-logo').addEventListener('change', function() {
                if (this.checked) {
                    customFileInput.value = '';
                    djangoFileField.value = '';
                    fileNameDisplay.style.display = 'none';
                    
                    const djangoClear = document.querySelector('input[name="logo-clear"]');
                    if (djangoClear) {
                        djangoClear.checked = true;
                    }
                }
            });
        }
    });
});