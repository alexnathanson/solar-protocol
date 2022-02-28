<?php

// This is for all public (non-password protected) data. Most of these functions previously lived in the chargecontroller.php script

//comment out these lines for production version
/*ini_set('display_errors', 1); 
ini_set('display_startup_errors', 1); 
error_reporting(E_ALL);*/

/**
 * in prior versions, not all systemInfo values were echoed as json
 * might need to be considered when changing cc.php to od.php
**/

$ccDir = "/home/pi/solar-protocol/charge-controller/data/";
$scaleIt = false;

$todayFile = $ccDir . "tracerData" . date("Y-m-d") . ".csv";
//$fileName = "/home/pi/solar-protocol/charge-controller/data/tracerData" . $fileDate . ".csv";

if ($_SERVER["REQUEST_METHOD"] == "GET") {

  //read the value of the query string, replace "-" with " "
  //var_dump($_GET);

  //most recent PV Data queries
  if(array_key_exists("value", $_GET)){
    //echo "Key = Value";

    //check if value queried exists
    if(!testValue($_GET["value"])){
      echo "Value not found. Acceptable values: PV-current, PV-current, PV-power-H,PV-power-L, PV-voltage, battery-percentage, battery-voltage, charge-current, charge-power-H, charge-power-L, load-current, load-power, load-voltage, datetime, scaled-wattage";
      exit;
    }

    $qValue = str_replace("-"," ",$_GET["value"]);

    if($qValue == "scaled wattage"){
      $qValue = "PV power L";
      $scaleIt = true;
    }

    if(array_key_exists("duration", $_GET) && intval($_GET["duration"]) != 0){
      //returns a given value over time
      $valueTimeSeries = [];

      //returns an array of all the file names in the charge controller data directory
      $dirArray = justTracerDataFiles($ccDir);

      //loop through each file name
      for ($f = 0; $f < intval($_GET["duration"]); $f++){
        if($f>= count($dirArray) || $f >= 7){
          break;
        }

        //get 1 file returned as array
        $tFile = chargeControllerData($ccDir . $dirArray[count($dirArray)-1-$f]);

        //determine the position of the requested value in the array
        $valuePosition = 0;

        //for each row
        foreach($tFile[0] as $k){
          if($k == $qValue){
            break;
          }
          $valuePosition++;
        }

        //scale the wattage if required
        if($qValue == 'PV-power-L' && $scaleIt == true){
          foreach(array_reverse($tFile) as $k => $l){
            if ($k == count($tFile) - 1){
              //skip row 0 which contains the headers
              continue;
            }
            $valueTimeSeries[$l[0]]=$l[$valuePosition] * wattageScaler();
            //array_push($valueTimeSeries, array($l[0] => $l[$valuePosition] * wattageScaler()));

          }
        } else { //unscaled wattage
          foreach(array_reverse($tFile) as $k => $l){
            if ($k == count($tFile) - 1){
              //skip row 0 which contains the headers
              continue;
            }
            $valueTimeSeries[$l[0]]=$l[$valuePosition];
            //array_push($valueTimeSeries, array($l[0] => $l[$valuePosition]));
          }
        }
         
      }

      $headerOutput = array(
        "datetime" => $_GET["value"]
      );

      $vDOutput = array(
        "header" => $headerOutput,
        "data" => $valueTimeSeries
      );

      echo json_encode($vDOutput);
    } else {
      $readData = chargeControllerData($todayFile);

      $outputVal = '';

      if ($readData != FALSE){    

        //loop through the header line to find the position of the requested value
        for ($v = 0; $v < sizeof($readData[0]);$v++){
          if($readData[0][$v]==$qValue){

            //scale wattage if required
            if($qValue == 'PV power L' && $scaleIt == true){
              $outputVal = $readData[count($readData)-1][$v] * wattageScaler();
            } else { //unscaled wattage
              $outputVal = $readData[count($readData)-1][$v];
            }
            break;
          }
        }
      }

      $vOutput = array(
        $_GET["value"] => $outputVal
      );

      echo json_encode($vOutput);
    }  
  }

  /**
   * get a line of data from the current day's file.
   * "len" returns length of current file,
   * "head" returns the column headers,
   * an integer returns the specified line. "0" returns most recent line. Increment up for other lines.
  * */

  else if (array_key_exists("line", $_GET)) {
    //echo "Key = Line";
    $readData = chargeControllerData($todayFile);

    if ($readData != FALSE){    
      
      if($_GET["line"] == "len"){//return the number of rows in the file
        $lOutput = array($_GET["line"] => (count($readData)-1));
      } else if($_GET["line"] == "head"){//return the CSV data headers

        $lOutput = array($_GET["line"] => $readData[0]);

      } else if ($_GET["line"] >= 0 && $_GET["line"] < count($readData)){
        //returns raw line
        //var_dump($readData[count($readData)-1-$_GET["line"]]);

        $returnArray = array();
        //package line with headers
        for ($p = 0; $p<count($readData[0]);$p++){

          $repKey = str_replace(" ","-",$readData[0][$p]);

          $returnArray[$repKey] = $readData[count($readData)-1-$_GET["line"]][$p];
          //array_push($returnArray, array($readData[0][$p] => $readData[count($readData)-1-$_GET["line"]][$p]));
        }  

        $lOutput = array(
          $_GET["line"] => $returnArray
        );
      }

      echo json_encode($lOutput);
    }
    

    //get a full file
  } else if (array_key_exists("day", $_GET)) {
    //echo "Key = File";

    if ($_GET["day"] == "list"){//list all charge controller data files

      echo json_encode(array($_GET["day"] =>justTracerDataFiles($ccDir)));

    } else if ($_GET["day"] == "len"){//list all charge controller data files
      echo json_encode(array($_GET["day"] =>count(justTracerDataFiles($ccDir))));

    } else if (intval($_GET["day"]) >= 1 && intval($_GET["day"]) <= 7){

      $multiDayData = [];
      $headerOutput = [];

      $dirArray = justTracerDataFiles($ccDir);
      for ($f = 0; $f < intval($_GET["day"]); $f++){
        if($f>= count($dirArray)){
          break;
        }

        $dData = chargeControllerData($ccDir . $dirArray[count($dirArray)-1-$f]);

        $allData = [];
        foreach(array_reverse($dData) as $k => $d){
          if ($k == count($dData) - 1){
            //skip row 0 which contains the headers
            $headerOutput = $d;
            //continue;
          } else {
            //$valueTimeSeries[$d[0]]=$l[$valuePosition];
            array_push($allData, $d);
          }
        }

        array_push($multiDayData, $allData);

      }

      $dayOutput = array(
        "header" => $headerOutput,
        "data" => $multiDayData
      );

      echo json_encode($dayOutput);

      //echo json_encode($multiDayData);

    } else if(strpos($_GET["day"],'tracerData') !== false){      //get CC data file by file name
      echo json_encode(chargeControllerData($ccDir . $_GET["day"] . '.csv'));
    }

    //this should be removed now that we can query the poe
    /*if($_GET["day"] == "deviceList"){
      $fileName = "/home/pi/solar-protocol/backend/data/deviceList.json";
      echo getFileContents($fileName);
    }*/

  } else if (array_key_exists("systemInfo", $_GET)) {
    //previously this wasn't encoded to json before output - might need to be considered when changing cc.php to od.php

    if ($_GET["systemInfo"] == "tz"){
      //get local time zone
      //echo date_default_timezone_get();
      echo json_encode(array($_GET["systemInfo"] =>date_default_timezone_get()), JSON_UNESCAPED_SLASHES);
    } else if ($_GET["systemInfo"] == "color"){
      //read local bgColor
      $fileContents = file_get_contents("/home/pi/local/local.json");
      //echo  json_decode($fileContents, true)['bgColor'];
      echo json_encode(array($_GET["systemInfo"] =>json_decode($fileContents, true)['bgColor']));
    } else if ($_GET["systemInfo"] == "description"){
      //read local description
      $fileContents = file_get_contents("/home/pi/local/local.json");
      //echo json_decode($fileContents, true)['description'];
      echo json_encode(array($_GET["systemInfo"] =>json_decode($fileContents, true)['description']));
    } else if ($_GET["systemInfo"] == "name"){
      //read local name
      $fileContents = file_get_contents("/home/pi/local/local.json");
      //echo json_decode($fileContents, true)['name'];
      echo json_encode(array($_GET["systemInfo"] =>json_decode($fileContents, true)['name']));
    } else if ($_GET["systemInfo"] == "location"){
      //read local location
      $fileContents = file_get_contents("/home/pi/local/local.json");
      //echo json_decode($fileContents, true)['location'];
      echo json_encode(array($_GET["systemInfo"] =>json_decode($fileContents, true)['location']));

    } else if ($_GET["systemInfo"] == "city"){
      //read local city
      $fileContents = file_get_contents("/home/pi/local/local.json");
      //echo json_decode($fileContents, true)['city'];
      echo json_encode(array($_GET["systemInfo"] =>json_decode($fileContents, true)['city']));
    } else if ($_GET["systemInfo"] == "country"){
      //read local country
      $fileContents = file_get_contents("/home/pi/local/local.json");
      //echo json_decode($fileContents, true)['country'];
      echo json_encode(array($_GET["systemInfo"] =>json_decode($fileContents, true)['country']));
    } else if ($_GET["systemInfo"] == "wattage-scaler"){
      //echo wattageScaler();
      echo json_encode(array($_GET["systemInfo"] =>wattageScaler()));
    } else if ($_GET["systemInfo"] == "pvWatts"){
      $fileContents = file_get_contents("/home/pi/local/local.json");
      //echo json_decode($fileContents, true)['pvWatts'];
      echo json_encode(array($_GET["systemInfo"] =>json_decode($fileContents, true)['pvWatts']));

    } else if ($_GET["systemInfo"] == "pvVoltage"){
      $fileContents = file_get_contents("/home/pi/local/local.json");
      //echo json_decode($fileContents, true)['pvVolts'];
      echo json_encode(array($_GET["systemInfo"] =>json_decode($fileContents, true)['pvVolts']));

    }  else if ($_GET["systemInfo"] == "dump"){
      //read local country
      $fileContents = file_get_contents("/home/pi/local/local.json");
      $infoArray = json_decode($fileContents, true);
      $infoDump = array(
        "timezone" => date_default_timezone_get(),
        "color" => $infoArray["bgColor"],
        "name" => $infoArray["name"],
        "description" => $infoArray["description"],
        "location" => $infoArray["location"],
        "city" => $infoArray["city"],
        "country" => $infoArray["country"],
        "wattage-scaler" => wattageScaler(),
        "pvWatts" => $infoArray["pvWatts"],
        "pvVolts" => $infoArray["pvVolts"]);
      echo json_encode(array($_GET["systemInfo"] =>$infoDump), JSON_UNESCAPED_SLASHES);

    }

  } else if (array_key_exists("networkInfo", $_GET)) {

    #return the list of names of all the servers stored locally
    if($_GET["networkInfo"] == "deviceList"){
  
      $output = [];

      $fileName = "/home/pi/solar-protocol/backend/data/deviceList.json";

      $contents = json_decode(file_get_contents($fileName),true);

      for ($d = 0; $d < count($contents);$d++){
        array_push($output,$contents[$d]["name"]);
      }
      //echo json_encode($output);
      echo json_encode(array($_GET["networkInfo"] =>$output));


    #return the list of time zones of all the servers stored locally
    } else if($_GET["networkInfo"] == "tz"){

        $output = [];

        $fileName = "/home/pi/solar-protocol/backend/data/deviceList.json";

        $contents = json_decode(file_get_contents($fileName),true);

        for ($d = 0; $d < count($contents);$d++){
          array_push($output,$contents[$d]["tz"]);
        }
        //echo json_encode($output);
        echo json_encode(array($_GET["networkInfo"] =>$output));


    #return the POE logs stored locally for all devices
    } else if($_GET["networkInfo"] == "poe"){
  
      $output = [];

      $fileName = "/home/pi/solar-protocol/backend/data/deviceList.json";

      $contents = json_decode(file_get_contents($fileName),true);

      for ($d = 0; $d < count($contents);$d++){
        array_push($output,$contents[$d]["log"]);
      }
      //echo json_encode($output);
      echo json_encode(array($_GET["networkInfo"] =>$output));

    #return the timestamp from when the device posted the data to the server
    } else if($_GET["networkInfo"] == "timestamp"){
  
      $output = [];

      $fileName = "/home/pi/solar-protocol/backend/data/deviceList.json";

      $contents = json_decode(file_get_contents($fileName),true);

      for ($d = 0; $d < count($contents);$d++){
        array_push($output,$contents[$d]["time stamp"]);
      }
      //echo json_encode($output);
      echo json_encode(array($_GET["networkInfo"] =>$output));

    } else if($_GET["networkInfo"] == "dump"){
  
      $fileName = "/home/pi/solar-protocol/backend/data/deviceList.json";
      $contents = json_decode(file_get_contents($fileName),true);

      $logDump = [];
      for ($d = 0; $d < count($contents);$d++){
        array_push($logDump,$contents[$d]["log"]);
      }

      $nameDump = [];
      for ($d = 0; $d < count($contents);$d++){
        array_push($nameDump,$contents[$d]["name"]);
      }

      $tzDump = [];
      for ($d = 0; $d < count($contents);$d++){
        array_push($tzDump,$contents[$d]["tz"]);
      }

      $tsDump = [];
      for ($d = 0; $d < count($contents);$d++){
        array_push($tsDump,$contents[$d]["time stamp"]);
      }

      $output = array(
        "name" => $nameDump,
        "poe" => $logDump,
        "tz" => $tzDump,
        "timestamp" => $tsDump);

      //echo json_encode($output, JSON_UNESCAPED_SLASHES);
      echo json_encode(array($_GET["networkInfo"] =>$output), JSON_UNESCAPED_SLASHES);

    }
  } else if(array_key_exists("server", $_GET)){
    getServerCCData();
  }
}

