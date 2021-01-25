<html>
<body>

<form method="POST">
  <?php if( $_SERVER['REQUEST_METHOD'] == 'POST' ) { ?>
    Invalid password
  <?php } ?>
  
  <p>Name <input type="text" name="name"></p>
  
  <p>Description <input type="text" name="description"></p>
  
   <p>Location <input type="text" name="location"></p>

   <p>City <input type="text" name="city"></p>

   <p>Country <input type="text" name="country"></p>

 	<p>Latitude <input type="text" name="lat"></p>

   <p>Longitude <input type="text" name="long"></p>

   <p>API key <input type="password" name="apiKey"></p>

   <p>Background Color <input type="text" name="bgColor"></p>

   <p>Server Color <input type="text" name="serverColor"></p>

   <p>Font <input type="radio" name="font" value=""></p>

   <p>Border Style <input type="text" name="borderStyle"></p>

  <p></p>
  <button type="submit">Update</button>
</form>

</body>
</html>