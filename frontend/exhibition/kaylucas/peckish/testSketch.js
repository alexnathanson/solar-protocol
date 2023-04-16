// Peckish (2023) by Kristin Lucas and Joe McKay
// Co-programmed in p5.js
// Commissioned by Solar Protocol
// http://solarprotocol.net

let birdNames = []
let birdNum = 11;
let todArray = ["Dawn", "Morning", "Late Morning", "Midday", "Afternoon", "Evening", "Dusk", "Night"];
let foodSupplyArray = ["Abundant", "Moderate", "Low", "Scarce", "Low", "Moderate", "Abundant", "Moderate"];
let SWList = [];
let pigeonList = [];
let roosterList = [];
let robinList = [];
let parrotList = [];
let lorikeetList = [];
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
let batteryLevel = 4.0;
let batteryLevelPer = 1.0;
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
let totalTiles = 20; // divided by two
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
let primeBirdPecking = false;
let primePeckingBuffer = false;
let primePeckingBufferNum = 0;
let killfood = false;
let globalPecknum = 0;
let nudgeFood = false;
let testStop = false;
let birdWalkBool = true;
let bwNum = 4;
let greyNum = 8;
let noLightsNum = 15;
let lightsOnNum = 35;
let camVertNum = 0;
let camHorNum = 0;
let camView = true;
let batPercentSlider;
let panelPowerSlider;
let hourSlider;
let foodFrequency = 30; // how much food there is at any one time
let sliderOnce = false;
let infoButton;
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
let povTimeLenght = 20 * 1000;
let camTimerLength = 120 * 1000;
let lookPoint;
let lookRot = 0;
let POVtoggle = true;
let birdNameLangNum = 0;
let birdTerrirotyNum = 0;
let globalFlying = false;
let globalFlyingTimer;
let globalFlyingInterval = 1000; // wait 1 second and fly away
let flyingIntervalHigh = 30000;
let flyingIntervalLow = 10000;
let pauseRotate = false;
let showDiv = true;
let territory = [];
let OVworld = false;
let camJiggle = false;
let showCity = false;
let serverNameList = [];

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
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
  let cnv = createCanvas(windowWidth, windowHeight, WEBGL);
  cnv.parent("myContainer");
  lookPoint = createVector(500, -200, 0);
  camTimer = millis();
  globalFlyingTimer = millis();
  povTimer = 0;
  camRot = HALF_PI;
  camRot2 = 3.7;
  textFont('Times');
  textSize(16);
  timer = millis();
  textDiv = createDiv('');
  textDiv.id("infoDiv2");
  let tsNum = int(map(displayWidth, 1680, 320, 16, 12));
  let ts = tsNum + "px";
  textDiv.style('font-size', ts);
  textDiv.style('color', 'black');
  let w = int(map(windowWidth, 1680, 320, 340, 270, true)); // 280 smallest 
  let ws = w + "px";
  textDiv.style('width', ws);
  textDiv.position(20, 20);

  infoButton = createButton("i");
  infoButton.style('font-style', 'italic');
  infoButton.style('font-size', '16pt')
  infoButton.style('font-family', 'serif');
  infoButton.position(16, 16);
  infoButton.mousePressed(hideDiv);
  infoButton.style('border-radius', '12px');
  infoButton.style('border-style', 'none');
  infoButton.style('background-color', 'rgba(220, 220, 220, 0.8');
  let sLocX = 225;
  let sWid = "150px"; // slider width desktop
  if (displayWidth < 900) {
    sLocX = 220; // slider position (left side)
    sWid = "90px"; // slider width phone
  }

  birdSlider = createSlider(0, 12, 6, 1);
  birdSlider.position(sLocX, 138);  // position slider
  birdSlider.input(bsout);
  birdSlider.mouseOver(overSlider);
  birdSlider.mouseOut(outSlider);
  birdSlider.class("slider");
  birdSlider.style('width', sWid);

  batPercentSlider = createSlider(0, 100, 50);
  batPercentSlider.position(sLocX, 79);  // position slider
  batPercentSlider.input(updateTextOnly);
  batPercentSlider.mouseOver(overSlider);
  batPercentSlider.mouseOut(outSlider);
  batPercentSlider.class("slider");
  batPercentSlider.style('width', sWid);

  panelPowerSlider = createSlider(0, 50, 25);
  panelPowerSlider.position(sLocX, 99);
  panelPowerSlider.input(updateTextOnly);
  panelPowerSlider.mouseOver(overSlider);
  panelPowerSlider.mouseOut(outSlider);
  panelPowerSlider.class("slider");
  panelPowerSlider.style('width', sWid);

  hourSlider = createSlider(0, 24, 12);
  hourSlider.position(sLocX, 175);
  hourSlider.input(newFood);
  hourSlider.mouseOver(overSlider);
  hourSlider.mouseOut(outSlider);
  hourSlider.class("slider");
  hourSlider.style('width', sWid);

  batteryLevel = 12
  batteryLevelPer = batPercentSlider.value() / 100;
  loadPower = 4
  panelPower = panelPowerSlider.value();
  timeOfDay = "2023-03-23 " + hourSlider.value() + ":30:01.053347";
  bgColor = skyColorArray[0];

  rectMode(CENTER)
  
  birdNames[0] = ["American Robin (English)", "chiskukus (Lenape)", "zwazo (Haitian Creole)", "rubin (Arabic)", "rouge-gorge (French)", "chim cổ đỏ (Vietnamese)", "Zhī gēng niǎo (Mandarin)", "pisco de peito vermelho (Portugese)"];
  birdNames[1] = ["Blue Jay (English)", "Teri-Teri (Mohawk)", "diindiisi (Ojibwe)", "gwiingwiish (Ojibwe)", "Geai bleu (French)", "Blauhäher (German)", "Blauwe Gaai (Dutch)", "modrosójka Błękitna (Polish)", "ghiandaia (Italian)", "Chara Azul (Spanish)", "藍松鴉 / Lán sōng yā (Mandarin)", "큰어치 / eochi (Korean)", "큰어치 / eochi (Arabic)", "પક્ષી / Pakṣī (Gujarati)", "نيل گنٹھ / Neel ghanth (Urdu)"];
  birdNames[2] = ["Australian Raven (English)", "wugan (Eora)", "wugan (Dharug)", "غراب أسود / ghurab 'aswad (Arabic)", "ագռավ / agrrav (Armenian)", "aribu (Assyrian)", "עוֹרֵב (Hebrew)", "烏鴉 / wūyā (Mandarin)", "갈가마귀 / galgamagwi (Korean)", "カラス / Karasu (Japanese)", "uwak (Filipino)", "con quạ (Vietnamese)", "อีกา / Xīkā (Thai)", "oreva (Samoan)", "काला कौआ / kaala kaua (Hindi)", "কাক / Kāka (Bangla)", "காகம் / Kākam (Tamil)", "ਕਾਂ / Kāṁ (Punjabi)", "કાગડો / Kāgaḍō (Gujarti)", "Krähe (German)", "kraai (Dutch)", "gala (Swedish)", "κοράκι / koráki (Greek)", "corvo (Italian)", "cuervo (Spanish)", "corbeau (French)", "ċawla (Maltese)", "corvo (Portugese)", "ворона / vorona (Russian)", "врана / vrana (Macedonian)", "врана / vrana (Serbian)", "wrona (Polish)"];
  birdNames[3] = ["Australian Ringneck (English)", "arlpatye (Arrernte)", "Twenty-eight Parrot (English)", "patilpa (Pitjantjatjara)", "darlmoorluk (Noongar)", "dowarn (Noongar)", "doomolok (Noongar)"];
  birdNames[4] = ["Rainbow Rooster (English)", "jogoo wa upinde wa mvua (Swahili)", "nyũngũ ya mbura (Kikuyu)", "ngũkũ (Kamba)", "ngwex (Sheng)", "ዶርሆ / dorho (Ge'ez)", "Luku (Rendille)", "मुरग़ा / muraga (Hindi)", "مرغ (Urdu)"];
  birdNames[5] = ["Red-crested Cardinal (English)", "üñüm (Picunche)", "üñüm (Mapudungun)", "Paroaria (Tupí)", "gunún (Mapuche)", "giñum (Huillche)", "jamach'i (Aymara)", "pisco (Quechua)", "manu (Rapa Nui)"];
  birdNames[6] = ["Laughing Gull (English)", "gua-tibiri (Tíano)", "gaviota (Dominican Spanish)", "gaviota (Spanish)"];
  birdNames[7] = ["Mediterranean Gull (English)", "meeuw (Dutch)", "gull (West Frisian)", "mås (Swedish)", "måge (Danish)", "Möwe (German)"];
  birdNames[8] = ["Northern Cardinal", "Cardenilla Crestada (Spanish)", "hmukwinùnd (Munsee)", "cit (Mohegan)", "pássaro (Portugese)", "चिड़िया / chidiya (Hindi)", "Vogel (German)", "ਪੰਛੀ / Pachī (Punjabi)", "پرنده (Persian)", "새 / sae (Korean)", "ꯎꯆꯦꯛ (Manipuri)", "éan (Irish)", "चरा / Carā (Nepali)", "पक्षी / Pakṣī (Marathi)", "ወፍ / wefi (Amharic)", "shimbir (Somali)", "ዒፍ (Tigrinya)", "anomaa (Akan)", "nnụnụ (Igbo)", "eye (Yoruba)", "akanyonyi (Ganda)", "inyoni (Kinyarwanda)", "ndeke (Lingala)", "ndege (Swahili)", "鳥 / Niǎo (Mandarin)", "oiseau (French)", "πουλί / poulí (Greek)", "zwazo (Haitian Creole)", "ציפור (Hebrew)", "uccello (Italian)", "ptak (Polish)", "птица / ptitas (Russian)", "pájaro (Spanish)", "پرندہ (Urdu])", "פויגל / foygi (Yiddish)"];
  birdNames[9] = ["Carrion Crow (English)", "小嘴乌鸦 / xiǎo zuǐ wūyā (Mandarin)", "shí fǔròu wū-yā (Pinyin)", "gaha (Manchu)", "kheree (Mongol)"];
  birdNames[10] = ["Rock Pigeon (English)", "cit (Mohegan)", "amimi (Munsee)", "pomba (Portugese)", "कबूतर / kabootar (Hindi)", "Taube (German)", "ਕਬੂਤਰ / Kabūtara (Punjabi)", "کبوتر (Persian)", "비둘기 / bidulgi (Korean)", "ꯈꯨꯅꯨ (Manipuri)", "colm (Irish)", "परेवा / Parēvā (Nepali)", "कबूतर / Kabūtara (Marathi)", "እርግብ / irigibi (Amharic)", "qoolley (Somali)", "ርግቢ (Tigrinya)", "aburuburo (Akan)", "nduru (Igbo)", "ẹyẹle (Yoruba)", "engiibwa (Ganda)", "inuma (Kinyarwanda)", "ebenga (Lingala)", "njiwa (Swahili)", "鴿子 / Gēzi (Mandarin)", "pigeonne (French)", "περιστέρι / peristéri (Greek)", "pijon (Haitian Creole)", "יוֹנָה (Hebrew)", "picciona (Italian)", "Gołąb (Polish)", "голубь (Russian)", "paloma (Spanish)", "کبوتر (Urdu)", "טויב / toyb (Yiddish)"];
  birdNames[11] = ["Rock Pigeon (English)", "cit (Mohegan)", "amimi (Munsee)", "pomba (Portugese)", "कबूतर / kabootar (Hindi)", "Taube (German)", "ਕਬੂਤਰ / Kabūtara (Punjabi)", "کبوتر (Persian)", "비둘기 / bidulgi (Korean)", "ꯈꯨꯅꯨ (Manipuri)", "colm (Irish)", "परेवा / Parēvā (Nepali)", "कबूतर / Kabūtara (Marathi)", "እርግብ / irigibi (Amharic)", "qoolley (Somali)", "ርግቢ (Tigrinya)", "aburuburo (Akan)", "nduru (Igbo)", "ẹyẹle (Yoruba)", "engiibwa (Ganda)", "inuma (Kinyarwanda)", "ebenga (Lingala)", "njiwa (Swahili)", "鴿子 / Gēzi (Mandarin)", "pigeonne (French)", "περιστέρι / peristéri (Greek)", "pijon (Haitian Creole)", "יוֹנָה (Hebrew)", "picciona (Italian)", "Gołąb (Polish)", "голубь (Russian)", "paloma (Spanish)", "کبوتر (Urdu)", "טויב / toyb (Yiddish)"];
  birdNames[12] = ["Rainbow Lorikeet (English)"];

  serverNameList = ["Swarthmore Solar", "Low-Carbon Research Methods", "Eora", "Uturne", "Solar-Power for Hackers", "Santiago", "Kalinago Territory", "Fiber Festival", "Solar Power for Artists", "CAFA", "Woodbine", "Hells Gate", "Uturne"];
  territory[0] = ["Lenapehoking (Lenni-Lenape)"];
  territory[1] = ["Anishinabewaki", "Wendake-Nionwentsïo", "Ho-de-no-sau-nee-ga", "Mississauga"];
  territory[2] = ["Eora", "Dharug"];
  territory[3] = ["Mparntwe (Arrente)", "Eastern Arrente"];
  territory[4] = ["n/a"];
  territory[5] = ["Wallmapu (Mapuche)"];
  territory[6] = ["Tíano", "Kalinago (Island Carib)"];
  territory[7] = ["n/a"];
  territory[8] = ["Canarsie", "Munsee Lenape"];
  territory[9] = ["n/a"];
  territory[10] = ["Canarsie", "Munsee Lenape"];
  territory[11] = ["Canarsie", "Wappinger", "Munsee Lenape"]
  territory[12] = ["Mparntwe (Arrente)", "Eastern Arrente"];


  camera(-600, -400, height / 2 / tan(PI / 6), 100, -100, 200, 0, 1, 0);
  // pigeon neck colors
  neckColorArray[0] = color(38, 204, 138);
  neckColorArray[1] = color(20, 128, 119);
  neckColorArray[2] = color(182, 125, 233);
  neckColorArray[3] = color(138, 110, 202);
  neckColorArray[4] = color(30, 46, 87);
  // rooster neck colors
  roosterNeckArray[0] = color(247, 78, 141);
  roosterNeckArray[1] = color(250, 160, 30);
  roosterNeckArray[2] = color(105, 67, 114);
  roosterNeckArray[3] = color(20, 128, 119);
  // rooster wing colors
  roosterWingArray[0] = color(225, 22, 17);
  roosterWingArray[1] = color(250, 160, 30);
  roosterWingArray[2] = color(20, 128, 119);
  roosterWingArray[3] = color(105, 67, 114);
  // rooster body colors
  roosterBodyArray[0] = color(30, 46, 87);
  roosterBodyArray[1] = color(250, 160, 30);
  roosterBodyArray[2] = color(105, 67, 114);
  roosterBodyArray[3] = color(20, 128, 119);
  // sky colors
  skyColorArray[0] = color(39, 33, 78);
  skyColorArray[1] = color(39, 33, 78);
  skyColorArray[2] = color(39, 33, 78);
  skyColorArray[3] = color(39, 33, 78);
  skyColorArray[4] = color(39, 33, 78);
  skyColorArray[5] = color(255, 107, 62);
  skyColorArray[6] = color(255, 107, 62);
  skyColorArray[7] = color(247, 193, 106);
  skyColorArray[8] = color(247, 193, 106);
  skyColorArray[9] = color(255, 239, 122);
  skyColorArray[10] = color(255, 239, 122);
  skyColorArray[11] = color(181, 214, 224);
  skyColorArray[12] = color(181, 214, 224);
  skyColorArray[13] = color(181, 214, 224);
  skyColorArray[14] = color(181, 214, 224);
  skyColorArray[15] = color(181, 214, 224);
  skyColorArray[16] = color(181, 214, 224);
  skyColorArray[17] = color(255, 239, 122);
  skyColorArray[18] = color(255, 239, 122);
  skyColorArray[19] = color(247, 193, 106);
  skyColorArray[20] = color(247, 193, 106);
  skyColorArray[21] = color(255, 107, 62);
  skyColorArray[22] = color(255, 107, 62);
  skyColorArray[23] = color(39, 33, 78);
  skyColorArray[24] = color(39, 33, 78);
  // ground colors 
  groundColorArray[0] = color(78, 62, 33);
  groundColorArray[1] = color(78, 62, 33);
  groundColorArray[2] = color(78, 62, 33);
  groundColorArray[3] = color(78, 62, 33);
  groundColorArray[4] = color(78, 62, 33);
  groundColorArray[5] = color(128, 100, 92);
  groundColorArray[6] = color(128, 100, 92);
  groundColorArray[7] = color(165, 217, 125);
  groundColorArray[8] = color(165, 217, 125);
  groundColorArray[9] = color(146, 255, 176);
  groundColorArray[10] = color(146, 255, 176);
  groundColorArray[11] = color(128, 125, 103);
  groundColorArray[12] = color(128, 125, 103);
  groundColorArray[13] = color(128, 125, 103);
  groundColorArray[14] = color(128, 125, 103);
  groundColorArray[15] = color(128, 125, 103);
  groundColorArray[16] = color(128, 125, 103);
  groundColorArray[17] = color(146, 255, 176);
  groundColorArray[18] = color(146, 255, 176);
  groundColorArray[19] = color(165, 217, 125);
  groundColorArray[20] = color(165, 217, 125);
  groundColorArray[21] = color(128, 100, 92);
  groundColorArray[22] = color(128, 100, 92);
  groundColorArray[23] = color(78, 62, 33);
  groundColorArray[24] = color(78, 62, 33);
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
    SWList.push(new SW(i * 1200, 1200));
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
  textDiv.html("Name: " + serverNameList[birdNum] + "<br>", true);
  textDiv.html("Battery Level: " + int(batteryLevelPer * 100) + "%" + "<br>", true);
  textDiv.html("Panel Power (0-50): " + panelPower + "<br><br>", true);
  textDiv.html("LOCATION" + "<br>", true);

  locCity = cities[birdNum];
  LocCountry = countries[birdNum];

  if (birdTerrirotyNum == -1) {
    textDiv.html("City / Country: " + locCity + ", " + LocCountry + "<br>", true);
  } else {
    textDiv.html("Territory: " + territory[birdNum][birdTerrirotyNum] + "<br>", true);
  }

  textDiv.html("Local Time: " + hour12 + ":" + nf(localMinute, 2, 0) + "" + ampm + "<br>", true);
  if (rainToggle) {
    textDiv.html("Weather: Overcast: Chance of Precipitation" + "<br><br>", true);
  } else {
    textDiv.html("Weather: Clear" + "<br><br>", true);
  }
  textDiv.html("LOCAL SCENE" + "<br>", true);
  textDiv.html("Bird: " + birdNames[birdNum][birdNameLangNum] + "<br>", true);
  let sp;
  if (batteryLevelPer < .20) {
    sp = "Slow-mo";
  }
  if (batteryLevelPer >= .20 && batteryLevelPer < .55) {
    sp = "Stroll";
  }
  if (batteryLevelPer >= .55 && batteryLevelPer < .75) {
    sp = "Strut";
  }
  if (batteryLevelPer >= .75) {
    sp = "Jaunty";
  }
  if (batteryLevelPer >= .85) {
    sp = "Zippy";
  }
 
  textDiv.html("Pace (Battery Level): " + sp + "<br>", true);

  let gl;
  let res;
  if (panelPower < bwNum) {
    gl = "Wireframe";
    res = "Thrifty";
  }
  if (panelPower >= bwNum && panelPower < greyNum) {
    gl = "Grayscale";
    res = "Frugal";
  }
  if (panelPower >= greyNum && panelPower < noLightsNum) {
    gl = "Color";
    res = "So-so";
  }
  if (panelPower >= noLightsNum && panelPower < lightsOnNum) {
    gl = "Lights";
    res = "Spendy";
  }
  if (panelPower >= lightsOnNum) {
    gl = "Lights & Shadow";
    res = "Extravagant";
  }
  textDiv.html("Graphics (Panel Power): " + gl + "<br>", true);
  textDiv.html("Render Quality (Panel Power): " + res + "<br>", true);
  textDiv.html("Food Supply (" + todArray[todNum] + "): " + foodSupplyArray[todNum] + "<br>", true);
  if (camView) {
    textDiv.html("Camera: Drag to Orbit View" + "<br>", true);
  } else {
    textDiv.html("Camera: Bird POV" + "<br>", true);
  }
  textDiv.html("<br>Welcome to the sandbox!", true);
  textDiv.html("<br>◇ Energy supply affects the scene.", true);
  textDiv.html("<br>◇ Time of day affects the food supply.", true);
  textDiv.html("<br>◇ Server location updates the bird.", true);
  textDiv.html("<br>◇ Sources for data are myriad and mutable.<br>", true);
  textDiv.html("<br>Return to <a href = live.html>Live Mode</a> </span>", true);
}

