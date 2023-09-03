//version 0.7

// by everest pipkin --- everest-pipkin.com/ --- spring 2023

//var object_tableURL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTud3SCx8T-h2oxqpAYcdoMSoydE1yOt6QNMgKNUTaqKw5A7ixcqxsEhhXbZd38Z7OmEuZAtqk7wtQf/pub?gid=0&single=true&output=csv"; // spreadsheet url (make sure it has been "published")

var object_tableURL ="objects.csv"; 


var object_table;
var rooms = {};

var currentRoom;
var previousRoom;
var lockedScroll;


//papaparse
function init() {
	if (localStorage.driftMineSave == "found"){
		loadSavedGame();		
	}
	else{
		newGame();
	}
}

function loadSavedGame(){
	currentRoom = JSON.parse(localStorage.currentRoomName);
	object_table = JSON.parse(localStorage.object_table);
	rooms = JSON.parse(localStorage.rooms);
	loadRoom(rooms.save_found)
}

function newGame(){
    Papa.parse(object_tableURL, {
    download: true,
    header: true,
    complete: function(results) {
        	object_table = results.data
        	sortObjects(object_table);
        	loadRoom(rooms.new_game)
        	starCast();
		}
		})
}

function saveGame(){
	if (currentRoom.name != "save_found" && currentRoom.name != "new_game" && currentRoom.name != "dream" && currentRoom.name != "you" ){
		localStorage.setItem('driftMineSave', "found");
		localStorage.setItem('currentRoomName', JSON.stringify(currentRoom.name));
		localStorage.setItem('object_table', JSON.stringify(object_table));
		localStorage.setItem('rooms', JSON.stringify(rooms));
	}
}

function sortObjects(object_table){
    //console.log(object_table)

    for (x=0;x<object_table.length;x++){
    	object_table[x].verbs = object_table[x].verbs.split("|");
    	object_table[x].verbs_display = object_table[x].verbs_display.split("|");
    	object_table[x].onVerb_description = object_table[x].onVerb_description.split("|");
    	object_table[x].onVerb_linksTo = object_table[x].onVerb_linksTo.split("|");
    	object_table[x].onVerb_alter = object_table[x].onVerb_alter.split("|");
    	object_table[x].onVerb_dialog = object_table[x].onVerb_dialog.split("|");
    	object_table[x].onVerb_make = object_table[x].onVerb_make.split("|");

    	if (object_table[x].kind == "room"){
    		object_table[x].objects = [];
    		rooms[object_table[x].name] = object_table[x];
    	}
    	 if (object_table[x].kind == "dialog"){
    		object_table[x].description = object_table[x].description.split("|");
      		object_table[x].replies = object_table[x].replies.split("|");
    	}
    }
    for (d=0;d<object_table.length;d++){
    	if (object_table[d].kind == "object" || object_table[d].kind == "person"){
    			if (rooms[object_table[d].room]){
    				rooms[object_table[d].room].objects.push(object_table[d])
    		}
    	}
    	else if (object_table[d].kind == "menu"){
    		for (let name in rooms) {
    			if (name != "you" && name != "new_game" && name != "save_found" && name != "starry"){
    				rooms[name].objects.push(object_table[d])
    			}
			}
    	}
    }
	loadRoom(rooms.dream);
}

//↠ ↞

var gameWindow = document.createElement("div");
gameWindow.id = "gameWindow";
document.body.appendChild(gameWindow);

var toolTipHolder = document.createElement("div");
toolTipHolder.id = "toolTipHolder";
document.body.appendChild(toolTipHolder);

var toolTip = document.createElement("div");
toolTip.id = "toolTip";
toolTipHolder.appendChild(toolTip);


document.body.addEventListener('mousedown', function (event) {
	//checks where tooltip is - could do a state instead if i want more control 
	if (Number(toolTipHolder.style.top.slice(0, -1)) > 0){
	    if (toolTipHolder.contains(event.target)) {
	    } else {
			toolTipOffscreen()
	    }
	}

});


function toolTipOffscreen(){
	toolTipHolder.style.left = "-100%"
	toolTipHolder.style.top = "-100%"
}

