<!DOCTYPE html>
<html>
<head>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.1.4/Chart.min.js"></script>
	<script type="text/javascript" src="js/json-graph.js?=1"></script>
	<title>Charge Controller Graph</title>
</head>
<body>

<?php 
// get files in directory
// https://www.php.net/manual/en/function.scandir.php
$directory = getcwd() . '/data';
$files = array_diff(scandir($directory), array('..', '.'));

// pass file to javascript (json-graph.js)
// if csv, convert it to json
foreach($files as $file){
	if (strpos($file, 'csv') !== false) {
		$json_from_csv = csvtojson($directory . "/" . $file, ",");

		// to read datatime correctly, replace space to T
		// e.g., "2020-05-15 14:00:30.089197" becomes "2020-05-15T14:00:30.089197" 
		$json_from_csv = preg_replace('/[[:space:]]+/', 'T', $json_from_csv);
		echo "<a id='$file' href='#$file' onclick=getcsv('$json_from_csv'); return false;>$file</a><br>";
	} else {
		// https://stackoverflow.com/questions/9702040/how-pass-reference-to-this-on-href-javascript-function
		echo "<a id='$file' href='#$file' onClick=getjson('$file'); return false;>$file</a><br>";
	}
}


// convert csv to json
// https://stackoverflow.com/questions/28118101/convert-csv-to-json-using-php
function csvtojson($file,$delimiter) {
    if (($handle = fopen($file, "r")) === false) {
        die("can't open the file.");
    }

    $csv_headers = fgetcsv($handle, 4000, $delimiter);
    $csv_json = array();

    while ($row = fgetcsv($handle, 4000, $delimiter)) {
        $csv_json[] = array_combine($csv_headers, $row);
    }

    fclose($handle);
    return json_encode($csv_json);
}

?>

<canvas id="voltageChart"></canvas>
<canvas id="currentChart"></canvas>
<canvas id="powerChart"></canvas>
<canvas id="batteryPercentage"></canvas>
<table id="dataTable" border=1 style="text-align: center;"></table>

</body>
</html>


