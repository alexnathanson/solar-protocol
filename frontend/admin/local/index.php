<html>
<body>

<form method="POST">
  <?php if( $_SERVER['REQUEST_METHOD'] == 'POST' ) { ?>
    Invalid password
  <?php } ?>
  
  <p>Name</p>
  <input type="text" name="name">
  
  <p>Description</p>
  <input type="text" name="description">
  
   <p>Location</p>
  <input type="text" name="location">

   <p>City</p>
  <input type="text" name="city">

   <p>Country</p>
  <input type="text" name="country">

 	<p>Latitude</p>
  <input type="text" name="lat">

   <p>longitude</p>
  <input type="text" name="long">

 <p>API key</p>
  <input type="password" name="apiKey">

   <p>Background Color</p>
  <input type="text" name="bgColor">

   <p>Server Color</p>
  <input type="text" name="serverColor">

  <!--make a drop down menu-->
   <p>Font</p>
  <input type="text" name="font">

   <p>Border Style</p>
  <input type="text" name="borderStyle">

  <p></p>
  <button type="submit">Update</button>
</form>

</body>
</html>