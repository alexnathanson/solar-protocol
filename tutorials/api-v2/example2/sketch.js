//Getting 3 days of data from active server
//Preview data at http://solarprotocol.net/api/v2/

//Set margins for the graph
let yMargin = 50;
let xMargin = 50;

let pd, ph = 0;
let v =0;
let colors;
let c=0; //color counter

let dates = [];
let params = [];

//these are the colors for our graph
colors = ["aqua", "blue", "red", "green", "yellow", "pink", "orange", "purple", "brown", "orangered", "violet", "white"];

// use 80 for HTTP and 443 for HTTPS
let port = 443;

function setup() {
  //this sets out canvas to the full dimensions of our browser window
  createCanvas(windowWidth, windowHeight);

  //this makes the GET request to the API
  //comment this out to use the offline data
  loadJSON('https://solarprotocol.net:' + port + '/api/v2/opendata.php?day=3', gotData); 

  // Offline data - note that this path assumes your root directory is api-v2.
  //  comment this in to use
  // loadJSON('data/day3.json', gotData); 

  //this sets the background color
  background(210);

  //this sets the stroke thickness
  strokeWeight(0.5);

  //this sets the font style
  textFont('Times');
  textSize(12);

  //in P5.JS the draw function will automatically loop, unless noLoop() is called
  noLoop();
}

function draw() {
  drawAxes();
}

//this is the callback that is run after our data is retrieved.
function gotData(tempData){
  //print out the raw data
  console.log(tempData)

  params = tempData["header"];
  print("params: "+params.length);

  //put data into a 2d array called data
  let data = tempData["data"];

  //this tells us how much data we have. each piece of data represents one moment in time from our solar power system. 
  print("timestamps: "+data.length);

  // put dates into their own array 
  for(let i=0; i< data.length; i++){
    dates.push(dayjs(data[i][0]));

  }

  // // draw data sending name and data array as arguments
  let parameterName;
  let maxYvalue=0;
  for(let i=1; i<data[0].length; i++){ //for each parameter  
    let values = [];
    parameterName = params[i];
    for(let j=0; j< data.length; j++){  //for each timestamp     
      // print("i:"+i);
      // print("j:"+j);
      if(float(data[j][i]) > maxYvalue){
        maxYvalue = float(data[j][i]);
      }
      values.push(float(data[j][i])); //put values into values array

    }

    drawData(parameterName, dates, values, maxYvalue);  //draw in data for that parameter
  }
  
}

function drawData(_name, _dates, _data, _maxY){
  //print(_dates[0].unix());
  
  //find minimum and maximum time stamps

  let minUnix = min(_dates.map(item => item.unix()));
  //print(minUnix);
  let maxUnix = max(_dates.map(item => item.unix()));
  //print(maxUnix);

  let px = xMargin;
  let py = height-yMargin;
  //graph data 
  for(let i=0; i<_data.length; i++){
    //get y coordinates of points by remapping the values to the y axis
    let y = map(_data[i], 0, _maxY, height - yMargin, 0 + yMargin);
    //get x coordinates of points by remapping the dates to the x axix
    let x = map(_dates[i].unix(), minUnix, maxUnix, xMargin, width - xMargin);
    if(i%100==0){
      noStroke();
      fill(0);
      text(_dates[i].format('MMM D'), x, height - yMargin + 15);
    }
    //set color
    stroke(colors[c]);
    fill(colors[c]);

    //draw data
    ellipse(x, y, 2, 2);

  }

  rect(xMargin+100*v, height-20, 10, 10);
  stroke(0);
  fill(0);
  text(_name, xMargin+20+100*v, height-10);
  v++; //shift over label 
  c++; //move to next

}


function drawAxes(){
    //draw axes
    stroke(0,0,0);
    line(0 + xMargin, height - yMargin, 0 + xMargin, 0 + yMargin); // y axis
    line(0 + xMargin, height - yMargin, width - xMargin, height - yMargin); //x axis
}
