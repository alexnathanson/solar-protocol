<?php
  require_once '/home/pi/solar-protocol/frontend/admin/protect.php';
  Protect\with('/home/pi/solar-protocol/frontend/admin/form.php', '$2y$10$P7eYN7FYf0ZpI0L80.WazuNHIIcmqIaF.u2VJ0PnLSBydHUKe.P8W');
?>

<html>
<body>


<?php

$localInfo = json_decode(getFile('/home/pi/local/local.json'), true);

if (isset($localInfo["name"])){
  $locName = $localInfo["name"];
}

if (isset($localInfo["description"])){
  $locDescription = $localInfo["description"];
}

if (isset($localInfo["location"])){
  $locLocation = $localInfo["location"];
}

if (isset($localInfo["city"])){
  $locCity = $localInfo["city"];
}

if (isset($localInfo["country"])){
  $locCountry = $localInfo["country"];
}

if (isset($localInfo["lat"])){
  $locLat = $localInfo["lat"];
}

if (isset($localInfo["long"])){
  $locLong = $localInfo["long"];
}

if (isset($localInfo["apiKey"])){
  $locKey = $localInfo["apiKey"];
}

if (isset($localInfo["bgColor"])){
  $locBg = $localInfo["bgColor"];
}

if (isset($localInfo["serverColor"])){
  $locSColor = $localInfo["serverColor"];
}

if (isset($localInfo["font"])){
  $locFont = $localInfo["font"];
}

if (isset($localInfo["borderStyle"])){
  $locBorderStyle = $localInfo["borderStyle"];
}

echo json_encode($localInfo);
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

<h1>Solar Protocol - Admin Console</h1>

<p><a href="/admin">Admin Console</a> | <a href="/admin/local">Local Info</a></p>

<form method="POST">
  <?php if( $_SERVER['REQUEST_METHOD'] == 'POST' ) { ?>
    Invalid password
  <?php } ?>
  
  <p>Name <input type="text" name="name" value="<?php if (isset($locName)){echo $locName;}?>"></p>
  
  <p>Description <input type="text" name="description" value="<?php if (isset($locDescription)){echo $locDescription;}?>"></p>
  
   <p>Location <input type="text" name="location" value="<?php if (isset($locLocation)){echo $locLocation;}?>"></p>

   <p>City <input type="text" name="city" value="<?php if (isset($locCity)){echo $locCity;}?>"></p>

   <p>Country <input type="text" name="country" value="<?php if (isset($locCountry)){echo $locCountry;}?>"></p>

 	<p>Latitude <input type="text" name="lat" value="<?php if (isset($locLat)){echo $locLat;}?>"></p>

   <p>Longitude <input type="text" name="long" value="<?php if (isset($locLong)){echo $locLong;}?>"></p>

   <p>API key <input type="password" name="apiKey" value="<?php if (isset($locKey)){echo $locKey;}?>"></p>

   <p>Background Color <input type="text" name="bgColor" value="<?php if (isset($locBg)){echo $locBg;}?>"></p>

   <p>Server Color <input type="text" name="serverColor" value="<?php if (isset($locSColor)){echo $locSColor;}?>"></p>

   <p>Font <input type="radio" name="font" value="<?php if (isset($locFont)){echo $locFont;}?>"></p>

   <p>Border Style <input type="text" name="borderStyle" value="<?php if (isset($locBorderStyle)){echo $locBorderStyle;}?>"></p>

  <p></p>
  <button type="submit">Update</button>
</form>

</body>
</html>
