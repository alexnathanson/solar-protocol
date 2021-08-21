<html>
<body>

<h1><a href="/">Solar Protocol</a></h1>

<form method="POST">
  <?php if( $_SERVER['REQUEST_METHOD'] == 'POST' ) { ?>
    Invalid user name or password
  <?php } ?>
  <p>Username</p>
  <input type="text" name="username">
  <p>Password</p>
  <input type="password" name="password">
  <button type="submit">Submit</button>
</form>

<p>
  If you have forgotten your password, contact Alex, Benedetta, or Tega for a temporary password.
</p>

<p>
  To reset your password, login and click on your user name.
</p>

</body>
</html>