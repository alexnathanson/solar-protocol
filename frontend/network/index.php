<!DOCTYPE html>
<html>

<head>
</head>
<body>
	<?php

		$deviceInfoFile = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";
		//Get device
		$deviceInfo = json_decode(getFile($deviceInfoFile), true);

		var_dump($deviceList);

		//make list of link
	?>
</body>
</html>