function loadRoom(room){
	clickable();
	if (room.type == "click"){
		room = rooms[room.target.linksTo];
	}

	if (previousRoom != currentRoom && currentRoom.name != "save_found"){
		previousRoom = currentRoom;
	}

	currentRoom = room;

	saveGame();

	gameWindow.innerHTML = "";
	gameWindow.style.left = "0%";
	gameWindow.style.top = "0%";

	for (x=0;x<room.objects.length;x++){
		makeRoomObject(room.objects[x])
	}

	var counter = 0;
	var interval = setInterval(function() {
		counter = counter + 4;
		gameWindow.style.opacity = (Number(gameWindow.style.opacity) + .04);
		if (counter >= 100){
	      	clearInterval(interval)
	      }
  		},
     20);

	var counter2 = 0;
	var interval2 = setInterval(function() {
		counter2 = counter2 + 4;
		if (toolTipHolder.style.opacity>0){
			toolTipHolder.style.opacity = toolTipHolder.style.opacity - .04;
		}
		if (counter2 >= 100){
			//moves tooltip out of the way
			toolTipHolder.style.left = "-100%";
			toolTipHolder.style.top = "-100%";
	      	clearInterval(interval2)
	      }
  		},
      	10);
}

function makeRoomObject(dataObject){
		var object = document.createElement("div");
		object.name = dataObject.name;
		object.classList = "objects"
		if (dataObject.description != ""){
			object.style.cursor = "pointer";
		}
		else {
			object.style.cursor = "default";
		}
		object.innerHTML = dataObject.display;
		object.style.left = dataObject.positionX + "%";
		object.style.top = dataObject.positionY + "%";
		if (dataObject.vertical == "left"){
			object.classList = "objects verticalText_left"
		}
		if (dataObject.vertical == "right"){
			object.classList = "objects verticalText_right"
		}
		if (dataObject.description != ""){
			object.onclick = objectDescription;
		}
		if (dataObject.linksTo != ""){
			object.onclick = scrollRoom;	
		}
		gameWindow.appendChild(object);
}

function objectDescription(){

	toolTipHolder.classList = "normalTooltip"
	toolTipHolder.style.left = this.style.left;
	toolTipHolder.style.top = this.style.top;
	toolTipHolder.style.opacity = 1;

	var object = returnObject(this.name)

	toolTip.innerHTML = object.description;

	if (object.verbs != ""){
		for (i = 0; i < object.verbs.length;i++){
			if (i==0){
				toolTip.innerHTML = toolTip.innerHTML + "<br><br>";
			}
			if (object.verbs[i] != "" && object.verbs[i] != undefined){
				verbPopulate(object,object.verbs[i],i)
			}
		}
	}

	checkIfInViewport(toolTipHolder)
}


function checkIfInViewport(elem){
	var bounding = elem.getBoundingClientRect();
	if (bounding.top < 0) {
		elem.style.top = "0%";
	}

	if (bounding.left < 0) {
		elem.style.left = "0%";
	}

	if (bounding.bottom > (window.innerHeight || document.documentElement.clientHeight)) {
		//not moving with object when window size changes... look into if it bugs you
		var percent = (((bounding.bottom - window.innerHeight)/window.innerHeight) * 100) + 1;
		elem.style.top = Number(elem.style.top.slice(0, -1)) - percent  + "%";
	}

	if (bounding.right > (window.innerWidth || document.documentElement.clientWidth)) {
		var percent = (((bounding.right - window.innerWidth)/window.innerWidth) * 100) + 1;
		elem.style.left = Number(elem.style.left.slice(0, -1)) - percent  + "%";
	}

}

function verbPopulate(object,verb,place){
	var link = document.createElement("a");
	if (object.verbs_display[place] != "" && object.verbs_display[place] != undefined){
		link.innerHTML = "<center>" + object.verbs_display[place] + "</center>"; 
	}
	else{
		link.innerHTML = "<center>" + verb + "</center>";
	}
	link.addEventListener("click", function(){doAction(object,verb,place)});
	toolTip.appendChild(link);
}

