<?php

/*
The purpose of this script is to artificially enable https, which is needed for most code editors.
This is intended to be used with Solar Protocol workshops and prototyping, but should not be used with production code.

This only works with the opendata.php, not other parts of the API.

This is a drop-in replacement:
replace http://solarprotocol.net with https://server.solarpowerforartists.com

For example: https://server.solarpowerforartists.com/api/v1/opendata.php?systemInfo=dump
*/

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

    foreach (array_keys($_GET) as $gK) {
        if ((isset($_GET[$gK]) && !empty($_GET[$gK])) || $_GET[$gK] == '0') {
            if ($apiVals != '') {
                $apiVals = $apiVals . "&";
            }

            $apiVals = $apiVals . $gK . "=" . $_GET[$gK];
        }
    }

    header('Access-Control-Allow-Origin: *');

    $apiCall = 'http://solarprotocol.net/api/v2/opendata.php?' . $apiVals;
    echo file_get_contents($apiCall, false, $streamContext);
}
