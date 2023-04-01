class robin {
  constructor(_w, _YRot, _x, _y, _z) {
    this.rootLoc = createVector(_x, _y, _z); //-114
    this.bodySize = 110;
    this.headsize = 44;
    this.leg1Length = 50;
    this.leg2Length = 60;
    this.walkRotSpeed = 0;
    this.bodyTilt = 0.77; // .5
    this.bodyTiltHome = 0.77;
    this.peckDRot = 2.2; // 1.71;
    this.peckSpeed = .1;
    this.peckDir = true;
    this.wingWidth = 50;
    this.wingLength = 180;
    this.wingWidthUp = 20;

    this.headColor = color(80); // 200, 150,  170); 
    this.bodyColor = color(250, 145, 25); // 200, 150,  170); 
    this.wingColor = color(80);
    this.neckColor = color(80) //fill(200, 150,  170)
    this.feetColor = color(80) //fill(200, 150,  170)  193, 173, 174
    this.legColor = color(220);
    this.beakColor = color(255, 255, 0)
    this.sideTiltAmount = 12;  // higher less tilt  12
    this.neckBobNum = 30; // 10 higher less tilt 
    this.headBobNum = 30; // higher less tilt 
    this.YRot = _YRot;
    this.mainBird = _w;
    this.detail = 20;

    this.headRotY = 0;
    this.birdPecking = false;
    this.pecknum = 0;
    this.peckNumMax = 1;
    this.foodNum = -1;
    this.lockedOnSeed = false;
    this.moveZValue = 0;
    this.returnToCenter = false;
    this.stColor = color(1, 1, 1);
    this.bw = false;
    this.gravity = 0.25;
    this.jumpNum = 0;
    this.jumpPower = 6;
    this.jumpPoint = this.rootLoc.y;
    this.bendDepth = 40;

    this.greyToggle = !greyScale;
    this.walkDir = false;

  }

  display() {
    // print(mouseY - 400)
    // print("test"); 
    // this.jumpPoint = mouseY - 400; 

    if (this.greyToggle != greyScale) {
      this.greyToggle = greyScale;

      if (greyScale) {
        this.headColor = color(95);
        this.bodyColor = color(234);
        this.wingColor = color(158);
        this.neckColor = color(115);
        this.feetColor = color(72);
        this.legColor = color(149);
        this.beakColor = color(92)
      }
      if (!greyScale) {
        this.headColor = color(80); // 200, 150,  170); 
        this.bodyColor = color(250, 145, 25); // 200, 150,  170); 
        this.wingColor = color(80);
        this.neckColor = color(80) //fill(200, 150,  170)
        this.feetColor = color(80) //fill(200, 150,  170)
        this.legColor = color(80);
        this.beakColor = color(255, 255, 0)
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
    let t = createVector(240, 0, this.rootLoc.z); // peck location
    // push()
    // translate(t.x, t.y, t.z); 
    // sphere(5)
    // pop() 
    if (this.mainBird && this.birdPecking == false) {
      for (let i = foodList.length - 1; i >= 0; i--) {
        let fd = foodList[i].loc;
        if (fd.dist(t) < 120 && foodList[i].ignore == false && fd.x < t.x) { // peck if it's within range. 
          this.birdPecking = true;
          primeBirdPecking = true; 
          birdWalkBool = false;
          this.foodNum = i;
          this.peckNumMax = foodList[i].peckNumFood
          let look = map(foodList[i].loc.z, 0, 50, .1, -.1)
          this.headRotY = look; //test 
        }
      }
      if (this.headRotY > .06) {
        this.headRotY -= .05
      } else if (this.headRotY < -.06) {
        this.headRotY += .05
      } else {
        this.headRotY = 0;
      }
      if (this.rootLoc.y >= this.jumpPoint + this.bendDepth) {
        this.jumpNum = -this.jumpPower;
        birdSteps ++; 
      } else {
        this.jumpNum += this.gravity;
      }
      this.rootLoc.y += this.jumpNum;
    }

    if (this.birdPecking && this.mainBird) { // if it's pecking 
      this.rootLoc.y = this.jumpPoint;
      this.bodyTilt += this.peckSpeed;
      this.moveZValue = 0;
     // primeBirdPecking = true;
      // let test = map(mouseX, 0, width, 0, TWO_PI)
      // print(test)
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
            //this.headRotY = 0;
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
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    translate(-this.bodySize / 2.5, -this.bodySize / 2.5, 0); // center of body
    fill(this.bodyColor)
    if (this.bw) {
      noFill();
    }
    ellipsoid(this.bodySize * .7, this.bodySize, this.bodySize * .8, this.detail, this.detail)  // draw body 
    // sphere(this.bodySize, this.detail, this.detail);
    // pop()
    // push();

    translate(-24, -1, 0); // back
    rotateZ(.15)
    fill(this.wingColor);  // back color
    if (this.bw) {
      noFill();
    }
    ellipsoid(this.bodySize * .55, this.bodySize - 2.75, this.bodySize * .7, this.detail, this.detail)  // back of bird
    pop(); // back to root
    push();
    translate(-18, -18, this.bodySize - 44); // right hip
    this.drawLeg(0);
    pop()
    pop(); // back to root

    push();
    translate(-18, -18, - this.bodySize + 44); // LEFT hip
    this.drawLeg(PI);
    pop()

    pop(); // back to root
    push()

    rotateZ(this.bodyTilt + 5.6); // tilt of the whole body
    rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // bob neck on the X 
    rotateZ(sin((this.walkRotSpeed * 2) + HALF_PI) / this.neckBobNum);  // bob neck 

    this.neckLength = 85;
    this.neckwidth = 55;
    this.neckwidthUp = 27;
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
        fill(255, 255, 255)
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
    rotateZ(6.05); // 6.14

    //sphere(this.headsize, int(this.detail / 1.6), int(this.detail / 1.6)) // test head
    ellipsoid(this.headsize * 1, 38, 38, this.detail, this.detail)
    push()
    translate(70, 7, 0)  // beak 
    fill(this.beakColor) // this.beakColor = color(255, 255, 0)
    if (this.bw) {
      noFill();
    }
    rotateZ(-HALF_PI + .025)
    cone(12, 70, this.detail, false);// beak size 
    pop()
    push()
    fill(255)
    stroke(255)
    if (this.bw) {
      noFill();
    }
    translate(15, -4, this.headsize - 7.5) // right eye 
    let torusDetail = int(map(this.detail, 0, 20, 1, 14));
    torus(7, 2, torusDetail, torusDetail);
    fill(1)
    stroke(1)
    if (this.bw) {
      noFill();
      stroke(255);
    }
    sphere(5, this.detail, this.detail)
    pop()

    push()

    fill(255)
    stroke(255)
    if (this.bw) {
      noFill();
    }
    translate(15, -4, -this.headsize + 7.5) // right eye 
    torus(7, 2, torusDetail, torusDetail);
    fill(1)
    stroke(1)
    if (this.bw) {
      noFill();
      stroke(255);
    }
    sphere(5, this.detail, this.detail)

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
    translate(-100, -20, this.bodySize * 0.7) // right wing
    //   rotateZ(3.51) 
    //   rotateY(0.6) 
    //   rotateX(6.05) 
    this.drawWing(3.51, 0.6, 6.05) // separate function for wings because there's two of them 
    pop()
    push() // right wing
    //translate(-80, -40, -this.bodySize)
    translate(-100, 0, -this.bodySize * 0.75) // left wing

    //this.drawWing(3.376, 3.0, 5.91)
    this.drawWing(3.51, 2.9, 6.05)
    pop()

    push()
    translate(-this.bodySize - (this.bodySize * .5) / 2, 90, 0) // tail 
    //  let  test = map(mouseX, 0, width, 0, TWO_PI)
    //   print(test)
    rotateZ(0.615)
    //rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
    fill(this.headColor)
    if (this.bw) {
      noFill();
    }
    cone(this.bodySize * .5, 325, this.detail, false, false)
    pop()
    pop()
    //his.rootLoc.y
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
      // let test = map(mouseX, 0, width, -500, 500)
      // print(test)
      // ellipse(test, 0, 5, 0); 
      ellipse(160 + wiggle, wiggle, 80, 80) // center of head 
      let tx = 215; // center of triangle 
      let tSize = 20;  // first is point
      triangle(tx + tSize + wiggle, wiggle, tx - tSize + wiggle, -tSize / 2 + wiggle, tx - tSize + wiggle, tSize / 2 + wiggle)
      tx = -210;
      tSize = 60;
      triangle(tx * 1.5 - tSize - wiggle, wiggle, tx + tSize + wiggle, -tSize / 2 + wiggle, tx + tSize + wiggle, tSize / 2 + wiggle)
    }
    pop();

  }
  drawLeg(_rotOffset) {
    // let joeX = map(mouseX, 0, width, 0, 2); 

     if (this.mainBird) {
    //   if (this.walkRotSpeed > TWO_PI - .2 && this.walkDir == false && _rotOffset == 0) {
    //     this.walkDir = true;
    //     birdSteps++;
    //   }
    //   if (this.walkRotSpeed < PI + .4 && this.walkRotSpeed > PI + .1 && _rotOffset == 0) {
    //     if (this.walkDir == true) {
    //       this.walkDir = false;
    //       birdSteps++;
    //     }
    //   }

      if (!primePeckingBuffer) {
        let legR = 0.15;
        let jdepth = this.rootLoc.y - this.jumpPoint;
        if (jdepth > 0 && jdepth < this.bendDepth) {
          legR = map(jdepth, 0, this.bendDepth, 0.15, 1.5) // 1.15
        }
        rotateZ(legR)
      } else {
        rotateZ(0.15); // was 1.06 was 0.5
      }
    } else {
      // print(random(2)); 
      rotateZ(0.15); //
    }
    translate(0, this.leg1Length / 2, 0); // upper  leg
    fill(this.legColor);
    if (this.bw) {
      noFill();
    }
    cylinder(12, this.leg1Length, this.detail);
    translate(0, this.leg1Length / 2, 0); //  knee
    if (this.mainBird) {
      if (!primePeckingBuffer) {
        //rotateZ(cos(this.walkRotSpeed + _rotOffset) / 2 + 4.8);
        let legR2 = -.2
        let jdepth = this.rootLoc.y - this.jumpPoint;
        if (jdepth > 0 && jdepth < this.bendDepth) {
          legR2 = map(jdepth, 0, this.bendDepth, -.2, -2.2)
          
        }
        rotateZ(legR2);
      } else {

        rotateZ(-.2)
        //rotateZ(-.2); // 5.23
      }
    } else {

      rotateZ(-.2); // 5.23
    }
    translate(0, this.leg2Length / 2, 0); // lower right leg
    fill(this.feetColor);
    if (this.bw) {
      noFill();
    }
    cylinder(3.5, this.leg2Length, this.detail);
    translate(0, this.leg2Length / 2, 0); // right heal

    if (this.mainBird) { // rotate the foot. 
      if (!primePeckingBuffer) {
        rotateZ(4.84) // 5.12
      } else {
        rotateZ(4.7); //
      }
    } else {
      rotateZ(4.7) // 5.12
    }

    push();

    translate(0, 15, 0); // right toe Center
    cylinder(3, 75);
    pop();
    push();
    rotateX(0.7);
    translate(0, 25, 0); // right toe Right
    cylinder(3, 43);
    pop();
    push();
    rotateX(-0.7);
    translate(0, 25, 0); // right toe Right
    cylinder(3, 43);
  }
  //   translate(0, this.leg2Length / 2, 0); // lower right leg
  //   fill(this.feetColor);
  //   if (this.bw) {
  //     noFill();
  //   }
  //   cylinder(6, this.leg2Length, this.detail);
  //   translate(0, this.leg2Length / 2, 0); // right heal
  //   let healRot = cos(this.walkRotSpeed) + 5.5
  //   let rotRheal = cos(this.walkRotSpeed) / 5 + 5.5;

  //   // let joetestR = map(mouseY, 0, height, 0, TWO_PI) // -93

  //   if (this.mainBird) { // rotate the foot. 
  //     if (!primeBirdPecking) {
  //       let legR2 = 4.7
  //       let jdepth = this.rootLoc.y - this.jumpPoint;
  //       if (jdepth > 0 && jdepth < this.bendDepth) {
  //         legR2 = map(jdepth, 0, this.bendDepth, 4.7, 5.4)
  //       }
  //       rotateZ(legR2);

  //       //rotateZ(4.7) // 5.12
  //     } else {
  //       rotateZ(4.7); //
  //     }

  //   } else {

  //     // this.rootLoc.y = joetestY;  
  //     rotateZ(4.7) // 5.12
  //   }

  //   push();
  //   translate(0, 16, 0); // right foot 
  //   rotateX(QUARTER_PI)
  //   box(2, 32, 32) // foot size is 32
  //   //pop()
  // }
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

      PHigh[i] = createVector(cos(rot), -this.wingLength * .6, sin(rot))

    }
    fill(this.neckColor) // fill(200, 150,  170)
    if (this.bw) {
      noFill();
    }
    let neckSec = map(this.detail, 0, 20, 1, 6);
    let test = map(mouseX, 0, width, 0, TWO_PI)
    // print(test)
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

    //   push()
    //   //translate(PLow[PLow.length/2].x, PLow[PLow.length/2].y, PLow[PLow.length/2].z)
    //   translate(PLow[int(PLow.length/2)].x, PLow[int(PLow.length/2)].y, PLow[int(PLow.length/2)].z)
    //   sphere(10)
    //   pop()
    //vertex(PLow[PLow.length/2].x, PLow[PLow.length/2].y, PLow[PLow.length/2].z)

    //   let w1 = createVector(60, -50, 5) // wing shape points
    //   let w2 = createVector(60, 50, 5)
    //   let w3 = createVector(-120, 20, 3)
    //   let w4 = createVector(-120, -20, 3)

    //   let w5 = createVector(w1.x, w1.y, -10) // wing is wider at the shoulder 
    //   let w6 = createVector(w2.x, w2.y, -10)
    //   let w7 = createVector(w3.x, w3.y, -3)
    //   let w8 = createVector(w4.x, w4.y, -3)
    //   fill(this.wingColor);
    //   if(this.bw){
    //     noFill(); 
    //   }
    //   rotateZ(5.3) // wing angle 
    //   beginShape(); // wing front 
    //   vertex(w1.x, w1.y, w1.z);
    //   vertex(w2.x, w2.y, w2.z);
    //   vertex(w3.x, w3.y, w3.z);
    //   vertex(w4.x, w4.y, w4.z);
    //   endShape(CLOSE);

    //   beginShape();  // wing back 
    //   vertex(w5.x, w5.y, w5.z);
    //   vertex(w6.x, w6.y, w6.z);
    //   vertex(w7.x, w7.y, w7.z);
    //   vertex(w8.x, w8.y, w8.z);
    //   endShape(CLOSE);

    //   beginShape(); // wing top 
    //   vertex(w1.x, w1.y, w1.z);
    //   vertex(w2.x, w2.y, w2.z);
    //   vertex(w6.x, w6.y, w6.z);
    //   vertex(w5.x, w5.y, w5.z);
    //   endShape(CLOSE);

    //   beginShape(); // wing bottom 
    //   vertex(w3.x, w3.y, w3.z);
    //   vertex(w4.x, w4.y, w4.z);
    //   vertex(w8.x, w8.y, w8.z);
    //   vertex(w7.x, w7.y, w7.z);
    //   endShape(CLOSE);

    //   beginShape(); // wing front 
    //   vertex(w1.x, w1.y, w1.z);
    //   vertex(w4.x, w4.y, w4.z);
    //   vertex(w8.x, w8.y, w8.z);
    //   vertex(w5.x, w5.y, w5.z);

    //   endShape(CLOSE);
    //   beginShape(); // wing front 
    //   vertex(w2.x, w2.y, w2.z);
    //   vertex(w3.x, w3.y, w3.z);
    //   vertex(w7.x, w7.y, w7.z);
    //   vertex(w6.x, w6.y, w6.z);
    //   endShape(CLOSE);
  }
}