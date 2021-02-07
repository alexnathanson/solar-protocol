<?php
  //password protection
  require_once '/home/pi/solar-protocol/frontend/admin/protect/protect.php';
  Protect\with('/home/pi/solar-protocol/frontend/admin/protect/form.php','admin');

  //file upload
 /* require_once '../frontend/admin/upload.php';
  Upload\uploadIt();*/
?>



<html>
<body>


<?php

//read local file
$localFile = '/home/pi/local/local.json';
$imgDir = '/home/pi/local/';

$localInfo = json_decode(getFile($localFile), true);

$apiErr = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  for ($k = 0; $k < count(array_keys($_POST));$k++){
    //echo array_keys($_POST)[$k];

    if(isset($_POST['apiKey'])){
      if(empty($_POST['apiKey'])){
        $apiErr = "No data entered.";
      } else {
        $localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
      }
    }else {
      $localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
    }
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

//add in a validation test?
function testAPIkey($data){
  echo !empty($data);
  if(!empty($data)){
    return true;
  } else {
    return false;
  }
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

<h1><a href="/">Solar Protocol</a> - Admin Console</h1>
<span>Logged in as <?php echo $_SESSION["username"]?> <a href="?logout">(Logout)</a></span>

<p><a href="/admin">Network Activity</a> | <a href="/admin/local.php">Local Data</a> | <a href="/admin/settings">Settings</a></p>

<h2>Local Settings</h2>

<h3>Info</h3>
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

<p>
<div style="padding: 10px; border: 2px solid black">
  <h3>System Photo</h3>
  <div style="width: 50%">
    <p>
      This image will appear on solar protocol pages when your server is the point of entry. The maximum individual image files size is TBD.
      <br>Accepted image file types: jpg, jpeg, png, gif
    </p>
    <form action="upload.php" method="post" enctype="multipart/form-data">
      Select image to upload:
      <p>
      <input type="file" name="fileToUpload" id="fileToUpload">
      <input type="hidden" name="directory" value="<?php echo $imgDir; ?>" />
      <input type="hidden" name="type" value="image" />
      <input type="hidden" name="rename" value="stewardImage"/>
    </p>
      <input type="submit" value="Upload Image" name="submit">
    </form>
  </div>
  <div style="width:50%"><!--should this float left?-->
    <!--display thumbnail image-->
    <img src="/local/bkrot-guide.png">
  </div>
</div>
</p>

<p>
<div style="padding: 10px; border: 5px; solid red">
  <h3>Danger Zone</h3>
  <form method="POST" onsubmit="return confirm('Are you sure you want to change the API key?');">
    <p>API key <input type="text" name="apiKey" value=""><span class="error" style="color:red"> <?php echo $apiErr;?></span></p>
    <button type="submit">Update</button>
  </form>
</div>
</p>

</body>
</html>
