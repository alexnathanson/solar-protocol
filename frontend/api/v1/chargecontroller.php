<?php

#This was previously the open data components of the API. Will not be updated further, but will be kept for servers that are still using the older system

#comment out these lines for production version
/*ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);*/


$ccDir = "/home/pi/solar-protocol/charge-controller/data/";
$scaleIt = false;

$todayFile = $ccDir . "tracerData" . date("Y-m-d") . ".csv";
//$fileName = "/home/pi/solar-protocol/charge-controller/data/tracerData" . $fileDate . ".csv";

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    //read the value of the query string, replace "-" with " "
    //var_dump($_GET);

    //most recent PV Data queries
    if (array_key_exists("value", $_GET)) {
        //echo "Key = Value";

        if (!testValue($_GET["value"])) {
            echo "Value not found. Acceptable values: PV-current, PV-current, PV-power-H,PV-power-L, PV-voltage, battery-percentage, battery-voltage, charge-current, charge-power-H, charge-power-L, load-current, load-power, load-voltage, datetime, scaled-wattage";
            exit;
        }

        $qValue = str_replace("-", " ", $_GET["value"]);

        if ($qValue == "scaled wattage") {
            $qValue = "PV power L";
            $scaleIt = true;
        }

        //echo $qValue;

        if (array_key_exists("duration", $_GET) && intval($_GET["duration"]) != 0) {
            //returns a given value over time
            $valueTimeSeries = [];

            $dirArray = justTracerDataFiles($ccDir);
            for ($f = 0; $f < intval($_GET["duration"]); $f++) {
                if ($f>= count($dirArray) || $f >= 7) {
                    break;
                }
                $tFile = chargeControllerData($ccDir . $dirArray[count($dirArray)-1-$f]);

                $valuePosition = 0;
                foreach ($tFile[0] as $k) {
                    if ($k == $qValue) {
                        break;
                    }
                    $valuePosition++;
                }

                //scale the wattage if required
                if ($qValue == 'PV-power-L' && $scaleIt == true) {
                    foreach ($tFile as $l) {
                        $valueTimeSeries[$l[0]]=$l[$valuePosition] * wattageScaler();
                    }
                } else { //unscaled wattage
                    foreach ($tFile as $l) {
                        $valueTimeSeries[$l[0]]=$l[$valuePosition];
                    }
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

            if ($readData != false) {
                for ($v = 0; $v < sizeof($readData[0]);$v++) {
                    if ($readData[0][$v]==$qValue) {
                        //scale wattage if required
                        if ($qValue == 'PV power L' && $scaleIt == true) {
                            echo $readData[count($readData)-1][$v] * wattageScaler();
                        } else { //unscaled wattage
                            echo $readData[count($readData)-1][$v];
                        }
                        break;
                    }
                }
            }
        }
    }
    //get a line of current data file. "len" returns length of current file, "head" returns the column headers, "0" returns most recent line. Increments up for other lines.
    elseif (array_key_exists("line", $_GET)) {
        //echo "Key = Line";

        $readData = chargeControllerData($todayFile);

        if ($readData != false) {
            if ($_GET["line"] == "len") {//return the number of rows in the file
                echo(count($readData)-1);
            } elseif ($_GET["line"] == "head") {//return the CSV data headers
                echo json_encode($readData[0]);
            } elseif ($_GET["line"] >= 0 && $_GET["line"] < count($readData)) {
                //returns raw line
                //var_dump($readData[count($readData)-1-$_GET["line"]]);

                $returnArray = array();
                //package line with headers
                for ($p = 0; $p<count($readData[0]);$p++) {
                    $returnArray[$readData[0][$p]] = $readData[count($readData)-1-$_GET["line"]][$p];
                }
                $returnJSON = json_encode($returnArray);
                echo $returnJSON;
            }
        }


    //get a full file
    } elseif (array_key_exists("day", $_GET)) {
        //echo "Key = File";

        if ($_GET["day"] == "list") {//list all charge controller data files
            echo json_encode(justTracerDataFiles($ccDir));
        //var_dump(justTracerDataFiles($ccDir));
        } elseif ($_GET["day"] == "len") {//list all charge controller data files
            echo count(justTracerDataFiles($ccDir));
        } elseif (intval($_GET["day"]) >= 1 && intval($_GET["day"]) <= 7) {
            $multiDayData = [];

            $dirArray = justTracerDataFiles($ccDir);
            for ($f = 0; $f < intval($_GET["day"]); $f++) {
                if ($f>= count($dirArray)) {
                    break;
                }
                array_push($multiDayData, chargeControllerData($ccDir . $dirArray[count($dirArray)-1-$f]));
            }

            echo json_encode($multiDayData);
        } elseif (strpos($_GET["day"], 'tracerData') !== false) {      //get CC data file by file name
            echo json_encode(chargeControllerData($ccDir . $_GET["day"] . '.csv'));
        }

        //this should be removed and made into a POST
        if ($_GET["day"] == "deviceList") {
            $fileName = "/home/pi/solar-protocol/backend/data/deviceList.json";
            echo getFileContents($fileName);
        }
    } elseif (array_key_exists("systemInfo", $_GET)) {
        //echo "system info! ";

        //get local time zone
        if ($_GET["systemInfo"] == "tz") {
            //if (ini_get('date.timezone')) {
            //echo ini_get('date.timezone');
            echo date_default_timezone_get();
        //}
        } /*else if ($_GET["systemInfo"] == "ping"){
      echo "ping";
    } */elseif ($_GET["systemInfo"] == "color") {
            //read local bgColor
            $fileContents = file_get_contents("/home/pi/local/local.json");
            // Convert to array
            echo json_decode($fileContents, true)['bgColor'];
        } elseif ($_GET["systemInfo"] == "description") {
            //read local bgColor
            $fileContents = file_get_contents("/home/pi/local/local.json");
            echo json_decode($fileContents, true)['description'];
        } elseif ($_GET["systemInfo"] == "name") {
            //read local name
            $fileContents = file_get_contents("/home/pi/local/local.json");
            echo json_decode($fileContents, true)['name'];
        } elseif ($_GET["systemInfo"] == "location") {
            //read local location
            $fileContents = file_get_contents("/home/pi/local/local.json");
            echo json_decode($fileContents, true)['location'];
        } elseif ($_GET["systemInfo"] == "city") {
            //read local city
            $fileContents = file_get_contents("/home/pi/local/local.json");
            echo json_decode($fileContents, true)['city'];
        } elseif ($_GET["systemInfo"] == "country") {
            //read local country
            $fileContents = file_get_contents("/home/pi/local/local.json");
            echo json_decode($fileContents, true)['country'];
        } elseif ($_GET["systemInfo"] == "wattage-scaler") {
            echo wattageScaler();
        } elseif ($_GET["systemInfo"] == "pvWatts") {
            $fileContents = file_get_contents("/home/pi/local/local.json");
            echo json_decode($fileContents, true)['pvWatts'];
        } elseif ($_GET["systemInfo"] == "pvVoltage") {
            $fileContents = file_get_contents("/home/pi/local/local.json");
            echo json_decode($fileContents, true)['pvVolts'];
        } elseif ($_GET["systemInfo"] == "dump") {
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
            echo json_encode($infoDump);
        }
    } elseif (array_key_exists("networkInfo", $_GET)) {
        if ($_GET["networkInfo"] == "deviceList") {
            $output = [];

            $fileName = "/home/pi/solar-protocol/backend/data/deviceList.json";

            $contents = json_decode(file_get_contents($fileName), true); #getFileContents($fileName);

            for ($d = 0; $d < count($contents);$d++) {
                array_push($output, $contents[$d]["name"]);
            }
            echo json_encode($output);
        }
    }
}

function testValue($v)
{
    $possibleValues = array('PV-current','PV-current','PV-power-H','PV-power-L','PV-voltage','battery-percentage','battery-voltage','charge-current','charge-power-H', 'charge-power-L','load-current','load-power','load-voltage','datetime','scaled-wattage');

    foreach ($possibleValues as $aV) {
        if ($aV == $v) {
            //$v = str_replace("-"," ",$v);
            return $v;
        }
    }
    return false;
}

function justTracerDataFiles($dir)
{
    $dirArray = scandir($dir);//returns list of directory contents
    $dirFiles = [];
    for ($f = 0; $f < count($dirArray);$f++) {
        if (strpos($dirArray[$f], 'tracerData') !== false) {
            array_push($dirFiles, $dirArray[$f]);
        }
    }

    return $dirFiles;
}

function chargeControllerData($fileName)
{
    //$fileDate = date("Y-m-d");
    //$fileName = "/home/pi/solar-protocol/charge-controller/data/tracerData" . $fileDate . ".csv";

    $rawDataArray = [];

    if (($h = fopen("{$fileName}", "r")) !== false) {
        // Each line in the file is converted into an individual array that we call $data
        // The items of the array are comma separated
        while (($data = fgetcsv($h, 1000, ",")) !== false) {
            // Each individual array is being pushed into the nested array
            $rawDataArray[] = $data;
        }

        // Close the file
        fclose($h);

        return $rawDataArray;
    } else {
        return false;
    }
}

function getFileContents($fileName)
{
    //echo $fileName;
    try {
        return file_get_contents($fileName);
    } catch(Exception $e) {
        echo $fileName;
        return false;
    }
}

//this function returns a scaler value for the wattage of the module so all modules across the network can be compared
//a more advance non-linear equation may need to be adopted in the future
function wattageScaler()
{
    //get local file
    $fileContents = file_get_contents("/home/pi/local/local.json");
    $localData = json_decode($fileContents, true);
    // Convert to array and get PV watts data
    if (array_key_exists('pvWatts', $localData)) {
        $localPVwatts = $localData['pvWatts'];
        if ($localPVwatts != "") {
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
