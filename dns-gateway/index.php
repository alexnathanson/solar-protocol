<?php
/*the dynamic dns service API key is stored in plain text in a file called key.php
this file must return the key as a string
the only code in that file is a 'return KEY_IN_QUOTES'
it must be located in the same directory as this script*/
$dnskey = require('key.php');

#header('Content-Type: application/json');

//in the future this should be either a database or a seperate json file
//white list
$serverHash = [
  "SPfA" => "$2y$10$8jr3efgV3/N2RosUY0cH1edYXYcYNE4Iwi6RHqYwyupnccYVX9f5.",
  "Hells Gate" => "$2y$10$5/O1zeTvLmxBNIRpmqve5u6x9RmL8JBi./dzgD3mwfudHEBuABFQ6",
  "Tega" => "",
  "Chile" => "$2y$10$M3RtM5fYwzUXYQJRx1OGDe9oPSAmnApDPlCWpYCpHXcQixCPVaNge",
  "Caddie" => "$2y$10$157Qs27b4.gUAHlF0o/i5ufIF/tclJ8GitcIQbgeA9t76XYF0S0Ve",
  "Low Carbon Methods" => "$2y$10$VUtTRwbT5N1dZi902Xa3BeLCRAKhC9BnjQ7M/7iEq9xiO6H3LTGqu"
];

//this is the black list. there could potentailly be multiple burned keys from the same server, so another data format might be necessary
$blackList = [
    /*"Dominica" => ""*/
];

//maybe switch to a post request in the future?
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  //echo "we got post!";
  //check if key is correct
  if(array_key_exists("ip", $_POST) && array_key_exists("key", $_POST)){
    verifyPW($_POST["key"],$_POST["ip"],$serverHash, $dnskey);
  }
} elseif ($_SERVER["REQUEST_METHOD"] == "GET") {
  //echo "GETTING!";
  if(array_key_exists("list", $_GET)){
    //echo $_GET["list"];
    if($_GET["list"] == "true"){
      echo json_encode($serverHash);
    } elseif($_GET["list"] == "false"){
      echo json_encode($blackList);
    }
  } elseif(array_key_exists("ip", $_GET)){
      #echo "get updating...<br>";
      verifyPW($_GET["key"],$_GET["ip"],$serverHash, $dnskey);
  } else {
    echo "no match";
  }
}

function verifyPW($key, $ip, $hashlist, $pw){
  $verified = false;
  # hash generated from password_hash() more info at https://www.php.net/manual/en/function.password-hash.php

  #loop through all hashes...
  foreach($hashlist as $name => $hash){
    //echo $hash . "<br>";
    if(password_verify($key, $hash)){
      //echo "updating ip...<br>";
      updateIP($ip, $pw);
      writeMostRecent($name);
      $verified = true;
    }
  }
  if ($verified == false) {
      echo "api key not verified";
  }
}

//makes the API call to the DNS registry to update it
function updateIP($ip, $pw){
  #echo "updating IP for real!<br>";

  $host='@';
  $domain='solarprotocol.net';

  $response = file_get_contents("https://dynamicdns.park-your-domain.com/update?host=" . $host . "&domain=" . $domain . "&password=" . $pw . "&ip=" . $ip);
  #header('Content-Type: application/json');
  echo $response;
  #exit();#not necessary...
}

function writeMostRecent($thisPOE){
  $file = 'poe.txt';
  // Open the file to get existing content
  #$current = file_get_contents($file);
  // Append a new person to the file
  #$current .= "John Smith\n";

  $current = $thisPOE;
  // Write the contents back to the file
  file_put_contents($file, $current);
}

?>