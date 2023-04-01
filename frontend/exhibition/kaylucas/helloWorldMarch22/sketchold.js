//The script retrieves  the most recent PV power data from active server and prints the text on the screen
//reference: https://p5js.org/reference/#/p5/text
// http://solarprotocol.net/guide-api1.html

let testBool = true; // true means you're in test mode 
let SWList = [];
let pigeonList = [];
let roosterList = [];
let robinList = [];
let parrotList = [];
let parakeetList = [];
let seagullList = [];
let bluejayList = [];
let cardinalList = [];
let ravenList = [];
let crowList = [];
let mgullList = [];
let ncardinalList = [];

let foodList = [];
let rainList = [];
let neckColorArray = [];
let roosterNeckArray = [];
let roosterWingArray = [];
let roosterBodyArray = [];
let skyColorArray = [];
let groundColorArray = [];
let bagColorArray = [];
let rainToggle = false;
//indent Shift + Option + F
// 2 
// names {"deviceList":["Swarthmore Solar","Hells Gate","SolarPower for Hackers","Caddie in Control"]} 
// time zones {"tz":["America\/New_York","America\/New_York","Africa\/Khartoum","Australia\/Melbourne"]}
// na, na, Swarthmore, city in Australia, Nairobi, Astoria,

let batteryLevel = 0.0;
let batteryLevelPer = 0.0;
let serverName = '';
let locName = ' ';
let locCity = ' ';
let LocCountry;
let timeOfDay;
let loadPower;

let timer = 0;
let timeOut = 5 * 60 * 1000;
let textDiv;
let walkSpeed = 1;
let totalTiles = 20 // actually divided by 2 :) 
let localHour = 0;
let panelPower;
let timezone;
let serverNum = 0;
let bgColor;
let localTime;
let riseArray = []
let setArray = []
let sunRotation = 0;
let dayNight = false;
let camRot, camRot2;
let primeBirdPecking = false; // test 
let killfood = false;
let globalPecknum = 0;
let nudgeFood = false;
let testStop = false;  // test 
let birdWalkBool = true;
let bwNum = 6;
let camVertNum = 0;
let camHorNum = 0;
//let camHorNum = 0; 

let camView = true;

let batPercentSlider;
let panelPowerSlider;
let hourSlider;
let locationSlider;
let foodFrequency = 30; // how much food there is at any one time. 
let sliderOnce = false;
// create Grass
let pw = 500 / 60
let grassPoints = [];
let showShadow = true;
let showLines = true;
let showLights = true;
let greyScale = true;
let pg;
let yoff = 0



//let bgColorList = [color(255, 100, 100), color(255, 255, 100), color(100, 255, 100), color(100, 255, 255), color(100, 100, 255), color(255, 100, 255), color(200, 200, 255)]


function preload() {
  if (testBool == false) {
    getData();
  }
}

