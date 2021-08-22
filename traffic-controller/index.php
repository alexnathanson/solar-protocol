<?php

//in the future this should be either a database or a seperate json file
$serverHash = [
  "SPfA" => "",
  "Hells Gate" => "",
  "Tega" => "",
  "Dominica" => "",
  "Chile" => "",
  "Caddie" => "",
  "Low Carbon Methods" => ""
];

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  //check if key is correct
  verifyPW($_POST["api_key"],$_POST["ip"]);
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

}

?>