<!DOCTYPE html>
<html>

<head>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<title>Solar Server</title>

</head>

<body>

<h1>Solar Protocol - Admin Console</h1>

<div id="server list"><h2>Servers:</h2></div>

<script>
  //make this dynamic at some point
  let tempIPList = ["74.73.93.241","67.85.62.144","108.29.41.133"];
  
  //get the most recent line of charge controller data
  let toGet = "0";

  for (let i = 0; i < tempIPList.length; i++){
    //pingServer(tempIPList[i], populate);
    makeGet(tempIPList[i], toGet, populate);
  }

  function makeGet(dst, getThis, callback) {
    let requestURL = "http://" + dst + "/api/v1/api.php?line="+getThis;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        callback(this.responseText, dst);
      } else if (this.readyState == 4) {
        callback(this.statusText, dst);
      }
    };
    xhttp.open("GET", requestURL, true);
    xhttp.send();
  }

  function populate(dataToDisplay, dst) {

    const sList = document.getElementById('server list');

    //server header
    const serverH3 = document.createElement('h3');
    serverH3.textContent = 'Server: ';
    //make it a link
    const serverLink = document.createElement('a');
    serverLink.href = "http://"+dst;
    serverLink.target = "_blank"; //open in new tab

    const serverLinkContent = document.createTextNode(dst);
    serverLink.appendChild(serverLinkContent);

    serverH3.appendChild(serverLink);
    //server info
    const serverInfo = document.createElement('p');

    let displayThis = toJSON(dataToDisplay);

    if(displayThis != false){
      serverInfo.textContent =  JSON.stringify(displayThis);//put this into a table in the future
    } else {
      serverInfo.textContent =  "no response or invalid format";
    }


    serverH3.appendChild(serverInfo);
    sList.appendChild(serverH3);
  }

  function addActions(){
    //ping the servers
  }

  //check data is formatted correctly
  function toJSON(aString){
    //check that it can be converted to JSON

    try{
      let newJSON = JSON.parse(aString);
      
      console.log(newJSON);
      return newJSON;
    } catch (e){
      console.log(aString);
      return false;
    }
  }
</script>

<?php

//get the query string
$date = htmlspecialchars($_GET["date"]);

$fileDate = date("Y-m-d");
if ($date == 'yesterday'){
	$fileDate = date("Y-m-") . (date(d)-1);
}elseif( $date == 'before'){
	$fileDate = date("Y-m-") . (date(d)-2);//make a conditional to account for single digit days!!!
}

//variables
$fileName = "/home/pi/solar-protocol/charge-controller/data/tracerData" . $fileDate . ".csv";
$rawDataArray = [];

echo "<h2>PV Data:</h2>";

echo "<p>View: <a href='/admin/?date=today' id='today'>Today</a> | <a href='/admin/?date=yesterday' id='yesterday'>Yesterday</a> | <a href='/admin/?date=before' id='daybefore'>The Day Before</a></p>";
echo "<h3>File Name:</h3>". $fileName . "<br>";

// current directory
//echo getcwd() . "\n";

// Open the file for reading (from https://phpenthusiast.com/blog/parse-csv-with-php)
if (($h = fopen("{$fileName}", "r")) !== FALSE) 
{
  // Each line in the file is converted into an individual array that we call $data
  // The items of the array are comma separated
  while (($data = fgetcsv($h, 1000, ",")) !== FALSE) 
  {
    // Each individual array is being pushed into the nested array
    $rawDataArray[] = $data;		
  }

  // Close the file
  fclose($h);
}

/*
// Display the code in a readable format
echo "<pre>";
var_dump($rawDataArray);
echo "</pre>";
*/

echo "<h4>Most Recent Data:</h4>";
$buildNow = '<table border=1px>';
//foreach($rawDataArray as $row)

//header
{
$buildNow .= '<tr>';
foreach($rawDataArray[0] as $item)  
{
$buildNow .= "<td>{$item}</td>";
}
$buildNow .= '</tr>';
}

//most recent data
$dataCount = count($rawDataArray);
$nowRow = $rawDataArray[$dataCount-1];

{
$buildNow .= '<tr>';
foreach($nowRow as $item)
{
$buildNow .= "<td>{$item}</td>";
}
$buildNow .= '</tr>';
}
$buildNow .= '</table>';
echo $buildNow;

?>

