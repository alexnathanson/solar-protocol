<?php
  //password protection
  require_once '/home/pi/solar-protocol/backend/protect/protect.php';
  Protect\with('/home/pi/solar-protocol/backend/protect/form.php', 'admin');

  //file upload
  require_once '/home/pi/solar-protocol/frontend/admin/settings/upload.php';
  //Upload\uploadIt();
  ?>

<html>
<head>
   <link rel="stylesheet" href="../admin.css">
</head>
<body>

<?php

  //read local file
  $localFile = '/home/pi/local/local.json';
  $imgDir = '/home/pi/local/www/';

  $spenv = '/home/pi/local/.spenv';

  $localInfo = json_decode(getFile($localFile), true);

  $apiErr = $dnsErr = $httpErr = "";

  if ($_SERVER["REQUEST_METHOD"] == "POST") {
      if (isset($_POST['key']) && $_POST['key'] == "form") {
          //handle the form data

          for ($k = 0; $k < count(array_keys($_POST));$k++) {
              //echo array_keys($_POST)[$k];

              if (isset($_POST['apiKey'])) {
                  if (empty($_POST['apiKey'])) {
                      $apiErr = "No data entered.";
                  } else {
                      //$localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
                      setEnv('API_KEY', $_POST['apiKey']);
                      //echo('API key received');
                  }
              } elseif (isset($_POST['dnsPW'])) {
                  if (empty($_POST['dnsPW'])) {
                      $dnsErr = "No data entered.";
                  } else {
                      //$localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
                      setEnv('DNS_KEY', $_POST['dnsPW']);
                      //echo('DNS key received');
                  }
              } elseif (isset($_POST['httpPort'])) {
                  if (! is_numeric($_POST['httpPort']) || strpos($_POST['httpPort'], '.')) {
                      $httpErr = "Port value is not an integer.";
                  } else {
                      $localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
                  }
              } else {
                  $localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
              }
          }

          file_put_contents($localFile, json_encode($localInfo, JSON_PRETTY_PRINT));
      } elseif (isset($_POST['key']) && $_POST['key'] == "file") {
          //handle the file
          //echo "file";
          Upload\uploadIt();
      }
  }

  //do not print directly except for debugging
  //echo json_encode($localInfo);


  $locName = $locDescription = $locLocation = $locCity = $locCountry = $locLat = $locLong = $locWatts = $locVolts= $httpPort = $httpsPort = "";

  if (isset($localInfo["name"])) {
      $locName = $localInfo["name"];
  }

  if (isset($localInfo["description"])) {
      $locDescription = $localInfo["description"];
  }

  if (isset($localInfo["location"])) {
      $locLocation = $localInfo["location"];
  }

  if (isset($localInfo["city"])) {
      $locCity = $localInfo["city"];
  }

  if (isset($localInfo["country"])) {
      $locCountry = $localInfo["country"];
  }

  if (isset($localInfo["lat"])) {
      $locLat = $localInfo["lat"];
  }

  if (isset($localInfo["long"])) {
      $locLong = $localInfo["long"];
  }

  if (isset($localInfo["pvWatts"])) {
      $locWatts = $localInfo["pvWatts"];
  }

  if (isset($localInfo["pvVolts"])) {
      $locVolts = $localInfo["pvVolts"];
  }

  if (isset($localInfo["httpPort"])) {
      $httpPort = $localInfo["httpPort"];
  } else {
      $httpPort = "80"; //display default port if no custom port info is found
  }

  //front end form for https needed
  /*if (isset($localInfo["httpsPort"])){
    $httpPort = $localInfo["httpsPort"];
  }*/

  function test_input($data)
  {
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
  /*function testAPIkey($data){
    echo !empty($data);
    if(!empty($data)){
      return true;
    } else {
      return false;
    }
  }*/

  function getFile($fileName)
  {
      //echo $fileName;
      try {
          return file_get_contents($fileName);
      } catch(Exception $e) {
          echo $fileName;
          return false;
      }
  }

  function setEnv($envKey, $envVal)
  {
      global $spenv;
      //test inputs
      $envKey = test_input($envKey);
      $envVal = test_input($envVal);

      /*  $execCmd = escapeshellcmd("bash /home/pi/solar-protocol/backend/set_env.sh \"${envKey}\" \"${envVal}\"");

        exec($execCmd, $shOutput);

        var_dump($shOutput);*/
      if (file_exists($spenv)) {
          //read in file
          $envVar = file($spenv);

          //var_dump($envVar);

          $newEnv = fopen($spenv, "w");

          for ($l = 0; $l < count($envVar); $l++) {
              if (strpos($envVar[$l], "export {$envKey}=") === false && $envVar[$l] !== "" && $envVar[$l] !== "\n") {
                  fwrite($newEnv, $envVar[$l]);
              }
          }

          fwrite($newEnv, "export {$envKey}={$envVal}\n");
          fclose($newEnv);
      } else {
          $output = "export {$envKey}={$envVal}\n";
          /*    echo $output;*/
          $newEnv = fopen($spenv, "w");
          fwrite($newEnv, $output);
          fclose($newEnv);
      }
  }

  ?>

<h1><a href="/">Solar Protocol (<?php echo $locName;?>)</a> - Admin Console</h1>

<span>Logged in as <a href="/admin/settings/user.php"><?php echo $_SESSION["username"]?></a> <a href="?logout">(Logout)</a></span>

<p><a href="/admin">Network Activity</a> | <a href="/admin/local.php">Local Data</a> | <a href="/admin/settings">Settings</a> | <a href="/admin/settings/local.php">Local Content</a></p>

<h2>Local Settings</h2>

<h3>Info</h3>
<form method="post" id="updateLocalInfo" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">

  <input type="hidden" name="key" value="form"/>

  <p>Name <input type="text" name="name" value="<?php if (isset($locName)) {
      echo $locName;
  }?>"></p>
  
  <p>Description (500 characters max)<br><!--  <input type="text" name="description" value="<?php if (isset($locDescription)) {
      echo $locDescription;
  }?>"></p> -->
  <textarea name="description" id="descriptionText" rows="5" cols="33" form="updateLocalInfo" maxlength="500"><?php if (isset($locDescription)) {
      echo $locDescription;
  }?></textarea>
  </p>

   <p>Location <input type="text" name="location" value="<?php if (isset($locLocation)) {
       echo $locLocation;
   }?>"></p>

   <p>City <input type="text" name="city" value="<?php if (isset($locCity)) {
       echo $locCity;
   }?>"></p>

   <p>Country <input type="text" name="country" value="<?php if (isset($locCountry)) {
       echo $locCountry;
   }?>"></p>

 	<p>Latitude <input type="text" name="lat" value="<?php if (isset($locLat)) {
 	    echo $locLat;
 	}?>"></p>

   <p>Longitude <input type="text" name="long" value="<?php if (isset($locLong)) {
       echo $locLong;
   }?>"></p>

   <p>PV Module Wattage <input type="text" name="pvWatts" value="<?php if (isset($locWatts)) {
       echo $locWatts;
   }?>"></p>

   <p>PV Module Voltage <input type="text" name="pvVolts" value="<?php if (isset($locVolts)) {
       echo $locVolts;
   }?>"></p>

  <p></p>
  <button type="submit">Update</button>
