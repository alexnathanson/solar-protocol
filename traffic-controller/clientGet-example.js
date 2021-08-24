
let result = JSON.parse(httpGet('http://108.29.41.133/api/v1/chargecontroller.php?value=PV-voltage'));

console.log(Object.keys(result));

console.log(result);

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}