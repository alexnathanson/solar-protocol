<?php
  require_once '/home/pi/solar-protocol/backend/protect/protect.php';
  Protect\with('/home/pi/solar-protocol/backend/protect/form.php','admin');
?>

<!DOCTYPE html>
<html>

<head>

<title>Solar Server</title>
<script src="https://cdn.jsdelivr.net/npm/p5@1.6.0/lib/p5.js"></script>
</head>

<body>

<!--THIS PHP CODE IS FOR THE SERVER NAME - REFACTOR NEEDED -->
<?php

//read local file
$localFile = '/home/pi/local/local.json';

$localInfo = json_decode(getFile($localFile), true);

if (isset($localInfo["name"])){
  $locName = $localInfo["name"];
} else {
  $locName = "";
}

if (isset($localInfo["httpPort"])){
  $locPort = $localInfo["httpPort"];
} else {
  $locPort = "80";
}

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

<h1><a href="/">Solar Protocol (<?php echo $locName;?>)</a> - Admin Console</h1>

<span>Logged in as <a href="/admin/settings/user.php"><?php echo $_SESSION["username"]?></a> <a href="?logout">(Logout)</a></span>

<p><a href="/admin">Network Status</a> | <a href="/admin/local.php">Local Data</a> | <a href="/admin/settings">Settings</a> | <a href="/admin/settings/local.php">Local Content</a></p>

<h2>Network Status</h2>

<div id="server list"><h3>Online Servers:</h3></div>

<div id="pointOfEntryViz"><h3>Point of Entry History:</h3></div>

<!-- <div id="pointOfEntry"><h3>Point of Entry History:</h3></div>
 --><!-- <div id="poe_chart" style="width: 1500px; height: 500px"></div> -->

<script src="js/networkActivity-LinearViz.js"></script>

<script>
  let ipList = [];
  let nameList = [];

  //get the most recent line of charge controller data
  let toGet = "0";

  let jsonPoe;