function getData() {
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?value=battery-percentage', gotBatPerData);
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?value=battery-voltage', gotBatData);
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=name', gotName);
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=location', gotLoc);
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=city', gotLocCity);
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=country', gotLocCountry);
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?value=datetime', gotTime);
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?value=load-power', gotPower);
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?value=PV-power-L', gotSolarPower);
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=tz', gotTimeZone);
}

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  camRot = HALF_PI;
  camRot2 = 3.7;
  textFont('Times');
  textSize(16);
  timer = millis();
  textDiv = createDiv('');
  textDiv.style('font-size', '16px');
  textDiv.style('color', 'black');
  textDiv.position(20, 20);

  //https://www.sunrisesunset.com/

  for (let i = -totalTiles; i < totalTiles; i++) {
    SWList.push(new SW(i * 1200, 1200)); // 500, 500
  }
  rectMode(CENTER)
  //camera(0, -400, height / 2 / tan(PI / 6), 300, -100, 200, 0, 1, 0);
  camera(-600, -400, height / 2 / tan(PI / 6), 100, -100, 200, 0, 1, 0);
  // pigeon neck colors
  neckColorArray[0] = color(38, 204, 138); // pink 244, 123, 190  mint green 78, 224, 158
  neckColorArray[1] = color(20, 128, 119); // green
  neckColorArray[2] = color(182, 125, 233); // lite purple 54, 69, 79 209, 125, 233
  neckColorArray[3] = color(138, 110, 202); // 138, 110, 202 purple
  neckColorArray[4] = color(30, 46, 87); //gray 30, 46, 87 

  // rooster neck colors
  roosterNeckArray[0] = color(247, 78, 141); // red pink 247, 78,131
  roosterNeckArray[1] = color(250, 160, 30); // 224, 176, 95 yellow-orange good
  roosterNeckArray[2] = color(105, 67, 114); // purple
  roosterNeckArray[3] = color(20, 128, 119); // darker green //20, 48, 73 green

  // rooster wing colors
  roosterWingArray[0] = color(225, 22, 17); // red orange
  roosterWingArray[1] = color(250, 160, 30); // yellow-orange orange-brown 250, 50, 30
  roosterWingArray[2] = color(20, 128, 119); // darker seagreen 05, 133, 128
  roosterWingArray[3] = color(105, 67, 114); // purple 

  // rooster body colors
  roosterBodyArray[0] = color(30, 46, 87); // navy
  roosterBodyArray[1] = color(250, 160, 30); // 224, 176, 95 yellow-orange good
  roosterBodyArray[2] = color(105, 67, 114); // purple
  roosterBodyArray[3] = color(20, 128, 119); // darker green //20, 48, 73 green

  skyColorArray[0] = color(39, 33, 78); // dark blue
  skyColorArray[1] = color(39, 33, 78); // dark blue
  skyColorArray[2] = color(39, 33, 78); // dark blue
  skyColorArray[3] = color(39, 33, 78); // dark blue
  skyColorArray[4] = color(39, 33, 78); // dark blue
  skyColorArray[5] = color(255, 107, 62); // orange
  skyColorArray[6] = color(255, 107, 62); // orange
  skyColorArray[7] = color(247, 193, 106); // dark yellow
  skyColorArray[8] = color(247, 193, 106); // dark yellow
  skyColorArray[9] = color(255, 239, 122); // light yellow
  skyColorArray[10] = color(255, 239, 122); // light yellow
  skyColorArray[11] = color(181, 214, 224); // light blue
  skyColorArray[12] = color(181, 214, 224); // light blue
  skyColorArray[13] = color(181, 214, 224); // light blue
  skyColorArray[14] = color(181, 214, 224); // light blue
  skyColorArray[15] = color(181, 214, 224); // light blue
  skyColorArray[16] = color(181, 214, 224); // light blue
  skyColorArray[17] = color(255, 239, 122); // light yellow
  skyColorArray[18] = color(255, 239, 122); // light yellow
  skyColorArray[19] = color(247, 193, 106); // dark yellow
  skyColorArray[20] = color(247, 193, 106); // dark yellow
  skyColorArray[21] = color(255, 107, 62); // orange
  skyColorArray[22] = color(255, 107, 62); // orange
  skyColorArray[23] = color(39, 33, 78); // dark blue
  skyColorArray[24] = color(39, 33, 78); // dark blue

  groundColorArray[0] = color(78, 62, 33); // dark blue
  groundColorArray[1] = color(78, 62, 33); // dark blue
  groundColorArray[2] = color(78, 62, 33); // dark blue
  groundColorArray[3] = color(78, 62, 33); // dark blue
  groundColorArray[4] = color(78, 62, 33); // dark blue
  groundColorArray[5] = color(178, 76, 43); // orange
  groundColorArray[6] = color(178, 76, 43); // orange
  groundColorArray[7] = color(173, 149, 74); // dark yellow
  groundColorArray[8] = color(173, 149, 74); // dark yellow
  groundColorArray[9] = color(179, 173, 85); // light yellow
  groundColorArray[10] = color(179, 173, 85); // light yellow
  groundColorArray[11] = color(224, 200, 181); // light blue
  groundColorArray[12] = color(224, 200, 181); // light blue
  groundColorArray[13] = color(224, 200, 181); // light blue
  groundColorArray[14] = color(224, 200, 181); // light blue
  groundColorArray[15] = color(224, 200, 181); // light blue
  groundColorArray[16] = color(224, 200, 181); // light blue
  groundColorArray[17] = color(179, 173, 85); // light yellow
  groundColorArray[18] = color(179, 173, 85); // light yellow
  groundColorArray[19] = color(173, 149, 74); // dark yellow
  groundColorArray[20] = color(173, 149, 74); // dark yellow
  groundColorArray[21] = color(178, 76, 43); // orange
  groundColorArray[22] = color(178, 76, 43); // orange
  groundColorArray[23] = color(78, 62, 33); // dark blue
  groundColorArray[24] = color(78, 62, 33); // dark blue

  bagColorArray[0] = color(70, 105, 74)
  bagColorArray[1] = color(20, 59, 24)
  bagColorArray[2] = color(227, 227, 227)
  bagColorArray[3] = color(51, 70, 166)

  // print(neckColorArray[0])
  // fill(skyColorArray[0])
  updateDiv();
}