function overSlider() {
  pauseRotate = true;
}
function outSlider() {
  pauseRotate = false;
  birdNameLangNum = 0
  birdTerrirotyNum = -1;
}
function hideDiv() {
  showDiv = !showDiv;
  if (showDiv) {
    textDiv.style('display', 'block');
  } else {
    textDiv.style('display', 'none');
  }
}

function updateDiv() {
  switch (locCity) {
    case "Swarthmore": // American Robin
      makeRobins();
      break;
    case "Queens": // Rock Pigeon
      makePigeons();
      break;
    case "Peterborough": // Blue Jay
      makeBluejays();
      break;
    case "Sydney": // Australian Raven
      makeRavens();
      break;
    case "Alice Springs": // Australian Ringneck (parrot)
      makeParrots(); // or Rainbow Lorikeet
      break;
    case "Nairobi": // Rainbow Rooster 
      makeRoosters();
      break;
    case "Santiago": // Red-crested Cardinal
      makeCardinals();
      break;
    case "Kalinago Territory": // Laughing Gull
      makeSeagulls();
      break;
    case "Amsterdam": // Mediterranean Gull
      makeMgulls()
      break;
    case "Brooklyn": // Northern Cardinal
      makeNCardinals(); 
      break;
    case "Beijing": // Carrion Crow
      makeCrows();
      break;
    case "Queens": // Rock Pigeon
      makePigeons();
      break;
     case "Brooklyn 2": // Rock Pigeon
      makePigeons();
      break;
    case "Alice Springs 2": // Australian Ringneck (parrot)
      makeLorikeets() // or  Rainbow Lorikeet
      break;
    default:
      makePigeons();  // change this if you want to test a particular bird
      break;
  }
  let splitString = split(timeOfDay, ' ');
  let justTime = splitString[1];
  let splitTime = split(justTime, ':');
  localHour = splitTime[0]; // 
  localMinute = splitTime[1];
  newFood();
}