//check if the requested value exists
function testValue($v){

  $possibleValues = array('PV-current','PV-current','PV-power-H','PV-power-L','PV-voltage','battery-percentage','battery-voltage','charge-current','charge-power-H', 'charge-power-L','load-current','load-power','load-voltage','datetime','scaled-wattage');

  foreach($possibleValues as $aV){
    if($aV == $v){
      //$v = str_replace("-"," ",$v);
      return $v;
    }
  }
  return FALSE;
}

//returns an array of all the file names in the charge controller data directory
function justTracerDataFiles($dir){
    $dirArray = scandir($dir);//returns list of directory contents
    $dirFiles = [];
    for ($f = 0; $f < count($dirArray);$f++){
      if(strpos($dirArray[$f],'tracerData') !== false){
        array_push($dirFiles, $dirArray[$f]);
      }
    }

    return $dirFiles;
}

//converts a file of CC data to an array
function chargeControllerData($fileName){
    
  $rawDataArray = [];

  if (($h = fopen("{$fileName}", "r")) !== FALSE) {
    /** 
     * Each line in the file is converted into an individual array that we call $data
     * The items of the array are comma separated
    **/
    while (($data = fgetcsv($h, 1000, ",")) !== FALSE) 
    {
      // Each individual array is being pushed into the nested array
      $rawDataArray[] = $data;        
    }

    // Close the file
    fclose($h);

    return $rawDataArray;
  } else {
    return FALSE;
  }
}

