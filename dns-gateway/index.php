<?php
/*the dynamic dns service API key is stored in plain text in a file called key.php
this file must return the key as a string
the only code in that file is a 'return KEY_IN_QUOTES'
it must be located in the same directory as this script*/
$dnskey = require('key.php');

//in the future this should be either a database or a seperate json file
//white list
$serverHash = [
  "SPfA" => "",
  "Hells Gate" => "",
  "Tega" => "",
  "Chile" => "",
  "Caddie" => "",
  "Low Carbon Methods" => ""
];

//this is the black list. there could potentailly be multiple burned keys from the same server, so another data format might be necessary
$blackList = [
    /*"Dominica" => ""*/
];

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  //check if key is correct
  verifyPW($_POST["api_key"],$_POST["ip"]);
} elseif ($_SERVER["REQUEST_METHOD"] == "GET") {
    if(array_key_exists("list", $_GET)){
      //echo $_GET["list"];
      if($_GET["list"] == "black"){
        echo json_encode($blackList);
      }
    } /*elseif(array_key_exists("update", $_GET)){
      echo "updating...";
      updateIP("174.95.54.93");
    }*/
}

function verifyPW($key, $ip){

  # hash generated from password_hash() more info at https://www.php.net/manual/en/function.password-hash.php

  #loop through all hashes...
  foreach($serverHash as $name => $hash){
    if(password_verify($key, $hash)){
      updateIP($ip);
    }
  }
}

//makes the API call to the DNS registry to update it
function updateIP($ip){

  $host='@';
  $domain='solarprotocol.net';

  $response = file_get_contents("https://dynamicdns.park-your-domain.com/update?host=" . $host . "&domain=" . $domain . "&password=" . $GLOBALS["dnskey"] . "&ip=" . $ip);
  echo $response;
}

?>


<!DOCTYPE html>
<html>

<head>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<title>DNS Gateway</title>

</head>

<body>

</body>
</html>