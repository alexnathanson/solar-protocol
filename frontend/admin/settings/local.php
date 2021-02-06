<?php
  require_once '/home/pi/solar-protocol/frontend/admin/protect/protect.php';
  Protect\with('/home/pi/solar-protocol/frontend/admin/protect/form.php','admin');
?>

<html>
<body>


<?php

//local www directory
$localWWW = "/home/pi/local/www/";

$totalDiskSpace = $availableDiskSpace = "";

diskSpace("/");

function diskSpace($dirSpace){
  global $totalDiskSpace, $availableDiskSpace;

  $totalDiskSpace = disk_total_space($dirSpace);
  $availableDiskSpace = disk_free_space($dirSpace);

  //echo $availableDiskSpace . " / " . $totalDiskSpace; 
}

/*
//read local file
$localFile = '/home/pi/local/local.json';
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
}*/

//from index
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

//from index
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

<h2>Local Content</h2>

<p>We are in the process of developing complete guidelines for uploading content. For the time being, we are only allowing static HTML pages and CSS, without any Javascript or PHP.</p>

<p>
  The maximum individual image files size is ?
  <br>The maximum size your site can take up cannot exceed more than 90% of the total disk space.
</p>

<p>
  <?php echo "Available disk space: ". $availableDiskSpace . " bytes"; ?>
  <br><?php echo "Total disk space: " . $totalDiskSpace . " bytes"; ?> 
</p>

<form action="upload.php" method="post" enctype="multipart/form-data">
  Select image to upload:
  <input type="file" name="fileToUpload" id="fileToUpload">
  <input type="submit" value="Upload Image" name="submit">
</form>

</body>
</html>
