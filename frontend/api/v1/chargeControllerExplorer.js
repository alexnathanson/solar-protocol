const params = new URLSearchParams(window.location.search);

let endPt,endPtVal,mod,modVal; 

if(params.get("value")){
	endPt = "value";
	endPtVal = params.get("value");
} else if(params.get("line")){
	endPt = "line";
	endPtVal = params.get("line");
} else if(params.get("day")){
	endPt = "day";
	endPtVal = params.get("day");
}

//example http://solarprotocol.net/api/v1/chargecontroller.php?file=list
let result = JSON.parse(httpGet(getBaseUrl() + '/api/v1/chargecontroller.php?' + endPt + "=" + endPtVal));

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