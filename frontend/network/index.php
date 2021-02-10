<?php

	$deviceInfoFile = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";
	//Get device
	$deviceInfo = json_decode(getFile($deviceInfoFile), true);

	foreach ($deviceInfo as $key => $value) {
		echo "<br>".$value['ip'];

		echo "<br>".file_get_contents($value['ip'] . "/api/v1/api.php?value=PV-voltage");

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