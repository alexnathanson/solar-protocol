<?php
	if ($_SERVER["REQUEST_METHOD"] == "GET") {

	  //this sets the timeout for the API calls
	  $streamContext = stream_context_create(
	    array('http'=>
	      array(
	          //120 seconds
	          'timeout' => 120
	      )
	    )
	  );

		$apiVals = '';

		foreach(array_keys($_GET) as $gK){
			if((isset($_GET[$gK]) && !empty($_GET[$gK])) || $_GET[$gK] == '0'){
				if($apiVals != ''){
					$apiVals = $apiVals . "&";
				}

			$apiVals = $apiVals . $gK . "=" . $_GET[$gK];
			}
		}

		//$_SERVER[SERVER_PORT] might need to be used as well for irregular ports
		$apiCall = 'http://' . $_SERVER["SERVER_NAME"] . '/api/v2/opendata.php?' . $apiVals;
		$localApiCall = 'http://localhost/api/v2/opendata.php?' . $apiVals;
		$apiResponse = file_get_contents($localApiCall, false, $streamContext);

	}
?>

 <!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<title>Open API Documentation</title>
</head>
<body>

<h1>Solar Protocol - Open API:V2 Documentation</h1>
<p>
	This server is: <?php echo file_get_contents('http://localhost/api/v2/opendata.php?systemInfo=name', false)?>
</p>

<p>
	Note: This is the publicly available open-access API. Developers on the network can view the complete API documentation on <a href="https://github.com/alexnathanson/solar-protocol/blob/master/API.md" target="_blank">Github</a>.
</p>

<p>
	Solar Protocol is a network of servers located all over the world. The primary server, which we call the "point of entry" or "POE", is determined by whichever server is in the most sunlight at a given time (determined by wattage scaled to a 50 watt module). The data returned from these GET requests pertains to the POE server only (calls to other servers in the system are explained below). This means that every call you make to the API might get a response from a different device with different values of data.
</p>

There are 2 main types of data this API provides:
<ol>
	<li>Charge controller data - This pertains to the PV system, such as solar power production, battery status, etc.</li>
	<li>System information - This pertains to local server info, such as location and hardware specs.</li>
</ol>
By default, these results are queried from the POE, which means the results may change if the POE changes. By using the server argument you can collect data from a specific server or from all the servers in the network. In this API explorer, the results from these API calls are displayed in the browser console. All times are in the timezone for the server that logged that data and have not been adjusted. Use the networkInfo = tz call to get the time zones to make the adjustments.

<h3>Using this API explorer</h3>
Enter the value you want return in the form provided. The syntax for the call will be show in the browser bar and the results of the call will open up in the browser console. The console can be opened via the browser's developer settings or by pression the Fn and F12 keys simultaniously (works on most browsers).

<h2>Charge Controller Data</h2>

Charge controller data:
<ul>
		<li>value: Individual pieces of data i.e. a single value like PV wattage or battery percentage.</li>
		<li>value & duration: Individual pieces of data over a particular length of time.</li>
		<li>line: Individual lines or a range of lines of data. Each line contains all the possible values for a particular time.</li>
		<li>day: An entire calendar day's worth of lines i.e. all the data collected on a particular date.</li>
	</ul>

<h3>Value</h3>
<strong>value</strong> returns the specified value from the most recently collected line of data.
<p>Example: <a href="http://solarprotocol.net/api/v2/opendata.php?value=PV-voltage" target="_blank">http://solarprotocol.net/api/v2/opendata.php?value=PV-voltage</a></p>
<p>Possible values:
	<ul>
		<li>PV-current</li>
		<li>PV-current</li>
		<li>PV-power-H</li>
		<li>PV-power-L</li>
		<li>PV-voltage</li>
		<li>battery-percentage</li>
		<li>battery-voltage</li>
		<li>charge-current</li>
		<li>charge-power-H</li>
		<li>charge-power-L</li>
		<li>load-current</li>
		<li>load-power</li>
		<li>load-voltage</li>
		<li>datetime</li>
		<li>scaled-wattage</li>
	</ul>
</p>
Optional modifier: <strong>duration</strong> returns the specified value over a given amount of days, from 1 to 7.
<p>
Example: <a href="http://solarprotocol.net/api/v2/opendata.php?value=PV-voltage&duration=2" target="_blank">http://solarprotocol.net/api/v2/opendata.php?value=PV-voltage&duration=2</a>
</p>

<form method="GET">
  <p>Value <input type="text" name="value"></p>
  <p>Duration (optional) <input type="text" name="duration"></p>
  <button type="submit">Get Value</button>
</form>

<h3>Line</h3>

<strong>line</strong> returns a line of data containing all of the possible values from the most recent file
<p>Example: <a href="http://solarprotocol.net/api/v2/opendata.php?line=0" target="_blank">http://solarprotocol.net/api/v2/opendata.php?line=0</a></p>
<p>Possible values:
	<ul>
		<li>len - returns the number of rows in the file</li>
		<li>head - returns the column headers</li>
		<li>[an integer from 0 through number if rows-1] - returns the specified line of data from the most recent day of data collected. For example, 0 will return the most recent row of data, 1 will return the 2nd most recent row, etc.</li>
	</ul>
</p>
<form method="GET">
  <p>Line <input type="text" name="line"></p>
  <button type="submit">Get Line</button>
</form>

<h3>Day</h3>