function newFood() { // update food
  localHour = hourSlider.value()
  localMinute = 30;
  foodList = [];
  if (localHour >= 5 && localHour < 7) { // dawn (moderate)
    foodFrequency = 30;
  }
  if (localHour >= 7 && localHour < 10) { // morning (abundant)
    foodFrequency = 40;
  }
  if (localHour >= 10 && localHour < 12) { // late morning (low)
    foodFrequency = 20;
  }
  if (localHour >= 12 && localHour < 14) { // midday (scarce)
    foodFrequency = 12;
  }
  if (localHour >= 14 && localHour < 17) { // afternoon (low)
    foodFrequency = 20;
  }
  if (localHour >= 17 && localHour < 21) { // evening (abundant)
    foodFrequency = 40;
  }
  if (localHour >= 21 && localHour < 23) { // dusk (moderate)
    foodFrequency = 30;
  }
  if (localHour > 23|| localHour < 5) { // night (low)
    foodFrequency = 15;
  }
  for (let i = 0; i < foodFrequency - 6; i++) {
    foodList.push(new food(random(-5000, 5000), random(-800, 800), false, false));
  }
  for (let i = 0; i < 10; i++) {
    foodList.push(new food(random(-5000, 5000), random(-200, 200), false, false)); // put more in the middle 
  }
  for (let i = 0; i < 5; i++) { // trash
    let tside = -500 - random(500)
    if (random(2) < 1) {
      tside = 500 + random(500)
    }
    foodList.push(new food(random(-5000, 5000), tside, true, false)); // put more in the middle 
  }
  updateTextOnly();
}

