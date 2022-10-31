# Open API V2 - Part 1

The Solar Protocol open API V2 is intended to allow anyone to get data from the network for educational, research, or artistic purposes.

It is a public, free, keyless service that enables GET requests for various pieces of data about specific servers and network activity.

### What is an API?

API stands for application protocol interface. It is a protocol that facilitates transferring data between pieces of software.

### Our API V2

The structure of our API is relatively simple, but because it can provide a lot of different types of data in different formats and because of the complex environmentally dependent nature of the Solar Protocol project it can seem overwhelming.

Our public API V2 only responds to GET requests at this endpoint: http://solarprotocol.net/api/v2/opendata.php. To get specific types of data, URI parameters are used.

### Support

Solar Protocol is in a constant state of evolution and development. We are a very small team of volunteers with sporadic grant funding and limited capacity for tech support, but we do our best to answer questions. Currently, the best way to have questions answered is by submitting a issue on Github. We also teach workshops on Solar Protocol in person and remotely.

## Exploring the API

Open the Solar Protocol API V2 explorer in a browser of your choosing.

http://solarprotocol.net/api/v2/

The structure of this tutorial mirrors the API explorer. Feel free to just use the form fields built in to the explorer or use the example API calls with any tool or language of your choosing, such as cURL, Javascript, python, etc.

If using the explorer, the results of the call will be displayed in the browser console. The console can be opened via the browser's developer settings or by pression the Fn and F12 keys simultaniously (works on most browsers).

Both the API responses and the API explorer page are served from whichever server in the Solar Protocol network is currently the active server. The active server changes as the available sunlight in a given location changes. (To learn more about what the active server is, check out the 'How It Works' tutorial.) [link needed] The data returned from the API pertains to the active server only. This means that if you make 2 identical API calls you could get different results if the server has changed between calls. This is an important thing to keep in mind for future trouble shooting. Calls to other servers in the system are possible and are explained below.

Note: In older versions of this project the terms "primary server" or "point of entry (POE)" were used interchangably with "active server" and you may still come across that older terminology in some documentation.)

The kinds of API data available are characterized by 4 types, charge controller data, system info, network info, and remote server data. We'll go through all 4 types; starting with the smallest piece of Solar Protocol, the individual server, and expanding out to the entire network.

### Charge Controller Data

Charge controller data is the electrical data that the solar power system's charge controller provides. The charge controller ensures that the battery is safely charged. The specific charge controller we use has a protocol that allows the server to communicate with it.

This data covers solar production, battery status, and electrical load info. When this data is archived all of the follow values are stored as 1 line in a CSV file by day.

* PV-current
* PV-power-H
* PV-power-L
* PV-voltage
* battery-percentage
* battery-voltage
* charge-current
* charge-power-H
* charge-power-L
* load-current
* load-power
* load-voltage
* datetime

#### Value

We can call for an individual <strong>value</strong>, which returns only 1 value from the most recent charge controller data. The value call also allows us to get the scaled-wattage of the PV module (note that this value isn't available in line or day calls, only value calls)

<strong>Let's make our first API call!</strong>

We're going to request the PV voltage from the API. This request is structured like this: http://solarprotocol.net/api/v2/opendata.php?value=PV-voltage

#### Value & Duration

This will give you these same individual pieces of data over a particular length of time. This is made available to minimize parsing that is required if you request an entire day of data for example.

A durational value request is structured like this: http://solarprotocol.net/api/v2/opendata.php?value=PV-voltage&duration=2

#### Line

Each line contains all the possible values for a particular time. Lines are only available for the current calendar day. Remember, these calls are coming from the active server, so the calendar day refers to the local time for that server. If you are not sure what the local server date is, see the system API calls below.

The amount of lines that are available depends on how many times the server has collected data that day. To find out you can use the 'len' value, like this:

http://solarprotocol.net/api/v2/opendata.php?line=len

Using a integer value will return that particular line.
http://solarprotocol.net/api/v2/opendata.php?line=10

#### Day

Day returns an entire calendar day's worth of lines i.e. all the data collected on a particular date.

You can pass it an integer from 1 to 7. This will return X number of days of past day. So 1 returns the most recent day of data, 2 returns the most recent 2 days of data, etc.

List returns a list of all the available files. Each file represents 1 day of data.

Example: http://solarprotocol.net/api/v2/chargecontroller.php?day=list

Len returns a count of all available files. Each file represents 1 day of data.

Example: http://solarprotocol.net/api/v2/chargecontroller.php?day=len

You can also request a specific date by passing the name of the file without the file type suffix. 

Example: http://solarprotocol.net/api/v2/chargecontroller.php?day=tracerData2020-05-17


### System Info

System info provides details about the active server, such as location and hardware specs.

Here's an example call: http://solarprotocol.net/api/v2/opendata.php?systemInfo=tz

These are the possible values you can request:

    tz - returns the timezone for the server
    color - returns the color that was set by the steward
    description - returns the description of the server that was set by the steward
    name - returns the name for the server
    location - returns the location
    city - returns the city the server is located in
    country - returns the country the server is located in
    wattage-scaler -returns the scaler value based on a standard of a 50 watt module
    pvWatts -returns the wattage of the module
    pvVoltage - returns the voltage of the module
    dump - returns a dictionary containing all of the above system info


### Network Info

Network info returns information other servers on the network and some network activity.

Example: http://solarprotocol.net/api/v2/opendata.php?networkInfo=devices

Possible values:

deviceList - returns a list of the names of servers
tz - returns a list of the timezones of each server. This is the prefered way to get all the timezones (rather than making a tz call via the server argument)
poe - returns the list of point of entry time stamps by server. note that these time stamps are in the local time of their server and haven't been adjusted.
timestamp - returns the time stamp from when the devices most recently posted their data. Note that this time stamp is in Unix time - seconds since epoch (1/1/1970) in UTC regardless of the server's timezone.
dump - returns an array containing all network info values

### Remote Server Data

As mentioned at the beginning of this tutorial, API responses are queried from the active server. This means the results may change if the light conditions change. However, by using the server argument you can collect data from a specific server or from all the servers in the network by name

Note that all times are in the timezone for the server that logged that data and have not been adjusted. Use the networkInfo = tz call to get the time zones to make the adjustments.

Example: http://solarprotocol.net/api/v2/opendata.php?server=1

Possible values:

    all - returns the specified value for all servers
    an integer - the integer corresponds to the order of servers returned from the device list query. The call returns the specified value for the specified server
    server name without spaces - the name of the server (as listed in the deviceList query) with spaces removed. The call returns the specified value for the specified server. This is not case sensitive.
    If 'err' is returned it indicates a failed response, likely because the remote data for that server isn't stored locally. 

<!-- # V3

/api/docs -->