<strong>day</strong> returns all the data from a specific day or range of days. Note that days may not be consequetive if the server was off for an extended period of time.
<p>Example: <a href="http://solarprotocol.net/api/v2/opendata.php?day=2" target="_blank">http://solarprotocol.net/api/v2/opendata.php?day=2</a></p>
<p>Possible values:
	<ul>
		<li>[an integer from 1-7] - returns the most recent X number of days of data. 1 returns the most recent day of data, 2 returns the most recent days of data, etc.</li>
		<li>list - Returns a list of all the available files. Each file represents 1 day of data.</li>
		<li>len - Return count of all available files. Each file represents 1 day of data.</li>
		<li>[file name without file type suffix] - Returns all the data from that particular day. Example: <a href="http://solarprotocol.net/api/v2/opendata.php?day=tracerData2020-05-17" target="_blank">http://solarprotocol.net/api/v2/chargecontroller.php?day=tracerData2020-05-17</a></li>
	</ul>
</p>

<form method="GET">
 <p>Day <input type="text" name="day"></p>
  <p></p>
  <button type="submit">Get Day</button>
</form>

<h2>System Info</h2>

<strong>systemInfo</strong> returns information about the system and that server's local variables
<p>Example: <a href="http://solarprotocol.net/api/v2/opendata.php?systemInfo=tz" target="_blank">http://solarprotocol.net/api/v2/opendata.php?systemInfo=tz</a></p>
<p>Possible values:
	<ul>
		<li>tz - returns the timezone for the server</li>
		<li>color - returns the color that was set by the steward</li>
		<li>description - returns the description of the server that was set by the steward</li>
		<li>name - returns the name for the server</li>
		<li>location - returns the location</li>
		<li>city - returns the city the server is located in</li>
		<li>country - returns the country the server is located in</li>
		<li>wattage-scaler -returns the scaler value based on a standard of a 50 watt module</li>
		<li>pvWatts -returns the wattage of the module</li>
		<li>pvVoltage - returns the voltage of the module</li>
		<li>dump - returns a dictionary containing all of the above system info</li>
	</ul>
</p>

<form method="GET">
 <p>System Info <input type="text" name="systemInfo"></p>
  <p></p>
  <button type="submit">Get System Info</button>
</form>


<h2>Network Info</h2>

<strong>networkInfo</strong> returns information about the network
<p>Example: <a href="http://solarprotocol.net/api/v2/opendata.php?networkInfo=devices" target="_blank">http://solarprotocol.net/api/v2/opendata.php?networkInfo=devices</a></p>
<p>Possible values:
	<ul>
		<li>deviceList - returns a list of the names of servers</li>
		<li>tz - returns a list of the timezones of each server. This is the prefered way to get all the timezones (rather than making a tz call via the server argument)</li>
		<li>poe - returns the list of point of entry time stamps by server. note that these time stamps are in the local time of their server and haven't been adjusted.</li>
		<li>timestamp - returns the time stamp from when the devices most recently posted their data. Note that this time stamp is in Unix time - seconds since epoch (1/1/1970) in UTC regardless of the server's timezone.</li>
		<li>dump - returns an array containing all network info values</li>
	</ul>
</p>

<form method="GET">
 <p>Network Info <input type="text" name="networkInfo"></p>
  <p></p>
  <button type="submit">Get Network Info</button>
</form>

<h2>Remote Server Data</h2>

<strong>server</strong> returns 4 calendar days worth of data from the specified server.
<p>Example: <a href="http://solarprotocol.net/api/v2/opendata.php?server=1" target="_blank">http://solarprotocol.net/api/v2/opendata.php?server=1</a></p>
<p>Possible values:
	<ul>
		<li>all - returns the specified value for all servers</li>
		<li>an integer - the integer corresponds to the order of servers returned from the device list query. The call returns the specified value for the specified server</li>
		<li>server name without spaces - the name of the server (as listed in the deviceList query) with spaces removed. The call returns the specified value for the specified server. This is not case sensitive.</li>
		<li>If 'err' is returned it indicates a failed response, likely because the remote data for that server isn't stored locally. <!-- The default timeout is 60 seconds, but the timeout for these server calls is 15 seconds. (The max time a call to 'all' should take is 15 seconds * number of servers. If false is return, it means the cumulative call time exceeded 120 seconds (the maximum time allowed). --></li>
	</ul>

</p>

<form method="GET">
	<p>Server <input type="text" name="server"></p>
<!-- 	Pick 1 of the below fields. See above for possible values:
  <p>Value <input type="text" name="value"> Duration (optional) <input type="text" name="duration"></p>
  <p>Line <input type="text" name="line"></p>
	<p>Day <input type="text" name="day"></p>
 	<p>System Info <input type="text" name="systemInfo"></p>
 	<p>Network Info <input type="text" name="networkInfo"></p> -->

  <p></p>
  <button type="submit">Get remote server data</button>
</form>

<h1>API Response</h1>
<h2>API call:</h2>
	<a href="<?php echo $apiCall; ?>" target="_blank"><?php echo $apiCall; ?></a>
<h2> API response (also available in browser console):</h2>
	<?php echo $apiResponse; ?>
	<script> console.log(<?php echo $apiResponse; ?>)</script>

<!-- <p>
Simple client side Python and JS examples are available in the <a href="https://github.com/alexnathanson/solar-protocol/tree/master/utilities/apiv2-examples" target="_blank">Solar Protocol repository</a>.
</p> -->

</body>
</html> 