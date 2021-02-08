<?php
  require_once '/home/pi/solar-protocol/backend/protect/protect.php';
  Protect\with('/home/pi/solar-protocol/backend/admin/protect/form.php','admin');
?>

<!DOCTYPE html>
<html>

<head>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<title>Solar Server</title>

</head>

<body>

<h1><a href="/">Solar Protocol</a> - Admin Console</h1>
<span>Logged in as <?php echo $_SESSION["username"]?> <a href="?logout">(Logout)</a></span>

<p><a href="/admin">Network Activity</a> | <a href="/admin/local.php">Local Data</a> | <a href="/admin/settings">Settings</a></p>

<h2>Network Activity</h2>

<div id="server list"><h3>Online Servers:</h3></div>

<div id="pointOfEntry"><h3>Point of Entry History:</h3></div>
<!-- <div id="poe_chart" style="width: 1500px; height: 500px"></div> -->

<script>
  //make this dynamic at some point
  //let tempIPList = ["74.73.93.241","67.85.62.144","108.29.41.133"];
  let ipList = [];
  //get the most recent line of charge controller data
  let toGet = "0";

  let jsonPoe;


  let devListURL = "http://"+ window.location.hostname +"/api/v1/chargecontroller.php?day=deviceList";
  console.log(devListURL);

  getRequest(devListURL,parseDevList);

  //point of entry
  //getRequest(poeURL,sortPoeLog);


  function getRequest(dst, callback){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        callback(this.responseText, dst);
      } else if (this.readyState == 4) {
        callback(this.statusText, dst);
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
    }


  //individual server data
    for (let i = 0; i < ipList.length; i++){
      //pingServer(tempIPList[i], populate);
      let requestURL = "http://" + ipList[i] + "/api/v1/chargecontroller.php?line="+toGet;
      getRequest(requestURL, populate);
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

    displayPOE(outputPoeLog);

  } 

  function displayPOE(poeArray){
    let poeID = document.getElementById('pointOfEntry');

    let para = document.createElement('p');

    for (let l = 0; l < poeArray.length;l++){
      let node = document.createTextNode(poeArray[l][0] + " " + jsonPoe[poeArray[l][1]]['name']);
      para.appendChild(node);
      para.appendChild(document.createElement('br'));//dont use a variable here, because then it will treat it as the same thing and only append it once, pushing it to the end of the p
    }

    poeID.appendChild(para);
  }


  function populate(dataToDisplay, dst) {

    let dstIP = dst.replace('/api/v1/chargecontroller.php?line=0','');
    //dstIP = dst.replace('http://','');

    const sList = document.getElementById('server list');

    //server header
    const serverH3 = document.createElement('h3');
    serverH3.textContent = 'Server: ';
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