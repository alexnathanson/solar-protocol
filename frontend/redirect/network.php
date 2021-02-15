<?php

$deviceInfoFile = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";
//Get device
$deviceInfo = json_decode(getFile($deviceInfoFile), true);

$listNetwork = true;


$default_socket_timeout = ini_get('default_socket_timeout');
//echo $default_socket_timeout;
ini_set('default_socket_timeout', 1);


if ($_SERVER["REQUEST_METHOD"] == "GET") {
	if(isset($_GET['steward'])){

		//remove leading or trailing slashes
		$_GET['steward'] = str_replace("/","", $_GET['steward']);
		//lower cases
		$_GET['steward'] = strtolower($_GET['steward']);

		$localURL ="";

		foreach ($deviceInfo as $key => $value) {
			if(formatURL($value['name'])==$_GET['steward']){
				$localURL = "http://" . $value['ip'] . "/local";
				$listNetwork = false;
			}
		}

		if($listNetwork == false){
			//header("Location: $localURL");

			if(isset($_GET['path']) && $_GET['path'] != ""){

				//set image mime type
				$imgTypes = ["jpg","jpeg","gif","png"];
				foreach ($imgTypes as $type) {
					if(strpos($_GET['path'], $type) !== false){
						header("content-type: image/".$type);
					}
				}
			
				//routes non-root file paths
				$localURL .= "/" . $_GET['path'];
			}

			//get request - error reporting supressed with the @ - remove it to see the error messages
			$redirected = @file_get_contents($localURL);

			if($redirected){
				/*echo str_replace(
			   '<head>', 
			   '<head><base href="http://solarprotocol.net/network/'.$_GET['steward'].'/">',
			    $redirected);*/

			    //replace url
			    $redirected = str_replace(
			   '<head>', 
			   '<head><base href="http://solarprotocol.net/network/'.$_GET['steward'].'/">',
			    $redirected);

			    //add banner
				$redirected = str_replace(
				   "<body>", 
				   "<body><div style='padding: 10px;border: 2px solid black;background-color:yellow'><h1><a href='/''>Solar Protocol</a> - An Intermittent Network</h1></div>",
				    $redirected
				);

			    echo $redirected;

			} else {
				echo 'Message: Request failed'; //.$e->getMessage();
				$listNetwork = true;
			}
			
			str_replace(
			   "<body>", 
			   "<body><div style='padding: 10px;border: 2px solid black;margin-top: 10px;margin-bottom: 10px;'><h1><a href='/''>Solar Protocol</a> - Network Sites</h1></div>",
			    $redirected
			);		
		}
	}
}

if($listNetwork == true){
	listNetworkSites();
}

function listNetworkSites(){
	global $deviceInfo;

	$newString = "";
	/*$newString .= "<!DOCTYPE html><html><head><title>Solar Server</title></head><body><div style='padding: 10px;border: 2px solid black;margin-top: 10px;margin-bottom: 10px;'><h1><a href='/''>Solar Protocol</a> - Network Sites</h1></div>";*/

	foreach ($deviceInfo as $key => $value) {

		//echo "<br>".file_get_contents('http://' . $value['ip'] . "/api/v1/api.php?value=PV-voltage");

		//add a try section to check that the site is online

		//add new link
		$newString .= "<div style='padding: 10px;border: 2px solid black;margin-top: 10px;margin-bottom: 10px;'>";
		$newString .= "<h3>" . $value['name'] . "</h3>";

		$newString .= "<p>Status:";
		if(@checkStatus($value['ip'])){
			$newString .= " online</p>";
		} else {
			$newString .= " offline</p>";
		}

		$newString .= "Last check-in: " . date('r', $value['time stamp']);
		
		if(isset($value['description'])){
			$newString .= "<p>About this site: " .$value['description'] . "</p>"; 
		}

		$newString .= "<p><a href='http://solarprotocol.net/network/". formatURL($value['name']) . "' target='_blank'>http://solarprotocol.net/network/".formatURL($value['name'])."</a></p>";
		$newString .= "</div>";

		//var_dump($value);
	}

	$networkTemplate = file_get_contents("/home/pi/solar-protocol/frontend/network.html");

	echo $networkTemplate;

	$networkTemplate = str_replace(
				   "<div class=network-overview>", 
				   "<div class=network-overview>" . $newString,
				    $networkTemplate
				);

	$networkTemplate = str_replace(
				   'href="style-small.css"', 
				   'href="/style-small.css"',
				    $networkTemplate
				);

	$networkTemplate = str_replace(
				   'href="style-large.css"', 
				   'href="/style-large.css"',
				    $networkTemplate
				);
	    

}

function checkStatus($checkIP){
	$s = false;
	
	if(file_get_contents("http://".$checkIP."/api/v1/api.php?value=PV-voltage")){
		$s = true;
	}
	return $s;
}

function formatURL($srcString){

	$srcString = strtolower($srcString);
	return preg_replace('/[^a-zA-Z0-9-_\.]/','', $srcString);
}
	
function getFile($fileName){
  //echo $fileName;
  try{
    return file_get_contents($fileName);
  }
  catch(Exception $e) {
    echo $fileName;
    return FALSE;
  }
}

?>