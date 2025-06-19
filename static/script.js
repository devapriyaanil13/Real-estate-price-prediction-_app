// Fetch and populate location dropdown when page loads
window.onload = async function () {
  const locationSelect = document.getElementById('location');
  const res = await fetch('/get_location_names');
  const data = await res.json();

  data.locations.forEach(loc => {
    const option = document.createElement('option');
    option.value = loc;
    option.textContent = loc;
    locationSelect.appendChild(option);
  });
};

// Handle form submission
document.getElementById('predictForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const location = document.getElementById('location').value.toLowerCase();
  const sqft = document.getElementById('sqft').value;
  const bhk = document.getElementById('bhk').value;
  const bath = document.getElementById('bath').value;

  const response = await fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, sqft, bhk, bath })
  });

  const data = await response.json();
  const resultElement = document.getElementById('result');

  if (data.price) {
    resultElement.innerText = `Estimated Price: ₹${data.price} Lakhs`;
  } else {
    resultElement.innerText = `Error: ${data.error}`;
  }
});