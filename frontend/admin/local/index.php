<html>
<body>

<form method="POST">
  <?php if( $_SERVER['REQUEST_METHOD'] == 'POST' ) { ?>
    Invalid password
  <?php } ?>
  <p>Server Location</p>
  <input type="Location" name="location">
  p>Server Details</p>
  <input type="details" name="details">
  <button type="submit">Submit</button>
</form>

</body>
</html>