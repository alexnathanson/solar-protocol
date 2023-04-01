class crow {
  constructor(_w, _YRot, _x, _y, _z) {
    this.rootLoc = createVector(_x, _y, _z); //-114
    this.bodySize = 110; //110
    this.headsize = 46; //46
    this.leg1Length = 70;
    this.leg2Length = 60;
    this.walkRotSpeed = 0;
    this.bodyTilt = 1.1; // .77 .5
    this.bodyTiltHome = 1.1;
    this.peckDRot = 2.2; // 1.71;
    this.peckSpeed = .1;
    this.peckDir = true;
    this.wingWidth = 50;
    this.wingLength = 200; //180
    this.wingWidthUp = 20;

    this.headColor = color(0); // 86, 86, 86
    this.bodyColor = color(0); // 200, 150,  170); 
    this.wingColor = color(0); //0, 180, 220 
    this.neckColor = color(0); //fill(200, 150,  170)
    this.feetColor = color(86, 86, 86); //fill(200, 150,  170) 162, 87, 127
    this.legColor = color(0); //26, 163, 109
    this.tailColor = color(0);
    this.sideTiltAmount = 12;  // higher less tilt  12
    this.neckBobNum = 18; // higher less tilt 
    this.headBobNum = 18; // higher less tilt 
    this.YRot = _YRot;
    this.mainBird = _w;
    this.detail = 20;

    this.headRotY = 0;
    this.birdPecking = true;
    this.pecknum = 0;
    this.peckNumMax = 1;
    this.foodNum = -1;
    //this.lockedOnSeed = false;
    this.moveZValue = 0;
    this.returnToCenter = false;
    this.stColor = color(1, 1, 1);
    this.bw = false;

    this.greyToggle = !greyScale;
    this.walkDir = false
    this.delayCounter = 0;
  }

  display() {

    if (this.greyToggle != greyScale) {
      this.greyToggle = greyScale;
      if (greyScale) {
        this.headColor = color(0); // 86, 86, 86
        this.bodyColor = color(0); // 200, 150,  170); 
        this.wingColor = color(0); //0, 180, 220 
        this.neckColor = color(0); //fill(200, 150,  170)
        this.feetColor = color(220); //fill(200, 150,  170) 162, 87, 127
        this.legColor = color(0); //26, 163, 109
        this.tailColor = color(0);
      }
      if (!greyScale) {
        this.headColor = color(0); // 86, 86, 86
        this.bodyColor = color(0); // 200, 150,  170); 
        this.wingColor = color(0); //0, 180, 220 
        this.neckColor = color(0); //fill(200, 150,  170)
        this.feetColor = color(86, 86, 86); //fill(200, 150,  170) 162, 87, 127
        this.legColor = color(0); //26, 163, 109
        this.tailColor = color(0);
      }
    }

    if (panelPower < bwNum) {
      this.bw = true;
      this.stColor = color(255, 255, 255)
    }
    else {
      this.bw = false;
      this.stColor = color(1)
    }

    let t = createVector(220, 0, this.rootLoc.z); // peck location
    // push()
    // translate(t.x, t.y, t.z); 
    // sphere(5)
    // pop() 


    if (this.mainBird && this.birdPecking == false) {
      for (let i = foodList.length - 1; i >= 0; i--) {
        let fd = foodList[i].loc;
        if (fd.dist(t) < 120 && foodList[i].ignore == false && fd.x < t.x) { // peck if it's within range. 
          this.birdPecking = true;
          birdWalkBool = false;
          this.foodNum = i;
          this.peckNumMax = foodList[i].peckNumFood
          let look = map(foodList[i].loc.z, 0, 50, .1, -.1)
          this.headRotY = look;
        }
      }
    
      if (this.headRotY > .06) {
        this.headRotY -= .05
      } else if (this.headRotY < -.06) {
        this.headRotY += .05
      } else {
        this.headRotY = 0;
      }

    }

    if (this.birdPecking && this.mainBird) { // if it's pecking 
      this.bodyTilt += this.peckSpeed;
      this.moveZValue = 0;
      primeBirdPecking = true;
      if (this.bodyTilt > this.peckDRot) { // this.peckDRot) {
        this.peckSpeed *= -1;
        this.pecknum++;
        foodPecked++; // here 
        if (this.pecknum >= this.peckNumMax) {
          if (this.foodNum >= 0) {
            if (foodList[this.foodNum].discard == false) {
              birdSteps = 0;  // here 
              foodPecked = 0; // here
              foodList[this.foodNum].remove = true; // if it's a normal seed, eat it.
            } else {
              //this.birdPecking = false;  // if its a discard seed, leave it alone and ignore it 
              foodList[this.foodNum].ignore = true;
            }
            this.pecknum = 0;
            this.peckNumMax = 1;
          }
        } else {
          foodList[this.foodNum].loc.x += random(-8, 8) // move food to Peck point. 
          foodList[this.foodNum].loc.z += random(-8, 8)
          foodList[this.foodNum].YRot += random(-.5, .5)
        }
      }
      if (this.bodyTilt < this.bodyTiltHome) { // this is where it bugs out. 
        this.delayCounter = 0;
        this.peckSpeed *= -1;
        this.birdPecking = false;
        primeBirdPecking = false;
        birdWalkBool = true;
      }
    }
    this.detail = int(map(panelPower, 0, 50, 5, 20)) // technically the panel can put out 50 W, but we should change this because it's rarley that high
    if (this.mainBird ) {
      if(!primeBirdPecking){
        this.walkRotSpeed += map(walkSpeed, 0, 6, 0, 0.1); //set the bird steps to match the walking speed was  .2
      }
    }
    else {
      this.rootLoc.x -= walkSpeed; // make birds that are not walking move with the sidewalk 
    }
    this.walkRotSpeed = this.walkRotSpeed % TWO_PI;
  //  if (this.mainBird ) {
  //   print(this.walkRotSpeed); 
  //  }
    if (this.rootLoc.x < -5000) { // reset bystandard  birds. 
      this.rootLoc.x = int(random(5000, 7000));
      if (this.rootLoc.z > 0) {
        this.rootLoc.z = random(3000, 200)
      } else {
        this.rootLoc.z = random(-3000, -200)
      }
    }
    push();
    stroke(this.stColor);
    if (!showLines) {
      noStroke();
    }
    if (this.bw) {
      stroke(255);
    }
    translate(this.rootLoc.x, this.rootLoc.y, this.rootLoc.z); // root: the pivot point of bird
    rotateY(this.YRot + this.headRotY);
    push();

    rotateZ(this.bodyTilt); //rotTest
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // 
    translate(-this.bodySize / 5, -this.bodySize / 3, 0); // center of body //-this.bodySize / 2.5, 0
    fill(this.bodyColor)
    if (this.bw) {
      noFill();
    }
    ellipsoid(this.bodySize * .6, this.bodySize * 1, this.bodySize * .7, this.detail, this.detail)  // draw body  //this.bodySize * .7, this.bodySize, this.bodySize * .9

    translate(-17, 2, 0);
    fill(this.wingColor);
    if (this.bw) {
      noFill();
    }
    ellipsoid(this.bodySize * .5, this.bodySize * .5, this.bodySize * .6, this.detail, this.detail)  // back of bird

    // sphere(this.bodySize, this.detail, this.detail);
    pop(); // back to root
  // if (this.mainBird ) {
  //     if(!primeBirdPecking){
  //       this.walkRotSpeed += map(walkSpeed, 0, 6, 0, 0.1); //set the bird steps to match the walking speed was  .2
  //     }
  //   }
    push();
    translate(30, -18, this.bodySize - 44); // right hip
     this.drawLeg(PI); // 0 is red 
     pop(); 
    pop(); // back to root;;
   
    //cylinder(100, 50); 
    push();
    translate(30, -18, - this.bodySize + 44); // LEFT hip
    this.drawLeg(0);  // normal color is PI
    pop(); 
    pop(); // back to root
    push()

    rotateZ(this.bodyTilt + 5.3); // tilt of the whole body //5.6
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // bob neck on the X 
    rotateZ(sin((this.walkRotSpeed * 2) + HALF_PI) / this.neckBobNum);  // bob neck 

    this.neckLength = 50; //90
    this.neckwidth = 48; //55
    this.neckwidthUp = 33; //30
    // translate(-this.bodySize / 6, -this.bodySize - this.neckLength / 2, 0) // middle of neck 
    translate(-this.bodySize / 2 + 115, -this.bodySize - this.neckLength / 8, 0) // middle of neck 


    let rNeckY = map(this.detail, 0, 20, 2.42, 1.288);
    // rotateY(rNeckY); // rotate so the neck color works 
    let PLow = []
    let PHigh = []
    let rot = 0;
    let faceNum = this.detail; // map(this.detail, 4, 20, 4, 12); //12; // # of sides of the neck 
    for (let i = 0; i < faceNum; i++) {
      let r = TWO_PI / faceNum;
      rot += r;
      // PLow are the points where the neck meets the body 
      // PHight are the points whre the neck meets the head
      PLow[i] = createVector(cos(rot) * this.neckwidth, this.neckLength / 2, sin(rot) * this.neckwidth)
      PHigh[i] = createVector(cos(rot) * this.neckwidthUp, -this.neckLength / 2, sin(rot) * this.neckwidthUp)
    }
    fill(this.neckColor)
    if (this.bw) {
      noFill();
    }
    let neckSec = map(this.detail, 0, 20, 1, 6);
    for (let i = 0; i < PLow.length - 1; i++) { // draw most of the neck
      beginShape();
      vertex(PLow[i].x, PLow[i].y, PLow[i].z);
      vertex(PLow[i + 1].x, PLow[i + 1].y, PLow[i + 1].z);
      vertex(PHigh[i + 1].x, PHigh[i + 1].y, PHigh[i + 1].z);
      vertex(PHigh[i].x, PHigh[i].y, PHigh[i].z);
      endShape(CLOSE);
    }
    // if(this.bw){
    //   noFill(); 
    // }
    beginShape(); // draw the final panel of the neck
    vertex(PLow[PLow.length - 1].x, PLow[PLow.length - 1].y, PLow[PLow.length - 1].z);
    vertex(PLow[0].x
      , PLow[0].y, PLow[0].z);
    vertex(PHigh[0].x, PHigh[0].y, PHigh[0].z);
    vertex(PHigh[PLow.length - 1].x, PHigh[PLow.length - 1].y, PHigh[PLow.length - 1].z);
    endShape(CLOSE);
    translate(0, -this.neckLength / 3 - this.headsize / 2, 0) // center of head
    rotateZ(sin((-this.walkRotSpeed * 2) - HALF_PI) / this.headBobNum);  // bob head 
    fill(this.headColor)
    if (this.bw) {
      noFill();
    }
    //rotateY(-rNeckY); // rotate back so the neck color works 
    translate(12, 6, 0);
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    // rotateY(this.headRotY); 
    rotateZ(6.3);

    ellipsoid(this.headsize, this.headsize * .7, this.headsize * .8, this.detail, this.detail) // test head
    push()

    translate(67, -10, 0)  // beak //70,0,0
    fill(86, 86, 86) //255, 255, 0
    if (this.bw) {
      noFill();
    }
    rotateZ(-HALF_PI + .05) // rotate beak down
    cone(10, 80, this.detail, false);// beak size scale //12, 70
    //fill(255, 0, 0); // red nose ellipsoid
    if (this.bw) {
      noFill();
    }
    push();
    translate(-8.75, 0, 0) // lower beak
    rotateZ(-HALF_PI + 1.35) // rotate lower beak
    fill(86, 86, 86);
    if (this.bw) {
      noFill();
    }
    cone(8, 80, this.detail, false);// beak size scale //12, 70
    pop();

    rotateZ(HALF_PI - .2)
    translate(-33, -5, 0) // nose ellipsoid
    ellipsoid(20, 12, 20, this.detail, this.detail) // red nose ellipsoid
    pop()
    push()
    fill(86, 86, 86)
    stroke(120, 120, 120) // torus 
    if (this.bw) {
      noFill();
      stroke(255);
    }
    translate(15, -10, this.headsize - 12) // right eye 
    rotateX(.325)
    rotateY(.3)
    let torusDetail = int(map(this.detail, 0, 20, 1, 14)); //0, 20, 1, 14
    torus(6, 2, torusDetail, torusDetail); //(14, 2
    fill(1)
    stroke(1)
    if (this.bw) {
      noFill();
      stroke(255);
    }
    sphere(6, this.detail, this.detail)
    pop()

    push()

    fill(120, 120, 120) //fill torus
    stroke(120, 120, 120) //fill torus
    if (this.bw) {
      noFill();
      stroke(255);
    }
    translate(15, -10, -this.headsize + 12) // right eye 
    rotateX(-.325)
    rotateY(-.3)
    torus(6, 2, torusDetail, torusDetail);
    fill(1); //1
    stroke(1)
    if (this.bw) {
      noFill();
      stroke(255);
    }
    sphere(6, this.detail, this.detail)

    pop()
    pop()
    push() // back to root
    fill(255)
    if (this.bw) {
      noFill();
    }
    rotateZ(this.bodyTilt); //rotTest
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);

    push() // left wing
    translate(-55, 10, this.bodySize * 0.6) // right wing
    rotateZ(-.25) // right wing rotation tilt
    //   rotateY(0.6) 
    //   rotateX(6.05) 
    this.drawWing(3.51, 0.6, 6.05) // separate function for wings because there's two of them 
    pop()
    push() // right wing
    //translate(-80, -40, -this.bodySize)
    translate(-55, 10, -this.bodySize * 0.6) // left wing //100, -20, .6
    rotateZ(-.15) // left wing rotation tilt
    //this.drawWing(3.376, 3.0, 5.91)
    this.drawWing(3.51, 3.0, 6.05)
    pop()

    push()
    translate(-50, 147, 0) // tail feather 
    rotateZ(0.25) //.615
    //rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    fill(this.tailColor)
    if (this.bw) {
      noFill();
    }
    cone(this.bodySize * .35, 200, this.detail, false, false)
    pop()
    pop()
    //this.rootLoc.y
    if (this.mainBird && showShadow) {
      translate(0, -this.rootLoc.y - 1, 0) // shaddow
      rotateX(HALF_PI)
      noStroke()
      fill(10, 30)
      if (this.bw) {
        noFill();
      }
      let wiggle = sin(this.walkRotSpeed) * 5
      ellipse(0, wiggle, 320, 210)  // center of body 
      translate(0, 0, 1)

      ellipse(160 + wiggle, wiggle, 80, 80) // center of head 
      let tx = 215; // center of triangle 
      let tSize = 20;  // first is point
      triangle(tx + tSize + wiggle, wiggle, tx - tSize + wiggle, -tSize / 2 + wiggle, tx - tSize + wiggle, tSize / 2 + wiggle)
      tx = -210;
      tSize = 60;
      triangle(tx * 1.5 - tSize - wiggle, wiggle, tx + tSize + wiggle, -tSize / 2 + wiggle, tx + tSize + wiggle, tSize / 2 + wiggle)
    }
    pop();
    if(this.delayCounter < 10){
      this.delayCounter ++; 
    }
    //print(this.delayCounter); 
  }
  drawLeg(_rotOffset) {
    // let joeX = map(mouseX, 0, width, 0, 2); 
    if (this.mainBird) {
      //  print(_rotOffset); 
        if (this.walkRotSpeed > TWO_PI - .4 && this.walkDir == false && _rotOffset == 0) {
          this.walkDir = true; 
          birdSteps ++; 
      } 
      if (this.walkRotSpeed < PI + .4 && this.walkRotSpeed > PI + .1 && _rotOffset == 0) {
        if (this.walkDir == true) {
          this.walkDir = false;
          birdSteps ++;
        }
      }
    }

   
    if (this.mainBird) {
      if (!primePeckingBuffer) {
        rotateZ(sin(this.walkRotSpeed + _rotOffset) / 2 + .15);
      } else {    
        rotateZ(0.15); // was 1.06 was 0.5
      }
    } else {
      rotateZ(0.15); //
    }
    translate(-10, this.leg1Length / 2.25, 0); // upper  leg
    fill(this.legColor);
    if(this.bw){
      noFill(); 
    }
    cylinder(12, this.leg1Length, this.detail);
    translate(0, this.leg1Length / 2, 0); //  knee
    if (this.mainBird) {
      if (!primePeckingBuffer) {
        rotateZ(cos(this.walkRotSpeed + _rotOffset) / 2 + 5.8); // 4.8
      } else {
        // let joeR = map(mouseX, 0, width, 0, TWO_PI); 
        rotateZ(-.2); // 5.23
      }
    } else {
      rotateZ(-.2); // 5.23
    }
    translate(0, this.leg2Length / 2, 0); // lower right leg
    fill(this.feetColor);
    if(this.bw){
      noFill(); 
    }
    cylinder(6, this.leg2Length, this.detail);
    translate(0, this.leg2Length / 2, 0); // right heal
    let healRot = cos(this.walkRotSpeed) + 5.5
    let rotRheal = cos(this.walkRotSpeed) / 5 + 5.5;

    if (this.mainBird) { // rotate the foot. 
      if (!primePeckingBuffer) {
        rotateZ(4.6) // 5.12 5.3 , 4.7 // 4.98
        //rotateZ(4.7) // 5.12
      } else {
        rotateZ(4.7); //
      }

    } else {
      rotateZ(4.7) // 5.12
    }

    push();
    push(); 
    translate(0, 36, 0); // right foot 
    rotateX(QUARTER_PI)
    //box(2, 40, 40) // right foot size is 32 box(2, 64, 64)
    pop()
    translate(0, 18, 0); // right toe Center 15
    cylinder(3, 80);
    pop();
    push();
    rotateX(0.7);
    translate(0, 26, 0); // right toe Right  translate(0, 25, 0)
    cylinder(3, 58);
    pop();
    push();
    rotateX(-0.7);
    translate(0, 26, 0); // right toe Right
    cylinder(3, 58);
  }
  drawWing(_rz, _ry, _rx) {

    let PLow = []
    let PHigh = []

    let rot = 0;
    let faceNum = this.detail; // map(this.detail, 4, 20, 4, 12); //12; // # of sides of the neck 
    for (let i = 0; i < faceNum; i++) {
      //let r = TWO_PI / faceNum;
      let r = PI / faceNum;
      rot += r;
      // PLow are the points where the neck meets the body 
      // PHight are the points whre the neck meets the head
      // this.wingWidth = 40; 
      // this.wingLength = 100; 
      PLow[i] = createVector(cos(rot) * this.wingWidth, this.wingLength / 2, sin(rot) * this.wingWidth)
      //PHigh[i] = createVector(cos(rot) * this.wingWidthUp, -this.wingLength / 2, sin(rot) * this.wingWidthUp)

      PHigh[i] = createVector(cos(rot), -this.wingLength * .7, sin(rot))

    }
    fill(this.wingColor) // fill(200, 150,  170) 
    if (this.bw) {
      noFill();
    }
    let neckSec = map(this.detail, 0, 20, 1, 6);
    let test = map(mouseX, 0, width, 0, TWO_PI)
   
    rotateZ(_rz)  // 3.376
    rotateY(_ry) // 3.0
    rotateX(_rx)
    //for (let i = 0; i < PLow.length - 1; i++) { // draw most of the neck
    for (let i = 0; i < PLow.length - 1; i++) { // draw most of the neck
      beginShape();
      vertex(PLow[i].x, PLow[i].y, PLow[i].z);
      vertex(PLow[i + 1].x, PLow[i + 1].y, PLow[i + 1].z);
      vertex(PHigh[i + 1].x, PHigh[i + 1].y, PHigh[i + 1].z);
      vertex(PHigh[i].x, PHigh[i].y, PHigh[i].z);
      endShape(CLOSE);
    }

    beginShape();
    vertex(PLow[PLow.length - 1].x, PLow[PLow.length - 1].y, PLow[PLow.length - 1].z);
    vertex(PLow[0].x, PLow[0].y, PLow[0].z);
    vertex(PHigh[0].x, PHigh[0].y, PHigh[0].z);
    vertex(PHigh[PLow.length - 1].x, PHigh[PLow.length - 1].y, PHigh[PLow.length - 1].z);
    endShape(CLOSE);

    beginShape();// top end cap 
    for (let i = 0; i < PLow.length - 1; i++) {
      vertex(PLow[i].x, PLow[i].y, PLow[i].z);
    }
    vertex(PLow[PLow.length - 1].x, PLow[PLow.length - 1].y, PLow[PLow.length - 1].z);
    endShape(CLOSE);

    beginShape();// top end cap 
    for (let i = 0; i < PHigh.length - 1; i++) {
      vertex(PHigh[i].x, PHigh[i].y, PHigh[i].z);
    }
    vertex(PHigh[PHigh.length - 1].x, PHigh[PHigh.length - 1].y, PHigh[PHigh.length - 1].z);
    endShape(CLOSE);

  }
}