function updateTextOnly() {
  textDiv.html(" ", false);

  textDiv.position(20, 20);
  textDiv.html("Active Server: " + serverName + "<br>", true);
  textDiv.html("Battery Voltage: " + batteryLevel + "<br>", true);
  textDiv.html("Battery Voltage %: " + batteryLevelPer + "<br>", true);
  textDiv.html("Load Power: " + loadPower + "<br>", true);
  textDiv.html("Panel Power: " + panelPower + "<br>", true);
  textDiv.html("Location: " + locName + "<br>", true);
  textDiv.html("City: " + locCity + "<br>", true);
  textDiv.html("Country: " + LocCountry + "<br>", true);
  textDiv.html("Local Time / Date: " + timeOfDay + "<br>", true);
  textDiv.html("Local Hour: " + localHour + "<br>", true);
  textDiv.html("Time Zone: " + timezone + "<br>", true);
  if (dayNight) {
    textDiv.html("day " + "<br>", true);
  } else {
    textDiv.html("night " + "<br>", true);
  }
}
function updateDiv() {
  textDiv.html(" ", false);
  if (testBool) {
    batPercentSlider = createSlider(0, 100, 50);
    batPercentSlider.position(170, 56);  // position the slider
    batPercentSlider.input(updateTextOnly);

    panelPowerSlider = createSlider(0, 50, 30);
    panelPowerSlider.position(170, 90);  // position the slider
    panelPowerSlider.input(updateTextOnly);

    hourSlider = createSlider(0, 24, 12);
    hourSlider.position(170, 190);  // position the slider
    hourSlider.input(updateTextOnly);

    locationSlider = createSlider(0, 5, 2);
    locationSlider.position(250, 2100);  // position the slider
    locationSlider.input(updateTextOnly);

    batteryLevel = 12
    batteryLevelPer = batPercentSlider.value() / 100; // was .5

    loadPower = 4
    panelPower = panelPowerSlider.value(); // was 7

    serverName = "Swarthmore Solar"
    locName = "Swarthmore College"

    //locCity = "Swarthmore"  


    switch (locationSlider.value()) {
      case 0:
        locCity = "Swarthmore"
        break;
      case 1:
        locCity = "Nairobi"
        break;
      case 2:
        locCity = "Astoria"
        break;
      case 3:
        locCity = "Sydney"
        break;
      default:
        locCity = "Default"
    }

    LocCountry = "US"

    //timeOfDay = "2023-01-22 23:30:01.053347" 
    timeOfDay = "2023-01-22 " + hourSlider.value() + ":30:01.053347";
    localHour = hourSlider.value();

    timezone = "Africa/Khartoum"
    // bgColor = skyColorArray[localHour]; 
    bgColor = skyColorArray[0];
  }



  let splitString = split(timeOfDay, ' ');

  if (locCity == "Swarthmore") {
    serverNum = 2;
  } else if (locCity == "Nairobi") {
    serverNum = 4;
  } else if (locCity == "Astoria") {
    serverNum = 5;
  } else if (locCity == "Sydney") {
    serverNum = 3;
  }
  else {
    serverNum = 5; // home town bias
    print("new server?");
  }

  let justTime = splitString[1];
  let splitTime = split(justTime, ':');
  localHour = splitTime[0]; // 
  let localMinute = splitTime[1];

  if (testBool) {
    localHour = hourSlider.value()
    localMinute = 30;
  }
  //localHour = 14; // test 


  let totalMinutes = int(localHour * 60 + localMinute);

  let dateArray = split(splitString[0], '-'); // split the date up 
  let y = dateArray[0]
  let m = dateArray[1]
  let d = dateArray[2]

  riseArray[2] = ["7:21", "7:07", "6:31", "6:40", "5:55", "5:28", "5:29", "5:53", "6:23", "6:53", "7:26", "7:01"] // Philly
  riseArray[5] = ["7:21", "7:07", "6:31", "6:40", "5:55", "5:28", "5:29", "5:53", "6:23", "6:53", "7:26", "7:01"] // nyc
  riseArray[3] = ["5:47", "6:16", "6:43", "7:07", "6:29", "6:51", "7:01", "6:48", "6:14", "6:33", "5:55", "5:37"] // Sydney
  riseArray[4] = ["6:30", "6:41", "6:41", "6:34", "6:28", "6:29", "6:35", "6:37", "6:30", "6:19", "6:12", "6:16"] // Nairobi

  setArray[2] = ["16:38", "17:12", "17:46", "19:20", "19:51", "20:20", "20:31", "20:13", "19:30", "18:40", "17:54", "16:30"] // Philly
  setArray[5] = ["16:38", "17:12", "17:46", "19:20", "19:51", "20:20", "20:31", "20:13", "19:30", "18:40", "17:54", "16:30"] // nyc
  setArray[3] = ["20:09", "20:01", "19:33", "18:52", "17:15", "16:54", "16:57", "17:15", "17:37", "18:57", "19:22", "19:50"] // Sydney
  setArray[4] = ["18:42", "18:51", "18:49", "18:40", "18:32", "18:32", "18:38", "18:41", "18:36", "18:26", "18:21", "18:27"] // Nairobi


  let sp = riseArray[serverNum];

  let sunR = split(riseArray[serverNum][m - 1], ':');
  let sunRTotal = int((sunR[0] * 60 + sunR[1]))
  let sunS = split(setArray[serverNum][m - 1], ':');
  let sunSTotal = int((sunS[0] * 60 + sunS[1]))


  if (totalMinutes > sunRTotal && totalMinutes < sunSTotal) {
    dayNight = true;

  } else {
    dayNight = false;

  }
  sunRotation = map(totalMinutes, sunRTotal, sunSTotal, TWO_PI, PI);

  textDiv.html("Active Server: " + serverName + "<br>", true);
  textDiv.html("Battery Voltage: " + batteryLevel + "<br>", true);
  textDiv.html("Battery Life %: " + batteryLevelPer * 100 + "<br>", true);
  textDiv.html("Load Power: " + loadPower + "<br>", true);
  textDiv.html("Panel Power: " + panelPower + "<br>", true);
  textDiv.html("Location: " + locName + "<br>", true);
  textDiv.html("City: " + locCity + "<br>", true);
  textDiv.html("Country: " + LocCountry + "<br>", true);
  textDiv.html("Local Time / Date: " + timeOfDay + "<br>", true);
  textDiv.html("Local Hour: " + localHour + "<br>", true);
  textDiv.html("Time Zone: " + timezone + "<br>", true);
  if (dayNight) {
    textDiv.html("day " + "<br>", true);
  } else {
    textDiv.html("night " + "<br>", true);
  }

  // let bgColorList = [color(255, 100, 100), color(255, 255, 100), color(100, 255, 100), color(100, 255, 255), color(100, 100, 255), color(255, 100, 255), color(200, 200, 255)]

  // bgColor = bgColorList[serverNum];
  //print(skyColorArray[0])

  if (localHour < 5) {
    foodFrequency = 12
  }
  if (localHour >= 5 && localHour < 10) {
    foodFrequency = 22
  }
  if (localHour >= 10 && localHour < 17) {
    foodFrequency = 14
  }
  if (localHour >= 17 && localHour < 21) {
    foodFrequency = 22
  }
  if (localHour > 21) {
    foodFrequency = 12
  }

  for (let i = 0; i < foodFrequency - 6; i++) { // 20 
    foodList.push(new food(random(-5000, 5000), random(-800, 800), false));
  }
  for (let i = 0; i < 6; i++) {
    foodList.push(new food(random(-5000, 5000), random(-200, 200), false)); // put more in the middle 
  }
  for (let i = 0; i < 5; i++) {
    let tside = -500 - random(500)
    if (random(2) < 1) {
      tside = 500 + random(500)
    }
    foodList.push(new food(random(-5000, 5000), tside, true)); // put more in the middle 
  }

  makePigeons(); 
  // makeRoosters();
  // makeRobins()
  // makeParrots()
  //makeParakeets()
  // makeSeagulls(); 
  // makeBluejays();
  //makeCardinals()
  // makeNCardinals()
  // makeRavens();
  // makeCrows();
  // makeMgulls();
}

