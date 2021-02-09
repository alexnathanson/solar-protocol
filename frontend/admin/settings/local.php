<?php
  require_once '/home/pi/solar-protocol/backend/protect/protect.php';
  Protect\with('/home/pi/solar-protocol/backend/protect/form.php','admin');

  require_once '/home/pi/solar-protocol/frontend/admin/settings/upload.php';
?>

<html>
<head>
   <link rel="stylesheet" href="../admin.css">
 </head>
<body>

<?php

//local www directory
$localWWW = "/home/pi/local/www/";

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  //var_dump($_POST);

  //make new directory
  if(isset($_POST['newDirectory']) && isset($_POST['parent'])){
    if(!is_dir($_POST['parent'] . $_POST['newDirectory'])){
      mkdir($_POST['parent'] . $_POST['newDirectory']);
    } else {
      echo "<br>Directory already exists.";
    }
  } else if (isset($_POST['type']) && $_POST['type'] == "delete"){//delete file or directory
    $pK = array_keys($_POST);
    foreach ($pK as $k => $f){
      if(strpos($f, "file") !== false){
        deleteFile($_POST[$f]);
      } else if (strpos($f, "directory") !== false){
        deleteDirectory($_POST[$f]);
      }
    }
  } else if (isset($_POST['type']) && $_POST['type'] == "upload"){//upload file
    $uploadStatus .= "Upload Status:";
    Upload\uploadIt();
  }
}


$totalDiskSpace = $availableDiskSpace = $diskUnits = "";

diskSpace("/");

function mapDirectory($mapThis, $count = 0){

  if(is_dir($mapThis)){
    //echo $count;

    $mappedDirectory = scandir($mapThis);

    $fileNum = 0;

    foreach ($mappedDirectory as $k => $f){
      if($f != "." && $f != ".."){
        for($c = 0; $c < $count; $c++){
          echo "-- ";
        }
        $fN = $mapThis.$f;
       
        if(!is_dir($fN)){
          outputCheck("file-".$fileNum, $fN, $fN . " (last modified: ".date("F d Y H:i:s.", filemtime($fN)) . ")");
        } else if(is_dir($fN)){
          outputCheck("directory-".$fileNum, $fN, $fN . " (last modified: ".date("F d Y H:i:s.", filemtime($fN)) . ")");
          mapDirectory($fN."/", $count + 1);
        } else {

        }
      }
      $fileNum++;
    }

  }
}

function listDirectories($mapThis, $nameRadio){

  if(is_dir($mapThis)){

    outputRadio($mapThis, $nameRadio);
    $mappedDirectory = scandir($mapThis);


    foreach ($mappedDirectory as $k => $f){
      if($f != "." && $f != ".."){
       
        $fN = $mapThis.$f;
       
        if(is_dir($fN)){
          listDirectories($fN."/", $nameRadio);
        }
      }
    }

  }
}

function outputCheck($checkName, $checkValue, $checkDisplay){
  echo "<input type='checkbox' name=" . $checkName . " value=" . $checkValue . ">
  <label for=" . $checkValue . ">" . $checkDisplay ."</label><br>";
}

function outputRadio($radioValue, $rN){
  echo "<input type='radio' name=" . $rN . " value=" . $radioValue . ">
  <label for=" . $radioValue . ">" . $radioValue ."</label><br>";
}

function deleteFile($delThis){
  if(strpos($delThis, $GLOBALS['localWWW'])!== false){
      unlink($delThis);
      echo "<br>".$delThis . " deleted";
  }
}

function deleteDirectory($delThis){

  if(strpos($delThis, $GLOBALS['localWWW'])!==false && is_dir($delThis)){

    $scanDir = scandir($delThis);

    if(!is_null($scanDir)){
      foreach ($scanDir as $k => $f){
        if($f != "." && $f != ".."){
          $fP = $delThis . "/" . $f;
          if(is_dir($fP)){
            deleteDirectory($fP);
          } else if (is_file($fP)){
            deleteFile($fP);
          }
        }
      }
    }

    rmdir($delThis);
    echo "<br>".$delThis . " deleted";
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

<p><a href="/admin">Network Activity</a> | <a href="/admin/local.php">Local Data</a> | <a href="/admin/settings">Settings</a> | <a href="/admin/settings/local.php">Local Content</a></p>

<h2>Local Public Content</h2>

<p>Local public content is located in the /home/pi/local/www directory.</p>

<p>We are in the process of developing complete guidelines for uploading content. For the time being, we are only allowing static HTML pages and CSS, without any Javascript or PHP.</p>

<p>
  The maximum individual image files size is <?php echo $maxFileSizeBytes . " " . $diskUnits; ?>.
<!--   <br>The maximum size your site can take up cannot exceed more than 90% of the total disk space.
 --></p>

<p>
  <?php echo "Available disk space: ". $availableDiskSpace . " " . $diskUnits; ?>
  <br><?php echo "Total disk space: " . $totalDiskSpace . " " . $diskUnits; ?> 
</p>

<div class="basicBox">
<h3>Current Files</h3>
  <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" onsubmit="return confirm('Are you sure you want to delete the selected files?');">
    <p>
     <?php mapDirectory($localWWW);?>
   </p>
      <input type="hidden" name="type" value="delete" />
      <input type="submit" value="Delete Selected Files" name="submit">
  </form>
</div>

<div class="basicBox">
<h3>Create New Directory:</h3>
  <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
    <p>Name <input type="text" name="newDirectory" value=""></p>
    <p>
      Select parent directory:<br>
      <?php listDirectories($localWWW, "parent");?>
    </p>
    <input type="submit" value="Create New Directory" name="submit">
  </form>
</div>

<div class="basicBox">

<div <?php if($uploadStatus != ""){echo "id='uploadStatus'"}; ?>>
  <?php echo $uploadStatus; ?>
</div>

<h3>Upload File:</h3>
  <form action="<?php echo $_SERVER["PHP_SELF"];?>" method="post" enctype="multipart/form-data">
    <p><input type="file" name="fileToUpload" id="fileToUpload"></p>
    <!-- <p>Save as (optional) <input type="text" name="saveAs" value=""></p> -->
    <p><input type="checkbox" name="replace" value="0">
    <label for="replace">Replace existing file if file with same name already exists?</label></p>
    <p>
      Save to directory:<br>
      <?php listDirectories($localWWW, "directory");?>
    </p>
    <input type="hidden" name="type" value="upload" />
    <input type="submit" value="Upload File" name="submit">
  </form>
</div>

</body>
</html>
