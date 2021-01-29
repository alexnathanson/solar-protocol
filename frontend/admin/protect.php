<?php
# based on : https://gist.github.com/4692807
namespace Protect;

# Will protect a page with a simple password.
# The optional scope allows access on one page to
# grant access on another page. If not specified then it only grants
# access to the current page.
# The user will only need to input the password once. After that their session will be enough
# to get them in. 

function with($form, $scope=null) {
  if( !$scope ) $scope = current_url();
  $session_key = 'password_protect_'.preg_replace('/\W+/', '_', $scope);

  session_start();

  # Check the POST for access
  if( isset($_POST['password']) && isset($_POST['username']) && verifyPW(retrieveHash($_POST['username']))) {
    $_SESSION[$session_key] = true;
    redirect(current_url());
    #return;
  }

  # If user has access then simply return so original page can render.
  if( isset($_SESSION[$session_key]) && $_SESSION[$session_key] ) return;

  require $form;
  exit;
}

function retrieveHash($un){
  //echo $fileName;
  $fileName = '/home/pi/local/access.json';

  try{
    $f = json_decode(file_get_contents($fileName),true);
    return $f['users'][$un];
  }
  catch(Exception $e) {
    echo $fileName;
    return FALSE;
  }
}

function verifyPW($hash){

# hash generated from password_hash() more info at https://www.php.net/manual/en/function.password-hash.php

  if(password_verify($_POST['password'], $hash)){
    return true;
  }
  return false;
}

#### PRIVATE ####

function current_url($script_only=false) {
  $protocol = 'http';
  $port = ':'.$_SERVER["SERVER_PORT"];
  if(isset($_SERVER["HTTPS"]) && $_SERVER["HTTPS"] == 'on') $protocol .= 's';
  if($protocol == 'http' && $port == ':80') $port = '';
  if($protocol == 'https' && $port == ':443') $port = '';
  $path = $script_only ? $_SERVER['SCRIPT_NAME'] : $_SERVER['REQUEST_URI'];
  return "$protocol://$_SERVER[SERVER_NAME]$port$path";
}

function redirect($url) {
  header("Location: $url");
  exit;
}