class mgull {
  constructor(_w, _YRot, _x, _y, _z) {
    this.rootLoc = createVector(_x, _y, _z);
    this.bodySize = 110;
    this.headsize = 46;
    this.leg1Length = 70;
    this.leg2Length = 60;
    this.walkRotSpeed = 0;
    this.bodyTilt = 1.5;
    this.bodyTiltHome = 1.5;
    this.peckDRot = 2.2;
    this.peckSpeed = .1;
    this.peckDir = true;
    this.wingWidth = 50;
    this.wingLength = 200;
    this.wingWidthUp = 20;
    this.headColor = color(30, 30, 30);
    this.bodyColor = color(255);
    this.wingColor = color(150);
    this.neckColor = color(255);
    this.feetColor = color(231, 66, 30);
    this.legColor = color(255);
    this.tailColor = color(255);
    this.beakColor = color(231, 66, 30)
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
    this.walkDir = false
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
        this.headColor = color(17);
        this.bodyColor = color(221);
        this.wingColor = color(136);
        this.neckColor = color(221);
        this.feetColor = color(102);
        this.legColor = color(221);
        this.tailColor = color(221);
        this.beakColor = color(102);
      }
      if (!greyScale) {
        this.headColor = color(30, 30, 30);
        this.bodyColor = color(255); 
        this.wingColor = color(150);
        this.neckColor = color(255);
        this.feetColor = color(231, 66, 30);
        this.legColor = color(255);
        this.tailColor = color(255);
        this.beakColor = color(231, 66, 30)
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

    let t = createVector(256, 0, this.rootLoc.z); // peck location
    if (this.mainBird && this.birdPecking == false && this.flying == false) {
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
        foodPecked++; // here 
        if(this.foodNum > foodList.length){
          this.foodNum = 0; 
        }
        if (this.pecknum >= this.peckNumMax) {
          if (this.foodNum >= 0) {
            if (foodList[this.foodNum].discard == false) {
              birdSteps = 0;  // here 
              foodPecked = 0; // here
              foodList[this.foodNum].remove = true; // if it's a normal seed, eat it
            } else {
              // if its a discard seed, leave it alone and ignore it 
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
    this.detail = int(map(panelPower, 0, 50, 5, 20)) // technically the panel can put out 50 W, but we should change this because it's rarley that high
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

    rotateZ(this.bodyTilt); //rotTest
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // 
    translate(-this.bodySize / 5, -this.bodySize / 4, 0); // center of body
    fill(this.bodyColor)
    if (this.bw) {
      noFill();
    }
    ellipsoid(this.bodySize * .6, this.bodySize * 1.1, this.bodySize * .7, this.detail, this.detail)  // draw body

    translate(-17, 2, 0);
    fill(this.wingColor);
    if (this.bw) {
      noFill();
    }
    pop(); // back to root

    push();
    translate(30, -18, this.bodySize - 44); // right hip
    this.drawLeg(0);
    pop()
    pop(); // back to root

    push();
    translate(30, -18, - this.bodySize + 44); // LEFT hip
    if (!this.flying) {
      this.drawLeg(PI);
    } else {
      this.drawLeg(0);
    }
    pop();

    pop(); // back to root
    push()

    rotateZ(this.bodyTilt + 5); // tilt of the whole body
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // bob neck on the X 
    rotateZ(sin((this.walkRotSpeed * 2) + HALF_PI) / this.neckBobNum);  // bob neck 

    this.neckLength = 65;
    this.neckwidth = 32;
    this.neckwidthUp = 25;
    translate(-this.bodySize / 2 + 140, -this.bodySize - this.neckLength / 20, 0) // middle of neck 


    let rNeckY = map(this.detail, 0, 20, 2.42, 1.288);
    // rotate so the neck color works 
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
    let neckSec = map(this.detail, 0, 20, 1, 6);
    for (let i = 0; i < PLow.length - 1; i++) { // draw most of the neck
      beginShape();
      vertex(PLow[i].x, PLow[i].y, PLow[i].z);
      vertex(PLow[i + 1].x, PLow[i + 1].y, PLow[i + 1].z);
      vertex(PHigh[i + 1].x, PHigh[i + 1].y, PHigh[i + 1].z);
      vertex(PHigh[i].x, PHigh[i].y, PHigh[i].z);
      endShape(CLOSE);
    }
    beginShape(); // draw the final panel of the neck
    vertex(PLow[PLow.length - 1].x, PLow[PLow.length - 1].y, PLow[PLow.length - 1].z);
    vertex(PLow[0].x
      , PLow[0].y, PLow[0].z);
    vertex(PHigh[0].x, PHigh[0].y, PHigh[0].z);
    vertex(PHigh[PLow.length - 1].x, PHigh[PLow.length - 1].y, PHigh[PLow.length - 1].z);
    endShape(CLOSE);
    translate(0, -this.neckLength / 2 - this.headsize / 2, 0) // center of head
    rotateZ(sin((-this.walkRotSpeed * 2) - HALF_PI) / this.headBobNum);  // bob head 
    fill(this.headColor)
    if (this.bw) {
      noFill();
    }
    // rotate back so the neck color works 
    translate(12, 6, 0);
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    rotateZ(6.3);

    ellipsoid(this.headsize, this.headsize * .9, this.headsize * .9, this.detail, this.detail) // test head
    push()
    translate(70, 0, 0);
    fill(this.beakColor);
    if (this.bw) {
      noFill();
    }
    rotateZ(-HALF_PI) // rotate beak down
    cylinder(5, 70, this.detail, false); // beak size scale
    // nose ellipsoid
    if (this.bw) {
      noFill();
    }
    translate(-12, 0, 0); // beak lower
    fill(this.beakColor);
    if (this.bw) {
      noFill();
    }
    rotateZ(.025) // rotate beak down
    cylinder(5, 70, this.detail, false);// beak size scale
    if (this.bw) {
      noFill();
    }
    pop()
    push()
    fill(255, 255, 255)
    stroke(255, 255, 255) // torus 
    if (this.bw) {
      noFill();
    }
    translate(10, -4, this.headsize - 7) // right eye 
    let torusDetail = int(map(this.detail, 0, 20, 1, 14));
    torus(7, 2, torusDetail, torusDetail);
    fill(1);
    noStroke();
    if (this.bw) {
      noFill();
      stroke(255);
    }
    sphere(6, this.detail, this.detail)
    pop()

    push()

    fill(255, 255, 255) //fill torus
    stroke(255, 255, 255) //fill torus
    if (this.bw) {
      noFill();
    }
    translate(10, -4, -this.headsize + 7) // left eye 
    torus(7, 2, torusDetail, torusDetail);
    fill(1);
    noStroke();
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
    rotateZ(this.bodyTilt); // rotTest
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);

    push() // left wing
    translate(-55, 10, this.bodySize * 0.6) // right wing
    rotateZ(-.25) // right wing rotation tilt
    this.drawWing(3.51, 0.6, 6.05, true) // separate function for wings because there's two of them 
    pop();
    push(); // right wing
    translate(-55, 10, -this.bodySize * 0.6); // left wing
    rotateZ(-.15); // left wing rotation tilt
    this.drawWing(3.51, 3.0, 6.05, false);
    pop()

    push()
    translate(-this.bodySize - (this.bodySize * -.95) / 2, 160, 0); // tail feather 
    rotateZ(0.25);
    fill(this.tailColor)
    if (this.bw) {
      noFill();
    }
    cone(this.bodySize * .25, 200, this.detail, false, false);
    pop();
    pop();
    if (this.mainBird && showShadow) {
      translate(0, -this.rootLoc.y - 1, 0) // shadow
      rotateX(HALF_PI)
      noStroke()
      let bDis = abs(this.rootLoc.y - this.onGroundY);
      let sSize = 320 - bDis / 2;
      let sAlpha = map(sSize, 0, 320, 0, 30);
      fill(10, sAlpha);
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
      if (this.walkRotSpeed > TWO_PI - .2 && this.walkDir == false && _rotOffset == 0) {
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
    translate(0, this.leg1Length / 2.5, 0); // upper  leg
    fill(this.legColor);
    if (this.bw) {
      noFill();
    }
    cylinder(15, this.leg1Length, this.detail);
    translate(0, this.leg1Length / 2, 0); // knee
    if (this.mainBird) {
      if (!primePeckingBuffer) {
        if (this.flying) {
          let l2R = map(abs(this.rootLoc.y - this.onGroundY), 0, 60, 5.3, 4, true)
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
    cylinder(5, this.leg2Length, this.detail);
    translate(0, this.leg2Length / 2, 0); // right heal
    let healRot = cos(this.walkRotSpeed) + 5.5
    let rotRheal = cos(this.walkRotSpeed) / 5 + 5.5;

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
    push();
    translate(0, 36, 0); // right foot 
    rotateX(QUARTER_PI)
    box(2, 40, 40); // right foot size
    pop();
    translate(0, 22, 0); // right toe Center
    cylinder(3, 80);
    pop();
    push();
    rotateX(0.7);
    translate(0, 22, 0); // right toe Right
    cylinder(3, 50);
    pop();
    push();
    rotateX(-0.7);
    translate(0, 22, 0); // right toe Right
    cylinder(3, 50);
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
      // PLow are the points where the neck meets the body 
      // PHight are the points whre the neck meets the head
      PLow[i] = createVector(cos(rot) * this.wingWidth, this.wingLength / 2, sin(rot) * this.wingWidth);
      PHigh[i] = createVector(cos(rot), -this.wingLength * .7, sin(rot))

    }
    fill(this.wingColor);
    if (this.bw) {
      noFill();
    }
    let neckSec = map(this.detail, 0, 20, 1, 6);
    let test = map(mouseX, 0, width, 0, TWO_PI)
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