<?php

// this should be a dictionary of hashes tied to the server names for reference
$serverHash = [];

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  //check if key is correct
  verifyPW($api_key)
}

function verifyPW($pw, $hash){

# hash generated from password_hash() more info at https://www.php.net/manual/en/function.password-hash.php

#loop through all hashes...
  if(password_verify($pw, $hash)){
    updateIP();
  }
  return false;
}

//makes the API call to the DNS registry to update it
function updateIP(){

}

?>