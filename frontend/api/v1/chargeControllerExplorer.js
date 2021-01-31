const params = new URLSearchParams(window.location.search);

//this could be much simplied by getting the url search params in a string and just adding it to the url...

let endPt,endPtVal,mod,modVal = ""; 
let modified = false;
if(params.get("value")){
	endPt = "value";
	endPtVal = params.get("value");

	if(params.get("duration")){
		mod= "duration";
		modVal=params.get("duration");
		modified = true;
	}
} else if(params.get("line")){
	endPt = "line";
	endPtVal = params.get("line");
} else if(params.get("day")){
	endPt = "day";
	endPtVal = params.get("day");
}

//example http://solarprotocol.net/api/v1/chargecontroller.php?file=list

let dst = getBaseUrl() + '/api/v1/chargecontroller.php?' + endPt + "=" + endPtVal;

if(modified){
	dst = dst + "&" + mod + "=" + modVal;
}

console.log(dst);

let result = JSON.parse(httpGet(dst));

console.log(result);

function getBaseUrl() {
    var re = new RegExp(/^.*\/\/[^\/]+/);
    //console.log(re.exec(window.location.href));
    return re.exec(window.location.href);
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}