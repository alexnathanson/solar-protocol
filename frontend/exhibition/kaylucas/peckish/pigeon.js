class pigeon {
  constructor(_w, _YRot, _x, _y, _z) {
    this.rootLoc = createVector(_x, _y, _z);
    this.bodySize = 110;
    this.headsize = 38;
    this.leg1Length = 50;
    this.leg2Length = 50;
    this.walkRotSpeed = 0;
    this.bodyTilt = 1.1;
    this.bodyTiltHome = 1.1;
    this.peckDRot = 2.2;
    this.peckSpeed = .1;
    this.peckDir = true;
    this.wingWidth = 50;
    this.wingLength = 180;
    this.wingWidthUp = 20;
    this.whiteBird = false;
    if (random(5) < 1) {
      this.whiteBird = true;
    }

    this.headColor = color(112, 128, 144);
    this.bodyColor = color(197, 204, 210);
    this.wingColor = color(94, 106, 114);
    this.nc = int(random(5));
    this.neckColor = neckColorArray[this.nc];
    this.feetColor = color(242, 99, 107);
    this.legColor = color(197, 204, 210);
    this.chestColor = color(138, 110, 202);
    this.beakColor = color(56, 64, 72);
    this.eyeRimColor = color(255, 68, 62);
    this.tailColor = color(54, 69, 79);

    if (this.whiteBird) {
      this.headColor = color(220);
      this.bodyColor = color(220);
      this.wingColor = color(220);
      this.neckColor = color(220);
      this.feetColor = color(220, 20, 20);
      this.legColor = color(220);
      this.chestColor = color(220);
      this.beakColor = color(220, 20, 20);
      this.eyeRimColor = color(196, 123, 45);
      this.tailColor = color(220);
    }

    this.sideTiltAmount = 12;
    this.neckBobNum = 18;
    this.headBobNum = 18;
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
        this.headColor = color(119);
        this.bodyColor = color(187);
        this.wingColor = color(119);
        this.neckColor = color(102);
        this.feetColor = color(136);
        this.legColor = color(204);
        this.chestColor = color(153);
        this.beakColor = color(68);
        this.eyeRimColor = color(170);
        this.tailColor = color(68);
      }
      if (!greyScale) {
        this.headColor = color(112, 128, 144);
        this.bodyColor = color(197, 204, 210);
        this.wingColor = color(94, 106, 114);
        this.neckColor = neckColorArray[this.nc];
        this.feetColor = color(244, 123, 159);
        this.legColor = color(197, 204, 210);
        this.chestColor = color(138, 110, 202);
        this.beakColor = color(54, 69, 79);
        this.eyeRimColor = color(238, 52, 62);
        this.tailColor = color(54, 69, 79);
        if (this.whiteBird) {
          this.headColor = color(220);
          this.bodyColor = color(220);
          this.wingColor = color(220);
          this.neckColor = color(220);
          this.feetColor = color(220, 20, 20);
          this.legColor = color(220);
          this.chestColor = color(220);
          this.beakColor = color(220, 20, 20);
          this.eyeRimColor = color(196, 123, 45);
          this.tailColor = color(220);
        }
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
    let t = createVector(230, 0, this.rootLoc.z); // peck location

    if (this.mainBird && this.birdPecking == false  && this.flying == false) {
      
      for (let i = foodList.length - 1; i >= 0; i--) {
        let fd = foodList[i].loc;
        if (fd.dist(t) < 120 && foodList[i].ignore == false && fd.x < t.x) { // peck if it's within range
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
      if (this.bodyTilt > this.peckDRot) {
        this.peckSpeed *= -1;
        this.pecknum++;
        foodPecked++;
        if(this.foodNum > foodList.length){
          this.foodNum = 0; 
        }
        if (this.pecknum >= this.peckNumMax) {
          if (this.foodNum >= 0) {
            if (foodList[this.foodNum].discard == false) {
              foodList[this.foodNum].remove = true; // if it's a normal seed, eat it 
              birdSteps = 0;
              foodPecked = 0;
            } else {
              foodList[this.foodNum].ignore = true;
            }
            this.pecknum = 0;
            this.peckNumMax = 1;
            this.lockedOnSeed = false;
          }
        } else {
          foodList[this.foodNum].loc.x = t.x + random(-8, 8) // move food to Peck point
          foodList[this.foodNum].loc.z = t.z + random(-8, 8)
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
    this.detail = int(map(panelPower, 0, 50, 5, 20)); // technically the panel can put out 50 W, but we should change this because it's rarely that high
    if (this.mainBird) {
      this.walkRotSpeed += map(walkSpeed, 0, 6, 0, 0.1); //set the bird steps to match the walking speed
    }
    else {
      this.rootLoc.x -= walkSpeed; // make birds that are not walking move with the sidewalk 
    }
    this.walkRotSpeed = this.walkRotSpeed % TWO_PI;

    if (this.rootLoc.x < -5000) { // reset bystandard  birds 
      this.rootLoc.x = int(random(5000, 7000));
      if (this.rootLoc.z > 0) {
        this.rootLoc.z = random(3000, 200)
      } else {
        this.rootLoc.z = random(-3000, -200)
      }
    }
    if (globalFlying) { 
      if (!this.birdPecking) {
        this.flying = true;
      }
    } else {
      if (OVworld == false) {
        this.flying = false;
      }
    }
    if (this.flying && this.mainBird) {
      this.walkRotSpeed = 0; // stop it from walking 
      POVtoggle = false;
      this.birdPecking = false;
      if (this.flyingDir) {
        this.rootLoc.y -= walkSpeed;
      } else {
        this.rootLoc.y += walkSpeed;
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
        this.flyingInterval = int(random(flyingIntervalLow, flyingIntervalHigh)); // get these globally 
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

    rotateZ(this.bodyTilt);
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    translate(-this.bodySize / 2.5, -this.bodySize / 4, 0); // center of body
    fill(this.bodyColor)
    if (this.bw) {
      noFill();
    }
    ellipsoid(this.bodySize * .65, this.bodySize * 1.1, this.bodySize * .6, this.detail, this.detail)  // draw body
    push();

    translate(-8, -60, 0) // chest
    rotateY(3);
    fill(this.chestColor); // chest color
    if (this.bw) {
      noFill();
    }
    ellipsoid(this.bodySize * .545, this.bodySize * .58, this.bodySize * .5, this.detail, this.detail)  // draw chest
    pop();
    pop(); // back to root

    push();
    translate(15, -36, this.bodySize - 52); // right hip
    this.drawLeg(0);
    pop()
    pop(); // back to root

    push();
    translate(15, -36, - this.bodySize + 52); // LEFT hip
    if (!this.flying) {
      this.drawLeg(PI);
    } else {
      this.drawLeg(0);
    }
    pop();
    pop(); // back to root
    push();

    rotateZ(this.bodyTilt + 5.5); // tilt of the whole body
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // bob neck on the X 
    rotateZ(sin((this.walkRotSpeed * 2) + HALF_PI) / this.neckBobNum);  // bob neck 

    this.neckLength = 95;
    this.neckwidth = 47;
    this.neckwidthUp = 25;
    translate(-this.bodySize / 2 + 85, -this.bodySize - this.neckLength / 2 - 12, 0) // middle of neck 


    let rNeckY = map(this.detail, 0, 20, 2.42, 1.288);
    rotateY(rNeckY); // rotate so the neck color works 
    let PLow = []
    let PHigh = []
    let rot = 0;
    let faceNum = this.detail; // # of sides of the neck 
    for (let i = 0; i < faceNum; i++) {
      let r = TWO_PI / faceNum;
      rot += r;
      // PLow are the points where the neck meets the body 
      // PHight are the points whre the neck meets the head
      PLow[i] = createVector(cos(rot) * this.neckwidth, this.neckLength / 2, sin(rot) * this.neckwidth)
      PHigh[i] = createVector(cos(rot) * this.neckwidthUp, -this.neckLength / 2, sin(rot) * this.neckwidthUp)
    }
    fill(this.neckColor);
    if (this.bw) {
      noFill();
    }
    for (let i = 0; i < PLow.length - 1; i++) { // draw most of the neck
      beginShape();
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
    rotateZ(sin((-this.walkRotSpeed * 2) - HALF_PI) / this.headBobNum); // bob head 
    fill(this.headColor)
    if (this.bw) {
      noFill();
    }
    rotateY(-rNeckY); // rotate back so the neck color works 

    translate(5, 6, 0);
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    rotateZ(6.3);

    ellipsoid(this.headsize, 36, 36, int(this.detail / 2) + 2, int(this.detail / 2) + 2);
    push();
    translate(52, 5, 0)  // beak
    fill(this.beakColor) // beak color
    if (this.bw) {
      noFill();
    }
    rotateZ(-HALF_PI + .3) // rotate beak down
    cone(7, 37, this.detail, false);// beak size scale
    if (this.bw) {
      noFill();
    }
    push();
    translate(-8, -5, 0); // lower beak
    rotateZ(-HALF_PI + 1.225); // rotate lower beak down
    cone(7, 37, this.detail, false); // beak size scale
    pop();

    rotateZ(HALF_PI - 1); // white nose flesh
    translate(-6, -20, 0);
    fill(255);
    if (this.bw) {
      noFill();
    }
    ellipsoid(7, 7, 12, int(this.detail / 2) + 2, int(this.detail / 2) + 2);
    pop();
    push();
    fill(this.eyeRimColor); // pupil
    stroke(this.eyeRimColor);
    if (this.bw) {
      noFill();
      stroke(255);
    }
    translate(10, -4, this.headsize - 5) // right eye
    rotateY(.2);
    let torusDetail = int(map(this.detail, 0, 20, 1, 14));
    torus(5, 2, torusDetail, torusDetail); // right outer torus

    fill(1); // pupil
    noStroke();
    if (this.bw) {
      noFill();
      stroke(255);
    }
    sphere(3, this.detail, this.detail)
    pop()

    push()
    fill(this.eyeRimColor) // left eye fill outer torus
    stroke(this.eyeRimColor) // fill outer torus
    if (this.bw) {
      noFill();
      stroke(255);
    }
    translate(10, -4, -this.headsize + 5) // left eye 
    rotateY(-.2);
    torus(5, 2, torusDetail, torusDetail);

    fill(1);
    noStroke();
    if (this.bw) {
      noFill();
      stroke(255);
    }
    sphere(3, this.detail, this.detail);

    pop();
    pop();
    push(); // back to root
    fill(255)
    if (this.bw) {
      noFill();
    }
    rotateZ(this.bodyTilt);
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);

    push() // left wing
    translate(-80, 18, this.bodySize * 0.6) // right wing
    this.drawWing(3.51, 0.6, 6.05, true) // separate function for wings because there's two of them 
    pop();

    push(); // right wing
    translate(-80, 18, -this.bodySize * 0.6) // left wing
    this.drawWing(3.51, 3.0, 6.05, false)
    pop()

    push()
    translate(-this.bodySize - (this.bodySize * .01) / 2, 130, 0) // tail 

    rotateZ(0.45);
    fill(this.tailColor); // change tail color
    if (this.bw) {
      noFill();
    }
    cone(this.bodySize * .3, 175, this.detail, false, false); // tail
    pop();
    pop();

    if (this.mainBird && showShadow) {
      translate(0, -this.rootLoc.y - 1, 0) // shadow
      rotateX(HALF_PI)
      noStroke()
      let bDis = abs(this.rootLoc.y - this.onGroundY);
      let sSize = 320 - bDis / 2;
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
        let tx = sSize / 1.48; // center of triangle 
        let tSize = sSize / 16;  // first is point
        triangle(tx + tSize + wiggle, wiggle, tx - tSize + wiggle, -tSize / 2 + wiggle, tx - tSize + wiggle, tSize / 2 + wiggle);
        tx = sSize / 1.52 * -1;
        tSize = sSize / 5.3;
        triangle(tx * 1.5 - tSize - wiggle, wiggle, tx + tSize + wiggle, -tSize / 2 + wiggle, tx + tSize + wiggle, tSize / 2 + wiggle);
      }
    }
    pop();

  }
  drawLeg(_rotOffset) {
    if (this.mainBird) {
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
        if (this.flying) {
          let l1R = map(abs(this.rootLoc.y - this.onGroundY), 0, 60, .4, 1.4, true)
          rotateZ(l1R); // 1.4
        } else {
          rotateZ(sin(this.walkRotSpeed + _rotOffset) / 2 + .2); // how far the  hip turns
        }
      } else {
        rotateZ(0.15);
      }
    } else {
      rotateZ(0.15);
    }
    translate(0, this.leg1Length / 2, 0); // upper  leg
    fill(this.legColor);
    if (this.bw) {
      noFill();
    }
    cylinder(10, this.leg1Length, this.detail);
    translate(0, this.leg1Length / 2, 0); // knee
    if (this.mainBird) {
      if (!primePeckingBuffer) {
        if (this.flying) {
          let l2R = map(abs(this.rootLoc.y - this.onGroundY), 0, 60, 5.3, 4, true);
          rotateZ(l2R); // 4.0
        } else {
          rotateZ(cos(this.walkRotSpeed + _rotOffset) / 2 + 5.8);
        }
      } else {
        rotateZ(-.2);
      }
    } else {
      rotateZ(-.2);
    }
    translate(0, this.leg2Length / 2, 0); // lower right leg
    fill(this.feetColor);
    if (this.bw) {
      noFill();
    }
    cylinder(4, this.leg2Length, this.detail);
    translate(0, this.leg2Length / 2, 0); // right heal
    if (this.mainBird) { // rotate the foot 
      if (!primePeckingBuffer) {
        if (this.flying) {
          rotateZ(5.9);
        } else {
          rotateZ(4.6);
        }
      } else {
        rotateZ(4.7);
      }
    } else {
      rotateZ(4.7);
    }

    push();
    translate(0, 15, 0); // right toe Center
    cylinder(3, 70);
    pop();
    push();
    rotateX(0.7);
    translate(0, 25, 0); // right toe Right
    cylinder(3, 45);
    pop();
    push();
    rotateX(-0.7);
    translate(0, 25, 0); // right toe Right
    cylinder(3, 45);
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
    let faceNum = this.detail; // # of sides of the neck 
    for (let i = 0; i < faceNum; i++) {
      let r = PI / faceNum;
      rot += r;
      PLow[i] = createVector(cos(rot) * this.wingWidth, this.wingLength / 2, sin(rot) * this.wingWidth)
      PHigh[i] = createVector(cos(rot), -this.wingLength * .5, sin(rot)) // WING LENGTH
    }
    fill(this.wingColor);
    if (this.bw) {
      noFill();
    }
    rotateZ(_rz);
    rotateY(_ry);
    rotateX(_rx);
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
    beginShape(); // top end cap 
    for (let i = 0; i < PLow.length - 1; i++) {
      vertex(PLow[i].x, PLow[i].y, PLow[i].z);
    }
    vertex(PLow[PLow.length - 1].x, PLow[PLow.length - 1].y, PLow[PLow.length - 1].z);
    endShape(CLOSE);
    beginShape(); // top end cap 
    for (let i = 0; i < PHigh.length - 1; i++) {
      vertex(PHigh[i].x, PHigh[i].y, PHigh[i].z);
    }
    vertex(PHigh[PHigh.length - 1].x, PHigh[PHigh.length - 1].y, PHigh[PHigh.length - 1].z);
    endShape(CLOSE); 
    pop(); 
  }
}