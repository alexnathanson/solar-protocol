<?php
//this script responds to post requests on the /secrets.php end point with the keys
//example: beta.solarpowerforartists.com/secrets.php?key=true

$networkkey = require('networkkey-beta.php');
$appid = require('appid.php');
$serverHash = require('list.php');

//check if POST Request
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  //check if key is include
  if(array_key_exists("key", $_POST)){
    //check if key is correct
    if(verifyPW($_POST["key"],$serverHash) == true){
      //check if secret key exists
      if(array_key_exists("secret", $_POST)){
        //check if secret requested is appid
        if($_POST["secret"] == 'appid'){
          echo $appid;
        //check if secret requested is network key
        } else if ($_POST["secret"] == 'networkkey'){
          echo $networkkey;
        }
      }
    }
  }
} 

function verifyPW($key, $hashlist){
  $verified = false;

  #loop through all hashes...
  foreach($hashlist as $name => $hash){
    //echo $hash . "<br>";
    if(password_verify($key, $hash)){

      $verified = true;
    }
  }
  if ($verified == false) {
      echo "api key not verified";
  }

  return $verified;
}

?>