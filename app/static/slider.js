document.addEventListener('DOMContentLoaded', function() {
    const temperatureSlider = document.getElementById('temperature');
    const temperatureValue = document.getElementById('temperature-value');

    temperatureSlider.addEventListener('input', function() {
        temperatureValue.textContent = temperatureSlider.value;
    });
});
