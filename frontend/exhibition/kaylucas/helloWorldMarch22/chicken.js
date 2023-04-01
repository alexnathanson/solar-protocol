class chicken {
    constructor(_w, _YRot, _x, _y, _z) {
        this.rootLoc = createVector(_x, _y, _z); //-114
        this.bodySize = 110; // 110 140
        this.headsize = 40; // 50 
        this.neckLength = 80; // 90; 140
        this.neckwidth = 48;  // 55;
        this.neckwidthUp = 25; // 0;

        this.leg1Length = 70;
        this.leg2Length = 50;
        this.walkRotSpeed = 0;
        this.bodyTilt = 1.2; // .5
        this.bodyTiltHome = 1.2; // .5
        this.peckDRot = 2.4;
        this.peckSpeed = .1;
        this.peckDir = true;

        this.wingWidth = 50;
        this.wingLength = 170;
        this.wingWidthUp = 20;

        this.eyeColor = color(1);
        this.torusColor = color(255);
        this.headColor = color(200, 65, 0); //214, 40, 40
        this.crownColor = color(255, 0, 0);
        this.bodyColorNum = int(random(4));
        this.bodyColor = color(200, 65, 0); // this.bodyColor = roosterBodyArray[this.bodyColorNum]
        //this.wingColorNum = int(random(4));
        this.wingColor = color(200, 65, 0);// roosterWingArray[this.wingColorNum];
        //this.neckColorNum = int(random(4));
        this.neckColor = color(200, 65, 0); // this.neckColor = roosterNeckArray[this.neckColorNum];
        this.feetColor = color(178, 154, 154); //fill(200, 150,  170)
        this.tailColor = color(0, 48, 73); //fill(200, 150,  170)
        this.beakColor = color(194, 185, 168); //200, 100, 0
        this.tailColor2 = color(255);


        // this.headColor = color(255);
        // this.crownColor = color(255);
        // this.bodyColor = color(255); // 140, 140, 170 // 200, 150,  170); 
        // this.wingColor = color(255);
        // this.neckColor = color(255) //fill(200, 150,  170)
        // this.feetColor = color(255) //fill(200, 150,  170)
        // this.tailColor = color(255) //fill(200, 150,  170)
        // this.beakColor = color(255)


        this.sideTiltAmount = 12;  // higher less tilt 
        this.neckBobNum = 10; // higher less tilt 
        this.headBobNum = 10; // higher less tilt 
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
                this.headColor = color(200, 65, 0); //214, 40, 40
                this.crownColor = color(255, 0, 0);
                this.bodyColorNum = int(random(4));
                this.bodyColor = color(200, 65, 0); // this.bodyColor = roosterBodyArray[this.bodyColorNum]
                //this.wingColorNum = int(random(4));
                this.wingColor = color(200, 65, 0);// roosterWingArray[this.wingColorNum];
                //this.neckColorNum = int(random(4));
                this.neckColor = color(200, 65, 0); // this.neckColor = roosterNeckArray[this.neckColorNum];
                this.feetColor = color(178, 154, 154); //fill(200, 150,  170)
                this.tailColor = color(0, 48, 73); //fill(200, 150,  170)
                this.beakColor = color(194, 185, 168); //200, 100, 0
                this.tailColor2 = color(255);
            }
        }

        let t = createVector(240, 0, 0); // peck location
        //      push()
        // translate(t.x, t.y, t.z); 
        // sphere(5)
        // pop() 
        if (this.mainBird && this.birdPecking == false) {
            for (let i = foodList.length - 1; i >= 0; i--) {
                let fd = foodList[i].loc;
                if (fd.dist(t) < 120 && foodList[i].ignore == false && fd.x < t.x) { // peck if it's within range. 
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
                if (this.pecknum >= this.peckNumMax) {
                    if (this.foodNum >= 0) {
                        if (foodList[this.foodNum].discard == false) {
                            foodList[this.foodNum].remove = true; // if it's a normal seed, eat it. 
                            birdSteps = 0;
                            foodPecked = 0;
                        } else {
                            //this.birdPecking = false;  // if its a discard seed, leave it alone and ignore it 
                            foodList[this.foodNum].ignore = true;
                        }
                        this.pecknum = 0;
                        this.peckNumMax = 1;
                        this.lockedOnSeed = false;
                    }
                } else {
                    foodList[this.foodNum].loc.x = t.x + random(-8, 8) // move food to Peck point. 
                    foodList[this.foodNum].loc.z = t.z + random(-8, 8)
                    foodList[this.foodNum].YRot += random(-.5, .5)
                }

                // if (this.pecknum >= this.peckNumMax) {
                //     if (this.foodNum >= 0) {
                //         foodList[this.foodNum].remove = true;
                //         this.pecknum = 0;
                //         this.peckNumMax = 1;
                //     }
                // } else {
                //     //nudgeFood = true;
                //     foodList[this.foodNum].loc.x += random(-8, 8)
                //     foodList[this.foodNum].loc.z += random(-8, 8)
                //     foodList[this.foodNum].YRot += random(-.5, .5)
                // }
            }
            if (this.bodyTilt < this.bodyTiltHome) {
                this.peckSpeed *= -1;
                this.birdPecking = false;
                globalPecking = false;
                birdWalkBool = true;
                // this.headRotY = 0;
            }
        }
        if (camView) {
            this.detail = int(map(panelPower, 0, 50, 5, 20)) // technically the panel can put out 50 W, but we should change this
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

            if (panelPower < bwNum) {
                this.bw = true;
                //this.stColor = color(255, 255, 255)
            }
            else {
                this.bw = false;
                //this.stColor = color(1)
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
            rotateZ(this.bodyTilt); //rotTest
            rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);

            translate(-this.bodySize / 2.5, -this.bodySize / 4, 0); // center of body
            fill(this.bodyColor)
            if (this.bw) {
                noFill();
            }
            ellipsoid(this.bodySize * .6, this.bodySize * 1, this.bodySize * .6, this.detail, this.detail); // draw body 

            // BEGIN BACK

            translate(-26.5, 0, 0); // back
            rotateZ(.0125);
            fill(this.headColor);  // back color
            if (this.bw) {
                noFill();
            }
            ellipsoid(this.bodySize * .45, this.bodySize * .9, this.bodySize * .55, this.detail, this.detail)  // back of bird
            pop(); // back to root
            // END BACK

            push();
            translate(-17, -18, this.bodySize - 52); // right hip
            this.drawLeg(0);
            pop()
            pop(); // back to root;;

            push();
            translate(-18, -18, - this.bodySize + 52); // LEFT hip
            this.drawLeg(PI);
            pop()

            pop(); // back to root
            push()
            rotateZ(this.bodyTilt + 5.4); // 5.7 tilt of the whole body
            rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount); // bob neck on the X 
            rotateZ(sin((this.walkRotSpeed * 2) + HALF_PI) / this.neckBobNum);  // bob neck 
            //   this.neckLength =  140; // 90;
            //   this.neckwidth =  80;  // 55;
            //   this.neckwidthUp = 30; // 0;
            translate(-this.bodySize / 2 + 82, -this.bodySize - this.neckLength / 2, 0)
            //translate(-this.bodySize / 6, -this.bodySize - this.neckLength / 2 + 30, 0) // middle of neck 

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
            //fill(this.neckColor) // fill(200, 150,  170)
            fill(0) // fill(200, 150,  170)
            if (this.bw) {
                noFill();
            }
            //stroke(1) // so you can see neck detail 
            //noStroke()
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

            //let testY = map(mouseY, 0, height, 0, TWO_PI)
            //rotateY(this.headRotY);
            fill(this.headColor)
            if (this.bw) {
                noFill();
            }
            sphere(this.headsize - 1, this.detail, this.detail) // head
            //camera(0, 0, 0, 0, 500, 0, 0, 1, 0);
            push()
            translate(50, 0, 0)  // beak 
            fill(this.beakColor)
            if (this.bw) {
                noFill();
            }
            rotateZ(-HALF_PI)
            cone(15, 45, this.detail, false);// beak size 
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
            translate(15, -10, -this.headsize + 5.5) // right eye 
            rotateY(-.3)
            torus(6, 2, torusDetail, torusDetail);
            fill(1); //1
            stroke(1)
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
            rotateZ(this.bodyTilt); //rotTest
            rotateX(sin(this.walkRotSpeed + HALF_PI) / this.sideTiltAmount);
            push() // left wing

            // translate(-80, -10, this.bodySize * 0.6) // left wing
            translate(-60, 5, this.bodySize * .55) // left wing
            if (this.birdPecking) {
                rotateX(1.2);
                //rotateZ(5.6);
            }
            translate(-30, 5, 0) // left wing
            this.drawWing(3.51, .3, 6.05)
            pop()

            push() // right wing

            translate(-60, 30, -this.bodySize * .55)
            if (this.birdPecking) {
                rotateX(-1.2);
                //rotateZ(5.6);
            }
            translate(-30, 30, 0)


            this.drawWing(3.51, 3.3, 6.05)
            pop()

            push()
            translate(-this.bodySize + 120, this.bodySize / 2 - 20, 0) // tail 
            this.tailRot = map(mouseX, 0, width, 0, TWO_PI)
            rotateZ(.75) // .1
            // print(this.bodySize )
            fill(this.tailColor)
            if (this.bw) {
                noFill();
            }
            translate(-60, 120, 0) // middle of tail 
            cone(this.bodySize * .53, 200, this.detail, false, false)
            //cone(this.bodySize * .8, 300, this.detail, false, false)
            //sphere(40)
            pop()
            pop()

            if (this.mainBird && showShadow) {
                translate(0, -this.rootLoc.y - 1, 0) // shadow
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
                rotateZ(sin(this.walkRotSpeed + _rotOffset) / 2 + 0.2); // 0.5 how far the right hip turns  
            } else {
                rotateZ(0.15); //
            }
        } else {
            rotateZ(0.15); //
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
        let healRot = cos(this.walkRotSpeed) + 5.5
        //let rotRheal = cos(this.walkRotSpeed) / 5 + 5.5;

        if (this.mainBird) { // rotate the foot. 
            if (!primePeckingBuffer) {
                rotateZ(4.6) // 4.6 5.18 5.12 5.3 , 4.7 // 4.98
                //rotateZ(4.7) // 5.12
            } else {
                rotateZ(4.7); // 4.7 5.08
            }

        } else {
            rotateZ(4.7) // 4.7 5.08 5.12
        }

        push();
        push();
        translate(0, 36, 0); // right foot 
        rotateX(QUARTER_PI)
        //box(2, 40, 40) // right foot size is 32 box(2, 64, 64)
        pop()
        translate(0, 18, 0); // right toe Center 15
        cylinder(3, 70);
        pop();
        push();
        rotateX(0.7);
        translate(0, 26, 0); // right toe Right  translate(0, 25, 0)
        cylinder(3, 48);
        pop();
        push();
        rotateX(-0.7);
        translate(0, 26, 0); // right toe Right
        cylinder(3, 48);

        // if (this.mainBird) { // rotate the foot. 
        //     if (!this.birdPecking) {
        //         rotateZ(5.3) // 5.12
        //     } else {
        //         rotateZ(5.12); //
        //     }

        // } else {
        //     rotateZ(5.12) // 5.12
        // }

        // push();
        // translate(0, 16, 0); // right foot 
        // rotateX(QUARTER_PI)
        // box(2, 50, 50) // foot size is 32
        // //pop()
    }
    drawWing(_rz, _ry, _rx) {

        let PLow = []
        let PHigh = []

        let rot = 0;
        let faceNum = int(this.detail / 2); // map(this.detail, 4, 20, 4, 12); //12; // # of sides of the neck 
        for (let i = 0; i < faceNum; i++) {
            let r = PI / faceNum;
            rot += r;
            PLow[i] = createVector(cos(rot) * this.wingWidth, this.wingLength / 2, sin(rot) * this.wingWidth)
            PHigh[i] = createVector(cos(rot), -this.wingLength * .7, sin(rot))
        }
        fill(this.wingColor) // fill(200, 150,  170)
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

        // let w1 = createVector(60, -50, 5) // wing shape points
        // let w2 = createVector(60, 50, 5)
        // let w3 = createVector(-90, 20, 3)
        // let w4 = createVector(-90, -20, 3)

        // let w5 = createVector(w1.x, w1.y, -10) // wing is wider at the shoulder 
        // let w6 = createVector(w2.x, w2.y, -10)
        // let w7 = createVector(w3.x, w3.y, -3)
        // let w8 = createVector(w4.x, w4.y, -3)
        // fill(this.wingColor);
        // rotateZ(5.3) // wing angle 

        // if(this.birdPecking ){
        // }
        // beginShape(); // wing front 
        // vertex(w1.x, w1.y, w1.z);
        // vertex(w2.x, w2.y, w2.z);
        // vertex(w3.x, w3.y, w3.z);
        // vertex(w4.x, w4.y, w4.z);
        // endShape(CLOSE);

        // beginShape();  // wing back 
        // vertex(w5.x, w5.y, w5.z);
        // vertex(w6.x, w6.y, w6.z);
        // vertex(w7.x, w7.y, w7.z);
        // vertex(w8.x, w8.y, w8.z);
        // endShape(CLOSE);

        // beginShape(); // wing top 
        // vertex(w1.x, w1.y, w1.z);
        // vertex(w2.x, w2.y, w2.z);
        // vertex(w6.x, w6.y, w6.z);
        // vertex(w5.x, w5.y, w5.z);
        // endShape(CLOSE);

        // beginShape(); // wing bottom 
        // vertex(w3.x, w3.y, w3.z);
        // vertex(w4.x, w4.y, w4.z);
        // vertex(w8.x, w8.y, w8.z);
        // vertex(w7.x, w7.y, w7.z);
        // endShape(CLOSE);

        // beginShape(); // wing front 
        // vertex(w1.x, w1.y, w1.z);
        // vertex(w4.x, w4.y, w4.z);
        // vertex(w8.x, w8.y, w8.z);
        // vertex(w5.x, w5.y, w5.z);

        // endShape(CLOSE);
        // beginShape(); // wing front 
        // vertex(w2.x, w2.y, w2.z);
        // vertex(w3.x, w3.y, w3.z);
        // vertex(w7.x, w7.y, w7.z);
        // vertex(w6.x, w6.y, w6.z);
        // endShape(CLOSE);
    }
}