// JavaScript to handle form submission and display output
document.getElementById('submitBtn').addEventListener('click', function() {
    var email = document.getElementById('emailInput').value;
    var message = document.getElementById('messageInput').value;
    
    if (email && message) {
      // Display the output section
      document.getElementById('outputEmail').innerText = email;
      document.getElementById('outputMessage').innerText = message;
      document.getElementById('output-section').style.display = 'block';
    } else {
      // Display an alert if fields are missing
      alert('Please fill out both the email and the message fields.');
    }
  });