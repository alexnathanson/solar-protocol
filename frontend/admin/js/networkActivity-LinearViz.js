//this script demonstrates how to work with time in JS

let baseURL = '/api/v2/opendata.php?';

/*let getTZ = 'systemInfo=tz';*/
let serverCall = 'server=all';
let poeCall = 'networkInfo=dump';
//Set margins for the graph
let yMargin = 100;
let xMargin = 140;

/*let tz;*/
let serverNames = [];
let timezoneArr = [];
//ms
let durationMS = 3 * 24 * 60 * 60 * 1000;
let durationMin = durationMS / 1000 / 60;
let minuteWidth;

let val = "scaled-wattage"; //"PV power L";
let valPos;
let amtServers;
let datetimePos;

let blacklist = ['swathmoresolar'] //not implemented

function setup() {
  createCanvas(windowWidth, min(windowHeight,800));

  //set the width of each data point
  minuteWidth = max((width - (xMargin * 2))/durationMin,1);

  //get time series data
  loadJSON(baseURL + serverCall, gotServerData); 

  loadJSON(baseURL + poeCall, gotPOEData);

  background(255);
  strokeWeight(0.5);
  textFont('Times');
  textSize(12);
 
  noLoop();
}

function draw() {
  drawAxes();
  drawKey();

  //save and reload page
  //setTimeout(saveIt, 10 * 60000);

/*  drawLabels();
*/}


function gotServerData(tempdata){
  console.log(tempdata);
  console.log(tempdata['data']);

  //get list of server names

  serverNames = Object.keys(tempdata['data']);
  timezoneArr = tempdata['timezone'];

  //get position of value in array
  for (let v = 0; v < tempdata['header'].length; v++){
    if(tempdata['header'][v]== val){
      valPos=v;
    }
  }
    //get position of datetime in array
  for (let v = 0; v < tempdata['header'].length; v++){
    if(tempdata['header'][v]== "datetime"){
      datetimePos=v;
    }
  }
  console.log("datetime pos: " + datetimePos);

  //loop through servers
  let dKeys = Object.keys(tempdata['data']);
  amtServers = dKeys.length;
  for(let s=0;s< amtServers;s++){
    let sD = tempdata['data'][dKeys[s]];
    //console.log(sD);
    if(sD != 'err'){

      let adjustedKeys=[];
      //loop through each line
      for (let k = 0; k < sD.length; k++){
        kDate = new Date(sD[k][datetimePos]);
        let tzOffset = getTimeZoneOffset(kDate,tempdata['timezone'][s]);
        let adjustedTime = adjustTimeToLocal(kDate,tzOffset);
        //console.log(tzOffset);
        adjustedKeys[adjustedTime] = sD[k][valPos];
        //adjustedKeys[k]['datetime']=adjustedTime;
      }

      //let filteredKeys = filterTime(adjustedKeys);
      //drawServerData(filteredKeys,s);
      drawServerData(adjustedKeys,s);
    }
  }
    drawLabels();
}

function gotPOEData(tempdata){
  console.log(tempdata);
  console.log(tempdata['dump']['poe']);
  console.log(tempdata['dump']['tz']);
  //adjust time zones
  let adjustedPOE = [];

  //loop through each server to adjust timezones and filter
  for (let s = 0; s < tempdata['dump']['poe'].length; s++){
    //console.log(tempdata['dump']['tz'][s]);

    let adjustedArray = [];
    for (let p = 0; p < tempdata['dump']['poe'][s].length; p++){
      let sD = tempdata['dump']['poe'][s];
      sDate = new Date(sD[p]);

      let tzOffset = getTimeZoneOffset(sDate,tempdata['dump']['tz'][s]);
      let adjustedTime = adjustTimeToLocal(sDate,tzOffset);


      //filter for time period
      //if(new Date(adjustedTime).getTime() > new Date(new Date().getTime()-durationMS)){
        adjustedArray[p] = adjustedTime;
      //}
    }

    adjustedPOE[s] = adjustedArray;
  }

  //console.log(adjustedPOE);
  
  //merge arrays
    amtServers = adjustedPOE.length;

  let mergedPOE = [];
   for (let s = 0; s < adjustedPOE.length; s++){
    for (let r = 0; r < adjustedPOE[s].length; r++){
      let tempR = [adjustedPOE[s][r],s];
      mergedPOE.push(tempR);
    }
  }

  //console.log(mergedPOE);

  //sort in decending order
  mergedPOE.sort(function(a,b){
        // Turn strings into date
        return new Date(b[0]) - new Date(a[0]);
      });

    //console.log(mergedPOE);

    //remove repetition
    let remPOE = [];
  for(let rr = 0; rr < mergedPOE.length-1; rr++){
    if(mergedPOE[rr][1] != mergedPOE[rr+1][1]){
      remPOE.push(mergedPOE[rr]);
    }
  }

  drawPOEData(remPOE);
}

