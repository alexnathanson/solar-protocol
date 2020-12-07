<?php
# based on: https://gist.github.com/4692807
namespace Protect;

# Will protect a page with a simple password.
# The optional scope allows access on one page to
# grant access on another page. If not specified then it only grants
# access to the current page.
# The user will only need to input the password once. After that their session will be enough
# to get them in. 

function with($form, $password, $scope=null) {
  if( !$scope ) $scope = current_url();
  $session_key = 'password_protect_'.preg_replace('/\W+/', '_', $scope);

  session_start();

  # Check the POST for access
  if( isset($_POST['password']) && $_POST['password'] == $password ) {
    $_SESSION[$session_key] = true;
    redirect(current_url());
    #return;
  }

  # If user has access then simply return so original page can render.
  if( isset($_SESSION[$session_key]) && $_SESSION[$session_key] ) return;

  require $form;
  exit;
}

#### PRIVATE ####

function current_url($script_only=false) {
  echo "CURRENT URL";
  $protocol = 'http';
  $port = ':'.$_SERVER["SERVER_PORT"];
  if(isset($_SERVER["HTTPS"]) && $_SERVER["HTTPS"] == 'on') $protocol .= 's';
  if($protocol == 'http' && $port == ':80') $port = '';
  if($protocol == 'https' && $port == ':443') $port = '';
  $path = $script_only ? $_SERVER['SCRIPT_NAME'] : $_SERVER['REQUEST_URI'];
  return "$protocol://$_SERVER[SERVER_NAME]$port$path";
}

function redirect($url) {
  echo "REDIRECT";
  header("Location: $url");
  exit;
}