function clearAll() {
  roosterList = [];
  pigeonList = [];
  robinList = [];
  parrotList = [];
  lorikeetList = [];
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

function makeAussieBird(_rx, _rz) {
  let rz = _rz;
  let rx = _rx;
  let ranBird = int(random(4));
  switch (ranBird) {
    case 0:
      ravenList.push(new raven(false, random(TWO_PI), rx, -114, rz));
      break;
    case 1:
      parrotList.push(new parrot(false, random(TWO_PI), rx, -114, rz));
      break;
    case 2:
      lorikeetList.push(new lorikeet(false, random(TWO_PI), rx, -114, rz));
    case 3:
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
      break;
  }
}

function makeNorthAmBird(_rx, _rz) {
  let rz = _rz;
  let rx = _rx;
  let ranBird = int(random(5));
  switch (ranBird) {
    case 0:
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
      break;
    case 1:
      ncardinalList.push(new ncardinal(false, random(TWO_PI), rx, -96, rz));
      break;
    case 2:
      robinList.push(new robin(false, random(TWO_PI), rx, -94, rz));
      break;
    case 3:
      seagullList.push(new seagull(false, random(TWO_PI), rx, -114, rz));
      break;
    case 4:
      bluejayList.push(new bluejay(false, random(TWO_PI), rx, -110, rz));
      break;
  }
}

function makePigeons() {
  clearAll();
  if (camView) {
    pigeonList.push(new pigeon(true, 0, 0, -68, 0)); // hero pigeon
  }
  for (let i = 0; i < 2; i++) {
    makeNorthAmBird(random(-5000, 5000), random(-2000, -100))
  }
  for (let i = 0; i < 2; i++) {
    makeNorthAmBird(random(-5000, 5000), random(2000, 100))
  }
}
function makeRobins() {
  clearAll();
  robinList.push(new robin(true, 0, 0, -94, 0)); // hero Robing
  for (let i = 0; i < 2; i++) {
    makeNorthAmBird(random(-5000, 5000), random(-2000, -100))
  }
  for (let i = 0; i < 2; i++) {
    makeNorthAmBird(random(-5000, 5000), random(2000, 100))
  }
}
function makeNCardinals() {
  clearAll();
  ncardinalList.push(new ncardinal(true, 0, 0, -96, 0)); // hero cardinal
  for (let i = 0; i < 2; i++) { // sideline birds
    makeNorthAmBird(random(-5000, 5000), random(-2000, -100))
  }
  for (let i = 0; i < 2; i++) {
    makeNorthAmBird(random(-5000, 5000), random(2000, 100))
  }
}
function makeSeagulls() {
  clearAll();
  seagullList.push(new seagull(true, 0, 0, -114, 0)); // hero seagull
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      seagullList.push(new seagull(false, random(TWO_PI), rx, -114, rz));
    }
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      seagullList.push(new seagull(false, random(TWO_PI), rx, -114, rz));
    }
  }
}
function makeBluejays() {
  clearAll();
  bluejayList.push(new bluejay(true, 0, 0, -110, 0)); // hero bluejay
  for (let i = 0; i < 2; i++) {
    makeNorthAmBird(random(-5000, 5000), random(-2000, -100))
  }
  for (let i = 0; i < 2; i++) {
    makeNorthAmBird(random(-5000, 5000), random(2000, 100))
  }
}
function makeRavens() {
  clearAll();
  ravenList.push(new raven(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 2; i++) {
    makeAussieBird(random(-5000, 5000), random(-2000, -100))
  }
  for (let i = 0; i < 2; i++) {
    makeAussieBird(random(-5000, 5000), random(2000, 100))
  }
}
function makeParrots() {
  clearAll();
  parrotList.push(new parrot(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 2; i++) {
    makeAussieBird(random(-5000, 5000), random(-2000, -100))
  }
  for (let i = 0; i < 2; i++) {
    makeAussieBird(random(-5000, 5000), random(2000, 100))
  }
}
function makeLorikeets() {
  clearAll();
  lorikeetList.push(new lorikeet(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 2; i++) {
    makeAussieBird(random(-5000, 5000), random(-2000, -100))
  }
  for (let i = 0; i < 2; i++) {
    makeAussieBird(random(-5000, 5000), random(2000, 100))
  }
}
function makeRoosters() {
  clearAll();
  roosterList.push(new rooster(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      chickenList.push(new chicken(false, random(TWO_PI), rx, -94, rz));
    }
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      chickenList.push(new chicken(false, random(TWO_PI), rx, -94, rz));
    }
  }
}
function makechickens() {
  clearAll();
  chickenList.push(new chicken(true, 0, 0, -94, 0)); // hero bird
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
function makeCrows() {
  clearAll();
  crowList.push(new crow(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      crowList.push(new crow(false, random(TWO_PI), rx, -114, rz));
    }
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      crowList.push(new crow(false, random(TWO_PI), rx, -114, rz));
    }
  }
}
function makeCardinals() {
  clearAll();
  cardinalList.push(new cardinal(true, 0, 0, -114, 0)); // hero seagull
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      cardinalList.push(new cardinal(false, random(TWO_PI), rx, -114, rz));
    }
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      cardinalList.push(new cardinal(false, random(TWO_PI), rx, -114, rz));
    }
  }
}
function makeMgulls() {
  clearAll();
  mgullList.push(new mgull(true, 0, 0, -114, 0)); // hero bird
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(-3000, -200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      mgullList.push(new mgull(false, random(TWO_PI), rx, -114, rz));
    }
  }
  for (let i = 0; i < 2; i++) {
    let rx = random(-5000, 5000)
    let rz = random(3000, 200)
    if (random(4) < 1) {
      pigeonList.push(new pigeon(false, random(TWO_PI), rx, -68, rz));
    } else {
      mgullList.push(new mgull(false, random(TWO_PI), rx, -114, rz));
    }
  }
}

