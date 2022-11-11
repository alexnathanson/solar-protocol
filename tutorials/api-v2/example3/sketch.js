//Equisite Corpse!!!

//variable to store the data we request from the API
let serverName = '';

let nextTime = 0;

let searchTerms = ['location','city','name', 'country'];
let searchLength = searchTerms.length

function setup() {
  //set the drawing canvas
  createCanvas(windowWidth, windowHeight);

  //make an asyncronous API call to get the server's location
  loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=location', gotLocation); 

  background(random(100)+155, random(100)+155,random(100)+155); 

}

function draw() {

  //get new images every 20 seconds
  if(millis() > nextTime){
    nextTime = millis() + (20*1000);
    //make an asyncronous API call to get the server's location
    loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=location', gotLocation); 
  }

}

function gotLocation(l){
  myQuery = l[Object.keys(l)[0]]
  //console.log(myQuery)

  //we must make sure we only get responses that have images
  loadJSON('https://collectionapi.metmuseum.org/public/collection/v1/search?q='+myQuery + '&hasImages=true', (r)=>{searchResults(r,myQuery)});
}

function searchResults(r,q){

  //if no results are returned from location, lets try city
  if(r['total']==0){
    let q = searchTerms[int(random(searchLength))]
    console.log(q);

    loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=' + q, gotLocation); 
  } else {
    //console.log(r)
    //console.log(r['objectIDs'].length)
    //lets pick a random image from the results
    let randomID = r['objectIDs'][int(random(r['objectIDs'].length))]
    //console.log(randomID)
    //now we request the object from the collection
    loadJSON('https://collectionapi.metmuseum.org/public/collection/v1/objects/' + randomID, (r)=>{gotObj(r,q)});
  }

}

function gotObj(o,q){
  //console.log(o)
  //console.log(o['primaryImageSmall'])

  let dst = o['primaryImageSmall'].replace('https://images.metmuseum.org','')
  //console.log(dst)

  let iX = int(random(windowWidth-100));
  let iY =  int(random(windowHeight/2));

  loadImage('http://127.0.0.1:5000'+dst, img => {
    image(img, iX, iY);
  });

  text(q,iX,iY);
  
}