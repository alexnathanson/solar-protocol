//The script retrieves  the most recent PV power data from active server and prints the text on the screen
//reference: https://p5js.org/reference/#/p5/text
// http://solarprotocol.net/guide-api1.html

let testBool = true ; // true means you're in test mode 

let birdNames = []
// let birdNames = ["American Robin", "Rock Pigeon", "Blue Jay", "Australian Raven", "Australian Ringneck", "Rainbow Rooster", "Red-crested Cardinal", "Laughing Gull", "Mediterranean Gull", "Northern Cardinal", "Carrion Crow", "Rock Pigeon"]
let birdNum = 0;
let todArray = ["Dawn", "Morning", "Late Morning", "Midday", "Afternoon", "Evening", "Dusk", "Night"];
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
let chickenlList = [];
let foodList = [];
let rainList = [];
let neckColorArray = [];
let roosterNeckArray = [];
let roosterWingArray = [];
let roosterBodyArray = [];
let skyColorArray = [];
let groundColorArray = [];
let sideWalkColorArray = [];
let SWrandomNum = 0;
let bagColorArray = [];
let rainToggle = false;
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
let localMinute = 0;
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
let primePeckingBuffer = false;
let primePeckingBufferNum = 0;
let killfood = false;
let globalPecknum = 0;
let nudgeFood = false;
let testStop = false;  // test 
let birdWalkBool = true;
let bwNum = 2;  //  up to this number it's b/w // was 6
let greyNum = 6; // 12
let noLightsNum = 12; // 26
let lightsOnNum = 25; // 35
let camVertNum = 0;
let camHorNum = 0;
let camView = true;
let batPercentSlider;
let panelPowerSlider;
let hourSlider;
let foodFrequency = 30; // how much food there is at any one time. 
let sliderOnce = false;
let pw = 500 / 60
let grassPoints = [];
let showShadow = true;
let showLines = true;
let showLights = true;
let greyScale = true;
let pg;
let yoff = 0
let globalPecking = false;
let cameraPecking = false;
let birdSteps = 0;
let oldBirdSteps = 0;
let foodPecked = 0;
let oldfoodPecked = 0;
let foodPeckedCounter = 0;
let streetLightX = 500;
let camTimer, povTimer;
let viewReadyToggle = false;
let povTimeLenght = 20 * 1000; // 20 seconds 
let camTimerLength = 120 * 1000; // two minutes 
let lookPoint;
let lookRot = 0;
let POVtoggle = true;
let birdNameLangNum = 0; 
let globalFlying = false; 
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
  lookPoint = createVector(500, -200, 0);
  camTimer = millis();
  povTimer = 0;
  camRot = HALF_PI;
  camRot2 = 3.7;
  textFont('Times');
  textSize(16);
  timer = millis();
  textDiv = createDiv('');
  textDiv.style('font-size', '16px');
  textDiv.style('color', 'black');
  textDiv.position(20, 20);
  rectMode(CENTER)

  birdNames [0] = ["American Robin (English)", "chiskukus (Lenape)",  "name three Robin"]; 
  birdNames [1] = ["Blue Jay (English)", "Teri-Teri (Mohawk)",  "diindiisi (Ojibwe)", "gwiingwiish (Ojibwe)", "Geai bleu (French)"]; 
  birdNames [2] = ["Australian Raven (English)", "angepe urrperle (Arrernte / Arandic)",  "uthipe (Western Arrarnta)" ]; 
  birdNames [3] = ["Australian Ringneck (English)", "arlpatye (Arrernte)", "Twenty-eight Parrot (English)", "darlmoorluk (Noongar)", "dowarn (Noongar)", "doomolok (Noongar)"]; 
  birdNames [4] = ["Rainbow Rooster (English)",  "jogoo wa upinde wa mvua (Swahili)", "nyũngũ ya mbura (Kikuyu"]; 
  birdNames [5] = ["Red-crested Cardinal (English)", "name two Cardinal", "name three Cardinal"]; 
  birdNames [6] = ["Laughing Gull (English)", "gua-tibiri (Tíano)", "gaviota (Spanish)"]; 
  birdNames [7] = ["Mediterranean Gull (English)", "gaviota (Dominican Spanish)", "Gaviota Cabecinegra (Spanish)"]; 
  birdNames [8] = ["Northern Cardinal (English)", "hmukwinùnd (Munsee Delaware / Lenape)", "cit (Mohegan)"]; 
  birdNames [9] = ["Carrion Crow (English)", "xiǎo zuǐ wūyā (Mandarin)", "shí fǔròu wū-yā (Mandarin)"]; 
  birdNames [10] = ["Rock Pigeon (English)", "cit (Mohegan)", "amimi (Munsee Delaware / Lenape)"];

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
  // sky colors
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
  // ground colors 
  groundColorArray[0] = color(78, 62, 33); // dark blue
  groundColorArray[1] = color(78, 62, 33); // dark blue
  groundColorArray[2] = color(78, 62, 33); // dark blue
  groundColorArray[3] = color(78, 62, 33); // dark blue
  groundColorArray[4] = color(78, 62, 33); // dark blue
  groundColorArray[5] = color(128, 100, 92); // orange
  groundColorArray[6] = color(128, 100, 92); // orange
  groundColorArray[7] = color(165, 217, 125); // dark yellow
  groundColorArray[8] = color(165, 217, 125); // dark yellow
  groundColorArray[9] = color(146, 255, 176); // light yellow
  groundColorArray[10] = color(146, 255, 176); // light yellow
  groundColorArray[11] = color(128, 125, 103); // light blue 224, 200, 181
  groundColorArray[12] = color(128, 125, 103); // light blue
  groundColorArray[13] = color(128, 125, 103); // light blue //224, 200, 181
  groundColorArray[14] = color(128, 125, 103); // light blue
  groundColorArray[15] = color(128, 125, 103); // light blue
  groundColorArray[16] = color(128, 125, 103); // light blue
  groundColorArray[17] = color(146, 255, 176); // light yellow //color(179, 173, 85)
  groundColorArray[18] = color(146, 255, 176); // light yellow //color(179, 173, 85)
  groundColorArray[19] = color(165, 217, 125); // dark yellow //173, 149, 74
  groundColorArray[20] = color(165, 217, 125); // dark yellow //173, 149, 74
  groundColorArray[21] = color(128, 100, 92); // orange // 178, 76, 43
  groundColorArray[22] = color(128, 100, 92); // orange //178, 76, 43
  groundColorArray[23] = color(78, 62, 33); // dark blue
  groundColorArray[24] = color(78, 62, 33); // dark blue
  // background colors 
  bagColorArray[0] = color(70, 105, 74)
  bagColorArray[1] = color(20, 59, 24)
  bagColorArray[2] = color(227, 227, 227)
  bagColorArray[3] = color(51, 70, 166)
  // sidewalk colors 
  sideWalkColorArray[0] = [color(128, 126, 120), color(57, 61, 71), color(99, 102, 106), color(54, 69, 79), color(110, 98, 89), color(96, 98, 99), color(82, 81, 83), color(102, 92, 89)]
  sideWalkColorArray[1] = [color(118, 134, 146), color(128, 126, 120), color(136, 139, 141), color(131, 145, 161), color(99, 102, 106), color(110, 98, 89), color(137, 142, 140), color(120, 121, 118)]
  sideWalkColorArray[2] = [color(178, 190, 181), color(140, 146, 172), color(165, 169, 160), color(151, 153, 155), color(168, 169, 173), color(172, 167, 158), color(133, 138, 126), color(207, 207, 196)]
  sideWalkColorArray[3] = [color(178, 190, 181), color(140, 146, 172), color(165, 169, 160), color(151, 153, 155), color(168, 169, 173), color(172, 167, 158), color(133, 138, 126), color(207, 207, 196)]
  sideWalkColorArray[4] = [color(178, 190, 181), color(140, 146, 172), color(165, 169, 160), color(151, 153, 155), color(168, 169, 173), color(172, 167, 158), color(133, 138, 126), color(207, 207, 196)]
  for (let i = -totalTiles; i < totalTiles; i++) {
    SWList.push(new SW(i * 1200, 1200)); // 500, 500
  }
  updateDiv();
}

