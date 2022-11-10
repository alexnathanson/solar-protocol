//The script retrieves  the most recent PV power data from active server and prints the text on the screen

//reference: https://p5js.org/reference/#/p5/text

let value = "Battery Voltage: ";

//variable to store the data we request from the API
let pvData = 0.0;

function setup() {
  //set the drawing canvas
  createCanvas(windowWidth, windowHeight);

  //make an asyncronous API call
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?value=battery-voltage', gotCCData); 


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

}

function gotCCData(tempData){
  //the raw data response
  console.log(tempData);
  //get an array with the different keys in the API response
  resKeys = Object.keys(tempData);
  console.log(resKeys);
  
  //get the data corresponding to the key we want
  pvData = tempData[resKeys[0]];
  console.log(pvData);

}