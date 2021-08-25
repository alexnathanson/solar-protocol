<?php
/*the dynamic dns service API key is stored in plain text in a file called key.php
this file must return the key as a string
the only code in that file is a 'return KEY_IN_QUOTES'
it must be located in the same directory as this script*/
$dnskey = require('key.php');

//in the future this should be either a database or a seperate json file
//white list
$serverHash = [
  "SPfA" => "$2y$10$8jr3efgV3/N2RosUY0cH1edYXYcYNE4Iwi6RHqYwyupnccYVX9f5.",
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
  echo "we got post!";
  //check if key is correct
  verifyPW($_POST["key"],$_POST["ip"],$serverHash);
} elseif ($_SERVER["REQUEST_METHOD"] == "GET") {
    if(array_key_exists("list", $_GET)){
      //echo $_GET["list"];
      if($_GET["list"] == "true"){
        echo json_encode($serverHash);
      } elseif($_GET["list"] == "false"){
        echo json_encode($blackList);
      }
    } elseif(array_key_exists("ip", $_GET)){
        echo "get updating...<br>";
        verifyPW($_GET["key"],$_GET["ip"],$serverHash);
    }
}

function verifyPW($key, $ip, $hashlist){
  $verified = false;
  # hash generated from password_hash() more info at https://www.php.net/manual/en/function.password-hash.php

  #loop through all hashes...
  foreach($hashlist as $name => $hash){
    echo $hash . "<br>";
    if(password_verify($key, $hash)){
      echo "updating ip...<br>";
      updateIP($ip);
      $verified = true;
    }
  }
  if ($verified == false) {
      echo "api key not verified";
  }
}

//makes the API call to the DNS registry to update it
function updateIP($ip){
  echo "updating IP for real!<br>";

  $host='@';
  $domain='solarprotocol.net';

  $response = file_get_contents("https://dynamicdns.park-your-domain.com/update?host=" . $host . "&domain=" . $domain . "&password=" . $GLOBALS["dnskey"] . "&ip=" . $ip);
  echo $response;
}

?>

<!-- 
<!DOCTYPE html>
<html>

<head>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<title>DNS Gateway</title>

</head>

<body>

</body>
</html> -->