var working = false;

$('.login').on('submit', function (e) {
  e.preventDefault();

  if (working) return;
  working = true;

  var $this = $(this),
    $state = $this.find('button > .state');

  $this.addClass('loading');
  $state.html('Authenticating');

  // Get values from the form
  var username = $this.find('input[type="text"]').val();
  var password = $this.find('input[type="password"]').val();
  console.log(username);

  // Make an AJAX request to the Flask server
  $.ajax({
    url: 'http://127.0.0.1:5000/login', // Update with your Flask server address
    method: 'POST',
    data: { username: username, password: password },
    success: function (response) {
      if (response.message === 'Authentication successful') {
        $this.addClass('ok');
        $state.html('Welcome back!');
        window.location.href = '/dashboard?username=' + username;
      }
    },
    error: function (xhr, status, error) {
      console.error('Error:', error);
      $state.html('Log in');
      $this.removeClass('ok loading');
      working = false;
    },
  });
});
