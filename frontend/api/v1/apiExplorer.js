const params = new URLSearchParams(window.location.search);

if(window.location.search.length > 0){

	let endPoint = '';

	for(let pair of params.entries()) {
/*	   console.log(pair[0]+ ', '+ pair[1]);*/

	   if (pair[1] == ''){
			if(endPoint != ''){
				endPoint = endPoint + "&";
			}
			endPoint = endPoint + pair[0] + "=" + pair[1];
		}	
	}

	let dst = getBaseUrl() + '/api/v1/opendata.php?' + endPoint;

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