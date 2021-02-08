<?php
# based on : https://gist.github.com/4692807
namespace Protect;

# Will protect a page with a simple password.
# The optional scope allows access on one page to
# grant access on another page. If not specified then it only grants
# access to the current page.
# The user will only need to input the password once. After that their session will be enough
# to get them in. 

$sUsername = $sPassword = $accessLevel = "";

function with($form, $scope=null) {
  if( !$scope ) $scope = current_url();
  $session_key = 'password_protect_'.preg_replace('/\W+/', '_', $scope);

  session_start();

  if(isset($_POST['username']) && isset($_POST['password'])){

    //sanitize input
    $sUsername = sanitize_input($_POST['username']);
    $sPassword = sanitize_input($_POST['password']);

  # Check the POST for access
    if(verifyPW($sPassword,retrieveUserInfo($sUsername))) {

      $_SESSION[$session_key] = true;
      $_SESSION["username"] = $sUsername;
      $_SESSION["accessLevel"] = $accessLevel;

      redirect(current_url());
      #return;
    }
  }


  if(isset($_GET["logout"])){// if user is currently logged in and is trying to log out
    logout();
  } else if( isset($_SESSION[$session_key]) && $_SESSION[$session_key] ){
    # If user has access then simply return so original page can render.
    return;
  } else {
  require $form;
  }

  exit;
}

function retrieveUserInfo($un){
  $fileName = '/home/pi/local/access.json';

  try{
    $f = json_decode(file_get_contents($fileName),true);
    if(isset($f['users'][$un]['hash']) && isset($f['users'][$un]['access'])){
      $accessLevel = $f['users'][$un]['access'];
      return $f['users'][$un]['hash'];
    } else {
      return FALSE;
    }
  }
  catch(Exception $e) {
    //echo $fileName;
    return FALSE;
  }
}

function verifyPW($pw, $hash){

# hash generated from password_hash() more info at https://www.php.net/manual/en/function.password-hash.php

  if(password_verify($pw, $hash)){
    return true;
  }
  return false;
}

function logout(){
  // remove all session variables
  session_unset();

  // destroy the session
  session_destroy(); 

  $redirect = str_replace("?logout","",$_SERVER['REQUEST_URI']);
  header("Location: " . $redirect);
}

function sanitize_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
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