function doAction(object,verb,place,domObject){
	
	var tool = "";
	var toolFound = false;

	if (verb.includes(":")){
		tool = verb.split(":")[0];
		verb = verb.split(":")[1];
	}

	for (f=0;f<rooms.you.objects.length;f++){
		if (tool == ""){
			toolFound = true;
			break;
		}
		else if (tool == rooms.you.objects[f].name){
			toolFound = true;
			break;
		}
	}

	var toolDisplay = findObjectByName(tool).display;

	if (toolFound == true){

		if (domObject == undefined){
			var domObject = getDOMElementByName(object.name);
		}

			if (object.onVerb_description[place] != ""){
				toolTip.innerHTML = object.onVerb_description[place];
			}
			else if (verb == "talk"){
				toolTip.innerHTML;
			}
			else {
				toolTipOffscreen();
			}

		//starting rooms
		if (verb == "new_game"){
			newGame();
		}
		if (verb == "load_save"){
			loadRoom(rooms[previousRoom])
		}
		//keep adding verbs as needed
		if (verb == "talk"){
			dialogPopulate(object,findObjectByName(object.onVerb_dialog[place]),0)
		}
		if (verb == "enter"){
			scrollRoom(domObject,object,place)
		}
		if (verb == "inspect"){
			toolTip.innerHTML = object.onVerb_description[place];	
		}
		if (verb == "close"){
			toolTipOffscreen();
		}


		//special cases 
		if (verb == "rotate"){
			rotateObject(object)
		}
		if (verb == "starry"){
			starCast(object)
		}
		if (verb == "end_game"){
			endGame();
		}
		//CAN ONLY make / take / place something once.
		if (verb == "take"){
			changeObjectRoom(object,"you")
			object.verbs[place]="";
		}
		if (verb == "make" && object.onVerb_make[place] != "" && object.onVerb_make[place] != undefined ){
			object.verbs[place]="";
			var newObjects = object.onVerb_make[place].split(",")
			for (g=0;g<newObjects.length;g++){
				var newObject = findObjectByName(newObjects[g]);
				newObject.room = currentRoom.name;
				currentRoom.objects.push(newObject)
				makeRoomObject(newObject)
			}
		}
		if (verb == "place"){
			var newObject = findObjectByName(tool);			
			changeObjectRoom(newObject,currentRoom.name)
			object.verbs[place]="";
		}

		//if an action changes something else
		var alter = object.onVerb_alter[place];

		if (alter != "" && alter != [] && alter != undefined){
			alterObject(alter, object)
		}
	}

	else {
		toolTip.innerHTML = "you need " + toolDisplay + " to do this.";		
	}

	saveGame();
}

function rotateObject(object){

	objectDom = getDOMElementByName(object.name)
	objectDom.classList.add("rotation");

	objectDom.style.left= "50%";
	objectDom.style.right= "50%";
}


function endGame(){
	var music = new Audio('darkasadungeon.mp3');
	music.play().catch((e)=>{console.log(e)})
	music.addEventListener('ended', newGame);

	//change room
	if (currentRoom.name != "tunnel_e_6"){
		loadRoom(rooms.tunnel_e_6);
	}
	
	toolTipHolder.style.opacity = 0;

	setTimeout(() => {
	creditDescription("drift mine satellite");
	}, "80000");

	setTimeout(() => {
		creditDescription("by <a href='https://everest-pipkin.com/' target='_blank'>everest pipkin</a>");
	}, "95000");

	setTimeout(() => {
		creditDescription("for solar protocol, spring 2023");
	}, "109000");

	setTimeout(() => {
		creditDescription("'dark as a dungeon' recorded by maddox brothers and rose, 1950");
	}, "121000");

	setTimeout(() => {
	  toolTipOffscreen()
	}, "133000");

	unclickable();

	for (d=0;d<currentRoom.objects.length;d++){

	//getDOMElementByName(currentRoom.objects[d].name).onclick = "";

		if (currentRoom.objects[d].kind == "person" || currentRoom.objects[d].name == "you"){
			objectDom = getDOMElementByName(currentRoom.objects[d].name)
			objectDom.style.animationDelay = (Math.random()*10000) + "ms";
			var mod = Math.floor(Math.random()*2)+1
			objectDom.classList.add("dance"+mod);
		}
	}
}

function clickable(){
	var unclickable = document.getElementById("unclickable");
	lockedScroll = false;
	unclickable.style.pointerEvents = "none";
}

function unclickable(){
	var unclickable = document.getElementById("unclickable");
	lockedScroll = true;
	unclickable.style.pointerEvents = "auto";
}

function creditDescription(description){

	if (toolTipHolder.style.opacity == 0){
		var counter3 = 0;
		var interval3 = setInterval(function() {
		counter3 = counter3 + 1;
		toolTipHolder.style.opacity = counter3/100;
		if (counter3 >= 100){
	      	clearInterval(interval3)
	      }
  		}, 50)
  	}

	toolTip.innerHTML = description;
	toolTipHolder.style.left = "50%";
	toolTipHolder.style.top = "50%";
	toolTipHolder.classList = "center"
}

function starCast(){
	for (d=0;d<rooms.starry.objects.length;d++){
		var dataObject = rooms.starry.objects[d];
		var object = document.createElement("div");
		object.name = dataObject.name;
		object.innerHTML = dataObject.display;
		object.classList = "objects fade"
		object.style.left = dataObject.positionX + "%";
		object.style.top = dataObject.positionY + "%";
		object.style.animationDelay = Math.floor(Math.random()*10) + "s";
		gameWindow.appendChild(object);
	}
}

