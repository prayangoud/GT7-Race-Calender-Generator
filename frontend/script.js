function updateOutput(val, outputId) {
    document.getElementById(outputId).textContent = val + (outputId.includes('Wear') ? 'x' : '');
}

function selectOption(button, className) {
    const buttons = document.querySelectorAll('.' + className);
    buttons.forEach(btn => btn.classList.remove('active'));

    // Add 'active' class to the clicked button
    button.classList.add('active');

    // Update the corresponding hidden input based on the button group
    if (className === 'car-type') {
        document.getElementById('selectedCarType').value = button.textContent;
    } else if (className === 'tire-type') {
        document.getElementById('selectedTireType').value = button.textContent;
    } else if (className === 'race-format') {
        document.getElementById('raceFormat').value = button.textContent;
    }
}

function toggleButton(button) {
    button.classList.toggle('active');
    if (button.classList.contains('active')) {
        button.textContent = "BoP Enabled";
        document.getElementById('balanceOfPower').value = "On";
    } else {
        button.textContent = "BoP";
        document.getElementById('balanceOfPower').value = "Off";
    }
}

document.getElementById('raceConfigForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    const formData = new FormData(this);
    const jsonObject = {};

    for (const [key, value] of formData.entries()) {
        jsonObject[key] = value;
    }

    fetch('https://your-api-id.execute-api.region.amazonaws.com/stage/submit-form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonObject)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
});