function clearAll() {
  roosterList = []; // 1
  pigeonList = []; //2 
  robinList = []; // 3
  parrotList = []; //4 
  parakeetList = []; // 7
  seagullList = []; // 5
  bluejayList = []; // 6
  cardinalList = []; // 8
  ravenList = []; // 8
  crowList = []; // 9
  mgullList = []; // 10
  ncardinalList = [];
}
function makePigeons() {
  print("hey"); 
  clearAll();
  if (camView) {
    pigeonList.push(new pigeon(true, 0, 0, -64, 0)); // hero pigeon was -114
  }
  //pigeonList.push(new pigeon(true, 0, 0, -114, 0)); // hero pigeon
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    pigeonList.push(new pigeon(false, random(TWO_PI), rx, -64, rz));
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    pigeonList.push(new pigeon(false, random(TWO_PI), rx, -64, rz));
  }
}
function makeRoosters() {
  clearAll();
  roosterList.push(new rooster(true, 0, 0, -114, 0)); // hero pigeon
  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    roosterList.push(new rooster(false, random(TWO_PI), rx, -114, rz));
  }
  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    roosterList.push(new rooster(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeParrots() {
  clearAll();
  parrotList.push(new parrot(true, 0, 0, -114, 0)); // hero bird
  for(let i = 0; i < 1; i++){ // sideline birds
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    parrotList.push(new parrot(false, random(TWO_PI), rx, -114, rz));
  }
  for(let i = 0; i < 1; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    parrotList.push(new parrot(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeRavens() {
  clearAll();
  ravenList.push(new raven(true, 0, 0, -114, 0)); // hero bird
  for(let i = 0; i < 1; i++){ // sideline birds
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    ravenList.push(new raven(false, random(TWO_PI), rx, -114, rz));
  }
  for(let i = 0; i < 1; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    ravenList.push(new raven(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeCrows() {
  clearAll();
  crowList.push(new crow(true, 0, 0, -114, 0)); // hero bird
  for(let i = 0; i < 1; i++){ // sideline birds
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    crowList.push(new crow(false, random(TWO_PI), rx, -114, rz));
  }
  for(let i = 0; i < 1; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    crowList.push(new crow(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeParakeets() {
  clearAll();
  parakeetList.push(new parakeet(true, 0, 0, -114, 0)); // hero bird
  for(let i = 0; i < 1; i++){ // sideline birds
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    parakeetList.push(new parakeet(false, random(TWO_PI), rx, -114, rz));
  }
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    parakeetList.push(new parakeet(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeRobins() {
  clearAll();
  robinList.push(new robin(true, 0, 0, -94, 0)); // hero Robing
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    robinList.push(new robin(false, random(TWO_PI), rx, -94, rz));
  }
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    robinList.push(new robin(false, random(TWO_PI), rx, -94, rz));
  }
}

function makeSeagulls() {
  clearAll();
  seagullList.push(new seagull(true, 0, 0, -114, 0)); // hero seagull
  for(let i = 0; i < 1; i++){
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    seagullList.push(new seagull(false, random(TWO_PI), rx, -114, rz));
  }
  for(let i = 0; i < 1; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    seagullList.push(new seagull(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeBluejays() {
  clearAll();
  bluejayList.push(new bluejay(true, 0, 0, -114, 0)); // hero bluejay
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    bluejayList.push(new bluejay(false, random(TWO_PI), rx, -114, rz));
  }
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    bluejayList.push(new bluejay(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeCardinals() {
  clearAll();
  cardinalList.push(new cardinal(true, 0, 0, -114, 0)); // hero cardinal
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    cardinalList.push(new cardinal(false, random(TWO_PI), rx, -114, rz));
  }
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    cardinalList.push(new cardinal(false, random(TWO_PI), rx, -114, rz));
  }
}
function makeNCardinals() {
  clearAll();
  ncardinalList.push(new ncardinal(true, 0, 0, -114, 0)); // hero cardinal
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    ncardinalList.push(new ncardinal(false, random(TWO_PI), rx, -114, rz));
  }
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    ncardinalList.push(new ncardinal(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeMgulls() {
  clearAll();
  mgullList.push(new mgull(true, 0, 0, -114, 0)); // hero bird
  for(let i = 0; i < 2; i++){ // sideline birds
    let rx = random (-5000, 5000)
    let rz = random (-3000, -200)
    mgullList.push(new mgull(false, random(TWO_PI), rx, -114, rz));
  }
  for(let i = 0; i < 2; i++){
    let rx = random (-5000, 5000)
    let rz = random (3000, 200)
    mgullList.push(new mgull(false, random(TWO_PI), rx, -114, rz));
  }
}

function keyPressed() {
  if (key == 'q') {
    showShadow = !showShadow;
  }
  if (key == 'w') {
    showLines = !showLines;
  }
  if (key == 'e') {
    showLights = !showLights;
  }
  if (key == 'r') {
    greyScale = !greyScale;
  }

  if (key == 'p') {
    primeBirdPecking = !primeBirdPecking;
  }
  if (key == 's') {
    testStop = !testStop;
  }
  if (key == 'r') {
    //rainList
    rainToggle = !rainToggle;
    if (rainToggle) {
      for (let i = 0; i < 60; i++) {
        // 10 * 500 each direction
        rainList.push(new rain());
      }
    }
    else {
      rainList = [];
    }
  }
  if (key == 'v') {
    camView = !camView;

    pigeonList = [];
    if (camView) {
      pigeonList.push(new pigeon(true, 0, 0, -92, 0)); // hero pigeon was -114
    }
    for (let i = 0; i < 2; i++) {
      let rx = random(-5000, 5000)
      let rz = random(-3000, -200)
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -92, rz));
    }
    for (let i = 0; i < 2; i++) {
      let rx = random(-5000, 5000)
      let rz = random(3000, 200)
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -92, rz));
    }

  }


  if (key == '1') {
    makePigeons();
  }
  if (key == '2') {
    makeRoosters();
  }

  if (key == '3') {
    makeRobins();
  }

  if (key == '4') {
    makeParakeets();
  }
  if (key == '5') {
    makeSeagulls();
  }
  if (key == '6') {
    makeBluejays();
  }
  if (key == '7') {
    makeCardinals();
  }
  if (key == 'n') {
    makeNCardinals();
  }
  if (key == '8') {
    makeRavens();
  }
  if (key == '9') {
    makeCrows();
  }
  if (key == '9') {
    makeMgulls();
  }
  if (key == '0') {
    makeParrots();
  }
}
function draw() {
  showShadow
  showLines
  showLights
  greyScale

  // bwNum = 6; 
  let greyNum = 12;
  let noLightsNum = 26;
  let lightsOnNum = 35;

  if (panelPower < bwNum) { // black and white
    textDiv.style('color', 'white');
  } else {
    textDiv.style('color', 'black');
  }
  if (panelPower >= bwNum && panelPower < greyNum) { // greyscale
    showShadow = false;
    showLines = false;
    showLights = false;
    greyScale = true;
  }
  if (panelPower >= greyNum && panelPower < noLightsNum) { // no lights color
    showShadow = false;
    showLines = false;
    showLights = false;
    greyScale = false;
  }
  if (panelPower >= noLightsNum && panelPower < lightsOnNum) { // lights on 
    showShadow = false;
    showLines = false;
    showLights = true;
    greyScale = false;
  }
  if (panelPower >= lightsOnNum) { // lights on shaddow on
    showShadow = true;
    showLines = false;
    showLights = true;
    greyScale = false;
  }
  // if (sliderOnce == true && !mouseIsPressed) {
  //   sliderOnce = false; 
  // }

  let x = 0;
  x = parseInt(localHour);
  //localHour = 0
  let mapsky = int(map(localHour, 0, 24, 0, skyColorArray.length - 1));
  bgColor = skyColorArray[localHour];
  background(bgColor) // 200 
  if (panelPower < greyNum){
    background(200);
  }
  if (panelPower < bwNum) {
    background(1);
  } 

 

  if (localHour > 8 && localHour < 16 && panelPower < 12) {
    if (rainToggle == false) {
      rainToggle = true;
      for (let i = 0; i < 60; i++) {
        // 10 * 500 each direction
        rainList.push(new rain());
      }
    }
  }
  else {
    rainToggle = false;
    if (rainList.length > 0) {
      rainList = [];
    }
  }

  if (testBool) {
    batteryLevel = 12
    batteryLevelPer = batPercentSlider.value() / 100
    loadPower = 4
    //panelPower = 7
    panelPower = panelPowerSlider.value(); // was 7
    serverName = "Swarthmore Solar"
    locName = "Swarthmore College"

    //   serverNum = 2;
    // } else if (locCity == "Nairobi") {
    //   serverNum = 4;
    // } else if (locCity == "Astoria") {
    //   serverNum = 5;
    // } else if (locCity == "Sydney") {
    //   serverNum = 3;
    // }

    switch (locationSlider.value()) {
      case 0:
        locCity = "Swarthmore"
        serverNum = 2;
        break;
      case 1:
        locCity = "Nairobi"
        serverNum = 4;
        break;
      case 2:
        locCity = "Astoria"
        serverNum = 5;
        break;
      case 3:
        locCity = "Sydney"
        serverNum = 3;
        break;
      default:
        locCity = "Astoria"
        serverNum = 5;
    }
    //bgColor = bgColorList[serverNum];
    LocCountry = "US"
    timeOfDay = "2023-01-22 " + hourSlider.value() + ":30:01.053347";
    //timeOfDay = "2023-01-22 23:59:01.053347" 
    timezone = "Africa/Khartoum"
    //  if(testBool){
    localHour = hourSlider.value()
    localMinute = 30;
    // }
  }


  if (camView) { // side of bird

    if (mouseIsPressed) {
      camRot += (mouseX - pmouseX) / 200;
      camRot2 += (mouseY - pmouseY) / 200;
      //3.2 4.2
      camRot2 = constrain(camRot2, 3.2, 4, 2);
    }
    let cx = cos(camRot) * 600 // as 10000 
    let cz = sin(camRot) * 600

    let cy = sin(camRot2) * 600 // as 10000 


    // camera(cx, -500, cz, 0, -100, 0, 0, 1, 0); // side view do not destroy
    camera(cx, cy, cz, 0, -100, 0, 0, 1, 0); // side view do not destroy

  } else { // bird eye view
    //rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    let cLoc = createVector(0, -300, 0,);
    let camBobAdd = map(walkSpeed, 1, 6, .001, .1)

    camVertNum += camBobAdd;
    camHorNum += camBobAdd;

    let camVert = sin(camVertNum) * 12
    cLoc.y = -200 + camVert; // was -200
    let mNum = random(20, 30) // random jerky 
    let camHor = sin(camHorNum * 3) * mNum

    cLoc.x = camHor;

    camera(cLoc.x, cLoc.y, cLoc.z, 500, cLoc.y, 0, 0, 1, 0);
  }
  //orbitControl();

  if (testBool) {
    sunRotation = map(hourSlider.value(), 0, 24, TWO_PI, PI);
  }
  // the sun has a direction and a point light. 
  if (showLights) {
    //print("hey Lights")
    let ldirZ = map(sunRotation, PI, TWO_PI, .5, -.5);
    let ldirY = 1 - (abs(sin(ldirZ))); //map(mouseY, 0, height, .75, -.25)
    directionalLight(255, 255, 200, 0, ldirY, ldirZ);
    directionalLight(255, 255, 200, -1, 0, 0);

    let pRot = map(mouseY, 0, height, 0, TWO_PI); //sunRotation; 
    if (!dayNight) {
      sunRotation = 3;  // not necessary but looks cool
    }
    let pz = cos(sunRotation + PI) * 700 // sun distance
    let py = sin(sunRotation) * 700
    //pointLight(255, 255, 255 , 400, py, pz);
    pointLight(255, 255, 255, 400, 40, 700); // 400, 20, 700
  }
  // if(!primeBirdPecking ){
  //   walkSpeed = map(batteryLevelPer, 0, 1, .2, 12)
  // }else {
  //   walkSpeed = 0; 
  // }
  if (birdWalkBool) {
    walkSpeed = map(batteryLevelPer, 0, 1, .2, 12)
  } else {
    walkSpeed = 0;
  }
  if (testStop) {
    walkSpeed = 0;
  }
  let bob = sin(frameCount / 6) * walkSpeed

  //every 5 minutes call the API again to update the data
  if (millis() - timer >= timeOut && testBool == false) { // timeOut
    print("get Server");
    textDiv.html(" ", false);
    getData()
    updateDiv();
    timer = millis();
  }
  for (let i = 0; i < SWList.length; i++) {
    // for (let i = SWList.length -1; i >= 0; i--) {
    if (SWList[i].reset) {
      if (i == 0) {
        SWList[i].loc.x = SWList[SWList.length - 1].loc.x + SWList[i].SWSize;
      }
      else {
        SWList[i].loc.x = SWList[i - 1].loc.x + SWList[i].SWSize + walkSpeed; // test 
      }
      SWList[i].reset = false;
    }
    SWList[i].display();
  }


  for (let i = 0; i < pigeonList.length; i++) {
    pigeonList[i].display();
  }

  for (let i = 0; i < rainList.length; i++) {
    rainList[i].display();
  }
  for (let i = 0; i < ravenList.length; i++) {
    ravenList[i].display();
  }

  for (let i = 0; i < roosterList.length; i++) {
    roosterList[i].display();
  }
  for (let i = 0; i < robinList.length; i++) {
    robinList[i].display();
  }

  for (let i = 0; i < parrotList.length; i++) {
    parrotList[i].display();
  }

  for (let i = 0; i < parakeetList.length; i++) {
    parakeetList[i].display();
  }

  for (let i = 0; i < seagullList.length; i++) {
    seagullList[i].display();
  }

  for (let i = 0; i < bluejayList.length; i++) {
    bluejayList[i].display();
  }

  for (let i = 0; i < cardinalList.length; i++) {
    cardinalList[i].display();
  }
  for (let i = 0; i < ncardinalList.length; i++) {
    ncardinalList[i].display();
  }
  for (let i = 0; i < crowList.length; i++) {
    crowList[i].display();
  }
  for (let i = 0; i < mgullList.length; i++) {
    mgullList[i].display();
  }

  for (let i = 0; i < foodList.length; i++) {
    foodList[i].display();
  }
  for (let i = foodList.length - 1; i >= 0; i--) {
    if (foodList[i].remove) {
      foodList.splice(i, 1);
    }
  }
  if (foodList.length < foodFrequency) {
    foodList.push(new food(5000, random(-800, 800)));
  }

  push()  // ground plane and horzon
  translate(0, 10, 0);
  noStroke()
  fill(groundColorArray[localHour])
  if (panelPower < greyNum){
    fill(80);
  }
  if (panelPower < bwNum) {
    fill(1);
  }
 

  cylinder(15000, 2);
  pop()

  // push()
  // translate(0, -100 + bob, 0)
  // sphere(80)
  // pop()

  // Sun
  if (dayNight) {
    push()
    translate(1600, 0, 0)
    let rot = map(mouseY, 0, height, TWO_PI, PI) // this is correct 
    rotateX(sunRotation) // sunRotation
    // box(10, 10, 400)
    translate(0, 0, -500)

    fill(255, 255, 0)
    noStroke()
    emissiveMaterial(200, 200, 0);
    // sphere(50);
    pop()
  }
  //  push()  // ground plane and horzon
  //  translate(0, 10, 0); 
  //  noStroke()
  //  fill(150, 130, 130)
  //  cylinder(10000, 2);
  //  pop()

}
class rain {
  constructor() {
    this.loc = createVector(random(-1000, 1600), random(-20, -2000), random(-1000, 1000))
    this.falling = true;
    this.timer = 0;
    this.rSpeed = random(8, 12)
    this.puddleSize = 1
  }
  display() {
    this.loc.x -= walkSpeed;
    if (this.falling) {
      this.loc.y += this.rSpeed;
    }
    if (this.loc.y >= -10) {
      this.falling = false
      //this.loc.y = 0
      this.timer++;
      this.puddleSize += .5
      if (this.timer > 100) {
        let mR = map(walkSpeed, 1, 12, 1600, 2600);
        this.loc.x = random(-500, mR);
        this.loc.y = random(-1000, -1500);
        this.loc.xz = random(-1000, 1000);
        this.falling = true;
        this.timer = 0;
        this.puddleSize = 1;

      }
    }
    push()
    translate(this.loc.x, this.loc.y, this.loc.z)
    stroke(100, 180, 255)
    if (panelPower < bwNum) {
      stroke(255)
    }
    if (this.falling == true) {
      line(0, 0, 0, 0, -40, 0)
    } else {
      rotateX(HALF_PI)
      fill(180, 220, 255, 100 - this.timer)
      ellipse(0, 0, this.puddleSize)
    }
    pop()
  }

}

class SW {
  constructor(_x, _s) {
    this.loc = createVector(_x, 0, 0);
    this.SWSize = _s;
    this.reset = false;
    this.SXColor = color(random(180, 220), random(180, 200), random(180, 200));
    this.SXGrey = color(random(100, 200));
    this.pg = createGraphics(this.SWSize, 200);
    this.grassPoints = [];
    // let pw =  this.SWSize / 60
    // let yoff = 0
    // for(let i = 0; i < 60; i++){
    //    yoff += 0.5;
    //   this.grassPoints[i]  = noise(yoff); 
    // }
    // this.grassPoints[60] = this.grassPoints[0]; 
    // this.pg.stroke(255); 

    // for(let i = 0; i < this.grassPoints.length -1; i++){
    //   this.pg.line(i * pw, this.grassPoints[i] * 40, (i + 1) * pw, this.grassPoints[i + 1] * 40); 
    // }

  }
  display() {
    // if(greyScale){
    //   this.SXColor
    // }
    this.loc.x -= walkSpeed;
    if (this.loc.x <= -totalTiles * this.SWSize) {
      //this.loc.x = 20 * this.SWSize
      this.reset = true;
    }
    push()
    translate(this.loc.x, this.loc.y, this.loc.z)
    //box(this.SWSize, 5, this.SWSize);
    rotateX(HALF_PI);
    fill(this.SXColor);
    if (greyScale) {
      fill(this.SXGrey);
    }
    stroke(1);
    if (!showLines) {
      noStroke();
    }
    if (panelPower < bwNum) {
      fill(1)
      stroke(255)
    }
    rect(0, 0, this.SWSize, this.SWSize)
    // rotateX(-HALF_PI);
    // translate(-this.SWSize/2, -200, -this.SWSize/2); 
    // image(pg, 0, 0, this.SWSize);
    pop()

  }
}



function gotBatData(tempData) {
  // console.log(tempData);
  resKeys = Object.keys(tempData);
  batteryLevel = tempData[resKeys[0]];
}
function gotBatPerData(tempData) {
  resKeys = Object.keys(tempData);
  batteryLevelPer = tempData[resKeys[0]];
}
function gotPower(tempData) {
  resKeys = Object.keys(tempData);
  loadPower = tempData[resKeys[0]];
}
function gotSolarPower(tempData) {
  resKeys = Object.keys(tempData);
  panelPower = tempData[resKeys[0]];
}
function gotName(tempData) {
  resKeys = Object.keys(tempData);
  serverName = tempData[resKeys[0]];
}
function gotLoc(tempData) {
  resKeys = Object.keys(tempData);
  locName = tempData[resKeys[0]];

}
function gotLocCity(tempData) {
  resKeys = Object.keys(tempData);
  locCity = tempData[resKeys[0]];

}
function gotLocCountry(tempData) {
  resKeys = Object.keys(tempData);
  LocCountry = tempData[resKeys[0]];
}
function gotTime(tempData) {
  resKeys = Object.keys(tempData);
  timeOfDay = tempData[resKeys[0]];

}

function gotTimeZone(tempData) {
  resKeys = Object.keys(tempData);
  timezone = tempData[resKeys[0]];

}






