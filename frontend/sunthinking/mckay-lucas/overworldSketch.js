// Peckish (2023) by Kristin Lucas and Joe McKay
// Co-programmed in p5.js
// Commissioned by Solar Protocol
// http://solarprotocol.net/

let testBool = true; // true means you're in test mode 

let birdNames = [];
let birdNum = 0;
let todArray = ["Dawn", "Morning", "Late Morning", "Midday", "Afternoon", "Evening", "Dusk", "Night"];
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
let totalTiles = 20 // divided by 2
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
let bwNum = 2; //  up to this number it's b/w
let greyNum = 6;
let noLightsNum = 12;
let lightsOnNum = 25;
let camVertNum = 0;
let camHorNum = 0;
let camView = true;
let batPercentSlider;
let panelPowerSlider;
let hourSlider;
let foodFrequency = 30; // how much food there is at any one time
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
let povTimeLength = 20 * 1000;
let camTimerLength = 120 * 1000;
let lookPoint;
let lookRot = 0;
let POVtoggle = true;
let birdNameLangNum = 0;
let globalFlying = false;
let globalFlyingTimer;
let globalFlyingInterval = 1000; // wait 1 second and fly away 
let flyingIntervalHigh = 30000;
let flyingIntervalLow = 10000;
let pauseRotate = false;
let b;

let flyDelay = 2000;
let pigeonTimer = flyDelay;
let pigeonBool = false;
let pigeonFlySpeed = .01;

let roosterTimer = flyDelay;
let roosterBool = false;
let roosterFlySpeed = .01;

let parrotTimer = flyDelay;
let parrotBool = false;
let parrotFlySpeed = .01;

let ravenTimer = flyDelay;
let ravenBool = false;
let ravenFlySpeed = .01;

let crowTimer = flyDelay;
let crowBool = false;
let crowFlySpeed = .01;

let lorikeetTimer = flyDelay;
let lorikeetBool = false;
let lorikeetFlySpeed = .01;

let robinTimer = flyDelay;
let robinBool = false;
let robinFlySpeed = .01;

let seagullTimer = flyDelay;
let seagullBool = false;
let seagullFlySpeed = .01;

let mgullTimer = flyDelay;
let mgullBool = false;
let mgullFlySpeed = .01;

let cardinalTimer = flyDelay;
let cardinalBool = false;
let cardinalFlySpeed = .01;

let ncardinalTimer = flyDelay;
let ncardinalBool = false;
let ncardinalFlySpeed = .01;

let bluejayTimer = flyDelay;
let bluejayBool = false;
let bluejayFlySpeed = .01;

let flyTopSpeed = 30.0;
let flyAccel = 0.25
let OVworld = true; 
let DO;

function goToPeckish() {
    window.open("live.html", "_self")
}
function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
    let w = int(map(windowWidth, 1680, 320, 380, 250, true));
    let ws = w   + "px";   
    textDiv.style('width', ws);

    if(deviceOrientation == LANDSCAPE){
        textDiv.position(width/2 - w/2 - 20, 20);
      }else{
        textDiv.position(width/2 - w/2 - 20, 120);
      }
}

function setup() {
    let cnv = createCanvas(windowWidth, windowHeight, WEBGL);
    cnv.parent("myContainer");
    DO = deviceOrientation; 
    pigeonTimer += random(-500, 500); 
    roosterTimer += random(-500, 500); 
    parrotTimer += random(-500, 500); 
    ravenTimer += random(-500, 500); 
    crowTimer += random(-500, 500);
    lorikeetTimer += random(-500, 500);
    robinTimer += random(-500, 500);
    seagullTimer += random(-500, 500);
    mgullTimer += random(-500, 500);
    cardinalTimer += random(-500, 500);
    ncardinalTimer += random(-500, 500);
    bluejayTimer += random(-500, 500);

    textDiv = createDiv('');
    textDiv.id("infoDiv1"); 
    let tsNum = int(map(displayWidth, 1680, 320, 24, 12)); 
    let ts = tsNum + "px"; 
    textDiv.style('font-size', ts);
    textDiv.style('color', 'black');
    let w = int(map(windowWidth, 1680, 320, 380, 250));
    let ws = w   + "px";   
    textDiv.style('width', ws);
    textDiv.position(width/2 - w/2, 120);


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
    updateDiv();
}

