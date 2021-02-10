<?php

	$deviceInfoFile = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";
	//Get device
	$deviceInfo = json_decode(getFile($deviceInfoFile), true);

	var_dump($deviceInfo);

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