<html>
<body>

<form method="POST">
  <?php if( $_SERVER['REQUEST_METHOD'] == 'POST' ) { ?>
    Invalid password
  <?php } ?>
  <p>Username</p>
  <input type="text" name="username">
  <p>Password</p>
  <input type="password" name="password">
  <button type="submit">Submit</button>
</form>

</body>
</html>