</form>

<div class="basicBox">
  <h3>Server Profile Photo</h3>
  <div style="width: 50%">
    <p>
      This image will be saved as serverprofile.gif and appear on solar protocol pages when your server is the point of entry. The maximum individual image files size is TBD.
      <br>The image file type must be a gif. It it recommended that you dither the image prior to uploading.
    </p>
    <form action="<?php echo $_SERVER["PHP_SELF"];?>" method="post" enctype="multipart/form-data">
      Select image to upload:
      <p>
      <input type="hidden" name="key" value="file"/>
      <input type="file" name="fileToUpload" id="fileToUpload">
      <input type="hidden" name="directory" value="<?php echo $imgDir; ?>" />
      <input type="hidden" name="rename" value="serverprofile"/>
      <input type="hidden" name="type" value="image" />
<!--       <input type="hidden" name="dither" value="true" />-->
    </p>
      <input type="submit" value="Upload Image" name="submit">
    </form>
  </div>
  <div style="width:50%"><!--should this float left?-->
    <!--display thumbnail image-->
    <img src="/local/serverprofile.gif" style="border: 2px solid black;width:150px; height:auto;">
  </div>
</div>

<div class="dangerBox">
  <h3>Network Info</h3>
  <form method="POST" onsubmit="return confirm('Are you sure you want to change the http port?');">
    <input type="hidden" name="key" value="form"/>
    <p>http port <input type="text" name="httpPort" value="<?php if (isset($httpPort)) {
        echo $httpPort;
    }?>"><span class="error" style="color:red"> <?php echo $httpErr;?></span></p>
    <button type="submit">Update Http Port</button>
  </form>
</div>

<div class="dangerBox">
  <h3>Security & Access Keys - Danger Zone!</h3>
  <form method="POST" onsubmit="return confirm('Are you sure you want to change the API key?');">
    <input type="hidden" name="key" value="form"/>
    <p>Network API key <input type="text" name="apiKey" value=""><span class="error" style="color:red"> <?php echo $apiErr;?></span></p>
    <button type="submit">Update API Key</button>
  </form>

  <form method="POST" onsubmit="return confirm('Are you sure you want to change the DNS password?');">
    <input type="hidden" name="key" value="form"/>
    <p>DNS Gateway Password <input type="text" name="dnsPW" value=""><span class="error" style="color:red"> <?php echo $dnsErr;?></span></p>
    <button type="submit">Update DNS Gateway Password</button>
  </form>
</div>

</body>
</html>