function draw() { 
  if (POVtoggle == true) { //  camView = true
    camTimerLength = 10000;
    povTimeLenght = 2000;
    if (millis() - camTimer > camTimerLength && camView && primeBirdPecking && foodPecked >= 1) {
      camView = false;  // set camera to POV
      camRot = 0; // rotate camera 
      povTimer = millis(); // start pov timer
      foodList.push(new food(random(-5000, 5000), 0, false, true)); // put safety food in the middle 
    }
    if (millis() - povTimer > povTimeLenght && camView == false && primeBirdPecking && foodPecked >= 1) { // second two varaibles test
      camView = true;  // set camera to side view
      camRot = HALF_PI; // rotate camera 
      camTimer = millis(); // start pov timer
      for (let i = 0; i < foodList.length; i++) {
        if (foodList[i].testFood) {
          foodList[i].remove = true;
        }
      }
    }
    if (millis() - povTimer > povTimeLenght * 10 && camView == false) {  // false safe to go back out of POV mode
      camView = true;  // set camera to side view
      camRot = HALF_PI; // rotate the camera 
      camTimer = millis(); // start pov timer
      for (let i = 0; i < foodList.length; i++) {
        if (foodList[i].testFood) {
          foodList[i].remove = true;
        }
      }
    }

    if (!primeBirdPecking) {
      foodPecked = 0;  // this nerfs the food pecking stats, but it works without writing code in every bird
    }
  }

  if (birdSteps != oldBirdSteps) {
    oldBirdSteps = birdSteps;
  }
  if (foodPecked != oldfoodPecked) {
    updateTextOnly();
    oldfoodPecked = foodPecked;
    if (foodPecked == 1 && primeBirdPecking) {
      foodPeckedCounter++;
      birdNameLangNum++;
    }
    if (birdNameLangNum >= birdNames[birdNum].length) {
      birdNameLangNum = 0;
    }
    birdTerrirotyNum++;
    if (birdTerrirotyNum >= territory[birdNum].length) {
      birdTerrirotyNum = -1;
    }
  }
  if (panelPower < bwNum || localHour < 5 || localHour > 22) { // black and white
    textDiv.style('color', 'white');
  } else {
    textDiv.style('color', 'black');
  }
  if (panelPower >= bwNum && panelPower < greyNum) { // grayscale
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
  if (panelPower >= lightsOnNum) { // lights on shadow on
    showShadow = true;
    showLines = false;
    showLights = true;
    greyScale = false;
  }
  let x = 0;
  x = parseInt(localHour);
  bgColor = skyColorArray[int(localHour)];
  background(bgColor);
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

  batteryLevel = 12
  batteryLevelPer = batPercentSlider.value() / 100
  loadPower = 4
  panelPower = panelPowerSlider.value();
  localHour = hourSlider.value()
  localMinute = 30;

  if (panelPower < bwNum || localHour < 5 || localHour > 22) { // black and white
    textDiv.style('color', 'white');
    var links = document.getElementsByTagName("a");
    for (var i = 0; i < links.length; i++) {
      if (links[i].href) {
        links[i].style.color = "white";
      }
    }
  } else {
    textDiv.style('color', 'black');
    var links = document.getElementsByTagName("a");
    for (var i = 0; i < links.length; i++) {
      if (links[i].href) {
        links[i].style.color = "black";
      }
    }
  }


  if (primeBirdPecking) {
    if (primePeckingBuffer == false) {
      lookRot = 0;
    }
    primePeckingBuffer = true;
    primePeckingBufferNum = 0;
  }
  if (!primeBirdPecking && primePeckingBuffer) { // eases boolean a bit 
    primePeckingBufferNum++;
    if (primePeckingBufferNum > 4) {
      primePeckingBuffer = false;
      primePeckingBufferNum = 0;
    }
  }
  if (camView) { // side of bird
    if (mouseIsPressed && !pauseRotate) {
      if (mouseX != pmouseX) {
        if (millis() - globalFlyingTimer > globalFlyingInterval) {
          globalFlying = true;
          globalFlyingTimer = millis();
          globalFlyingInterval = 5 * 1000; // resets every 5 seconds
        }
      }
      camRot += (mouseX - pmouseX) / 200;
      camRot2 += (mouseY - pmouseY) / 200;
      camRot2 = constrain(camRot2, 3.2, 4, 2);
    }
    if (camJiggle == false && foodPecked == 1) {
      camRot += random(-.65, .65);
      camJiggle = true;
    }
    if (foodPecked == 0) {
      camJiggle = false;
    }
    let cx = cos(camRot) * 600;
    let cz = sin(camRot) * 600;
    let cy = sin(camRot2) * 600;
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
    cLoc.y = camVert;
    let mNum = random(5, 10) // random jerky 
    let camHor = sin(camHorNum * 3) * mNum
    let outFront = 280;
    cLoc.x = camHor + outFront;
    let cx2 = cos(camRot) * 600;
    let cz2 = sin(camRot) * 600;
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
    let ldirY = 1 - (abs(sin(ldirZ)));
    directionalLight(255, 255, 200, 0, ldirY, ldirZ);
    directionalLight(255, 255, 200, -1, 0, 0);
    let pRot = map(mouseY, 0, height, 0, TWO_PI); // sunRotation
    if (!dayNight) {
      sunRotation = 3;
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
  for (let i = 0; i < SWList.length; i++) {
    if (SWList[i].reset) {
      if (i == 0) {
        SWList[i].loc.x = SWList[SWList.length - 1].loc.x + SWList[i].SWSize;
      }
      else {
        SWList[i].loc.x = SWList[i - 1].loc.x + SWList[i].SWSize + walkSpeed;
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
  for (let i = 0; i < lorikeetList.length; i++) {
    lorikeetList[i].display();
  }
  for (let i = 0; i < seagullList.length; i++) {
    seagullList[i].display();
  }
  for (let i = bluejayList.length - 1; i >= 0; i--) {
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
  push();  // ground plane and horizon
  translate(0, 10, 0);
  noStroke();
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
    push();
    translate(1600, 0, 0);
    let rot = map(mouseY, 0, height, TWO_PI, PI);
    rotateX(sunRotation);
    translate(0, 0, -500);
    fill(255, 255, 0);
    noStroke();
    emissiveMaterial(200, 200, 0);
    pop();
  }
}
class rain {
  constructor() {
    this.loc = createVector(random(-1000, 1600), random(-20, -2000), random(-1000, 1000));
    this.falling = true;
    this.timer = 0;
    this.rSpeed = random(8, 12);
    this.puddleSize = 1;
  }
  display() {
    this.loc.x -= walkSpeed;
    if (this.falling) {
      this.loc.y += this.rSpeed;
    }
    if (this.loc.y >= -10) {
      this.falling = false
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
    translate(this.loc.x, this.loc.y, this.loc.z);
    stroke(100, 180, 255);
    fill(50, 100 - this.timer);
    if (panelPower < greyNum) {
      stroke(80);
      fill(50, 100 - this.timer);
    }
    if (panelPower < bwNum) {
      stroke(255);
      fill(180, 100 - this.timer);
    }
    if (this.falling == true) {
      line(0, 0, 0, 0, -40, 0);
    } else {
      rotateX(HALF_PI);
      noStroke()
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



let cities = ["Swarthmore", "Peterborough", "Sydney", "Alice Springs", "Nairobi", "Santiago", "Kalinago Territory", "Amsterdam", "Brooklyn", "Beijing", "Brooklyn 2", "Queens", "Alice Springs 2"]
let countries = ["USA", "Canada", "Australia", "Australia", "Kenya", "Chile", "Dominica", "The Netherlands", "USA", "China", "USA", "USA", "Australia"]

function bsout() {
  primeBirdPecking = false;
  birdNum = birdSlider.value();
  locCity = cities[birdNum];
  LocCountry = countries[birdNum];
  birdNameLangNum = 0;
  birdWalkBool = true; 
  updateDiv();
}