function fadeObject(object){
	objectDom = getDOMElementByName(object.name)
	objectDom.classList.add("fade");
}

function alterObject(alter,object){
	alter = alter.split(",")

	for (c=0;c<alter.length;c++){
		alter[c] = alter[c].split(":");
		if (alter[c].length > 1){
			var objectToAlter = findObjectByName(alter[c][0]);
			var newObject = findObjectByName(alter[c][1])
		}
		else{
			var objectToAlter = object;
			var newObject = findObjectByName(alter[c][0])
		}

		newObject.room = objectToAlter.room;

		if (objectToAlter.positionX != newObject.positionX || objectToAlter.positionY != newObject.positionY){
			objectToAlter.description = [];
			objectToAlter.verbs = [];
			movePerson(objectToAlter,newObject.positionX,newObject.positionY,newObject)
		}
		
		else{
			finishAlterObject(objectToAlter,newObject)
		}
	}
}

function dialogPopulate(object,dialog,count){

	toolTip.innerHTML = "<br>" + dialog.description[count];

	var link = document.createElement("a");
	link.innerHTML = "->";

	var name = document.createElement("text");
	name.innerHTML = dialog.room + ":       ";
	name.style.display = "inline-block";
	name.style.width = "300px";

	if (dialog.description.length > count + 1){
		link.addEventListener("click", function(){dialogPopulate(object,dialog,count+1)});
		name.appendChild(link);
	}
	else {
		link.addEventListener("click", function(){replyPopulate(object,dialog)});
		name.appendChild(link);
	}

	toolTip.prepend(name) 
}

function replyPopulate(object,dialog){
	toolTip.innerHTML = "";

	if (dialog.replies != undefined){
		for (i = 0; i < dialog.replies.length;i++){
			const reply = dialog.replies[i];
			const verb = dialog.verbs[i];
			const d = i;
			var link = document.createElement("a");
			link.innerHTML = reply;
			if (i != dialog.replies.length - 1){
				link.innerHTML = link.innerHTML + "<br><br>";
			}
			link.addEventListener("click",
				function(){
					doAction(dialog,verb,d,getDOMElementByName(dialog.room))
				});
			toolTip.appendChild(link);
		}
	}
}

document.addEventListener("keydown", (e) => {
	if (lockedScroll != true){
		if (e.keyCode == "38" && returnObject("north") != "not found"){
			scrollRoom("keypress",returnObject("north"),0)
			}
		else if (e.keyCode == "40" && returnObject("south") != "not found"){
			scrollRoom("keypress",returnObject("south"),0)
			}
		else if (e.keyCode == "37" && returnObject("west") != "not found"){
			scrollRoom("keypress",returnObject("west"),0)
			}
		else if (e.keyCode == "39" && returnObject("east") != "not found"){
			scrollRoom("keypress",returnObject("east"),0)
			}
		}
	}
)

function scrollRoom(element,object,place){
	unclickable();
	//object elements in the world
	if (element == "keypress"){
		object = object
		roomChangeDescription(object.description)
		//element.style.opacity = 0;
		if (object.linksTo != "previousRoom"){
			newRoom = rooms[object.linksTo];
		}
		else if (previousRoom != currentRoom) {
			newRoom = previousRoom;
		}
		else {
			newRoom = rooms["train_car"];			
		}
		direction = object.name; // currently uses name match 
	}

	//object elements in the world
	else if (element.type == "click"){
		object = returnObject(element.target.name)
		roomChangeDescription(object.description)
		element.target.style.opacity = 0;

		if (object.linksTo != "previousRoom"){
			newRoom = rooms[object.linksTo];
		}
		else if (previousRoom != currentRoom) {
			newRoom = previousRoom;
		}
		else {
			newRoom = rooms["train_car"];			
		}
		direction = object.name; // currently uses name match 
	}

	//verb interactions from objects
	else {
		roomChangeDescription(object.onVerb_description[place])
		element.style.opacity = 0;
		newRoom = rooms[object.onVerb_linksTo[place]];
		direction = object.name;		
	}

	if (direction == "north"){
		goalX = 0;
		goalY = 100;
	}
	else if (direction == "east"){
		goalX = -100;
		goalY = 0;

	}
	else if (direction == "south"){
		goalX = 0;
		goalY = -100;
	}
	else if (direction == "west"){
		goalX = 100;
		goalY = 0;
	}
	else {
		goalX = 0;
		goalY = 0;		
	}

	var counter = 0;
	var interval = setInterval(function() {
		counter = counter + 2;
		gameWindow.style.left = (Number(gameWindow.style.left.slice(0, -1)) + goalX/150) + "%"; 
		gameWindow.style.top = (Number(gameWindow.style.top.slice(0, -1)) + goalY/150) + "%"; 
		gameWindow.style.opacity = 100 - counter + "%";
		
		if (counter == 100){
	     	if (loadRoom != undefined){
	     		loadRoom(newRoom)
	     	}
	      	clearInterval(interval)
	      }
  		},
     20);
}