<script type="text/javascript">
	google.charts.load('current', {'packages':['corechart', 'line']});
	google.charts.setOnLoadCallback(drawChart);

	var phpData = <?php echo json_encode($rawDataArray) ?>;

	//remove the time column from the end
	for (var p =0; p <phpData.length; p++){
		phpData[p].pop();
	}
      
	Array.prototype.clone = function() {
		return JSON.parse(JSON.stringify(this)); //deep copy

	};

//PV DATA

//add date column to front
	var pvData = cleanData(phpData.clone(), "date");

	//remember this happens AFTER the columns are shuffled around!
	for (var sp = 0; sp < pvData.length;sp++){
		//pvData[sp].splice(1,3);//remove columns
		pvData[sp].splice(5);//remove colums
	}
	
	console.log(pvData);

//BAT DATA
	//var batData = phpData.slice(4,6);

	var batData = cleanData(phpData.clone(), "date");

  console.log(batData);
	//remember this happens AFTER the columns are shuffled around!
	for (var sp = 0; sp < batData.length;sp++){
		batData[sp].splice(1,4);//remove columns
		batData[sp].splice(4,7);//remove colums
	}
	console.log(batData);

  let percentPosition = batData[0].length - 1;
	//scale bat percentage to 0-100
	for (var bper = 1; bper < batData.length; bper++){
		batData[bper][percentPosition] *= 100.0;
	}

//LOAD DATA
	//var loadData = phpData.slice(9);//if only 1 element it goes to the end
	var loadData = cleanData(phpData.clone(), "date");

	//remember this happens AFTER the columns are shuffled around!
	for (var sp = 0; sp < loadData.length;sp++){
		loadData[sp].splice(1,8);//remove columns
		loadData[sp].splice(5);//remove colums
	}  

//moves date column to front to be used as X data on graphs
      function cleanData(tempData, stringForX){

      	console.log(tempData[0]) //print headers

      	//Set X axis
      	var useAsX = 0;
      	//find string in first row
      	for (var getX = 0; getX < tempData[0].length; getX++){
      		if (tempData[0][getX] == stringForX){
      			useAsX = getX;
      			console.log(stringForX + " " + useAsX);
      			break;
      		}
      	}
		//go through each row
      	for (var i = 0; i < tempData.length; i++) {
      	//send the first column to the back until the selected column is first
	      	for (var c=0; c < useAsX;c++){
			 	tempData[i][tempData[i].length-1] = tempData[i].shift();
	      		}
		}

      //make floats, exclude header and X-axis
      for (var i = 1; i < tempData.length; i++) {
      	for (var c=1; c < tempData[i].length;c++){
		 	tempData[i][c] = parseFloat(tempData[i][c]);
      		}
		}

      //console.log(tempData);

      return tempData;
      }

      function drawChart() {
        var PVdataMap = google.visualization.arrayToDataTable(pvData);
        var BATdataMap = google.visualization.arrayToDataTable(batData);
        var LOADdataMap = google.visualization.arrayToDataTable(loadData);

        //console.log(data);

        var PVoptions = {
          title: 'PV',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 1500,
        	height: 500
        };

        var BAToptions = {
          title: 'Battery',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 1500,
        	height: 500
        };

        var LOADoptions = {
          title: 'Load',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 1500,
        	height: 500
        };

        var PVchart = new google.visualization.LineChart(document.getElementById('PV_chart'));

        PVchart.draw(PVdataMap, PVoptions);

        var BATchart = new google.visualization.LineChart(document.getElementById('BAT_chart'));

        BATchart.draw(BATdataMap, BAToptions);

        var LOADchart = new google.visualization.LineChart(document.getElementById('LOAD_chart'));

        LOADchart.draw(LOADdataMap, LOADoptions);
    }

    
</script>

<div id="PV_chart" style="width: 1500px; height: 500px"></div>
<div id="BAT_chart" style="width: 1500px; height: 500px"></div>
<div id="LOAD_chart" style="width: 1500px; height: 500px"></div>

<?php
//also from https://phpenthusiast.com/blog/parse-csv-with-php
$build = '<table border=1px>';
foreach($rawDataArray as $row)
{
$build .= '<tr>';
foreach($row as $item)
{
$build .= "<td>{$item}</td>";
}
$build .= '</tr>';
}
$build .= '</table>';
echo $build;
?>

</body>
</html>