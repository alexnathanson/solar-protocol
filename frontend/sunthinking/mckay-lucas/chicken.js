class chicken {
    constructor(_w, _YRot, _x, _y, _z) {
        this.rootLoc = createVector(_x, _y, _z);
        this.bodySize = 110;
        this.headsize = 40; 
        this.neckLength = 80;
        this.neckwidth = 48;
        this.neckwidthUp = 25;
        this.leg1Length = 70;
        this.leg2Length = 50;
        this.walkRotSpeed = 0;
        this.bodyTilt = 1.2;
        this.bodyTiltHome = 1.2;
        this.peckDRot = 2.4;
        this.peckSpeed = .1;
        this.peckDir = true;
        this.wingWidth = 50;
        this.wingLength = 170;
        this.wingWidthUp = 20;
        this.eyeColor = color(1);
        this.torusColor = color(255);
        this.headColor = color(200, 65, 0);
        this.crownColor = color(255, 0, 0);
        this.bodyColorNum = int(random(4));
        this.bodyColor = color(200, 65, 0);
        this.wingColor = color(200, 65, 0);
        this.neckColor = color(200, 65, 0);
        this.feetColor = color(178, 154, 154);
        this.tailColor = color(0, 48, 73);
        this.beakColor = color(194, 185, 168);
        this.tailColor2 = color(255);
        this.sideTiltAmount = 12;
        this.neckBobNum = 10;
        this.headBobNum = 10;
        this.headRotY = 0;
        this.YRot = _YRot;
        this.mainBird = _w;
        this.detail = 20;
        this.birdPecking = false;
        this.pecknum = 0;
        this.peckNumMax = 1;
        this.foodNum = -1;
        this.greyToggle = !greyScale;
        this.walkDir = false;
    }

    display() {
        if (this.greyToggle != greyScale) {
            this.greyToggle = greyScale;
            if (greyScale) {
                this.headColor = color(52);
                this.crownColor = color(181);
                this.bodyColor = color(30);
                this.wingColor = color(31);
                this.neckColor = color(170);
                this.feetColor = color(75);
                this.tailColor = color(86);
                this.beakColor = color(220);
            }
            if (!greyScale) {
                this.eyeColor = color(1);
                this.torusColor = color(255);
                this.headColor = color(200, 65, 0);
                this.crownColor = color(255, 0, 0);
                this.bodyColorNum = int(random(4));
                this.bodyColor = color(200, 65, 0);
                this.wingColor = color(200, 65, 0);
                this.neckColor = color(200, 65, 0);
                this.feetColor = color(178, 154, 154);
                this.tailColor = color(0, 48, 73);
                this.beakColor = color(194, 185, 168);
                this.tailColor2 = color(255);
            }
        }

        let t = createVector(240, 0, 0); // peck location
        if (this.mainBird && this.birdPecking == false) {
            for (let i = foodList.length - 1; i >= 0; i--) {
                let fd = foodList[i].loc;
                if (fd.dist(t) < 120 && foodList[i].ignore == false && fd.x < t.x) { // peck if it's within range
                    this.birdPecking = true;
                    globalPecking = true;
                    birdWalkBool = false;
                    this.foodNum = i;
                    this.peckNumMax = foodList[i].peckNumFood
                    let look = map(foodList[i].loc.z, 0, 50, .14, -.14)
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
        if (this.birdPecking && this.mainBird) {
            this.bodyTilt += this.peckSpeed;
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
                            foodList[this.foodNum].remove = true; // if it's a normal seed, eat it
                            birdSteps = 0;
                            foodPecked = 0;
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
                globalPecking = false;
                birdWalkBool = true;
            }
        }
        if (camView) {
            this.detail = int(map(panelPower, 0, 50, 5, 20)) // technically the panel can put out 50 W, but we should change this
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

            if (panelPower < bwNum) {
                this.bw = true;
            }
            else {
                this.bw = false;
            }

            stroke(1);
            if (!showLines) {
                noStroke();
            }
            if (this.bw) {
                stroke(255);
            }

            push();
            translate(this.rootLoc.x, this.rootLoc.y, this.rootLoc.z); // root: the pivot point of bird
            rotateY(this.YRot + this.headRotY);
            push();
            rotateZ(this.bodyTilt); // rotTest
            rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);

            translate(-this.bodySize / 2.5, -this.bodySize / 4, 0); // center of body
            fill(this.bodyColor)
            if (this.bw) {
                noFill();
            }
            ellipsoid(this.bodySize * .6, this.bodySize * 1, this.bodySize * .6, this.detail, this.detail); // draw body 
            translate(-26.5, 0, 0); // back
            rotateZ(.0125);
            fill(this.headColor);  // back color
            if (this.bw) {
                noFill();
            }
            ellipsoid(this.bodySize * .45, this.bodySize * .9, this.bodySize * .55, this.detail, this.detail)  // back of bird
            
            pop(); // back to root
            push();
            translate(-17, -18, this.bodySize - 52); // right hip
            this.drawLeg(0);
            pop()
            pop(); // back to root

            push();
            translate(-18, -18, - this.bodySize + 52); // LEFT hip
            this.drawLeg(PI);
            pop()

            pop(); // back to root
            push()
            rotateZ(this.bodyTilt + 5.4); // tilt of the whole body
            rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // bob neck on the X 
            rotateZ(sin((this.walkRotSpeed * 2) + HALF_PI) / this.neckBobNum);  // bob neck 
            translate(-this.bodySize / 2 + 82, -this.bodySize - this.neckLength / 2, 0);

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
            fill(0);
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
            sphere(this.headsize - 1, this.detail, this.detail) // head
            push()
            translate(50, 0, 0)  // beak 
            fill(this.beakColor)
            if (this.bw) {
                noFill();
            }
            rotateZ(-HALF_PI)
            cone(15, 45, this.detail, false); // beak size 
            pop()
            push()

            fill(86, 86, 86)
            stroke(120, 120, 120) // torus 
            if (this.bw) {
                noFill();
                stroke(255);
            }
            translate(17, -10, this.headsize - 5.5) // right eye 
            rotateY(.3)
            let torusDetail = int(map(this.detail, 0, 20, 1, 14));
            torus(6, 2, torusDetail, torusDetail);
            fill(1);
            noStroke();
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
            translate(15, -10, -this.headsize + 5.5) // right eye 
            rotateY(-.3)
            torus(6, 2, torusDetail, torusDetail);
            fill(1);
            noStroke();
            if (this.bw) {
                noFill();
                stroke(255);
            }
            sphere(6, this.detail)
            pop()
            push() // crown 
            translate(-8, -this.headsize / 2 + 10, 0)
            rotateX(HALF_PI)
            fill(this.crownColor)
            if (this.bw) {
                noFill();
            }
            cylinder(42, 6, this.detail);
            pop()

            push() // gobbler
            translate(15, this.headsize / 2 + 12, 0)
            rotateX(HALF_PI)
            fill(this.crownColor)
            if (this.bw) {
                noFill();
            }
            cylinder(30, 6, this.detail)
            pop()

            pop()
            push() // back to root
            fill(255)
            if (this.bw) {
                noFill();
            }
            rotateZ(this.bodyTilt); // rotTest
            rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
            push(); // left wing
            translate(-60, 5, this.bodySize * .55); // left wing
            if (this.birdPecking) {
                rotateX(1.2);
            }
            translate(-30, 5, 0) // left wing
            this.drawWing(3.51, .3, 6.05)
            pop();
            push(); // right wing

            translate(-60, 30, -this.bodySize * .55);
            if (this.birdPecking) {
                rotateX(-1.2);
            }
            translate(-30, 30, 0);


            this.drawWing(3.51, 3.3, 6.05);
            pop();

            push();
            translate(-this.bodySize + 120, this.bodySize / 2 - 20, 0); // tail 
            this.tailRot = map(mouseX, 0, width, 0, TWO_PI);
            rotateZ(.75);
            fill(this.tailColor)
            if (this.bw) {
                noFill();
            }
            translate(-60, 120, 0) // middle of tail 
            cone(this.bodySize * .53, 200, this.detail, false, false)
            pop();
            pop();

            if (this.mainBird && showShadow) {
                translate(0, -this.rootLoc.y - 1, 0) // shadow
                rotateX(HALF_PI)
                noStroke()
                fill(10, 30)
                if (this.bw) {
                    noFill();
                }
                let wiggle = sin(this.walkRotSpeed) * 5
                ellipse(0, wiggle, 320, 210); // center of body 
                translate(0, 0, 1);
                ellipse(160 + wiggle, wiggle, 80, 80) // center of head 
                let tx = 215; // center of triangle 
                let tSize = 20; // first is point
                triangle(tx + tSize + wiggle, wiggle, tx - tSize + wiggle, -tSize / 2 + wiggle, tx - tSize + wiggle, tSize / 2 + wiggle)
                tx = -210;
                tSize = 60;
                triangle(tx * 1.5 - tSize - wiggle, wiggle, tx + tSize + wiggle, -tSize / 2 + wiggle, tx + tSize + wiggle, tSize / 2 + wiggle)
            }
            pop();

        }
    }
    drawLeg(_rotOffset) {
        if (this.mainBird) {
            if (this.walkRotSpeed > TWO_PI - .4 && this.walkDir == false && _rotOffset == 0) {
                this.walkDir = true; 
                birdSteps ++; 
            } 
            if (this.walkRotSpeed < PI + .42 && this.walkRotSpeed > PI + .1 && _rotOffset == 0) {
              if (this.walkDir == true) {
                this.walkDir = false;
                birdSteps ++;
              }
            }
            
            if (!primePeckingBuffer) {
                rotateZ(sin(this.walkRotSpeed + _rotOffset) / 2 + 0.2); // how far the right hip turns  
            } else {
                rotateZ(0.15);
            }
        } else {
            rotateZ(0.15);
        }
        translate(10, this.leg1Length / 2 - 20, 0); // upper right leg
        fill(this.bodyColor);
        if (this.bw) {
            noFill();
        }
        cylinder(12, this.leg1Length, this.detail);
        translate(0, this.leg1Length / 2, 0); // right knee
        if (this.mainBird) {
            if (!primePeckingBuffer) {
                rotateZ(cos(this.walkRotSpeed + _rotOffset) / 2 + 5.8);
            } else {
                rotateZ(-.2); // 5.3
            }
        } else {
            rotateZ(-.2); // 5.3
        }
        translate(0, this.leg2Length / 2, 0); // lower right leg
        fill(this.feetColor);
        if (this.bw) {
            noFill();
        }
        cylinder(4, this.leg2Length, this.detail);
        translate(0, this.leg2Length / 2, 0); // right heal
        let healRot = cos(this.walkRotSpeed) + 5.5;

        if (this.mainBird) { // rotate the foot. 
            if (!primePeckingBuffer) {
                rotateZ(4.6);
            } else {
                rotateZ(4.7);
            }

        } else {
            rotateZ(4.7);
        }

        push();
        push();
        translate(0, 36, 0); // right foot 
        rotateX(QUARTER_PI);
        pop();
        translate(0, 18, 0); // right toe Center
        cylinder(3, 70);
        pop();
        push();
        rotateX(0.7);
        translate(0, 26, 0); // right toe Right
        cylinder(3, 48);
        pop();
        push();
        rotateX(-0.7);
        translate(0, 26, 0); // right toe Right
        cylinder(3, 48);
    }
    drawWing(_rz, _ry, _rx) {

        let PLow = []
        let PHigh = []

        let rot = 0;
        let faceNum = int(this.detail / 2); // # of sides of the neck 
        for (let i = 0; i < faceNum; i++) {
            let r = PI / faceNum;
            rot += r;
            PLow[i] = createVector(cos(rot) * this.wingWidth, this.wingLength / 2, sin(rot) * this.wingWidth)
            PHigh[i] = createVector(cos(rot), -this.wingLength * .7, sin(rot))
        }
        fill(this.wingColor);
        if (this.bw) {
            noFill();
        }
        let neckSec = map(this.detail, 0, 20, 1, 6);
        let test = map(mouseX, 0, width, 0, TWO_PI)
        // print(test)
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
    }
}