//the day=deviceList end point should be moved to system info
  let devListURL = "http://"+ window.location.hostname + ":"+ <?php echo $locPort; ?> + "/api/v1/chargecontroller.php?day=deviceList";

  console.log(devListURL);

  getRequest(devListURL,parseDevList);

  //point of entry
  //getRequest(poeURL,sortPoeLog);

  function getRequest(dst, callback, dstNum){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if(dstNum && typeof dstNum === "number"){
        if (this.readyState == 4 && this.status == 200) {
          callback(this.responseText, dst, dstNum);
        } else if (this.readyState == 4) {
          callback(this.statusText, dst, dstNum);
        }
      } else {
         if (this.readyState == 4 && this.status == 200) {
          callback(this.responseText, dst);
        } else if (this.readyState == 4) {
          callback(this.statusText, dst);
        }
      }
     
    };
    xhttp.open("GET", dst, true);
    xhttp.send();
  }

  function parseDevList(response){

    console.log(JSON.parse(response));
    jsonDevList = JSON.parse(response);

    for (let p = 0; p < jsonDevList.length;p++){
      ipList.push(jsonDevList[p]["ip"]);   
      nameList.push(jsonDevList[p]["name"]);   
    }


  //individual server data
    for (let i = 0; i < ipList.length; i++){
      //pingServer(tempIPList[i], populate);
      let requestURL = "http://" + ipList[i] + "/api/v1/chargecontroller.php?line="+toGet;
      getRequest(requestURL, populate, i);

 /*     requestURL = "http://" + ipList[i] + "/server-status?auto"
      getRequest(requestURL, populateServerInfo, i)*/
    }

  //point of entry
  sortPoeLog(response);
  }

  function sortPoeLog(response){
    console.log(JSON.parse(response));
    jsonPoe = JSON.parse(response);

    let justPoeLog = []

    let storePos = [];//store the position for that particular log

    //get just the logs
    for (let p = 0; p < jsonPoe.length;p++){
      justPoeLog.push(jsonPoe[p]["log"]);   
      storePos[p] = 0; 
    }

    let outputPoeLog = [];

    for (let p = 0; p < 100;p++){

      //get next items from logs
      let tempPos = [];
      let sorted = [];
      for (let l = 0; l < storePos.length;l++){
        tempPos[l] = justPoeLog[l][storePos[l]];
        sorted[l] = justPoeLog[l][storePos[l]];
      }

      //sort in decending order
      sorted.sort(function(a,b){
            // Turn strings into date
            return new Date(b) - new Date(a);
          });

      //compare the sorted value to the unsorted list
      for (let x = 0; x < tempPos.length; x++){
        if (sorted[0] == tempPos[x]){
          //add new value to list only if it has changed...
          if(outputPoeLog.length == 0){
            outputPoeLog[outputPoeLog.length] = [justPoeLog[x][storePos[x]],x];
          } else if(outputPoeLog[outputPoeLog.length-1][1] != x){
            outputPoeLog[outputPoeLog.length] = [justPoeLog[x][storePos[x]],x];
          }
          storePos[x]++;
          break;
        }
      }
    }

    //console.log(outputPoeLog);

    //displayPOE(outputPoeLog);

    //asciiPoeViz(outputPoeLog)
  } 

  /*function displayPOE(poeArray){
    let poeID = document.getElementById('pointOfEntry');

    let para = document.createElement('p');

    for (let l = 0; l < poeArray.length;l++){
      let node = document.createTextNode(poeArray[l][0] + " " + jsonPoe[poeArray[l][1]]['name']);
      para.appendChild(node);
      para.appendChild(document.createElement('br'));//dont use a variable here, because then it will treat it as the same thing and only append it once, pushing it to the end of the p
    }

    poeID.appendChild(para);
  }*/

  function asciiPoeViz(poeArray){
    let poeID = document.getElementById('pointOfEntryViz');

    //an array of all the server names that were PoE
    let poeNames = [];
    let poeNumbers = [];
    //an array of all the ascii lines by device
    let poeStrings = [];

    let countSpaces = 0;

    let spaceChar = "_";

    for (let l = 0; l < poeArray.length;l++){
      //console.log(poeArray[l]);
      //check if it is a new name
      if (!poeNumbers.includes(poeArray[l][1])){
        //if its a new name, add the name
        poeNumbers.push(poeArray[l][1]);
        poeNames.push(jsonPoe[poeArray[l][1]]['name']);

        let newString = '';
        //back fill this new entry with blank spaces
        for(let s = 0; s < countSpaces;s++){
          newString += spaceChar;
        }
        newString += poeArray[l][1];
        poeStrings.push(newString);

        //add a space to all other entries
        for(let s = 0;s< poeStrings.length-1;s++){
          poeStrings[s] += spaceChar;
        }

      } else {
        //get position of name
        for(let n = 0; n < poeNumbers.length;n++){
          if(poeArray[l][1] == poeNumbers[n]){
            poeStrings[n] += poeNumbers[n];
          } else {
            poeStrings[n] += spaceChar;
          }
        }
      }
      countSpaces ++;
    }

    let sT = document.createElement("table"); 
    sT.style.width = '100%';
    sT.setAttribute('border', '1');
    let tbdy = document.createElement('tbody');
    let tr = document.createElement('tr');
    let tdNames = document.createElement('td');

    for(let s = 0; s < poeStrings.length;s ++){
      let nameLine = document.createTextNode(poeNames[s]);
      tdNames.appendChild(nameLine);
      tdNames.appendChild(document.createElement('br'))
    }

    let tdData = document.createElement('td');

    //let para = document.createElement('p');
    for(let s = 0; s < poeStrings.length;s ++){
      let asciiLine = document.createTextNode(poeStrings[s]);
      tdData.appendChild(asciiLine);
      tdData.appendChild(document.createElement('br'))
    }
    //poeID.appendChild(para);
    
    tr.appendChild(tdNames);
    tr.appendChild(tdData);

    tbdy.appendChild(tr);
    poeID.appendChild(tbdy);
  }

  function populate(dataToDisplay, dst, dstNum) {

    let dstIP = dst.replace('/api/v1/chargecontroller.php?line=0','');
    //dstIP = dst.replace('http://','');

    let dstName = nameList[dstNum] /*getRequest(dstIP + '/api/v1/chargecontroller.php?systemInfo=name');*/
    console.log(dstName);

    const sList = document.getElementById('server list');

    //server header
    const serverH3 = document.createElement('h3');
    serverH3.textContent = 'Server: ' + dstName + ' ';
    //make it a link
    const serverLink = document.createElement('a');
    serverLink.href = /*"http://"+*/dstIP;
    serverLink.target = "_blank"; //open in new tab

    const serverLinkContent = document.createTextNode(dstIP.replace('http://',''));
    serverLink.appendChild(serverLinkContent);

    serverH3.appendChild(serverLink);
    
    let displayThis = toJSON(dataToDisplay);

    let dataPara = document.createElement('p');

    if(displayThis != false){
      dataPara.appendChild(createTable(displayThis));
    } else {
      dataPara.textContent =  "no response or invalid format";
    }
    sList.appendChild(serverH3);
    sList.appendChild(dataPara);

    //add the div for server status
    let sS = document.createElement("div");
    sS.id = "serverStatus" + dstNum;

    sList.appendChild(sS);

    let requestSS = dstIP + "/server-status?auto"
    getRequest(requestSS, populateServerInfo, dstNum)
  }

  function populateServerInfo(dataToDisplay, dst, dstNum) {

    let sSLines = dataToDisplay.split("\n");

    console.log(sSLines)

    let sSDict = {};

    for (let l = 0; l < sSLines.length; l++){
      splitPos = sSLines[l].search(":");

      sSKey = sSLines[l].substring(0,splitPos).trim();
      //console.log(sSKey);
      sSValue = sSLines[l].substring(splitPos + 1).trim();
      //console.log(sSValue);

      sSDict[sSKey] = sSValue;
    }

    //console.log(sSDict);

    sS = document.getElementById("serverStatus" + dstNum);

    sSP = document.createElement("p")

    sSP.appendChild(document.createTextNode('Server Uptime: ' + sSDict['ServerUptime'] + " | " + "Requests Per Second: " + sSDict["ReqPerSec"] + " | " + 'Total Accesses: ' + sSDict['Total Accesses'] + " | " + 'CPU Load: ' + sSDict['CPULoad'] + "%"))
/*
    sSP.appendChild(document.createElement("br"))

    sSP.appendChild(document.createTextNode('Total Accesses: ' + sSDict['Total Accesses']))

    sSP.appendChild(document.createElement("br"))

    sSP.appendChild(document.createTextNode('CPU Load: ' + sSDict['CPULoad']))*/

    sS.appendChild(sSP)
  }


  function createTable(jsonData){
    let sT = document.createElement("table"); 
    sT.style.width = '100%';
    sT.setAttribute('border', '1');

    let tbdy = document.createElement('tbody');

    for (let r = 0; r <2;r++) {
      let tr = document.createElement('tr');
      for (let c = 0; c < Object.keys(jsonData).length; c++) {
        let td = document.createElement('td');
        if (r == 0) {//headers
          td.appendChild(document.createTextNode(Object.keys(jsonData)[c]));
          tr.appendChild(td);
        } else if (r == 1){//content
          td.appendChild(document.createTextNode(jsonData[Object.keys(jsonData)[c]]));
          tr.appendChild(td);
        }
      }
      tbdy.appendChild(tr);
    }
    sT.appendChild(tbdy);
    return sT;
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

</body>
</html>