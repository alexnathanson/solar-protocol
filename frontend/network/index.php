<?php

	$deviceInfoFile = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";
	//Get device
	$deviceInfo = json_decode(getFile($deviceInfoFile), true);

	foreach ($deviceInfo as $key => $value) {

		#echo "<br>".file_get_contents('http://' . $value['ip'] . "/api/v1/api.php?value=PV-voltage");

		//add a try section to check that the site is online
		
		//add new link
		echo "<div style='padding: 10px;border: 2px solid black;margin-top: 10px;margin-bottom: 10px;'>"
		echo "<h3>" . $value['name'] . "</h3>";
		echo "About this site: " .$value['description']; 
		echo "<br><a href='http://". $value['ip'] . "/local' target='_blank'>".$value['ip']."</a>";
		echo "</div>";

		//var_dump($value);
	}

	//make list of link

	
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


<!DOCTYPE html>
<html>

<head>
</head>
<body>

</body>
</html>