<?php
  require_once '/home/pi/solar-protocol/frontend/admin/protect.php';
  Protect\with('/home/pi/solar-protocol/frontend/admin/form.php', '$2y$10$P7eYN7FYf0ZpI0L80.WazuNHIIcmqIaF.u2VJ0PnLSBydHUKe.P8W');
?>

<html>
<body>


<h1>Solar Protocol - Admin Console</h1>

<p><a href="/admin">Admin Console</a> | <a href="/admin/local">Local Info</a></p>

<form method="POST">
  <?php if( $_SERVER['REQUEST_METHOD'] == 'POST' ) { ?>
    Invalid password
  <?php } ?>
  
  <p>Name <input type="text" name="name" value=<?php echo $lName;?>></p>
  
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

<?php

$localInfo = getFile('/home/pi/local/local.json');

$lName = 'Van Brunt St.';

echo $localInfo;
//dump_var($localInfo);

function getFile($fileName){
  //echo $fileName;
  try{
    return file_get_contents($fileName);
  }
  catch(Exception $e) {
    echo $fileName;
    return FALSE;
  }

}

?>