function getFileContents($fileName){
  //echo $fileName;
  try{
    return file_get_contents($fileName);
  }
  catch(Exception $e) {
    echo $fileName;
    return FALSE;
  }
}

/**
 * this function returns a scaler value for the wattage of the module so all modules across the network can be compared.
 * a more advanced non-linear equation may need to be adopted in the future
**/
function wattageScaler(){
  //get local file
  $fileContents = file_get_contents("/home/pi/local/local.json");
  $localData = json_decode($fileContents, true);
  // Convert to array and get PV watts data
  if (array_key_exists('pvWatts', $localData)){
    $localPVwatts = $localData['pvWatts'];
    if($localPVwatts != ""){
      return 50.0 / $localPVwatts;
    }
  } else {
    return 1;
  }
}

/*
function getFile($fileName){
  //echo $fileName;
  try{
    return file($fileName);
  }
  catch(Exception $e) {
    echo $fileName;
    return FALSE;
  }
}*/


/**
 * in the future, it might be best to use cURL not file_get_contents
 * the php7.3-curl package doesn't work on Raspberry Pi for whatever reason
 * if using php8 at somepoint, try cURL,
 * because it allows for me granular control over the request, like timeouts and authentication
**/

function getServerCCData(){

    $fileName = "/home/pi/solar-protocol/backend/data/deviceList.json";

    //should this use the getFileCotnents function?
    $contents = json_decode(file_get_contents($fileName),true); //retrieve contents of the deviceList file
    $nameList = [];

    #loop through contents of device list and collect IP addresses
    for ($d = 0; $d < count($contents);$d++){
      $aName = strtolower(str_replace(' ', '', $contents[$d]["name"]));
      array_push($nameList,$aName);
    }

    $dataPath = "/home/pi/local/data/";
    //chargeControllerData($fileName);

    if (is_numeric($_GET["server"])){
      
      //echo file_get_contents($dataPath . strtolower(str_replace(' ', '', $nameList[$_GET["server"]])) . '.json');
      $output = json_decode(file_get_contents($dataPath . strtolower(str_replace(' ', '', $nameList[$_GET["server"]])) . '.json'));
      echo json_encode(array($_GET["server"] =>$output));
    } else if($_GET["server"] == "all"){

      $output = [];

      #retrieve all files
      for ($d = 0; $d < count($nameList);$d++){
        //error_log('API destination: http://' . $ipList[$d] . $endPoint, 0);

        $resp = file_get_contents($dataPath . strtolower(str_replace(' ', '', $nameList[$d])) . '.json');

        if($resp != null){
          error_log('JSON_DECODE not NULL');
          $resp = json_decode($resp);
        } else {
          $resp = 'err';
        }

        $output[$nameList[$d]] = $resp;

        //array_push($output, $resp);
        
      }

      //echo json_encode($output);
      echo json_encode(array($_GET["server"] =>$output));

    } else {
      //echo file_get_contents($dataPath . strtolower(str_replace(' ', '', $_GET["server"])) . '.json' );
      $output = json_decode(file_get_contents($dataPath . strtolower(str_replace(' ', '', $_GET["server"])) . '.json' ));
      echo json_encode(array($_GET["server"] =>$output));
    }

}

//assemble all of the GET key:value pairs into the end point for the API request
function assembleGETstring(){

  $call = '';

  foreach($_GET as $gKey => $gValue) {
    if($gKey != 'server'){
      if($call != ''){
        $call = $call . '&';
      }
      $call = $call . $gKey . "=" . $gValue;
    }
  }

  //change chargecontroller.php to opendata.php when this gets updated on all servers
  $call = '/api/v1/chargecontroller.php?' . $call;
  return $call;
}

function getContentsErr($dst,$bool, $context){
  $req = file_get_contents($dst, $bool, $context);
  if($req === false) {
    return 'err';
  } else {
    return $req;
  }
}

?>