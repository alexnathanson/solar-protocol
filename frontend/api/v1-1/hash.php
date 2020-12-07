
<?php
/**
 * We just want to hash our password using the current DEFAULT algorithm.
 * This is presently BCRYPT, and will produce a 60 character result.
 *
 * Beware that DEFAULT may change over time, so you would want to prepare
 * By allowing your storage to expand past 60 characters (255 would be good)
 */
if( isset($_POST['password'])) {
	echo $_POST['password'];
	echo password_hash($_POST['password'], PASSWORD_DEFAULT);
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