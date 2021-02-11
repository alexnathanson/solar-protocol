<?php

$deviceInfoFile = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";
//Get device
$deviceInfo = json_decode(getFile($deviceInfoFile), true);

$listNetwork = true;

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

			$redirected = file_get_contents($localURL);
			/*echo str_replace(
			   '<head>', 
			   '<head><base href="'. $localURL.'/" target="_blank">',
			    $redirected
			);*/

				/*$image = JURI::base().DS.'files'.DS.'images'.DS.'icon.png';
				$imginfo = getimagesize($image);
				header("Content-type: ".$imginfo['mime']);
				echo($image);*/
			
			echo str_replace(
		   '<head>', 
		   '<head><base href="http://solarprotocol.net/network/'.$_GET['steward'].'/">',
		    $redirected);
			//}
			
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