function updateDiv() {

    textDiv.html("<div class=\"center\">→ <a href = live.html>enter</a></div>", false);
    flying = true;
    globalFlying = true;
    pigeonList.push(new pigeon(false, random(TWO_PI), -600, -68 - 400, -200));
    roosterList.push(new rooster(false, random(TWO_PI), -200, -94 - 400, -200));
    parrotList.push(new parrot(false, random(TWO_PI), 200, -114 - 400, -200));
    ravenList.push(new raven(false, random(TWO_PI), 600, -114 - 400, -200));

    crowList.push(new crow(false, random(TWO_PI), -600, -114, -200));
    lorikeetList.push(new lorikeet(false, random(TWO_PI), -200, -114, -200));
    robinList.push(new robin(false, random(TWO_PI), 200, -94, -200));
    seagullList.push(new seagull(false, random(TWO_PI), 600, -114, -200));

    mgullList.push(new mgull(false, random(TWO_PI), -600, -114 + 400, -200));
    cardinalList.push(new cardinal(false, random(TWO_PI), -200, -114 + 400, -200));
    ncardinalList.push(new ncardinal(false, random(TWO_PI), 200, -93 + 400, -200));
    bluejayList.push(new bluejay(false, random(TWO_PI), 600, -114 + 400, -200));
}

