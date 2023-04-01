//Hello! Welcome to the javascript side of Orbital Decay! 
//This was assembled by Rory Gillen and I hope you can make sense of it, please reach out with any comments or questions. 


//estimated lat lon location of each shepherd server (to 3 decimal places)
//used by the function getLocation to then feed into the function getSats to get above satellites
locationMap = {
    Sydney: { lat: '-33.865', lon: '151.209' },
    'Alice Springs': { lat: '-23.698', lon: '133.880' },
    Beijing: { lat: '39.904', lon: '116.407' },
    Nairobi: { lat: '-1.292', lon: '36.817' },
    Santiago: { lat: '-33.448', lon: '-70.669' },
    'Kalinago Territory': { lat: '15.490', lon: '-61.253' },
    'New York City': { lat: '40.712', lon: '-74.005' },
    Swarthmore: { lat: '39.952', lon: '-75.165' },
    Peterborough: { lat: '44.309', lon: '-78.319' },
  }

// Creates a table based on the number of satellites above the shepherd server at the moment the page is loaded
function createTable(satellites) {
  const table = document.createElement('table');
  table.innerHTML = `
    <thead>
      <tr>
        <th>Name</th>
        <th>Launch Date</th>
        <th>Latitude</th>
        <th>Longitude</th>
        <th>Altitude</th>
        <th id="decay">Estimated Time to Decay</th>
      </tr>
    </thead>
  `;
  //calling the timeToDecay Function on each satellite above host server
  const tbody = document.createElement('tbody');
  satellites.above.forEach((satellite) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${satellite.satname}</td>
      <td>${satellite.launchDate}</td>
      <td>${satellite.satlat}</td>
      <td>${satellite.satlng}</td>
      <td>${satellite.satalt}</td>
      <td id="decay">${timeToDecay(satellite.launchDate)}</td>
    `;
    tbody.appendChild(row);
  });

  table.appendChild(tbody);
  return table;
}

//uses the solar protocol api to get the location (city) of current active server and references the locationMap to get lat and lon.
async function getLocation(){
    const response = await fetch('http://solarprotocol.net/api/v2/opendata.php?systemInfo=city');
    const place = await response.json();
    const city = place.city;
    const location = locationMap[city];
    // console.log(city);
    // console.log(location);
    document.getElementById('place').textContent = `Location: ${city}. Lat: ${location.lat}, Lon: ${location.lon}`;
    return location;
  }

// uses the n2yo above api to get list and launch dates of starlink sats above the host server
//API key is also present in plain text, no login is required to obtain a key, so it is more for rate limiting
//the satellites shown in the api call are based on a 65 degree feild of view from the observer lat lon
async function getSats(){
    const location = await getLocation();
    //temporarily added a CORS proxy in order to make the site entirely front end, will need to change for final install
    const response = await fetch(`https://cors-anywhere.herokuapp.com/https://api.n2yo.com/rest/v1/satellite/above/${getLocation.lat}/${getLocation.lon}/0/65/52/&apiKey=3L6Y8W-2CEDLJ-CKC7EJ-4ZRU`);
    const sats = await response.json();
    console.log(sats);
    return sats;
}

//Create a table and fill with the date supplied from the n2yo call 
async function renderSats() {
    const sats = await getSats();
    const table = createTable(sats)
    document.getElementById('satellites').appendChild(table);
}

//Calculates the remaining time of satellite before re-entry and destruction based on a 5 year life expectancy
function timeToDecay(launchDate){
    const today = new Date();
    const epoch = new Date(launchDate);
    const decay = new Date(epoch.getFullYear() + 5,epoch.getMonth(),epoch.getDate());

    const nowToDecay= decay.getTime()-today.getTime();
    const days = Math.ceil(nowToDecay / (1000*60*60*24));
    const years = Math.floor(days / 365);
    const remaining = days % 365;
    return `${years} years and ${remaining} days.`;
}

//to save on calls the script is only run once and to update you must refresh the page
renderSats()
