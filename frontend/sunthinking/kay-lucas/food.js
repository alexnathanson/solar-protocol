class food {
  constructor(_x, _z, _big, _testFood) {
    let range = 1000;
    this.loc = createVector(_x, -5, _z)
    this.color = color(random(255), random(255), random(255));
    this.greyColor = color(random(20, 230));
    this.YRot = random(TWO_PI);
    this.remove = false;
    this.w = random(5, 20);
    this.h = random(5, 20);
    this.l = random(5, 20);
    this.peckNum = 3;
    this.peckFlag = false;
    this.ignore = false; 
    this.discard = false; 
    this.peckNumFood = int(random(1, 8)); 
    this.foodType = int(random(4)); 
    this.big = _big; 
    this.garbageType = int(random(2)) // 0-box, 1 box with bag, 2 bag
    this.gbNum = int(random(4)); 
    this.testFood = _testFood; 
    if(_big){
      this.foodType = 4; 
      this.w = random(80, 220); 
      this.h = random(80, 120); 
      this.l = random(80, 220); 
      this.loc.y = this.h/2; 
    }
    this.detail = 8; 
    if(this.foodType == 3){ // make donut smaller 
      this.w = random(3, 12); 
      this.h = this.w * 2; 
    }
    let ran = random(3); 
    if(ran< 1){
      
      this.ignore = true; 
    }
    if(ran > 1 && ran < 2){
      this.discard  = true; 
    }
    if(this.w + this.l + this.h > 40){
      this.discard  = true; 
    }
    if(_testFood){
      this.loc.x = int(random(2000, 3000)); 
      this.loc.z = 0; 
      this.ignore = false; 
      this.w = 10; 
      this.l = 10; 
      this.h = 10; 
      this.peckNumFood = int(random(2, 6)); 
    }
  }
  display() {
    
    this.detail = int(map(panelPower, 0, 50, 4, 8))
    fill(this.color);
    if(greyScale){
      fill(this.greyColor); 
    }
    stroke(1); 
    if (!showLines) {
      noStroke();
    }
    if(panelPower < bwNum){
      noFill(); 
      stroke(255)
    }
    
    this.loc.x += -walkSpeed;
    if (this.loc.x < -5000) {
      if(this.big){
        this.loc.x = 5000; 
        if(random(2) < 1){
          this.loc.z = 500 + random (200)
        }else{
          this.loc.z = -500 - random (200)
        }
        this.garbageType = int(random(3))
      }else{
      this.remove = true;
      }
    }
   
    push();
    this.loc.y = -this.h/2
    translate(this.loc.x, this.loc.y + 2, this.loc.z)
    rotateY(this.YRot); 
    if(this.foodType == 0){
      box(this.w, this.h, this.l); 
    } else if(this.foodType == 1){
      sphere(this.h, this.detail, this.detail); 
    }
    else if(this.foodType == 2){
      cylinder(this.h, this.w, this.detail, 1); 
    }
    else if(this.foodType == 3){
      rotateX(HALF_PI); 
      torus(this.h, this.w, this.detail, this.detail); 
    }
    else if(this.foodType == 4){

      if(this.garbageType ==0 ){ // bag
      fill(bagColorArray[this.gbNum]); 
      if(greyScale){
        fill(this.greyColor); 
      }
      if(panelPower < bwNum){
        noFill(); 
        stroke(255)
        
      }
          push() 
        translate(0,this.h/4, 0)
        ellipsoid(this.w/2 -2, this.h/2-2, this.l/2 -2, int(this.detail/2)+2, int(this.detail/2)+2)
       pop()
    }
    
    if(this.garbageType == 1){
      fill(50);
      push()
      translate(0, 36, 0)
      rotateX(HALF_PI + .1)
      torus(60, 20, this.detail);
      pop()
    }
  }

    pop();
  }
}