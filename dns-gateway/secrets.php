<?php
$networkkey = require('networkkey.php');
$weatherkey = require('weatherkey.php');
$serverHash = require('list.php');


//maybe switch to a post request in the future?
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  //check if key is correct
  if(array_key_exists("key", $_POST)){
    if(verifyPW($_POST["key"],$serverHash) == true){
      if(array_key_exists("weatherkey")){
        echo $weatherkey;
      } else if (array_key_exists("networkkey")){
        echo $networkkey;
      }
    }
  }
} 

function verifyPW($key, $ip, $hashlist, $pw){
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