function saveIt(){
  let epoch = new Date().getTime();
  saveCanvas('canvas' + epoch, 'jpg');

  setTimeout(()=>{location.reload();}, 10000);

   
}

//returns an integer representing the timezone offset in ms
function getTimeZoneOffset(date, tzO) {
  //convert to specific timezone
  if(tzO != null){
      let adjustedDate = date.toLocaleString('en-US', { timeZone: tzO});

      let offset = new Date(adjustedDate).getTime() - new Date(date).getTime();

      return offset;
    } else {
      return 0;
    }

}

//returns a date object
function adjustTimeToLocal(date, timeZoneOffset){
  //console.log(date, timeZoneOffset);
  let adjustedTime = date - timeZoneOffset;
  return new Date(adjustedTime);

}


function filterTime(data){
  let now = new Date().getTime();

  let cutOff = new Date(now-durationMS);

  let filteredData = [];
  //console.log(new Date(Object.keys(data)[0]).getTime());

  for (let d = 0; d < Object.keys(data).length; d++){
    let t = new Date(Object.keys(data)[d]);
    if(t.getTime() > cutOff){
      filteredData[Object.keys(data)[d]] = data[Object.keys(data)[d]];
    }
  }

  return filteredData;
}

function drawServerData(data, pos){
  //console.log(data);
  let k = Object.keys(data);
  let mostRecent = new Date().getTime();
  let farthest = mostRecent - durationMS; 

  //console.log(new Date(mostRecent) + " - " + new Date(farthest));

  let yRange = (height - (2*yMargin))/amtServers;
  for (let x=0;x < k.length; x++){
    let d = new Date(k[x]);
    drawX =parseInt(constrain(map(d.getTime(), mostRecent, farthest, width-xMargin, xMargin),xMargin,width-xMargin));
    //console.log(drawX);

    if(drawX >= xMargin){

      //width of rect (this might cause an error if the server goes down)
      /*if (x+1 < k.length){
        drawXw =parseInt(map(new Date(k[x-1]).getTime(), mostRecent, farthest, width-xMargin, xMargin));
      } else {
        drawXw = xMargin;
      }*/
      drawXw = constrain(drawX - minuteWidth, xMargin,width - xMargin);

      drawY = map(data[k[x]],0.0, 50.0, yRange, 0);
      drawColor = map(data[k[x]],0.0, 50.0, 0, 255);
      noStroke();
      fill(drawColor,1,1);
      rectMode(CORNERS);
      rect(drawX, drawY + yMargin + (yRange*pos),drawXw, yMargin + yRange + (yRange*pos));
    }
  }
  
}

