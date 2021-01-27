<?php
  require_once '/home/pi/solar-protocol/frontend/admin/protect.php';
  Protect\with('/home/pi/solar-protocol/frontend/admin/form.php', '$2y$10$P7eYN7FYf0ZpI0L80.WazuNHIIcmqIaF.u2VJ0PnLSBydHUKe.P8W','admin');
?>

<html>
<body>


<?php

//validate form
if ($_SERVER["REQUEST_METHOD"] == "POST") {

  //check if this works...
  for ($k = 0; $k < count(array_keys($_POST));$k++){
    //$_POST[array_keys($_POST)[$k]] = test_input()
    echo $k;
    echo array_keys($_POST)[$k];
  }

if (isset($_POST["name"])){
  $name = test_input($_POST["name"]);
}
  $email = test_input($_POST["email"]);
  $website = test_input($_POST["website"]);
  $comment = test_input($_POST["comment"]);
  $gender = test_input($_POST["gender"]);
}

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}

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

//echo json_encode($localInfo);

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

function putFile($fileName, $putData){
    file_put_contents($filename, $putData);
}

?>

<h1>Solar Protocol - Admin Console</h1>

<p><a href="/admin">Admin Console</a> | <a href="/admin/local">Local Info</a></p>

<h3>Local Info</h3>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">

  
  <p>Name <input type="text" name="name" value="<?php if (isset($locName)){echo $locName;}?>"></p>
  
  <p>Description <input type="text" name="description" value="<?php if (isset($locDescription)){echo $locDescription;}?>"></p>
  
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
    <p>API key <input type="password" name="apiKey" value=""></p>
    <button type="submit">Update</button>
  </form>
</div>
</body>
</html>