function updateTextOnly() {
  let ampm = "AM";
  if (localHour >= 12) {
    ampm = "PM";
  }
  let hour12 = localHour % 12;
  if (hour12 == 0) {
    hour12 = 12;
  }
  let todNum = 0;
  if (localHour >= 5 && localHour < 7) {
    todNum = 0;
  }
  if (localHour >= 7 && localHour < 9) {
    todNum = 1;
  }
  if (localHour >= 9 && localHour < 11) {
    todNum = 2;
  }
  if (localHour >= 11 && localHour < 13) { // midday
    todNum = 3;
  }
  if (localHour >= 13 && localHour < 17) { // afternoon
    todNum = 4;
  }
  if (localHour >= 17 && localHour < 20) { // evening
    todNum = 5;
  }
  if (localHour >= 20 && localHour < 22) { // dust
    todNum = 6;
  }
  if (localHour >= 22 || localHour < 5) { // night
    todNum = 7;
  }
  textDiv.html(" ", false);
  textDiv.position(20, 20);
  textDiv.html("SERVER" + "<br>", true);
  textDiv.html("Name: " + serverName + "<br>", true);
  textDiv.html("Battery Level: " + int(batteryLevelPer * 100) + "%" + "<br>", true);
  textDiv.html("Panel Power: " + panelPower + "<br><br>", true);
  textDiv.html("LOCATION" + "<br>", true);
  textDiv.html("City/Country: " + locCity + ", " + LocCountry + "<br>", true);
  textDiv.html("Local Time: " + hour12 + ":" + nf(localMinute, 2, 0) + " " + ampm + "<br>", true);
  textDiv.html("Time of day: " + todArray[todNum] + "<br>", true);
  if (rainToggle) {
    textDiv.html("Weather: Overcast, Chance of Precipitation" + "<br><br>", true);
  } else {
    textDiv.html("Weather: Clear" + "<br><br>", true);
  }
  textDiv.html("LOCAL SCENE" + "<br>", true);
 // textDiv.html("Being: " + birdNames[birdNum][0] + "<br>", true);
  textDiv.html("Being: " + birdNames[birdNum][birdNameLangNum] + "<br>", true);
  let sp;
  if (batteryLevelPer < .50) {
    sp = "Slow";
  }
  if (batteryLevelPer >= .50 && batteryLevelPer < .75) {
    sp = "Moderate";
  }
  if (batteryLevelPer >= .75) {
    sp = "Fast";
  }
  if (testBool) {
    birdSteps
    textDiv.html("Steps: " + birdSteps + "<br>", true);
    textDiv.html("Pecks: " + foodPeckedCounter + "<br>", true);
    //  textDiv.html("Press 'V' key to toggle Being POV ON/OFF" + "<br>", true);
  }
  textDiv.html("Speed: " + sp + "<br>", true);
  let gl;
  if (panelPower < bwNum) {
    gl = "Wireframe";
  }
  if (panelPower >= bwNum && panelPower < greyNum) {
    gl = "Grayscale";
  }
  if (panelPower >= greyNum && panelPower < noLightsNum) {
    gl = "Color";
  }
  if (panelPower >= noLightsNum && panelPower < lightsOnNum) {
    gl = "Light";
  }
  if (panelPower >= lightsOnNum) {
    gl = "Light & Shadow";
  }
  textDiv.html("Graphics: " + gl + "<br>", true);
  if (camView) {
    textDiv.html("Camera: Drag to Orbit View" + "<br>", true);
  } else {
    textDiv.html("Camera: Being POV" + "<br>", true);
  }
  textDiv.html("Press 'V' to toggle Being POV on/off" + "<br>", true);
}
function updateDiv() {
  textDiv.html(" ", false);
  //print("hey");
  if (testBool) { // make the sliders in test mode 
    batPercentSlider = createSlider(0, 100, 50);
    batPercentSlider.position(200, 55);  // position the slider
    batPercentSlider.input(updateTextOnly);
    panelPowerSlider = createSlider(0, 50, 30);
    panelPowerSlider.position(200, 76);  // position the slider
    panelPowerSlider.input(updateTextOnly);
    hourSlider = createSlider(0, 24, 12);
    hourSlider.position(200, 168);  // position the slider
    hourSlider.input(updateTextOnly);
    batteryLevel = 12
    batteryLevelPer = batPercentSlider.value() / 100; // was .5
    loadPower = 4
    panelPower = panelPowerSlider.value(); // was 7
    serverName = "Low-Carbon Research Methods"
    locName = "Peterborough"
    locCity =  "Peterborough"; 
    LocCountry = "Canada"
    timeOfDay = "2023-03-23 " + hourSlider.value() + ":30:01.053347";
    timezone = "EST"
    bgColor = skyColorArray[0];
  }

  switch (locCity) {
    case "Swarthmore": // American Robin
      makeRobins();
      birdNum = 0;
      break;
    case "Astoria": // Rock Pigeon
      makePigeons();
      birdNum = 1;
      break;
    case "Peterborough": // Blue Jay
      makeBluejays();
      birdNum = 2;
      break;
    case "Syndney": // Australian Raven
      makeRavens();
      birdNum = 3;
      break;
    case "Alice Springs": // Australian Ringneck (parrot)
      makeParrots();
      birdNum = 4;
      break;
    case "Nairobi": // Rainbow Rooster 
      makeRoosters();
      birdNum = 5;
      break;
    case "Santiago": // Red-crested Cardinal
      makeCardinals();
      birdNum = 6;
      break;
    case "Kalinago Territory": // Laughing Gull
      makeSeagulls();
      birdNum = 7;
      break;
    case "Amsterdam": // Mediterranean Gull
      makeMgulls()
      birdNum = 8;
      break;
    case "NYC": // Northern Cardinal
      makeNCardinals
      birdNum = 9;
      break;
    case "Beijing": // Carrion Crow
      makeCrows();
      birdNum = 10;
      break;
    case "New York": // Rock Pigeon
      makePigeons();
      birdNum = 11;
      break;
    default:
      makePigeons();  // change this if you want to test a particular bird. 
      birdNum = 10; 
      break;
  }
  let splitString = split(timeOfDay, ' ');
  let justTime = splitString[1];
  let splitTime = split(justTime, ':');
  localHour = splitTime[0]; // 
  localMinute = splitTime[1];
  if (testBool) {
    localHour = hourSlider.value()
    localMinute = 30;
  }
  if (localHour < 5) {
    foodFrequency = 14
  }
  if (localHour >= 5 && localHour < 10) {
    foodFrequency = 28
  }
  if (localHour >= 10 && localHour < 17) {
    foodFrequency = 18
  }
  if (localHour >= 17 && localHour < 21) {
    foodFrequency = 28
  }
  if (localHour > 21) {
    foodFrequency = 14
  }
  //foodFrequency = 100 // test 
  for (let i = 0; i < foodFrequency - 6; i++) { // 20 
    foodList.push(new food(random(-5000, 5000), random(-800, 800), false, false));
  }
  for (let i = 0; i < 10; i++) { // was 6
    foodList.push(new food(random(-5000, 5000), random(-200, 200), false, false)); // put more in the middle 
  }
  for (let i = 0; i < 5; i++) { // trash
    let tside = -500 - random(500)
    if (random(2) < 1) {
      tside = 500 + random(500)
    }
    foodList.push(new food(random(-5000, 5000), tside, true, false)); // put more in the middle 
  }
}

