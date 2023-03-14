
var object_tableURL =
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vTud3SCx8T-h2oxqpAYcdoMSoydE1yOt6QNMgKNUTaqKw5A7ixcqxsEhhXbZd38Z7OmEuZAtqk7wtQf/pub?gid=0&single=true&output=csv"; // spreadsheet url (make sure it has been "published")

var object_table;
var rooms = [];

//papaparse
function init() {

            Papa.parse(object_tableURL, {
	        download: true,
	        header: true,
	        complete: function(results) {
	            object_table = results.data
	            sortObjects(object_table);
	           // if (localStorage.savedGame == "found"){
				//	beginGame();		
				//}
				}
   			})
}

function sortObjects(object_table){
    //console.log(object_table)

    //splitting into arrays... may rethink this in the future again
    for (x=0;x<object_table.length;x++){
    	object_table[x].verbs = object_table[x].verbs.split("|");
    	object_table[x].verbs_display = object_table[x].verbs_display.split("|");
    	object_table[x].onVerb_description = object_table[x].onVerb_description.split("|");
    	object_table[x].onVerb_linksTo = object_table[x].onVerb_linksTo.split("|");
    	object_table[x].onVerb_alter = object_table[x].onVerb_alter.split("|");
    	object_table[x].onVerb_dialog = object_table[x].onVerb_dialog.split("|");
    	object_table[x].onVerb_make = object_table[x].onVerb_make.split("|");
    	object_table[x].onVerb_unmake = object_table[x].onVerb_unmake.split("|");

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
    			if (name != "you"){
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

var toolTip = document.createElement("div");
toolTip.id = "toolTip";
document.body.appendChild(toolTip);


document.body.addEventListener('mousedown', function (event) {
	//checks where tooltip is - could do a state instead if i want more control 
	if (Number(toolTip.style.top.slice(0, -1)) > 0){
	    if (toolTip.contains(event.target)) {
	    } else {
			toolTipOffscreen()
	    }
	}


    var xCord = event.clientX;
    var yCord = event.clientY;

    var xPercent = ((xCord/window.innerWidth)*100).toString().slice(0,2);
    var yPercent = ((yCord/window.innerHeight)*100).toString().slice(0,2);

	console.log("x: " + xPercent+", y:" +yPercent);

});

var currentRoom;
var previousRoom;

function toolTipOffscreen(){
	toolTip.style.left = "-100%"
	toolTip.style.top = "-100%"
}

function loadRoom(room){
	if (room.type == "click"){
		room = rooms[room.target.linksTo];
	}

	previousRoom = currentRoom;
	currentRoom = room;

	gameWindow.innerHTML = "";
	gameWindow.style.left = "0%";
	gameWindow.style.top = "0%";

	for (x=0;x<room.objects.length;x++){
		makeRoomObject(room.objects[x])
	}

	var counter = 0;
	var interval = setInterval(function() {
		counter = counter + 2;
		gameWindow.style.opacity = Number(gameWindow.style.opacity) + counter/100;
		if (counter > 100){
	      	clearInterval(interval)
	      }
  		},
     20);

	var interval2 = setInterval(function() {
		counter = counter + 2;
		if (toolTip.style.opacity>0){
			toolTip.style.opacity = toolTip.style.opacity - (counter/100);
		}
		if (counter > 100){
			//moves tooltip out of the way
			toolTip.style.left = "-100%";
			toolTip.style.top = "-100%";
	      	clearInterval(interval2)
	      }
  		},
      	10);
}

function makeRoomObject(dataObject){
		var object = document.createElement("div");
		object.name = dataObject.name;
		object.classList = "objects"
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
		gameWindow.appendChild(object)
}

function objectDescription(){

	toolTip.classList = "normalTooltip"
	toolTip.style.left = this.style.left;
	toolTip.style.top = this.style.top;
	toolTip.style.opacity = 1;

	var object = returnObject(this.name)

	toolTip.innerHTML = object.description;

	if (object.verbs != ""){
		for (i = 0; i < object.verbs.length;i++){
			if (i==0){
				toolTip.innerHTML = toolTip.innerHTML + "<br><br>";
			}
			verbPopulate(object,object.verbs[i],i)
		}
	}

	checkIfInViewport(toolTip)
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
	//console.log(object.verbs_display[place])
	if (object.verbs_display[place] != "" && object.verbs_display[place] != undefined){
		link.innerHTML = "<center>" + object.verbs_display[place] + " " + object.display + "</center>"; //might want to remove object word
	}
	else{
		link.innerHTML = "<center>" + verb + " " + object.display + "</center>";
	}
	link.addEventListener("click", function(){doAction(object,verb,place)});
	toolTip.appendChild(link);
}

function doAction(object,verb,place,domObject){
	
	//console.log(object,verb,place);
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
			else if (verb == "talk to"){
				toolTip.innerHTML;
			}
			else {
				toolTipOffscreen();
			}

		//keep adding verbs as needed
		if (verb == "talk to"){
			dialogPopulate(object,findObjectByName(object.onVerb_dialog[place]),0)
		}
		if (verb == "enter" || verb == "leave"){
			scrollRoom(domObject,object,place)
		}
		if (verb == "inspect" || verb == "touch"){
			toolTip.innerHTML = object.onVerb_description[place];	
		}

		if (verb == "close"){
			toolTipOffscreen();
		}
		//this works BUT it will get fiddly with objects "editing" themselves... beware
		//CAN ONLY make / take something once. object stays with you forever. key item energy
		if (verb == "take"){
			changeObjectRoom(object,"you")
			object.verbs.splice(object.verbs.indexOf("take"),1);
		}
		if (verb == "make"){
			object.verbs.splice(object.verbs.indexOf("make"),1);
			var newObject = findObjectByName(object.onVerb_make[place]);
			newObject.room = currentRoom.name;
			currentRoom.objects.push(newObject)
			makeRoomObject(newObject)
		}
		if (verb == "unmake"){
			object.verbs.splice(object.verbs.indexOf("unmake"),1);
			var deleteObject = returnObject(object.onVerb_unmake[place]);
			changeObjectRoom(deleteObject,"")
		}
		if (verb == "place"){
			var newObject = findObjectByName(tool);			
			changeObjectRoom(newObject,currentRoom.name)
			object.verbs.splice(object.verbs.indexOf("place"),1);
		}

		var alter = object.onVerb_alter[place];
		//edits object. note- changes mean that objects now need unique names!
		/*
		if (alter != "" && alter != [] && alter != undefined){
			for (g=0; g<currentRoom.objects.length; g++){
				if (currentRoom.objects[g].name == object.name){
					alteredObject = findObjectByName(object.onVerb_alter[place]);
					alteredObject.room = currentRoom;
					domObject.name = alteredObject.name
					currentRoom.objects[g] = alteredObject;
				}
			}
		}
	*/

		if (alter != "" && alter != [] && alter != undefined){

			alter = alter.split(",")
			console.log(alter)

			for (c=0;c<alter.length;c++){
				alter[c] = alter[c].split(":");
				console.log(alter[c])
				if (alter[c].length > 1){
					var objectToAlter = findObjectByName(alter[c][0]);
					var newObject = findObjectByName(alter[c][1])
				}
				else{
					var objectToAlter = object;
					var newObject = findObjectByName(alter[c][0])
				}
				console.log(objectToAlter,newObject)

				newObject.room = objectToAlter.room;
				
				for (g=0; g<rooms[objectToAlter.room].objects.length; g++){
					if (rooms[objectToAlter.room].objects[g].name == objectToAlter.name){
						rooms[objectToAlter.room].objects[g] = newObject;
					}
				}

				if (objectToAlter.room == currentRoom.name){
						getDOMElementByName(objectToAlter.name).name = newObject.name;
				}	

			}

		}
	}

	else {
		toolTip.innerHTML = "you need " + toolDisplay + " to do this.";		
	}
}

function dialogPopulate(object,dialog,count){

	toolTip.innerHTML = dialog.room + ": " + dialog.description[count];

	var link = document.createElement("a");
	link.style.float = "right";
	link.innerHTML = "->";

	if (dialog.description.length > count + 1){
		link.addEventListener("click", function(){dialogPopulate(object,dialog,count+1)});
		toolTip.appendChild(link);
	}
	else {
		link.addEventListener("click", function(){replyPopulate(object,dialog)});
		toolTip.appendChild(link);
	}
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

function scrollRoom(element,object,place){

	//object elements in the world
	if (element.type == "click"){
		object = returnObject(element.target.name)
		roomChangeDescription(object.description)
		element.target.style.opacity = 0;
		if (object.linksTo != "previousRoom"){
			newRoom = rooms[object.linksTo];
		}
		else {
			newRoom = previousRoom;
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
	toolTip.style.left = "50%";
	toolTip.style.top = "50%";
	toolTip.classList = "center"
	toolTip.style.opacity = 1;
}

//movePerson(this,30,70)
function movePerson(person,positionX,positionY){

	for (x=0;x<people.length;x++){

		if (person.name == people[x].name){
			people[x].positionX = positionX;
			people[x].positionY = positionY;
		}
	}

	var differenceX = positionX - person.style.left.slice(0, -1); //30 - 50 = -20
	var differenceY = positionY - person.style.top.slice(0, -1); //70 - 50 = 20

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
	     	//console.log("clearing interval")
	      	clearInterval(interval)
	      }
  		},
      	200);
}

//changes what object a room is in
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

/*
var objectFound = false;

    for (x=0; x<rooms.length; x++){
    	for (f=0; f<rooms[x].objects; f++){
    		if (rooms[x].objects[f].name == name){
    			objectFound = true;
				return rooms[x].objects[f];
				break;
			}
    	}
    }

	if (objectFound == false){*/
	    for (x=0;x<object_table.length;x++){
	    	if (object_table[x].name == name){
				return object_table[x];
			}
		}	
	//}
}


window.addEventListener("DOMContentLoaded", init);