function draw() {
    if(DO != deviceOrientation){
        let w = int(map(windowWidth, 1680, 320, 400, 250, true));
        let ws = w   + "px";   
        textDiv.style('width', ws);
        if(deviceOrientation == LANDSCAPE){
          textDiv.position(width/2 - w/2 - 20, 20);
        }else{
          textDiv.position(width/2 - w/2 - 20, 120);
        }
        DO = deviceOrientation; 
    }
    panelPower = 50;
    if (panelPower >= lightsOnNum) { // lights on shadow on
        showShadow = false;
        showLines = false;
        showLights = true;
        greyScale = false;
    }
    let x = 0;
    localHour = 12;
    x = parseInt(localHour);
    bgColor = skyColorArray[int(localHour)];
    background(bgColor);

    if (panelPower < greyNum) {
        background(200);
    }
    if (panelPower < bwNum) {
        background(1);
    }
    batteryLevel = 12
    loadPower = 4
    camera(0, -320, 2000, 0, -100, 0, 0, 1, 0); // side view do not destroy
    walkSpeed = 0;
    let homeRotY = .01;
    globalFlying = true;

    pigeonList[0].display(); // show the pigeon
    if (pigeonBool) { // if it's flying
        pigeonList[0].rootLoc.x += sin(pigeonList[0].YRot + HALF_PI) * pigeonFlySpeed;
        pigeonList[0].rootLoc.z += cos(pigeonList[0].YRot + HALF_PI) * pigeonFlySpeed;
        pigeonList[0].flying = true;
        pigeonList[0].rootLoc.y -= pigeonFlySpeed;
        if (pigeonFlySpeed < flyTopSpeed) {
            pigeonFlySpeed += flyAccel;
        }
    }
    else {
        pigeonList[0].YRot += homeRotY;
    }
    if (millis() > pigeonTimer && !pigeonBool) { // make pigeon fly after timer 
        let tempRot = pigeonList[0].YRot; // get rotation of pigeon
        pigeonList.splice(0, 1); // delete pigeon 
        pigeonBool = true;
        pigeonList.push(new pigeon(true, tempRot, -600, -68 - 400, -200)); // make a new pigeon
    }
    roosterList[0].display(); // show the pigeon
    if (roosterBool) { // if it's flying
        roosterList[0].rootLoc.x += sin(roosterList[0].YRot + HALF_PI) * roosterFlySpeed;
        roosterList[0].rootLoc.z += cos(roosterList[0].YRot + HALF_PI) * roosterFlySpeed;
        roosterList[0].flying = true;
        roosterList[0].rootLoc.y -= roosterFlySpeed;
        if (roosterFlySpeed < flyTopSpeed) {
            roosterFlySpeed += flyAccel;
        }
    }
    else {
        roosterList[0].YRot += homeRotY;
    }
    if (millis() > roosterTimer && !roosterBool) { 
        let tempRot = roosterList[0].YRot; 
        roosterList.splice(0, 1);  
        roosterBool = true;
        roosterList.push(new rooster(true, tempRot, -200, -94 - 400, -200));
    }

    parrotList[0].display(); 
    if (parrotBool) { 
        parrotList[0].rootLoc.x += sin(parrotList[0].YRot + HALF_PI) * parrotFlySpeed;
        parrotList[0].rootLoc.z += cos(parrotList[0].YRot + HALF_PI) * parrotFlySpeed;
        parrotList[0].flying = true;
        parrotList[0].rootLoc.y -= parrotFlySpeed;
        if (parrotFlySpeed < flyTopSpeed) {
            parrotFlySpeed += flyAccel;
        }
    }
    else {
        parrotList[0].YRot += homeRotY;
    }
    if (millis() > parrotTimer && !parrotBool) {  
        let tempRot = parrotList[0].YRot; 
        parrotList.splice(0, 1); 
        parrotBool = true;
        parrotList.push(new parrot(true, tempRot, 200, -114 - 400, -200));
    }

    ravenList[0].display(); 
    if (ravenBool) { 
        ravenList[0].rootLoc.x += sin(ravenList[0].YRot + HALF_PI) * ravenFlySpeed;
        ravenList[0].rootLoc.z += cos(ravenList[0].YRot + HALF_PI) * ravenFlySpeed;
        ravenList[0].flying = true;
        ravenList[0].rootLoc.y -= ravenFlySpeed;
        if (ravenFlySpeed < flyTopSpeed) {
            ravenFlySpeed += flyAccel;
        }
    }
    else {
        ravenList[0].YRot += homeRotY;
    }
    if (millis() > ravenTimer && !ravenBool) { 
        let tempRot = ravenList[0].YRot; 
        ravenList.splice(0, 1); 
        ravenBool = true;
        ravenList.push(new raven(true, tempRot, 600, -114 - 400, -200));
    }

    crowList[0].display(); 
    if (crowBool) { 
        crowList[0].rootLoc.x += sin(crowList[0].YRot + HALF_PI) * crowFlySpeed;
        crowList[0].rootLoc.z += cos(crowList[0].YRot + HALF_PI) * crowFlySpeed;
        crowList[0].flying = true;
        crowList[0].rootLoc.y -= crowFlySpeed;
        if (crowFlySpeed < flyTopSpeed) {
            crowFlySpeed += flyAccel;
        }
    }
    else {
        crowList[0].YRot += homeRotY;
    }
    if (millis() > crowTimer && !crowBool) { 
        let tempRot = crowList[0].YRot; 
        crowList.splice(0, 1); 
        crowBool = true;
        crowList.push(new crow(true, tempRot, -600, -114, -200));
    }
    
    lorikeetList[0].display(); 
 if (lorikeetBool) { 
    lorikeetList[0].rootLoc.x += sin(lorikeetList[0].YRot + HALF_PI ) * lorikeetFlySpeed; 
    lorikeetList[0].rootLoc.z += cos(lorikeetList[0].YRot + HALF_PI) *  lorikeetFlySpeed; 
    lorikeetList[0].flying = true;
    lorikeetList[0].rootLoc.y -= lorikeetFlySpeed;
    if (lorikeetFlySpeed < flyTopSpeed) {
        lorikeetFlySpeed += flyAccel;
    }
 }
else {
    lorikeetList[0].YRot += homeRotY;
 }
 if (millis() > lorikeetTimer && !lorikeetBool) {
   let tempRot = lorikeetList[0].YRot;
  lorikeetList.splice(0, 1); 
   lorikeetBool = true;
   lorikeetList.push(new lorikeet(true, tempRot, -200, -114, -200));
 }
 globalFlying = true;
 robinList[0].display();
 if (robinBool) {
    
    robinList[0].rootLoc.x += sin(robinList[0].YRot + HALF_PI ) * robinFlySpeed; 
    robinList[0].rootLoc.z += cos(robinList[0].YRot + HALF_PI) *  robinFlySpeed; 
    robinList[0].flying = true;
    robinList[0].rootLoc.y -= robinFlySpeed;
    if (robinFlySpeed < flyTopSpeed) {
        robinFlySpeed += flyAccel;
    }
 }
else {
    robinList[0].YRot += homeRotY;
 }
 if (millis() > robinTimer && !robinBool) {
   let tempRot = robinList[0].YRot;
  robinList.splice(0, 1); 
   robinBool = true;
   
   robinList.push(new robin(true, tempRot, 200, -94, -200));
 }

 seagullList[0].display();
 if (seagullBool) {
    seagullList[0].rootLoc.x += sin(seagullList[0].YRot + HALF_PI ) * seagullFlySpeed; 
    seagullList[0].rootLoc.z += cos(seagullList[0].YRot + HALF_PI) *  seagullFlySpeed; 
    seagullList[0].flying = true;
    seagullList[0].rootLoc.y -= seagullFlySpeed;
    if (seagullFlySpeed < flyTopSpeed) {
        seagullFlySpeed += flyAccel;
    }
 }
else {
    seagullList[0].YRot += homeRotY;
 }
 if (millis() > seagullTimer && !seagullBool) {
   let tempRot = seagullList[0].YRot;
  seagullList.splice(0, 1);
   seagullBool = true;
   seagullList.push(new seagull(true, tempRot,  600, -114, -200));
 }

 mgullList[0].display();
 if (mgullBool) {
    mgullList[0].rootLoc.x += sin(mgullList[0].YRot + HALF_PI ) * mgullFlySpeed; 
    mgullList[0].rootLoc.z += cos(mgullList[0].YRot + HALF_PI) *  mgullFlySpeed; 
    mgullList[0].flying = true;
    mgullList[0].rootLoc.y -= mgullFlySpeed;
    if (mgullFlySpeed < flyTopSpeed) {
        mgullFlySpeed += flyAccel;
    }
 }
else {
    mgullList[0].YRot += homeRotY;
 }
 if (millis() > mgullTimer && !mgullBool) {
   let tempRot = mgullList[0].YRot;
  mgullList.splice(0, 1); 
   mgullBool = true;
   mgullList.push(new mgull(true, tempRot,  -600, -114 + 400, -200));
 }

 cardinalList[0].display();
 if (cardinalBool) {
    cardinalList[0].rootLoc.x += sin(cardinalList[0].YRot + HALF_PI ) * cardinalFlySpeed; 
    cardinalList[0].rootLoc.z += cos(cardinalList[0].YRot + HALF_PI) *  cardinalFlySpeed; 
    cardinalList[0].flying = true;
    cardinalList[0].rootLoc.y -= cardinalFlySpeed;
    if (cardinalFlySpeed < flyTopSpeed) {
        cardinalFlySpeed += flyAccel;
    }
 }
else {
    cardinalList[0].YRot += homeRotY;
 }
 if (millis() > cardinalTimer && !cardinalBool) {
   let tempRot = cardinalList[0].YRot;
  cardinalList.splice(0, 1); 
   cardinalBool = true;
   cardinalList.push(new cardinal(true, tempRot, -200, -114 + 400, -200));
 }

 ncardinalList[0].display();
 if (ncardinalBool) {
    ncardinalList[0].rootLoc.x += sin(ncardinalList[0].YRot + HALF_PI ) * ncardinalFlySpeed; 
    ncardinalList[0].rootLoc.z += cos(ncardinalList[0].YRot + HALF_PI) *  ncardinalFlySpeed; 
    ncardinalList[0].flying = true;
    ncardinalList[0].rootLoc.y -= ncardinalFlySpeed;
    if (ncardinalFlySpeed < flyTopSpeed) {
        ncardinalFlySpeed += flyAccel;
    }
 }
else {
    ncardinalList[0].YRot += homeRotY;
 }
 if (millis() > ncardinalTimer && !ncardinalBool) { 
   let tempRot = ncardinalList[0].YRot;
  ncardinalList.splice(0, 1);
   ncardinalBool = true;
   ncardinalList.push(new ncardinal(true, tempRot,  200, -93 + 400, -200));
 }

 bluejayList[0].display();
 if (bluejayBool) {
    bluejayList[0].rootLoc.x += sin(bluejayList[0].YRot + HALF_PI ) * bluejayFlySpeed; 
    bluejayList[0].rootLoc.z += cos(bluejayList[0].YRot + HALF_PI) *  bluejayFlySpeed; 
    bluejayList[0].flying = true;
    bluejayList[0].rootLoc.y -= bluejayFlySpeed;
    if (bluejayFlySpeed < flyTopSpeed) {
        bluejayFlySpeed += flyAccel;
    }
 }
else {
    bluejayList[0].YRot += homeRotY;
 }
 if (millis() > bluejayTimer && !bluejayBool) { 
   let tempRot = bluejayList[0].YRot;
  bluejayList.splice(0, 1); 
   bluejayBool = true;
   bluejayList.push(new bluejay(true, tempRot,  600, -114 + 400, -200));
 }

}