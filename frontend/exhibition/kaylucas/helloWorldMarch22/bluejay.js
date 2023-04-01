class bluejay {
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

    this.headColor = color(6, 105, 192); // 200, 150,  170); 
    this.crownColor = color(6, 105, 192);
    this.bodyColor = color(255, 255, 255); // 200, 150,  170); 
    this.wingColor = color(16, 105, 192); //0, 180, 220
    this.neckColor = color(0, 0, 0); //fill(200, 150,  170)
    this.feetColor = color(100, 100, 100); //fill(200, 150,  170) 162, 87, 127
    this.legColor = color(255, 255, 255); //26, 163, 109
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
    this.lockedOnSeed = false;
    this.moveZValue = 0;
    this.returnToCenter = false;
    this.stColor = color(1, 1, 1);
    this.bw = false;
    this.greyToggle = !greyScale;
    this.walkDir = false;
    this.onGroundY = this.rootLoc.y;
    this.flying = false;
    this.flyingNum = 0;
    this.flyingDir = true;
    this.flapNum = 0;
    this.flap = true;
    this.flyingTimer = millis(); 
    this.flyingInterval = 5000; 
  }
  display() {

    if (this.greyToggle != greyScale) {
      this.greyToggle = greyScale;
      if (greyScale) {
        this.headColor = color(190);
        this.crownColor = color(33);
        this.bodyColor = color(140);
        this.wingColor = color(113);
        this.neckColor = color(58);
        this.feetColor = color(124);
        this.legColor = color(231);
      }
      if (!greyScale) {
        this.headColor = color(6, 105, 192); // 200, 150,  170); 
        this.crownColor = color(6, 105, 192);
        this.bodyColor = color(255, 255, 255); // 200, 150,  170); 
        this.wingColor = color(16, 105, 192); //0, 180, 220
        this.neckColor = color(0, 0, 0); //fill(200, 150,  170)
        this.feetColor = color(100, 100, 100); //fill(200, 150,  170) 162, 87, 127
        this.legColor = color(255, 255, 255); //26, 163, 109
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
    let t = createVector(180, 0, this.rootLoc.z); // peck location
    // push()
    // translate(t.x, t.y, t.z); 
    // sphere(5)
    // pop() 
    if (this.mainBird && this.birdPecking == false && this.flying == false) {
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
      // let test = map(mouseX, 0, width, 0, TWO_PI)
      // print(test)
      if (this.bodyTilt > this.peckDRot) { // this.peckDRot) {
        this.peckSpeed *= -1;
        this.pecknum++;
        foodPecked++;
        if (this.pecknum >= this.peckNumMax) {
          if (this.foodNum >= 0) {
            if (foodList[this.foodNum].discard == false) {
              foodList[this.foodNum].remove = true; // if it's a normal seed, eat it. 
              birdSteps = 0;  // here 
              foodPecked = 0; // here
            } else {
              //this.birdPecking = false;  // if its a discard seed, leave it alone and ignore it 
              foodList[this.foodNum].ignore = true;
            }
            this.pecknum = 0;
            this.peckNumMax = 1;
            this.lockedOnSeed = false;
          }
        } else {
          // foodList[this.foodNum].loc.x = t.x +  random(-8, 8) // move food to Peck point. 
          // foodList[this.foodNum].loc.z = t.z +  random(-8, 8)
          // foodList[this.foodNum].YRot +=  random(-.5, .5)
          foodList[this.foodNum].loc.x += random(-8, 8) // move food to Peck point. 
          foodList[this.foodNum].loc.z += random(-8, 8)
          foodList[this.foodNum].YRot += random(-.5, .5)
        }
      }
      if (this.bodyTilt < this.bodyTiltHome) {
        this.peckSpeed *= -1;
        this.birdPecking = false;
        primeBirdPecking = false;
        birdWalkBool = true;
      }
    }
    this.detail = int(map(panelPower, 0, 50, 5, 20)) // technically the panel can put out 50 W, but we should change this because it's rarley that high
    if (this.mainBird) {
      this.walkRotSpeed += map(walkSpeed, 0, 6, 0, 0.1); //set the bird steps to match the walking speed was  .2
    }
    else {
      this.rootLoc.x -= walkSpeed; // make birds that are not walking move with the sidewalk 
    }
    this.walkRotSpeed = this.walkRotSpeed % TWO_PI;

    if (this.rootLoc.x < -5000) { // reset bystandard  birds. 
      this.rootLoc.x = int(random(5000, 7000));
      if (this.rootLoc.z > 0) {
        this.rootLoc.z = random(3000, 200)
      } else {
        this.rootLoc.z = random(-3000, -200)
      }
    }

    // this.flyingTimer = millis(); 
    // this.flyingInterval = 5000; 
    if(millis() - this.flyingTimer > this.flyingInterval){ // this.flyingInterval){
      if (!this.birdPecking) {
        globalFlying = true; 
      }
    }

    if (globalFlying) { // get the letter preesed for now 
      if (!this.birdPecking) {
        this.flying = true;
      }
    } else {
      this.flying = false;
    }
    if (this.flying && this.mainBird) {
      this.walkRotSpeed = 0; // stop it from walking 
      POVtoggle = false;
      this.birdPecking = false;
      if (this.flyingDir) {
        this.rootLoc.y -= 12;
      } else {
        this.rootLoc.y += 12;
      }
      if (this.rootLoc.y < -1000) {
        this.flyingDir = false;
      }
      if (this.rootLoc.y >= this.onGroundY) {
        this.rootLoc.y = this.onGroundY;
        this.flyingDir = true;
        globalFlying = false;
        POVtoggle = true;
        this.flyingTimer = millis(); 
        this.flyingInterval = int(random(10000, 30000)); 
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
    translate(-this.bodySize / 2.5, -this.bodySize / 4, 0); // center of body //-this.bodySize / 2.5, 0
    fill(this.bodyColor)
    if (this.bw) {
      noFill();
    }
    ellipsoid(this.bodySize * .6, this.bodySize * 1.1, this.bodySize * .7, this.detail, this.detail)  // draw body  //this.bodySize * .7, this.bodySize, this.bodySize * .9
    // sphere(this.bodySize, this.detail, this.detail);

    translate(-20, 0, 0);
    fill(this.wingColor);
    if (this.bw) {
      noFill();
    }
    ellipsoid(this.bodySize * .5, this.bodySize * 1.05, this.bodySize * .6, this.detail, this.detail)  // back of bird
    pop(); // back to root
    push();
    translate(-17, -18, this.bodySize - 44); // right hip
    this.drawLeg(0);
    pop()
    pop(); // back to root;;

    push();
    translate(-18, -18, - this.bodySize + 44); // LEFT hip
    this.drawLeg(PI);
    pop()

    pop(); // back to root
    push()

    rotateZ(this.bodyTilt + 5.7); // tilt of the whole body //5.6
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // bob neck on the X 
    rotateZ(sin((this.walkRotSpeed * 2) + HALF_PI) / this.neckBobNum);  // bob neck 

    this.neckLength = 75; //90
    this.neckwidth = 42; //55
    this.neckwidthUp = 25; //30
    // translate(-this.bodySize / 6, -this.bodySize - this.neckLength / 2, 0) // middle of neck 
    translate(-this.bodySize / 2 + 70, -this.bodySize - this.neckLength / 2, 0) // middle of neck 


    let rNeckY = map(this.detail, 0, 20, 2.42, 1.288);
    rotateY(rNeckY); // rotate so the neck color works 
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
    fill(this.neckColor) // fill(200, 150,  170)
    let neckSec = map(this.detail, 0, 20, 1, 6);
    for (let i = 0; i < PLow.length - 1; i++) { // draw most of the neck
      beginShape();
      if (i < neckSec) {
        fill(0, 0, 0) //255, 255, 255 // 26, 163, 109
      }
      else {
        fill(this.neckColor)// 
      }
      if (this.bw) {
        noFill();
      }
      vertex(PLow[i].x, PLow[i].y, PLow[i].z);
      vertex(PLow[i + 1].x, PLow[i + 1].y, PLow[i + 1].z);
      vertex(PHigh[i + 1].x, PHigh[i + 1].y, PHigh[i + 1].z);
      vertex(PHigh[i].x, PHigh[i].y, PHigh[i].z);
      endShape(CLOSE);
    }
    if (this.bw) {
      noFill();
    }
    beginShape(); // draw the final panel of the neck
    vertex(PLow[PLow.length - 1].x, PLow[PLow.length - 1].y, PLow[PLow.length - 1].z);
    vertex(PLow[0].x, PLow[0].y, PLow[0].z);
    vertex(PHigh[0].x, PHigh[0].y, PHigh[0].z);
    vertex(PHigh[PLow.length - 1].x, PHigh[PLow.length - 1].y, PHigh[PLow.length - 1].z);
    endShape(CLOSE);
    translate(0, -this.neckLength / 2 - this.headsize / 2, 0) // center of head
    rotateZ(sin((-this.walkRotSpeed * 2) - HALF_PI) / this.headBobNum);  // bob head 
    fill(this.headColor)
    if (this.bw) {
      noFill();
    }
    rotateY(-rNeckY); // rotate back so the neck color works 


    translate(12, 6, 0);
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    //rotateY(this.headRotY); 
    rotateZ(6.14);

    ellipsoid(this.headsize * 1.1, 42, 42, int(this.detail / 2) + 2, int(this.detail / 2) + 2) // test head
    translate(5, 15, 0); // cheecks
    fill(this.bodyColor);
    if (this.bw) {
      noFill();
    }

    ellipsoid(this.headsize * 1, 38, 38, int(this.detail / 2) + 2, int(this.detail / 2) + 2) // Cheeks 

    push()
    translate(60, 5, 0)  // beak //70,0,0
    fill(86, 86, 86) //255, 255, 0
    if (this.bw) {
      noFill();
    }
    rotateZ(-HALF_PI + .2) // rotate beak down
    cone(10, 60, this.detail, false);// beak size scale //12, 70
    fill(0, 0, 0); // red nose ellipsoid
    if (this.bw) {
      noFill();
    }
    rotateZ(HALF_PI - .2)
    translate(-32, -15, 0) // nose ellipsoid
    ellipsoid(22, 12, 20, this.detail, this.detail) // red nose ellipsoid
    pop()
    push()
    fill(255, 255, 255); // left eye torus fill
    stroke(255, 255, 255); // left eye torus fill
    if (this.bw) {
      noFill();
    }
    translate(10, -4, this.headsize - 7.5) // right eye 
    rotateY(.3)
    let torusDetail = int(map(this.detail, 0, 20, 1, 14)); //0, 20, 1, 14
    torus(8, 2, torusDetail, torusDetail); //(14, 2
    fill(1) // pupil
    stroke(1) // pupil
    if (this.bw) {
      noFill();
      stroke(255);
    }
    sphere(6, this.detail, this.detail)
    pop()

    push()

    fill(255, 255, 255) //right eye torus fill
    stroke(255, 255, 255) //right eye torus stroke
    if (this.bw) {
      noFill();
    }
    translate(10, -4, -this.headsize + 7.5) // left eye 
    rotateY(-.3)
    torus(8, 2, torusDetail, torusDetail);
    fill(1) // pupil
    stroke(1) // pupil
    if (this.bw) {
      noFill();
      stroke(255);
    }
    sphere(6, this.detail, this.detail)
    pop()
    push() // crown 
    translate(-40, -this.headsize / 2 - 22, 0)
    rotateZ(-4.3)
    //rotateZ(HALF_PI + 20) //HALF_PI + 20
    fill(this.crownColor)
    if (this.bw) {
      noFill();
    }
    cone(30, 80, this.detail);
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
    // this.wingWidth

    // translate(- this.wingWidth/2, -this.wingLength/2, this.bodySize * 0.6) // right wing
    // sphere(10)

    // translate(this.wingWidth/2, this.wingLengt/2, 0) // right wing

    translate(-80, -10, this.bodySize * 0.6) // left wing //100, -20, .6

    this.drawWing(3.51, 0.6, 6.05, true) // separate function for wings because there's two of them 
    pop()

    push() // right wing
    translate(-80, -10, -this.bodySize * 0.6) // left wing //100, -20, .6
    this.drawWing(3.51, 3.0, 6.05, false)
    pop()

    push()
    translate(-this.bodySize - (this.bodySize * .5) / 2, 170, 0) // tail feather
    //  let  test = map(mouseX, 0, width, 0, TWO_PI)
    //   print(test)
    rotateZ(0.45) //.615
    //rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    fill(this.headColor) //this.headColor 16, 105, 192
    if (this.bw) {
      noFill();
    }
    cone(this.bodySize * .2, 300, this.detail, false, false)
    pop()
    pop()

    if (this.mainBird && showShadow) {
      translate(0, -this.rootLoc.y - 1, 0) // shaddow
      rotateX(HALF_PI)
      noStroke()
      let bDis = abs(this.rootLoc.y - this.onGroundY);
      let sSize = 320 - bDis/2;
      let sAlpha = map(sSize, 0, 320, 0, 30)
      fill(10, sAlpha) // 30
      if (this.bw) {
        noFill();
      }
      let wiggle = sin(this.walkRotSpeed) * 5
      if (sSize > 0) {
        ellipse(0, wiggle, sSize, sSize / 1.53)  // center of body 
        translate(0, 0, 1)
        ellipse(sSize / 2 + wiggle, wiggle, sSize / 4, sSize / 4) // center of head 
        let tx = sSize / 1.48; // 215center of triangle 
        let tSize = sSize / 16;  // 20  first is point
        triangle(tx + tSize + wiggle, wiggle, tx - tSize + wiggle, -tSize / 2 + wiggle, tx - tSize + wiggle, tSize / 2 + wiggle)
        tx = sSize / 1.52 * -1 // -210;
        tSize = sSize / 5.3; //60;
        triangle(tx * 1.5 - tSize - wiggle, wiggle, tx + tSize + wiggle, -tSize / 2 + wiggle, tx + tSize + wiggle, tSize / 2 + wiggle)
      }
    }
    pop();
  }
  drawLeg(_rotOffset) {
    // let joeX = map(mouseX, 0, width, 0, 2); 

    if (this.mainBird) {
      //  print(_rotOffset); 
      if (this.walkRotSpeed > TWO_PI - .4 && this.walkDir == false && _rotOffset == 0) {
        this.walkDir = true;
        birdSteps++;
      }
      if (this.walkRotSpeed < PI + .4 && this.walkRotSpeed > PI + .1 && _rotOffset == 0) {
        if (this.walkDir == true) {
          this.walkDir = false;
          birdSteps++;
        }
      }

      if (!primePeckingBuffer) {
        rotateZ(sin(this.walkRotSpeed + _rotOffset) / 2 + .2); // how far the  hip turns  was 1.5// .5 // .8 
      } else {
        rotateZ(0.15); // was 1.06 was 0.5
      }
    } else {
      rotateZ(0.15); //
    }
    translate(0, this.leg1Length / 2, 0); // upper  leg
    fill(this.legColor);
    if (this.bw) {
      noFill();
    }
    cylinder(10, this.leg1Length, this.detail);
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
    if (this.bw) {
      noFill();
    }
    cylinder(4, this.leg2Length, this.detail);
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
    //translate(0, 16, 0); // right foot 
    //rotateX(QUARTER_PI)
    //box(2, 64, 64) // right foot size is 32
    //pop()
    translate(0, 15, 0); // right toe Center
    cylinder(3, 80);
    pop();
    push();
    rotateX(0.7);
    translate(0, 25, 0); // right toe Right
    cylinder(3, 55);
    pop();
    push();
    rotateX(-0.7);
    translate(0, 25, 0); // right toe Right
    cylinder(3, 55);
  }
  drawWing(_rz, _ry, _rx, leftSide) {
    push()
    translate(this.wingWidth / 2, -this.wingLength / 2, 0)
    if (this.flying && this.mainBird) {
      if (this.flap) {
        this.flapNum += .2
      } else {
        this.flapNum -= .2
      }
      if (this.flapNum > HALF_PI || this.flapNum < 0) {
        this.flap = !this.flap;
      }
    } else {
      this.flapNum = 0;
    }
    if (leftSide) {
      rotateX(this.flapNum) // right wing
    } else {
      rotateX(-this.flapNum) // left wing
    }
    translate(-this.wingWidth / 2, this.wingLength / 2, 0)

    let PLow = []
    let PHigh = []
    let rot = 0;
    let faceNum = this.detail; // map(this.detail, 4, 20, 4, 12); //12; // # of sides of the neck 
    for (let i = 0; i < faceNum; i++) {
      let r = PI / faceNum;
      rot += r;
      PLow[i] = createVector(cos(rot) * this.wingWidth, this.wingLength / 2, sin(rot) * this.wingWidth)
      PHigh[i] = createVector(cos(rot), -this.wingLength * .7, sin(rot))
    }
    fill(this.wingColor) // fill(200, 150,  170) // right wing color
    if (this.bw) {
      noFill();
    }
    let neckSec = map(this.detail, 0, 20, 1, 6);

    rotateZ(_rz)  // 
    rotateY(_ry) //
    rotateX(_rx) // good for flapping
    for (let i = 0; i < PLow.length - 1; i++) {
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
    pop()
  }
}