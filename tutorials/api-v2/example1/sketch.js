//The script retrieves  the most recent PV power data from active server and prints the text on the screen

//reference: https://p5js.org/reference/#/p5/text

let value = "Battery Voltage: ";

//variable to store the data we request from the API
let pvData = 0.0;
let serverName = '';

// use 80 for HTTP and 443 for HTTPS
let port = 443;

function setup() {
  //set the drawing canvas
  createCanvas(windowWidth, windowHeight);

  //make an asyncronous API call to get the battery voltage
  loadJSON('https://solarprotocol.net:' + port + '/api/v2/opendata.php?value=battery-voltage', gotBatData); 

  //make an asyncronous API call to get the name of the server
  loadJSON('https://solarprotocol.net:' + port + '/api/v2/opendata.php?systemInfo=name', gotName); 

  //set the font family
  textFont('Times');

  //align the text in the vertical and horrizontal center
  textAlign(CENTER, CENTER);

  //set text border weight
  strokeWeight(3)
}

function draw() {
  let time = millis()/1000;

  //get a float between 0.0-1.0
  timeScalar = (sin(time)+1)*.5;
  //console.log(timeScalar);

  //set the background color
  background(timeScalar*255,255-(timeScalar*255),200+(timeScalar*55));


  //set text size
  textSize(24);
  //write the server name to the screen
  text("Active Server: " + serverName, 250,50);

  //translate the origin point
  translate((timeScalar*windowWidth), (time*100)%windowHeight);



/*  rectangle(-300,-300,300,300);
*/
  //rotate the canvas
  rotate(timeScalar * TWO_PI);

  //this is the interior text color
  fill(timeScalar*255,time%255,255-(time%255));

  //this is the text border color
  stroke(0);

  //set text size
  textSize((time%60)+10);

  //write the text to the screen
  text(value + pvData, 0,0);

  //every 5 minutes call the API again to update the data
  if(time >= 60*5){

    //make an asyncronous API call to get the battery voltage
    loadJSON('http://solarprotocol.net/api/v2/opendata.php?value=battery-voltage', gotBatData); 

    //make an asyncronous API call to get the name of the server
    loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=name', gotName); 
  }

}

function gotBatData(tempData){
  //the raw data response
  console.log(tempData);
  //get an array with the different keys in the API response
  resKeys = Object.keys(tempData);
  console.log(resKeys);
  
  //get the data corresponding to the key we want
  pvData = tempData[resKeys[0]];
  console.log(pvData);

}

function gotName(tempData){
  //the raw data response
  console.log(tempData);
  //get an array with the different keys in the API response
  resKeys = Object.keys(tempData);
  console.log(resKeys);
  
  //get the data corresponding to the key we want
  serverName = tempData[resKeys[0]];
  console.log(serverName);

}