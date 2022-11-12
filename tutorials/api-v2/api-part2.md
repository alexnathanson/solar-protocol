# Open API V2 - Part 2

## What can you do with this API???

Now that you know what kinds of data you can retrieve with API and how to interact with it, lets look at some example projects.

The four examples we'll look at below are:
1) making simple API calls
2) making larger API calls and graphing time-series data
3) API Exquisite Corpse

These examples use P5.JS, mostly because its a convienant and accessible way to start making visual things with a common programming language (Javascript).

You can learn more about P5.JS at https://p5js.org/.

### Set up

In order to run the examples, you will need to run a local server on your machine and one of the simplest ways to do this is with Python. Python is generally pre-installed on Macs, but Windows users will need to download it. You will need to use command line/ terminal.

   * To check if you already have Python installed and the version, open terminal and type `python --version`. If its not installed, install python.
   * Navigate to the directory that contains your HTML file.
   		* Different OS and command line interfaces use slightly different syntax. It is easy to find an introduction to command line for your specific OS by searching online. To run the serrver, all you need to know is how to move around the directory structure. The command to change directory used by most, if not all, systems is `cd` + `name of the directory` or `cd ..` to move up in the directory stucture. It may also be useful to list the contents of the directory. `dir` works in windows. `ls` will lists the contents for Mac.
   * Run the below code based on which version of python you are using.
         * Python 3 `python -m http.server`
         * Python 2 `python -m SimpleHTTPServer`
   * If the server is running properly you should see something like this in the terminal Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
   * In a browser, go to http://localhost:8000/

## Example Project 1: Hello Solar Protocol API!

First, lets make a call to the API to retrieve the battery voltage and do something visual with it.

You can find the code for this example in the example1 directory

To do get the battery voltage data, we use this call: `http://solarprotocol.net/api/v2/opendata.php?value=battery-voltage`

This will return an object that looks like this: `{ "battery-voltage": "12.69" }` Of course the number value will be different depending on the status at the moment you make the call.

The data we get comes from the active server. This means that if the server changes, because the sun conditions change, the data will be different. To demonstrate this, we are also going to request the server name from the API.

We'll use this call to get the name: `http://solarprotocol.net/api/v2/opendata.php?systemInfo=name`. 

The response to this call looks like this: `{ name: "Solar-Power for Hackers" }`

In order to display updated data every 5 minutes we'll make both of these API calls again. Everytime it updates or you refresh the page you may see the server name and voltage amount change.

`if(time >= 60*5){`<br>
 `loadJSON('http://solarprotocol.net/api/v2/opendata.php?value=battery-voltage', gotBatData);`<br>
 `loadJSON('http://solarprotocol.net/api/v2/opendata.php?systemInfo=name', gotName);`<br>
`}`<br>

Experiment with changing the type of data you are requesting. For example, if you want PV voltage you should use this API call: `http://solarprotocol.net/api/v2/opendata.php?value=PV-voltage`

<br><br>
![Screenshot of example 1](../images/api-example1.png)
*Screenshot of API tutorial example 1.*
<br><br>

### Trouble shooting example 1

* If you are having trouble getting example 1 to load in a browser, the most likely culprit is the local server.
   * Make sure you are in the tutorials/api/example1 directory when you launch the server. If you are in a different directory you will need to navigate to the correct directory.
   * Also, make sure you are going to the correct port.
* Use the console in the browser's development tools to view error messages.
* If the example is running but isn't retrieving data, confirm http://solarprotocol.net is online by opening up the main page in a web browser. You can also try make a get request directly in the browser to confirm the system is running by going to this URL: http://solarprotocol.net/api/v2/opendata.php?value=battery-voltage

## Example Project 2: Data Viz

Now that you know how to make API calls, lets request a more significant amount of time-series data and graph it.

For this example, we are making 1 API call which will return the 3 most recent calendar days worth of data. This means it will return all the data from today, yesterday, and the day before. Note that this corresponds to the server's local time, which is not necessarily your time (unless you happen to be in the same time zone as the server that is responding to you.)

The call to get this data is `http://solarprotocol.net/api/v2/opendata.php?day=3`

When the script is run, the API call and some styling commands are made in the setup function. Immediately after that the axis for the graph are drawn.

Once the API returns a response, that data sent to the `gotData()` function. Our API call will return an object with 3 elements: the timezone for the server and 2 arrays containing the headers and the actual data we want to display, respectively. The `gotData()` function parses the data and puts it in the format we want to visualize it. Then it is passed on to the `drawData()` function which scales the data to fit our canvas and draws it to the screen. It also uses the header array to draw labels.


## Example Project 3: API Exquisite Corpse

This project uses the Solar Protocol network activity to manipulate an image and create an emergent/collaborative illustration, in a similar way as the game Exquisite Corpse. Exquisite Corpse is collaborative drawing game that was popular with surrealist artists in the 1920s. The rules of the game are that each person is to add to a drawing without seeing any of the previous work. One person starts a drawing and then folds the paper over so only the bottom edge of the drawing is visible. The next person continues the illustration starting from the small bit that is visible from the previous person's work. This continues until the paper is full. The result is often a silly grotesque creation.

In our version, we'll be making an emergent collage. Every time the active server changes, the illustration will be ammended with an image relating to the location of the new server. To do this, we'll be using the MET Museums Art Collection API. Their API is nice for this because its completely open access and doesn't require you to register. You don't necessarily need to dig in to their API documentation, but if you're curious about how it works and want to remix this example you can find their docs at https://metmuseum.github.io/.

However, the MET doesn't enable CORS on their server, which means we need to use a proxy server to be able to retrieve the images. 

### Python Proxy Server with Flask

install pip
install flask: `pip install flask`
install flask_cors: `pip install flask_cors`

navigate to the `example3` directory and start the server with this code:`flask --app simpleFlaskProxy run`

### Javascript

Note that you still need to spin up a normal Python server, like you did for the other 2 examples for this to work.

We will do this by calling the location of the server with this command: `http://solarprotocol.net/api/v2/opendata.php?systemInfo=location`

We then compare the location to the previous location. If the location hasn't changed, we distort the existing data. If it has changed, we add a new image.

<br><br>
![Screenshot of example 3](../images/api-example3.png)
*Screenshot of API tutorial example 3.*
<br><br>

<!-- ## Example Project 4: Drawing Machine -->
