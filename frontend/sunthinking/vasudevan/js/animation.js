let stars = [];
let spirals = [];
let smallStars = [];

let starImgs = [];
let spiralImgs = [];

let textAlpha = [0, -30, -60, -90, -120, -150];

let smallStarImg;
let stanza = 0;

let projectText = [['What would it mean to simply “turn off”?', 'To set aside time to hibernate and recuperate?', 'To not access or be accessed?', 'What would it mean to extend this permission beyond ourselves and other humans?', 'How would it change what we expect, and where we expect it from?'], ['Deep down, we each have a rhythm that guides us.', "It's hardwired into us—like hunger, thirst, or pain.", "It dictates when we rise, and when we rest.", "It's why we deflate as the days get shorter and shorter,", "And celebrate each extra minute of sunshine we can get."], ['But most of the time, we actively work against that rhythm.', 'We think we need everything now, immediately, all the time.', 'Constant connectivity, exchange, gratification, feedback, updates.', 'Are we actually built for this this sustained alertness?', 'Or do we now just accept overwhelm and fatigue as givens?'], ['What would it mean to simply “turn off”?', 'And to understand that other things are turning off too?', 'What does this free within us? What does it open up?', 'What changes by centering not what we demand,', 'But, instead, the correct time to get what we desire?']];

let liteText = [['When the sun goes down near the artist, this artwork goes down too.', "And when there's not enough sun to power it, it conserves its own energy.", 'The piece, in its entirety, only functions when there is natural energy to sustain it.', 'Why do we expect availability on demand?', 'Where does this expectation guide other parts of our lives?'], ['(The server’s battery is currently below 50% charged. Please check back at another time to view the full artwork.)']];

let offText = 'This artwork is currently in its “off” state and will be fully functional when the Solar Power for Artists server (closest geographically to the artist) is active and has over 50% battery charge.\n\nYou will most likely be able to view the piece during daylight hours on the US Eastern time zone; please return to this page then.';

let bgText = [];

function preload() {
  smallStarImg = loadImage('img/smallstar.png');

  for (var i = 0; i < 3; i++) {
    starImgs[i] = loadImage('img/star-' + i + '.png');
  }

  for (var i = 0; i < 2; i++) {
    spiralImgs[i] = loadImage('img/spiral-' + i + '.png');
  }


}

function setup() {
  createCanvas(windowWidth, windowHeight);
  // console.log(deviceOrientation);
  imageMode(CENTER);
  textAlign(CENTER);
  textFont("Times New Roman");
  textStyle(ITALIC);

  for (var i = 0; i < 20; i++) {
    var index = floor(random(3));
    let s = new Star(starImgs[index]);
    stars.push(s);
  }

  for (var i = 0; i < 2; i++) {
    let tempSpeed;
    if(i == 0) {
      tempSpeed = 1;
    } else {
      tempSpeed = -1;
    }
    let sp = new Spiral(spiralImgs[i], i * width, i * height, tempSpeed);
    spirals.push(sp);
  }

  for (var i = 0; i < 100; i++) {
    let sm = new Small(smallStarImg);
    smallStars.push(sm);
  }

  let wholeText = [];

  for (var i = 0; i < projectText.length; i++) {
    for (var j = 0; j < projectText[i].length; j++) {
      wholeText.push(projectText[i]);
    }
  }

  for (var i = 0; i < 20; i++) {

    var selection = floor(random(wholeText.length));
    bgText.push([wholeText[selection], random(1000), random(3)]);

    wholeText.splice(selection, 1);
  }

}

function draw() {
  if (windowWidth >= 1024) {
    if (state == 'on') { //if Swarthmore server is active and power is above 50%
      fullArtwork();
    } else if (state == 'low') { //if Swarthmore server is active and power is below 50%
      liteArtwork();
    } else { //is Swarthmore server is inactive
      artworkOff();
    }
  } else {
    background(0);
    rectMode(CENTER);
    textAlign(CENTER);
    textSize(100);
    textWrap(WORD);
    fill(255);
    text("This project is not optimized for portrait mode. Please view in landscape mode on a device, or on desktop.", width/2, height/2-width/2, width-100);
    // console.log('portrait');
  }


  // artworkOff();
  // liteArtwork();
  // fullArtwork();

}

function fullArtwork() { //full artwork
  background('#fb9f9f');

  drawShapes(false);
  drawText('full');
}

function liteArtwork() { //lite artwork
  background(75, 75, 75);

  drawShapes(true);
  drawText('lite');
}

function artworkOff() { //artwork is non-functional
  background(0);

  drawBackgroundText('off', false);
  drawText('off');
}

