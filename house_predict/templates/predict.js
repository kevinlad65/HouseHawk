document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("prediction-form");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        // Gather form data
        const formData = new FormData(form);
        const data = {};
        formData.forEach(function(value, key){
            data[key] = value;
        });

        // Check for missing fields
        let missingFields = [];
        if (!data["location_encoded"]) missingFields.push("Location");
        if (!data["BHK_numeric"]) missingFields.push("BHK");
        if (!data["Floor_numeric"]) missingFields.push("Floor");
        if (!data["Furnishing_encoded"]) missingFields.push("Furnishing");
        if (!data["Car Parking_numeric"]) missingFields.push("Car Parking");
        if (!data["Super Area_numeric"]) missingFields.push("Super Area");
        if (!data["Carpet Area_numeric"]) missingFields.push("Carpet Area");

        if (missingFields.length > 0) {
            // Display error message for missing fields
            const errorMessage = "Please fill in the following fields: " + missingFields.join(", ");
            const resultElement = document.getElementById("result");
            resultElement.innerText = errorMessage;
            return; // Stop further execution
        }

        // Make a POST request to your Django backend
        fetch("{% url 'predict' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': getCookie('csrftoken'), // Add CSRF token
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            // Update UI with predicted amount
            const predictedAmount = data.predicted_amount; // Adjust key based on response
            const resultElement = document.getElementById("result");
            resultElement.innerText = "Predicted Amount: " + predictedAmount;
        })
        .catch(error => console.error("Error:", error));
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
