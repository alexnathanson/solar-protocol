<?php
#comment out these lines for production version
ini_set('display_errors', 1); 
ini_set('display_startup_errors', 1); 
error_reporting(E_ALL);
/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp32-esp8266-mysql-database-php/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

/*
DB name: ipDB
Table name: ipList
columns: Stamp, IP
*/

$servername = "localhost";

// REPLACE with your Database name
$dbname = "ipDB";
// REPLACE with Database user
$username = "solar";
// REPLACE with Database user password
$password = "protocol";

// Keep this API Key value to be compatible with the ESP32 code provided in the project page. 
// If you change this value, the ESP32 sketch needs to match
$api_key_value = "tPmAT5Ab3j7F9";

$api_key= $stamp = $ip = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $api_key = test_input($_POST["api_key"]);
    if($api_key == $api_key_value) {
        $stamp = test_input($_POST["stamp"]);
        $ip = test_input($_POST["ip"]);
        
        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 
        
        $sql = "INSERT INTO ipList (stamp, ip)
        VALUES ('" . $stamp . "', '" . $ip . "')";  
        
        if ($conn->query($sql) === TRUE) {
            echo "New record created successfully";
        } 
        else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
        
        $conn->close();
    }
    else {
        echo "Wrong API Key provided.";
    }

}
else if ($_SERVER["REQUEST_METHOD"] == "GET") {

    echo "GET IT!";

    $fileDate = date("Y-m-d");
    $fileName = "/home/pi/EPSolar_Tracer/data/tracerData" . $fileDate . ".csv";
    $rawDataArray = [];

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
    
      //return most recent voltage
    echo $rawDataArray[count($rawDataArray)-1][3];
    }

}
else {
    echo "No data posted with HTTP POST.";
}

function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