function clearAll() {
  roosterList = [];
  pigeonList = [];
  robinList = [];
  parrotList = [];
  parakeetList = [];
  seagullList = [];
  bluejayList = [];
  cardinalList = [];
  ravenList = [];
  crowList = [];
  mgullList = [];
  ncardinalList = [];
  chickenList = [];
  birdSteps = 0;
  oldBirdSteps = 0;
  foodPecked = 0;
  oldfoodPecked = 0;
}
function makePigeons() {
  clearAll();
  if (camView) {
    pigeonList.push(new pigeon(true, 0, 0, -68, 0)); // hero pigeon was -114
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-2000, -100)
    pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(2000, 100)
    pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
  }
}
function makeRoosters() {
  clearAll();
  roosterList.push(new rooster(true, 0, 0, -114, 0)); // hero pigeon

  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    chickenList.push(new chicken(false, random(TWO_PI), rx, -94, rz));
  }
  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    chickenList.push(new chicken(false, random(TWO_PI), rx, -94, rz));
  }
}

function makechickens() {
  clearAll();
  chickenList.push(new chicken(true, 0, 0, -94, 0)); // hero bird
  for (let i = 0; i < 1; i++) { // sideline birds
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    chickenList.push(new chicken(false, random(TWO_PI), rx, -94, rz));
  }
  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    chickenList.push(new chicken(false, random(TWO_PI), rx, -94, rz));
  }
}

