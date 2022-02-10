const params = new URLSearchParams(window.location.search);

if(window.location.search.length > 0){

	//this could be much simplied by getting the url search params in a string and just adding it to the url...

	let endPt,endPtVal,mod,modVal = ""; 
	let modified = false;

/*	let paramKeys = params.keys();
	let paramValues = params.values();

	console.log(paramKeys);
	console.log(paramValues);*/

	let endPoint = '';


	for(let pair of params.entries()) {
	   console.log(pair[0]+ ', '+ pair[1]);

	   if (pair[0] != 'server'){
			if(endPoint != ''){
				endPoint = endPoint + "&";
			}
			endPoint = endPoint + pair[0] + "=" + pair[1];
		}	
	}
/*
	for(let p = 0; p < paramKeys.length; p ++){
		if (paramKeys[p] != 'server'){
			if(p != 0){
				endPoint = endPoint + "&";
			}
			endPoint = endPoint + paramKeys[p] + "=" + paramValues[p];
		}	
	}*/

	console.log(endPoint);

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
	} else if (params.get("systemInfo")){
		endPt = "systemInfo";
		endPtVal = params.get("systemInfo");
	} else if (params.get("networkInfo")){
		endPt = "networkInfo";
		endPtVal = params.get("networkInfo");
	}

	//example http://solarprotocol.net/api/v1/opendata.php?file=list

	let dst = getBaseUrl() + '/api/v1/opendata.php?' + endPt + "=" + endPtVal;

	if(modified){
		dst = dst + "&" + mod + "=" + modVal;
	}

	console.log(dst);

	let result = httpGet(dst);

	if(typeof result === "object"){
		result = JSON.parse(result);
	}

	console.log(result);
}

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