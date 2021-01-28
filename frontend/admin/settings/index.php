<?php
  require_once '/home/pi/solar-protocol/frontend/admin/protect.php';
  Protect\with('/home/pi/solar-protocol/frontend/admin/form.php', '$2y$10$P7eYN7FYf0ZpI0L80.WazuNHIIcmqIaF.u2VJ0PnLSBydHUKe.P8W','admin');
?>

<html>
<body>


<?php

//read local file
$localFile = '/home/pi/local/local.json';
$localInfo = json_decode(getFile($localFile), true);


//validate form

//$postedData = array();

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  for ($k = 0; $k < count(array_keys($_POST));$k++){
    //echo array_keys($_POST)[$k];
    $localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
  }

  file_put_contents($localFile, json_encode($localInfo, JSON_PRETTY_PRINT));

}

//this will display the api key so DO NOT print directly except for debugging
//echo json_encode($localInfo);


$locName = $locDescription = $locLocation = $locCity = $locCountry = $locLat = $locLong = "";

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

function test_input($data) {
 /* $data = str_replace("\r", " ", $data) //rm line breaks
  $data = str_replace("\n", " ", $data) //rm line breaks
  $data = str_replace("  ", " ", $data) //replace double spaces with single space*/
  $data = str_replace(array("\n", "\r", "  "), ' ', $data);
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}

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

<p><a href="/admin">Network Activity</a> | <a href="/admin/local.php">Local Data</a> | <a href="/admin/settings">Settings</a></p>

<h2>Local Settings</h2>
<form method="post" id="updateLocalInfo" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">

  
  <p>Name <input type="text" name="name" value="<?php if (isset($locName)){echo $locName;}?>"></p>
  
  <p>Description (500 characters max)<br><!--  <input type="text" name="description" value="<?php if (isset($locDescription)){echo $locDescription;}?>"></p> -->
  <textarea name="description" id="descriptionText" rows="5" cols="33" form="updateLocalInfo" maxlength="500"><?php if (isset($locDescription)){echo $locDescription;}?></textarea>
  </p>

   <p>Location <input type="text" name="location" value="<?php if (isset($locLocation)){echo $locLocation;}?>"></p>

   <p>City <input type="text" name="city" value="<?php if (isset($locCity)){echo $locCity;}?>"></p>

   <p>Country <input type="text" name="country" value="<?php if (isset($locCountry)){echo $locCountry;}?>"></p>

 	<p>Latitude <input type="text" name="lat" value="<?php if (isset($locLat)){echo $locLat;}?>"></p>

   <p>Longitude <input type="text" name="long" value="<?php if (isset($locLong)){echo $locLong;}?>"></p>

  <p></p>
  <button type="submit">Update</button>
</form>


<div style="padding: 10px; border: 5px solid red">
  <h3>Danger Zone</h3>
  <form method="POST" onsubmit="return confirm('Are you sure you want to change the API key?');">
    <p>API key <input type="text" name="apiKey" value=""></p>
    <button type="submit">Update</button>
  </form>
</div>
</body>
</html>
