document.addEventListener('DOMContentLoaded', function() {
    const brandSelect = document.getElementById('brandSelect');
    const carSelect = document.getElementById('carSelect');

    if (brandSelect && carSelect) {
        brandSelect.addEventListener('change', function() {
            const selectedBrandId = this.value;
            const carOptions = carSelect.getElementsByTagName('option');
            
            // Show "Select car" option
            carOptions[0].style.display = '';
            carSelect.value = '';

            // Show/hide car options based on selected brand
            for (let i = 1; i < carOptions.length; i++) {
                const option = carOptions[i];
                if (!selectedBrandId || option.dataset.brand === selectedBrandId) {
                    option.style.display = '';
                } else {
                    option.style.display = 'none';
                }
            }
        });
    }
});