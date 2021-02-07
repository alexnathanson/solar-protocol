<?php
  require_once '/home/pi/solar-protocol/frontend/admin/protect/protect.php';
  Protect\with('/home/pi/solar-protocol/frontend/admin/protect/form.php','admin');
?>

<html>
<body>


<?php

//local www directory
$localWWW = "/home/pi/local/www/";

/*var_dump(scandir($localWWW));
*/

$totalDiskSpace = $availableDiskSpace = $diskUnits = "";

diskSpace("/");

function mapDirectory($mapThis, $count = 0){

  if(is_dir($mapThis)){
    //echo $count;

    $mappedDirectory = scandir($mapThis);

    foreach ($mappedDirectory as $k => $f){
      if($f != "." && $f != ".."){
        for($c = 0; $c < $count; $c++){
          echo "-- ";
        }
        $fN = $mapThis.$f;
        echo $fN;
        echo " (last modified: ".date("F d Y H:i:s.", filemtime($fN)) . ")";
        echo "<br>";
        if(is_dir($fN)){
          mapDirectory($fN."/", $count + 1);
        }
      }
    }

  }
}

function diskSpace($dirSpace){
  global $totalDiskSpace, $availableDiskSpace, $diskUnits;

  $totalDiskSpace = disk_total_space($dirSpace);
  $availableDiskSpace = disk_free_space($dirSpace);

  $diskUnits = "bytes";
  //echo $availableDiskSpace . " / " . $totalDiskSpace; 
}


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

<h2>local/www Directory</h2>

<p>
  <?php echo "Available disk space: ". $availableDiskSpace . " " . $diskUnits; ?>
  <br><?php echo "Total disk space: " . $totalDiskSpace . " " . $diskUnits; ?> 
</p>

<h3>Current Files</h3>
<!-- <form action="/action_page.php">
  <input type="checkbox" id="vehicle1" name="vehicle1" value="Bike">
  <label for="vehicle1"> I have a bike</label><br>
  <input type="checkbox" id="vehicle2" name="vehicle2" value="Car">
  <label for="vehicle2"> I have a car</label><br>
  <input type="checkbox" id="vehicle3" name="vehicle3" value="Boat">
  <label for="vehicle3"> I have a boat</label><br><br>
  <input type="submit" value="Remove Selected Files">
</form> -->

<p>
  <?php mapDirectory($localWWW);?>
</p>


<form action="upload.php" method="post" enctype="multipart/form-data">
  Select file to upload:<br>
  <p><input type="file" name="fileToUpload" id="fileToUpload"></p>
  <p>Save as (option) <input type="text" name="saveAs" value=""></p>
  <input type="submit" value="Upload Image" name="submit">
</form>

</body>
</html>