function drawBackgroundText(status, motion) {

  if (status === 'full') {
    fill(253, 226, 226, 60);
  } else if (status === 'lite') {
    fill(150, 150, 150, 30);
  } else {
    fill(50, 50, 50, 60);
  }
  noStroke();

  textAlign(LEFT);
  textSize(145);

  for (var i = 0; i < bgText.length; i++) {
    text(bgText[i][0], 0-bgText[i][1], (i + 1) * 50);

    if (motion) {
      if (bgText[i][1] >= textWidth(bgText[i][0])) {
        bgText[i][1] = 0-textWidth(bgText[i][0]);
      } else {
        bgText[i][1] = bgText[i][1] + bgText[i][2];
      }
    } else {
      bgText[i][1] = bgText[i][1] + 0;
    }
  }

  textAlign(CENTER);
}

function drawShapes(lite) {

  for (var i = 0; i < smallStars.length; i++) {
    if (!lite) {
      smallStars[i].spin();
    }
    smallStars[i].display();
  }

  if (lite) {
    drawBackgroundText('lite', false);
  } else {
    drawBackgroundText('full', true);
  }

  for (var i = 0; i < spirals.length; i++) {
    spirals[i].display();

    if (!lite) {
      spirals[i].move();
    }
  }

  for (var i = 0; i < stars.length; i++) {
    stars[i].display();

    if (!lite) {
      stars[i].move();
    }
  }

  if (lite) {
    filter(GRAY);
  }

}

function drawText(status) {
  rectMode(CENTER);
  if (status === "full") {
    fill(199, 88, 88);
    stroke(255);
  } else if (status === "lite") {
    fill(75);
    stroke(200);
  } else {
    fill(0);
    stroke(75);
  }

  strokeWeight(3);
  rect(width / 2, height / 2, 3.5*width/5, 1.5*height/3);

  noStroke();
  textSize(height/30);
  textAlign(CENTER);

  if (status == "full") {

    for (var i = 0; i < projectText[stanza].length; i++) {
      fill(255, textAlpha[i]);
      text(projectText[stanza][i], width/2, (height/2 - height/11) + (height/25*i));
      textAlpha[i] = textAlpha[i] + 0.5;
    }
    textAlpha[i]+= 0.5;
    fill(255, textAlpha[5]);
    textSize(height/45);
    textStyle(NORMAL);
    textAlign(RIGHT);

    if (stanza < projectText.length - 1) {
      text("Click to continue.", 4.1*width/5, 2.2*height/3 - height/25);
    } else {
      text("Click to restart.", 4.1*width/5, 2.2*height/3 - height/25);
    }

    textStyle(ITALIC);
    textAlign(CENTER);


  } else if (status == "lite") {

    for (var i = 0; i < liteText[0].length; i++) {
      fill(255, textAlpha[i]);
      text(liteText[0][i], width/2, (height/2 - height/8) + (height/25*i));
      textAlpha[i] = textAlpha[i] + 3;
    }
    textAlpha[i]+= 2;
    fill(255, textAlpha[5]);
    textSize(height/45);
    textStyle(NORMAL);
    textWrap(WORD);
    text(liteText[1], width/2, 2*height/3 - height/25, 3.5*width/5);
    textStyle(ITALIC);

    if (textAlpha[5] >= 255) {
      textAlpha = [0, -30, -60, -90, -120, -150];
    }

  } else {

    fill(175);
    textWrap(WORD);
    text(offText, width/2, height/2 - (0.35*height/3), 3*width/5);
  }

}

function mousePressed() {
  if (state === "on" && stanza >= projectText.length-1) {
    stanza = 0;
  } else if (state === "on") {
    stanza++;
  }

  textAlpha = [0, -30, -60, -90, -120, -150];
}

class Star {
  constructor(img) {
    this.x = random(50, width - 50);
    this.y = random(height);
    this.img = img;
    this.speed = random(0.1, 5);

    this.img.resize(0, 100);
  }

  display() {
    image(this.img, this.x, this.y);
  }

  move() {
    if (this.x > width + this.img.width / 2) {
      this.x = -this.img.width / 2;
    } else {
      this.x = this.x + this.speed;
    }
  }
}

class Spiral {

  constructor(img, x, y, speed) {
    this.x = x;
    this.y = y;
    this.img = img;
    this.speed = speed;
    this.startingX = this.x;
    this.startingY = this.y;
    this.rads = 0;
    this.rotateSpeed = random(-0.01, 0.02);
  }

  display() {
    push();
      translate(this.x, this.y);
      rotate(this.rads);
      image(this.img, 0, 0);
    pop();
  }

  move() {
    if (this.x > width + this.img.width / 2 || this.x < -this.img.width / 2) {
      this.speed = this.speed * -1;
    }
    this.x = this.x + this.speed;
    this.y = this.y + this.speed;

    this.rads += this.rotateSpeed;
  }
}

class Small {
  constructor(img) {
    this.img = img;
    this.x = random(width);
    this.y = random(height);
    this.speed = random(0.005, 0.03);
    this.rads = 0;
  }

  display() {
    push();
      translate(this.x, this.y);
      rotate(this.rads);
      image(this.img, 0, 0);
    pop();
  }

  spin() {

    this.rads += this.speed;
  }
}