function drawPOEData(data){
  let mostRecent = new Date().getTime();
  let farthest = mostRecent - durationMS;
  //console.log(new Date(mostRecent) + " - " + new Date(farthest));

  let yRange = (height - (2*yMargin))/amtServers;
  for (let x=0;x < data.length; x++){
    let d = new Date(data[x][0]);
    //console.log(d);
    drawX =parseInt(min(map(d.getTime(), mostRecent, farthest, width-xMargin, xMargin), width - xMargin));
    //drawX =parseInt(map(d.getTime(), mostRecent, farthest, width-xMargin, xMargin));
    //console.log(drawX);
    //width of rect
    if (x >= 1){
      drawXw =parseInt(map(new Date(data[x-1][0]).getTime(), mostRecent, farthest, width-xMargin, xMargin));
      //drawXw =parseInt(constrain(map(new Date(data[x-1][0]).getTime(), mostRecent, farthest, width-xMargin, xMargin),xMargin,width - xMargin));
    } else if (x == 0) {
      drawXw = width - xMargin;
      //circle(drawX,  yMargin + (yRange*data[x][1]), 10);
    }

    drawXw = min(drawXw,width - xMargin);

    noStroke();
    fill(0,255,0,155);
    rectMode(CORNERS);

    if(drawX >= xMargin){

      rect(drawXw, yMargin + (yRange*data[x][1]),drawX, yMargin + yRange + (yRange*data[x][1]));

      //mark start of POE period
      stroke(0,0,255);
      line(drawX,yMargin + (yRange*data[x][1]),drawX,yMargin + (yRange*data[x][1])+ (yRange))
    } else if (drawX < xMargin && drawXw >= xMargin ){
      rect(drawXw, yMargin + (yRange*data[x][1]),xMargin, yMargin + yRange + (yRange*data[x][1]));
    }

  }
  
}

function drawAxes(){
    //draw axes
    stroke(0,0,0);
    line(0 + xMargin, height - yMargin, 0 + xMargin, 0 + yMargin); // y axis
    line(0 + xMargin, height - yMargin, width - xMargin, height - yMargin); //x axis
}

function drawKey(){
  let keyH = 50
  textAlign(LEFT);
  textSize(20);
  fill(0);
  text("Key: ", xMargin, keyH);

  rectMode(CORNER);
  fill(0,255,0);
  rect(xMargin + 48, 28, 130,28);
  fill(0);
  text("Point of Entry ", xMargin + 50, keyH);

  fill(0,0,255);
  rect(xMargin + 48 + 130, 28, 200,28);
  fill(0);
  text("Start of Point of Entry ", xMargin + 50 + 130, keyH);

  fill(255,0,0);
  rect(xMargin + 48 + 310, 28, 150,28);
  fill(0);
  text("PV Power ", xMargin + 50 + 310, keyH);
}

function drawLabels(){

  let xAx = height - yMargin;
  let yAx = xMargin;

  fill(0);

  //title
  /*textSize(50);
  textAlign(CENTER);
  text("Solar Protocol Routing", width *.5, yMargin-50);*/

  //AXIS
  textSize(30);
  textAlign(CENTER);
  //y axis
  /*push()
  translate(yAx - 40, height/2);
  rotate(PI*1.5);
  text("SERVER",0,0);
  pop();*/

  //x axis
  push()
    translate(width/2, (xAx) + 60);
    text("Local Time",0,0);
  pop();

  //TICKS
  textSize(15);

  //y ticks
  textAlign(RIGHT);

  stroke(1);
  textSize(15);
  let yRange = (height - (2*yMargin))/amtServers;
  for(let s = 0; s < amtServers; s++){
    line(xMargin-10,yMargin + (yRange*s),width - xMargin,yMargin + (yRange*s));
    text(serverNames[s],yAx - 5,(yMargin + (yRange*s))+(yRange*.5));

    if(timezoneArr[s] != null){
      let tzCity = timezoneArr[s].split("/")[1];
      text("tz: " + tzCity ,yAx - 5,(yMargin + (yRange*s))+(yRange*.5)+25);
    }
  }

  //x ticks
  let timeNow = new Date();

  let amtTick = 8;
  for(let t=0; t < amtTick ; t++){
    let tickTime = new Date(timeNow-((durationMS/(amtTick-1))*t));

    let tickX =  xMargin + (((width-(2*xMargin))/(amtTick-1)) * (amtTick - 1 - t));
    if(t==0){
      console.log(t);
      textAlign(RIGHT);
    } else if (t == amtTick -1){
      textAlign(LEFT);
    } else {
      textAlign(CENTER);
    }
       line(tickX,xAx-5,tickX,xAx + 10);
      text(tickTime.toLocaleString(), tickX,xAx + 25);
  }
}