function makeParrots() {
  clearAll();
  parrotList.push(new parrot(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 1; i++) { // sideline birds
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    parrotList.push(new parrot(false, random(TWO_PI), rx, -114, rz));
  }
  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    parrotList.push(new parrot(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeRavens() {
  clearAll();
  ravenList.push(new raven(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 1; i++) { // sideline birds
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    ravenList.push(new raven(false, random(TWO_PI), rx, -114, rz));
  }
  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    ravenList.push(new raven(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeCrows() {
  clearAll();
  crowList.push(new crow(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 1; i++) { // sideline birds
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    crowList.push(new crow(false, random(TWO_PI), rx, -114, rz));
  }
  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    crowList.push(new crow(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeParakeets() {
  clearAll();
  parakeetList.push(new parakeet(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 1; i++) { // sideline birds
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    parakeetList.push(new parakeet(false, random(TWO_PI), rx, -114, rz));
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    parakeetList.push(new parakeet(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeRobins() {
  clearAll();
  robinList.push(new robin(true, 0, 0, -94, 0)); // hero Robing
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    robinList.push(new robin(false, random(TWO_PI), rx, -94, rz));
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    robinList.push(new robin(false, random(TWO_PI), rx, -94, rz));
  }
}

function makeSeagulls() {
  clearAll();
  seagullList.push(new seagull(true, 0, 0, -114, 0)); // hero seagull
  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    seagullList.push(new seagull(false, random(TWO_PI), rx, -114, rz));
  }
  for (let i = 0; i < 1; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    seagullList.push(new seagull(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeBluejays() {
  clearAll();
  bluejayList.push(new bluejay(true, 0, 0, -114, 0)); // hero bluejay
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    bluejayList.push(new bluejay(false, random(TWO_PI), rx, -114, rz));
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    bluejayList.push(new bluejay(false, random(TWO_PI), rx, -114, rz));
  }
}

function makeCardinals() {
  clearAll();
  cardinalList.push(new cardinal(true, 0, 0, -114, 0)); // hero cardinal
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    cardinalList.push(new cardinal(false, random(TWO_PI), rx, -114, rz));
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    cardinalList.push(new cardinal(false, random(TWO_PI), rx, -114, rz));
  }
}
function makeNCardinals() {
  clearAll();
  ncardinalList.push(new ncardinal(true, 0, 0, -93, 0)); // hero cardinal
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    ncardinalList.push(new ncardinal(false, random(TWO_PI), rx, -93, rz));
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    ncardinalList.push(new ncardinal(false, random(TWO_PI), rx, -93, rz));
  }
}

function makeMgulls() {
  clearAll();
  mgullList.push(new mgull(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 2; i++) { // sideline birds
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    mgullList.push(new mgull(false, random(TWO_PI), rx, -114, rz));
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
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
  if (key == 'a') {
    foodList.push(new food(random(-5000, 5000), 0, false, true)); // put more in the middle 
  }
  if(key=='f'){
    globalFlying = !globalFlying; 
  }

  if (key == 'p') {
    primeBirdPecking = !primeBirdPecking;
  }
  if (key == 's') {
    testStop = !testStop;
  }
  if (key == 'v') {
    // camView = !camView;
    // if (!camView) {
    //   camRot = 0;
    // } else {
    //   camRot = HALF_PI;
    // }
    POVtoggle = !POVtoggle
    if (POVtoggle == false) {
      camView = true;
      camRot = HALF_PI;
    }

  }
  if (key == 't') {
    window.open("test.html", "_self")
  }

  if (key == '1') {
    makePigeons();
    birdNum = 10; 
  }
  if (key == '2') {
    makeRoosters();
    birdNum = 4
  }
  if (key == '3') {
    makeRobins();
    birdNum = 0; 
  }
  if (key == '4') {
    makeParakeets();
    birdNum = 3; 
  }
  if (key == '5') {
    makeSeagulls();
    birdNum = 7; 
  }
  if (key == '6') {
    makeBluejays();
    birdNum = 1; 
  }
  if (key == '7') {
    makeCardinals();
    birdNum = 5; 
  }
  if (key == 'n') {
    makeNCardinals();
    birdNum = 8; 
  }
  if (key == 'm') {
    makeCrows();
    birdNum = 9; 
  }
  if (key == '8') {
    makeRavens();
    birdNum = 2; 
  }
  if (key == '9') {
    makeMgulls();
    birdNum = 7; 
  }
  if (key == '0') {
    makeParrots();
    birdNum = 3; 
  }
}
function draw() {
  if (POVtoggle == true) { //  camView = true;
    camTimerLength = 10000; // test 
    povTimeLenght = 5000; // test 
    if (millis() - camTimer > camTimerLength && camView && primeBirdPecking && foodPecked >= 1) {
      camView = false;  // set the camera to POV
      camRot = 0; // rotate the camera 
      povTimer = millis(); // start the pov timer
    }
    if (millis() - povTimer > povTimeLenght && camView == false) {
      camView = true;  // set the camera to side view
      camRot = HALF_PI; // rotate the camera 
      camTimer = millis(); // start the pov timer
    }
    if (!primeBirdPecking) {
      foodPecked = 0;  // this nerfs the food pecking stats, but it works without writing code in every bird. 
    }
  }

  if (birdSteps != oldBirdSteps) {
    updateTextOnly();

    oldBirdSteps = birdSteps;
  }
  if (foodPecked != oldfoodPecked) {
    updateTextOnly();
    oldfoodPecked = foodPecked;
    foodPeckedCounter++;
    birdNameLangNum ++; 
     if(birdNameLangNum >= birdNames[birdNum].length ){
      birdNameLangNum = 0; 
     }
  }
  if (panelPower < bwNum || localHour < 5 || localHour > 22) { // black and white
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
  let x = 0;
  x = parseInt(localHour);
  bgColor = skyColorArray[int(localHour)];
  background(bgColor) // 200 
  if (panelPower < greyNum) {
    background(200);
  }
  if (panelPower < bwNum) {
    background(1);
  }
  if (localHour > 8 && localHour < 18 && panelPower < 7) {
    if (rainToggle == false) {
      rainToggle = true;
      for (let i = 0; i < 60; i++) {
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
    panelPower = panelPowerSlider.value(); // was 7
    // serverName = "Swarthmore Solar"
    // locName = "Swarthmore College"
    // timezone = "Africa/Khartoum"
    localHour = hourSlider.value()
    localMinute = 30;
  }

  if (primeBirdPecking) {
    if (primePeckingBuffer == false) {
      lookRot = 0;
    }
    primePeckingBuffer = true;
    primePeckingBufferNum = 0;
  }
  if (!primeBirdPecking && primePeckingBuffer) { // eases the boolean a bit 
    primePeckingBufferNum++;
    if (primePeckingBufferNum > 4) { // was 10
      primePeckingBuffer = false;
      primePeckingBufferNum = 0;
    }
  }
  if (camView) { // side of bird
    if (mouseIsPressed) {
      camRot += (mouseX - pmouseX) / 200;
      camRot2 += (mouseY - pmouseY) / 200;
      camRot2 = constrain(camRot2, 3.2, 4, 2);
    }
    let cx = cos(camRot) * 600 // as 10000 
    let cz = sin(camRot) * 600
    let cy = sin(camRot2) * 600 // as 10000 
    camera(cx, cy, cz, 0, -100, 0, 0, 1, 0); // side view do not destroy
  } else { // bird eye view
    if (globalPecking && !cameraPecking) {
      cameraPecking = true;
    }
    if (!globalPecking && cameraPecking) {
      cameraPecking = false;
    }
    let cLoc = createVector(0, 0, 0,);
    let camBobAdd = map(walkSpeed, 1, 6, .001, .1)
    camVertNum += camBobAdd;
    camHorNum += camBobAdd;
    let camVert;
    camVert = (sin(camVertNum) * 12) - 300
    cLoc.y = camVert; // was -200
    let mNum = random(5, 10) // random(20, 30) // random jerky 
    let camHor = sin(camHorNum * 3) * mNum
    let outFront = 280;
    cLoc.x = camHor + outFront;
    let cx2 = cos(camRot) * 600 // as 600
    let cz2 = sin(camRot) * 600
    cz2 += cos(camHorNum) * 10;
    let YBump = sin(camHorNum * 2) * 2;
    let lookY = -300;
    if (primePeckingBuffer) {
      lookRot -= .08;
      lookRot = lookRot % PI;
    } else {
      if (lookRot < 4.3) {
        lookRot += .1;
      } else {
        lookRot = 4.3;
      }
    }
    lookY = sin(lookRot) * 300;
    camera(cLoc.x, cLoc.y + YBump, cLoc.z, cx2, lookY, cz2, 0, 1, 0);
  }
  if (showLights) {
    let ldirZ = map(sunRotation, PI, TWO_PI, .5, -.5);
    let ldirY = 1 - (abs(sin(ldirZ))); //map(mouseY, 0, height, .75, -.25)
    directionalLight(255, 255, 200, 0, ldirY, ldirZ);
    directionalLight(255, 255, 200, -1, 0, 0);
    let pRot = map(mouseY, 0, height, 0, TWO_PI); //sunRotation; 
    if (!dayNight) {
      sunRotation = 3;  // not necessary but looks cool
    }
    if (localHour > 20) {
      streetLightX -= walkSpeed;
      if (streetLightX < -2500) {
        streetLightX = 2500;
      }
      pointLight(255, 255, 255, streetLightX, -400, 0);
    }
    else {
      pointLight(255, 255, 255, 400, 20, 700);
    }
  }

  if (birdWalkBool) {
    walkSpeed = map(batteryLevelPer, 0, 1, .2, 12)
  } else {
    walkSpeed = 0;
  }
  if (testStop) {
    walkSpeed = 0;
  }
  //every 5 minutes call the API again to update the data
  if (millis() - timer >= timeOut && testBool == false) { // timeOut
    textDiv.html(" ", false);
    getData()
    updateDiv();
    timer = millis();
  }
  for (let i = 0; i < SWList.length; i++) {
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
  for (let i = 0; i < chickenList.length; i++) {
    chickenList[i].display();
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
  if (foodList.length < foodFrequency + 5) {
    foodList.push(new food(5000, random(-800, 800), false, false));
  }
  push()  // ground plane and horzon
  translate(0, 10, 0);
  noStroke()
  fill(groundColorArray[int(localHour)])
  if (panelPower < greyNum) {
    fill(80);
  }
  if (panelPower < bwNum) {
    fill(1);
  }
  cylinder(15000, 2);
  pop()
  // Sun
  if (dayNight) {
    push()
    translate(1600, 0, 0)
    let rot = map(mouseY, 0, height, TWO_PI, PI) // this is correct 
    rotateX(sunRotation) // sunRotation
    translate(0, 0, -500)
    fill(255, 255, 0)
    noStroke()
    emissiveMaterial(200, 200, 0);
    pop()
  }
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
    fill(180, 220, 255, 100 - this.timer)
    if (panelPower < greyNum) {
      stroke(80)
      fill(180, 100 - this.timer)
    }
    if (panelPower < bwNum) {
      stroke(255)
      noFill()
    }
    if (this.falling == true) {
      line(0, 0, 0, 0, -40, 0)
    } else {
      rotateX(HALF_PI);
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
    this.localHourSW = localHour;
    this.getColor();
  }

  getColor() {
    let rand = int(random(1, 7));
    SWrandomNum += rand;
    SWrandomNum = SWrandomNum % 8; // keeps it from being a repeat
    if (localHour < 5) {
      this.SXColor = sideWalkColorArray[0][SWrandomNum];
    }
    if (localHour >= 5 && localHour < 7) {
      this.SXColor = sideWalkColorArray[1][SWrandomNum]
    }
    if (localHour >= 7 && localHour < 9) {
      this.SXColor = sideWalkColorArray[2][SWrandomNum]
    }
    if (localHour >= 9 && localHour < 11) {
      this.SXColor = sideWalkColorArray[3][SWrandomNum]
    }
    if (localHour >= 11 && localHour < 17) {
      this.SXColor = sideWalkColorArray[4][SWrandomNum]
    }
    if (localHour >= 17 && localHour < 19) {
      this.SXColor = sideWalkColorArray[3][SWrandomNum]
    }
    if (localHour >= 19 && localHour < 21) {
      this.SXColor = sideWalkColorArray[2][SWrandomNum]
    }
    if (localHour >= 21 && localHour < 23) {
      this.SXColor = sideWalkColorArray[1][SWrandomNum]
    }
    if (localHour >= 23) {
      this.SXColor = sideWalkColorArray[0][SWrandomNum]
    }
  }
  display() {
    if (this.localHourSW != localHour) {
      this.getColor()
      this.localHourSW = localHour
    }
    this.loc.x -= walkSpeed;
    if (this.loc.x <= -totalTiles * this.SWSize) {
      this.reset = true;
    }
    push()
    translate(this.loc.x, this.loc.y, this.loc.z)
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
    pop()
  }
}



function gotBatData(tempData) {
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






