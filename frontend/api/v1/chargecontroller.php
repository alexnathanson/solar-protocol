<?php
#comment out these lines for production version
/*ini_set('display_errors', 1); 
ini_set('display_startup_errors', 1); 
error_reporting(E_ALL);*/


$ccDir = "/home/pi/solar-protocol/charge-controller/data/";

$todayFile = $ccDir . "tracerData" . date("Y-m-d") . ".csv";
//$fileName = "/home/pi/solar-protocol/charge-controller/data/tracerData" . $fileDate . ".csv";

if ($_SERVER["REQUEST_METHOD"] == "GET") {

  //read the value of the query string, replace "-" with " "
  //var_dump($_GET);

  //most recent PV Data queries
  if(array_key_exists("value", $_GET)){
    //echo "Key = Value";
  

    if(!testValue($_GET["value"])){
      echo "Value incorrect";
      exit;
    }

    $qValue = str_replace("-"," ",$_GET["value"]);

    //echo $qValue;

    if(array_key_exists("duration", $_GET)){
      //returns a given value over time
      $valueTimeSeries = [];

      $dirArray = justTracerDataFiles($ccDir);
      for ($f = 0; $f < intval($_GET["duration"]); $f++){
        if($f>= count($dirArray)){
          break;
        }
        $tFile = chargeControllerData($ccDir . $dirArray[count($dirArray)-1-$f]);

        $valuePosition = 0;
        foreach($tFile[0] as $k){
          if($k == $qValue){
            break;
          }
          $valuePosition++;
        }

        foreach($tFile as $l){
          $valueTimeSeries[$l[0]]=$l[$valuePosition];
        }

        /*
        $vTime = chargeControllerData($ccDir . $dirArray[count($dirArray)-1-$f]);
        $vValue = 
        $valueTimeSeries[$vTime]=$vValue;
        *///array_push($valueTimeSeries, );
        }

      echo json_encode($valueTimeSeries);
    } else {
      $readData = chargeControllerData($todayFile);

      if ($readData != FALSE){    
        for ($v = 0; $v < sizeof($readData[0]);$v++){
            if($readData[0][$v]==$qValue){
                echo $readData[count($readData)-1][$v];
                break;
            }
        }
      }
    }
    
  }
  //get a line of current data file. "len" returns length of current file, "head" returns the column headers, "0" returns most recent line. Increments up for other lines.
  else if (array_key_exists("line", $_GET)) {
    //echo "Key = Line";
    
    $readData = chargeControllerData($todayFile);

    if ($readData != FALSE){    
      
      if($_GET["line"] == "len"){//return the number of rows in the file
        echo count($readData);
      } else if($_GET["line"] == "head"){//return the CSV data headers
        echo json_encode($readData[0]);
      } else if ($_GET["line"] >= 0 && $_GET["line"] < count($readData)){
        //returns raw line
//        var_dump($readData[count($readData)-1-$_GET["line"]]);

        $returnArray = array();
        //package line with headers
        for ($p = 0; $p<count($readData[0]);$p++){
          $returnArray[$readData[0][$p]] = $readData[count($readData)-1-$_GET["line"]][$p];
        }  
          $returnJSON = json_encode($returnArray);
          echo $returnJSON;
      }
    }

    //get a full file
  } else if (array_key_exists("file", $_GET)) {
    //echo "Key = File";

    if($_GET["file"] == "deviceList"){ //deviceList should be a POST
      $fileName = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";
      echo getFileContents($fileName);

    } else if ($_GET["file"] == "list"){//list all charge controller data files
      echo json_encode(justTracerDataFiles($ccDir));
      //var_dump(justTracerDataFiles($ccDir));

    } else if ($_GET["file"] == "len"){//list all charge controller data files
      echo count(justTracerDataFiles($ccDir));

    } else if (intval($_GET["file"]) >= 1 && intval($_GET["file"]) <= 7){

      $multiDayData = [];

      $dirArray = justTracerDataFiles($ccDir);
      for ($f = 0; $f < intval($_GET["file"]); $f++){
        if($f>= count($dirArray)){
          break;
        }
        array_push($multiDayData, chargeControllerData($ccDir . $dirArray[count($dirArray)-1-$f]));
      }

      echo json_encode($multiDayData);

    } else if(strpos($_GET["file"],'tracerData') !== false){      //get CC data file by file name
      echo json_encode(chargeControllerData($ccDir . $_GET["file"] . '.csv'));
    }
  }
}

function testValue($v){

  $possibleValues = array('PV-current','PV-current','PV-power-H','PV-power-L','PV-voltage','battery-percentage','battery-voltage','charge-current','charge-power-H', 'charge-power-L','load-current','load-power','load-voltage','datetime');

  foreach($possibleValues as $aV){
    if($aV == $v){
      //$v = str_replace("-"," ",$v);
      return $v;
    }
  }
  return FALSE;
}

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

function chargeControllerData($fileName){
  //$fileDate = date("Y-m-d");
  //$fileName = "/home/pi/solar-protocol/charge-controller/data/tracerData" . $fileDate . ".csv";
    
  $rawDataArray = [];

  if (($h = fopen("{$fileName}", "r")) !== FALSE) {
    // Each line in the file is converted into an individual array that we call $data
    // The items of the array are comma separated
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