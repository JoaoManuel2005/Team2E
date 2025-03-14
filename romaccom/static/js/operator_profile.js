document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_logo');
    const fileNameDisplay = document.getElementById('file-name-display');
    const fileName = document.getElementById('file-name');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if(this.files && this.files.length > 0) {
                fileName.textContent = this.files[0].name;
                fileNameDisplay.style.display = 'flex';
            } else {
                fileName.textContent = 'No file selected';
                fileNameDisplay.style.display = 'none';
            }
        });
    }
});