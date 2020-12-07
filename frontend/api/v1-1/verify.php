
<?php
// See the password_hash() example to see where this came from.
$hash = '$2y$07$BCryptRequires22Chrcte/VlQH0piJtjXl.0t1XkA8pw9dMXTpOq';

if( isset($_POST['password'])) {

	if (password_verify($_POST['password'], $hash)) {
	    echo 'Password is valid!';
	} else {
	    echo 'Invalid password.';
	}
}
?>

<html>
<body>

<form method="POST">
  <?php if( $_SERVER['REQUEST_METHOD'] == 'POST' ) { ?>
    Invalid password
  <?php } ?>
  <p>Enter password for access:</p>
  <input type="password" name="password">
  <button type="submit">Submit</button>
</form>

</body>
</html>