function roomChangeDescription(description){
	toolTip.innerHTML = description;
	//need to actually center these
	toolTipHolder.style.left = "50%";
	toolTipHolder.style.top = "50%";
	toolTipHolder.classList = "center"
	toolTipHolder.style.opacity = 1;
}

function movePerson(objectToAlter,positionX,positionY,newObject){
	unclickable();

	person = getDOMElementByName(objectToAlter.name)

	if (person != undefined){
		var differenceX = positionX - person.style.left.slice(0, -1); //30 - 50 = -20
		var differenceY = positionY - person.style.top.slice(0, -1); //70 - 50 = 20
		var roomHolder = currentRoom;
		  var interval = setInterval(function() {
		  	if (differenceX != 0 ){
			  	if (differenceX > 0){
			  		person.style.left = (Number(person.style.left.slice(0, -1)) + 1) + "%"; 
			  		differenceX = differenceX - 1;
			  	}
			  	else if (differenceX < 0){
					person.style.left = (Number(person.style.left.slice(0, -1)) - 1) + "%"; 
					differenceX = differenceX + 1;
			  	}
			}
			if (differenceY != 0){
			  	if (differenceY > 0){
			  		person.style.top = (Number(person.style.top.slice(0, -1)) + 1) + "%"; 
			  		differenceY = differenceY - 1;
			  	}
			  	else if (differenceY < 0){
					person.style.top = (Number(person.style.top.slice(0, -1)) - 1) + "%"; 
					differenceY = differenceY + 1;
			  	}
			}
		     if (differenceX == 0 && differenceY == 0){
		     	finishAlterObject(objectToAlter,newObject)
		      	clearInterval(interval)
		      }
		     else if (previousRoom == roomHolder){
		     	finishAlterObject(objectToAlter,newObject)
		      	clearInterval(interval)
		     }
	  		},
	      200);
     }
}

function finishAlterObject(objectToAlter,newObject){

	for (g=0; g<rooms[objectToAlter.room].objects.length; g++){
		if (rooms[objectToAlter.room].objects[g].name == objectToAlter.name){
			rooms[objectToAlter.room].objects[g] = newObject;
		}
	}

	if (objectToAlter.room == currentRoom.name){
		var domObject = getDOMElementByName(objectToAlter.name);
		if (domObject != undefined){
			domObject.name = newObject.name;
			domObject.innerHTML = newObject.display;
		}
	}	

	if (newObject.moveTo != "" && newObject.moveTo != undefined && newObject.moveTo != []){
		if (newObject.moveToX != undefined && newObject.moveToX != ""){
			newObject.positionX = newObject.moveToX;
		}
		if (newObject.moveToY != undefined && newObject.moveToY != ""){
			newObject.positionY = newObject.moveToY;
		}
		changeObjectRoom(newObject,newObject.moveTo)
	}

	clickable();
	saveGame();

}

//changes what room an object is in
function changeObjectRoom(object,roomToMoveTo){
	var objectArray = rooms[object.room].objects;
	object.room = roomToMoveTo;
	if (getDOMElementByName(object.name) != undefined){
		getDOMElementByName(object.name).remove();
	}
	else {
		makeRoomObject(object)
	}
	objectArray.splice(objectArray.indexOf(object),1);
	rooms[roomToMoveTo].objects.push(object);
}

//helper function returns object in objects list by name - current room only
function returnObject(objectName){
	object = "not found";

	for (g=0; g<currentRoom.objects.length; g++){
		if (currentRoom.objects[g].name == objectName){
				object = currentRoom.objects[g];
		}
	}
	return object;
}

//the inverse - get dom element by name - current room only
function getDOMElementByName(name){
	for (d=0; d<gameWindow.children.length; d++){
		if (gameWindow.children[d].name == name){
			return gameWindow.children[d];
		}
	}
}

//or - all objects from object table?
function findObjectByName(name){
	    for (x=0;x<object_table.length;x++){
	    	if (object_table[x].name == name){
				return object_table[x];
			}
		}	
}


window.addEventListener("DOMContentLoaded", init);

