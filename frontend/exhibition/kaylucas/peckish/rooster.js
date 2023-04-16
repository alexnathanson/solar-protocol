class rooster {
    constructor(_w, _YRot, _x, _y, _z) {
        this.rootLoc = createVector(_x, _y, _z);
        this.bodySize = 110;
        this.headsize = 40; 
        this.neckLength = 105;
        this.neckwidth = 55;
        this.neckwidthUp = 25;
        this.leg1Length = 80;
        this.leg2Length = 70;
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
        this.bodyColor = roosterBodyArray[this.bodyColorNum];
        this.wingColorNum = int(random(4));
        this.wingColor = roosterWingArray[this.wingColorNum];
        this.neckColorNum = int(random(4));
        this.neckColor = roosterNeckArray[this.neckColorNum];
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
                this.headColor = color(136);
                this.crownColor = color(68);
                this.bodyColor = color(68);
                this.wingColor = color(136);
                this.neckColor = color(102);
                this.feetColor = color(153);
                this.tailColor = color(51);
                this.beakColor = color(153);
            }
            if (!greyScale) {
                this.headColor = color(200, 65, 0);
                this.crownColor = color(255, 0, 0);
                this.bodyColor = roosterBodyArray[this.bodyColorNum];
                this.wingColor = roosterWingArray[this.wingColorNum];
                this.neckColor = roosterNeckArray[this.neckColorNum];
                this.feetColor = color(162, 87, 127);
                this.tailColor = color(0, 48, 73);
                this.beakColor = color(200, 100, 0);
            }
        }

        let t = createVector(240, 0, 0); // peck location
        if (this.mainBird && this.birdPecking == false && this.flying == false) {
            for (let i = foodList.length - 1; i >= 0; i--) {
                let fd = foodList[i].loc;
                if (fd.dist(t) < 120 && foodList[i].ignore == false && fd.x < t.x) { // peck if it's within range 
                    this.birdPecking = true;
                    primeBirdPecking = true;
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
                            // if its a discard seed, leave it alone and ignore it 
                            foodList[this.foodNum].ignore = true;
                        }
                    }
                } else {
                    foodList[this.foodNum].loc.x += random(-8, 8)
                    foodList[this.foodNum].loc.z += random(-8, 8)
                    foodList[this.foodNum].YRot += random(-.5, .5)
                }
            }
            if (this.bodyTilt < this.bodyTiltHome) {
                this.peckSpeed *= -1;
                this.birdPecking = false;
                primeBirdPecking = false;
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
                    this.rootLoc.z = random(3000, 200);
                } else {
                    this.rootLoc.z = random(-3000, -200);
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
            ellipsoid(this.bodySize * .7, this.bodySize * 1.1, this.bodySize * .7, this.detail, this.detail); // draw body 

            translate(-26.5, 0, 0); // back
            rotateZ(.0125);
            fill(this.headColor);  // back color
            if (this.bw) {
                noFill();
            }
            ellipsoid(this.bodySize * .55, this.bodySize * 1, this.bodySize * .65, this.detail, this.detail)  // back of bird
            pop(); // back to root

            push();
            translate(-17, -18, this.bodySize - 44); // right hip
            this.drawLeg(0);
            pop()
            pop(); // back to root

            push();
            translate(-18, -18, - this.bodySize + 44); // LEFT hip
            if (!this.flying) {
                this.drawLeg(PI);
            } else {
                this.drawLeg(0);
            }
            pop()

            pop(); // back to root
            push()
            rotateZ(this.bodyTilt + 5.4); // tilt of the whole body
            rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // bob neck on the X 
            rotateZ(sin((this.walkRotSpeed * 2) + HALF_PI) / this.neckBobNum);  // bob neck 
            translate(-this.bodySize / 2 + 85, -this.bodySize - this.neckLength / 2, 0);

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
            beginShape(); // draw the final panel of the neck
            vertex(PLow[PLow.length - 1].x, PLow[PLow.length - 1].y, PLow[PLow.length - 1].z);
            vertex(PLow[0].x, PLow[0].y, PLow[0].z);
            vertex(PHigh[0].x, PHigh[0].y, PHigh[0].z);
            vertex(PHigh[PLow.length - 1].x, PHigh[PLow.length - 1].y, PHigh[PLow.length - 1].z);
            endShape(CLOSE);
            translate(0, -this.neckLength / 2 - this.headsize / 2, 0) // center of head
            rotateZ(sin((-this.walkRotSpeed * 2) - HALF_PI) / this.headBobNum);  // bob head 

            fill(this.headColor);
            if (this.bw) {
                noFill();
            }
            sphere(this.headsize, this.detail, this.detail) // head
            push()
            translate(60, 0, 0)  // beak 
            fill(this.beakColor)
            if (this.bw) {
                noFill();
            }
            rotateZ(-HALF_PI)
            cone(20, 60, this.detail, false);// beak size 
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
            fill(1); // pupil
            noStroke();
            if (this.bw) {
                noFill();
                stroke(255);
            }
            sphere(6, this.detail, this.detail)
            pop()

            push()
            fill(120, 120, 120) // fill torus
            stroke(120, 120, 120) // fill torus
            if (this.bw) {
                noFill();
                stroke(255);
            }
            translate(15, -10, -this.headsize + 5.5) // right eye 
            rotateY(-.3)
            torus(6, 2, torusDetail, torusDetail);
            fill(1); // pupil
            noStroke();
            if (this.bw) {
                noFill();
                stroke(255);
            }
            sphere(6, this.detail)
            pop()
            push() // crown 
            translate(-15, -this.headsize / 2, 0)
            rotateX(HALF_PI)
            fill(this.crownColor)
            if (this.bw) {
                noFill();
            }
            cylinder(48, 6, this.detail);
            pop()

            push() // gobbler
            translate(25, this.headsize / 2 + 12, 0)
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
            rotateZ(this.bodyTilt);
            rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
            push(); // left wing

            translate(-60, 5, this.bodySize * .7); // left wing
            if (this.birdPecking) {
                rotateX(1.2);
            }
            translate(-30, 5, 0); // left wing
            this.drawWing(3.51, .3, 6.05, true)
            pop();
            push(); // right wing

            translate(-60, 30, -this.bodySize * .7);
            if (this.birdPecking) {
                rotateX(-1.2);
            }
            translate(-30, 30, 0);

            this.drawWing(3.51, 3.3, 6.05, false);
            pop();

            push();
            translate(-this.bodySize, this.bodySize / 2, 0) // tail 
            rotateZ(2.25);
            fill(this.tailColor)
            if (this.bw) {
                noFill();
            }
            translate(0, 0, 0) // middle of tail 

            rotateX(HALF_PI)
            cylinder(this.bodySize * .9, 5, this.detail) // tail
            translate(-30, 5, 0) // middle of tail 
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
            rotateZ(0.15); //
        }
        translate(10, this.leg1Length / 2 - 20, 0); // upper right leg
        fill(this.bodyColor);
        if (this.bw) {
            noFill();
        }
        cylinder(15, this.leg1Length, this.detail);
        translate(0, this.leg1Length / 2, 0); // right knee
        if (this.mainBird) {
            if (!primePeckingBuffer) {
                if (this.flying) {
                    let l2R = map(abs(this.rootLoc.y - this.onGroundY), 0, 60, 5.3, 4, true)
                    rotateZ(l2R);
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
        cylinder(6, this.leg2Length, this.detail);
        translate(0, this.leg2Length / 2, 0); // right heel
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
        rotateX(QUARTER_PI);
        pop()
        translate(0, 18, 0); // right toe Center
        cylinder(3, 80);
        pop();
        push();
        rotateX(0.7);
        translate(0, 26, 0); // right toe Right
        cylinder(3, 58);
        pop();
        push();
        rotateX(-0.7);
        translate(0, 26, 0); // right toe Right
        cylinder(3, 58);
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
        let test = map(mouseX, 0, width, 0, TWO_PI);

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