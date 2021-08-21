<?php
  //password protection
  require_once '/home/pi/solar-protocol/backend/protect/protect.php';
  Protect\with('/home/pi/solar-protocol/backend/protect/form.php','admin');


  if(isset($_POST['hash']) && isset($_POST['rehash']) && $_POST['hash'] != "" ) {

    if(testInput()){
      updateUserInfo($_SESSION["username"], password_hash($_POST['hash'], PASSWORD_DEFAULT));
    }
  } 


  //read local file to get current server name
  $localFile = '/home/pi/local/local.json';

  $localInfo = json_decode(file_get_contents($localFile), true);

  if (isset($localInfo["name"])){
    $locName = $localInfo["name"];
  } else {
    $locName = "";
  }



function updateUserInfo($un, $pwHash){
  $fileName = '/home/pi/local/access.json';

  try{
    $f = json_decode(file_get_contents($fileName),true);
    
    //var_dump($f);

    $f['users'][$un]['hash']=$pwHash;
    //var_dump($f);
    file_put_contents($fileName, json_encode($f, JSON_PRETTY_PRINT));

    echo "Password for user " . $_SESSION["username"] . " has been successfully changed.<br>";
  }
  catch(Exception $e) {

    echo "Error";

  }
}

//what are the criteria to test the password?
function testInput(){

  //check that passwords match
  if($_POST['hash'] != $_POST['rehash']){
    echo "Passwords do not match.";
    return false;
  }

  //check for white spaces
  if(strpos($_POST['hash'],' ') !== false){
    echo "White space is not allowed.";
    return false;
  }

  /*check for password strength - something worth considering adding in the future
    a minimum of 8 characters
    at least one uppercase letter
    at least one number (digit)
    at least one of the following special characters !@#$%^&*-
  */

  return true;
}

?>


<html>
<head>
   <link rel="stylesheet" href="../admin.css">
</head>

<body>


<h1><a href="/">Solar Protocol (<?php echo $locName;?>)</a> - Admin Console</h1>

<span>Logged in as <a href="/admin/settings/user.php"><?php echo $_SESSION["username"]?></a> <a href="?logout">(Logout)</a></span>

<p><a href="/admin">Network Activity</a> | <a href="/admin/local.php">Local Data</a> | <a href="/admin/settings">Settings</a> | <a href="/admin/settings/local.php">Local Content</a></p>

<p>
  <strong>Submtting this form will change the password for the current user (<?php echo $_SESSION["username"]; ?>) only on this server.</strong>
</p>
<p>
  If you have forgotten your previous password, contact one of the Solar Protocol project leads via email or Discord to have your password reset. If you have access to multiple servers, you will need to manually update your password on each one.
</p>

<form method="POST" onsubmit="return confirm('Are you sure you want to change your password?');">

  <p>Enter new password to hash:</p>
  <p>
    <input type="password" name="hash" required>
  </p>
  <p>Re-enter new password to hash:</p>
  <p>
    <input type="password" name="rehash" required>
  </p>
  <button type="submit">Submit</button>
</form>

</body>
</html>