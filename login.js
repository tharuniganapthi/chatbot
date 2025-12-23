document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
   
    // Check credentials (You can replace this with your backend authentication logic)
    if (username === 'admin' && password === 'password') {
      // Redirect to another page
      window.location.href = 'temp.html'; // Change 'welcome.html' to your desired page
    } else {
      alert('Invalid username or password');
    }
  });



















































  