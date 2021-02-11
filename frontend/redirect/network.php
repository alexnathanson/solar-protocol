<?php

$deviceInfoFile = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";
//Get device
$deviceInfo = json_decode(getFile($deviceInfoFile), true);

$listNetwork = true;

if ($_SERVER["REQUEST_METHOD"] == "GET") {
	if(isset($_GET['steward'])){

		//remove leading or trailing slashes
		$_GET['steward'] = str_replace("/","", $_GET['steward']);
		
		$localURL ="";

		foreach ($deviceInfo as $key => $value) {
			if(formatURL($value['name'])==$_GET['steward']){
				$localURL = "http://" . $value['ip'] . "/local";
				$listNetwork = false;
			}
		}

		if($listNetwork == false){
		  echo file_get_contents($localURL);
		}
	}
}

if($listNetwork == true){
	listNetworkSites();
}

function listNetworkSites(){
	global $deviceInfo;

	foreach ($deviceInfo as $key => $value) {

		#echo "<br>".file_get_contents('http://' . $value['ip'] . "/api/v1/api.php?value=PV-voltage");

		//add a try section to check that the site is online

		//add new link
		echo "<div style='padding: 10px;border: 2px solid black;margin-top: 10px;margin-bottom: 10px;'>";
		echo "<h3>" . $value['name'] . "</h3>";

		if(isset($value['description'])){
			echo "About this site: " .$value['description'] . "<br>"; 
		}

		echo "<a href='http://solarprotocol.net/network/". formatURL($value['name']) . "' target='_blank'>http://solarprotocol.net/network/".formatURL($value['name'])."</a>";
		echo "</div>";

		//var_dump($value);
	}
}

function formatURL($srcString){
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