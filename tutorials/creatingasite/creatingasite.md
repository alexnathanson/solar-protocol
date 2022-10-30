#Hosting a Website on Solar Protocol

There are two ways to host a site on Solar Protocol: 

#### 1: On a specific server
If you are a steward of a server, you can host a site on your specific server. This means that your site may be intermittant, where if your server runs out of power or gets disconnected from the internet, your website will go down. 

#### 2: On the Solar Protocol Platform

You can also publish a website on the Solar Protocol platform, even if you aren't stewarding a server. The platform is served from different servers in the network depending on which is generating the most energy at the time. This gives the platform more uptime than if it were hosted on a single server.

## How to request a SP website

## How to upload your site

## Intro to coding a website

Tools needed:

* An editor like [VSCode](https://code.visualstudio.com/)   
* How to set up your workspace in VSCode editor    

## Basics
#### Files

Create a file called index.html. This is the file that will contain the structure and content of your webpage. Create a file and call is style.css. This file will define the style (color, font, size) of the elements on your page.

#### HTML Tags
HTML is a markup language that tells a browser how to structure a webpage. 
HTML is written with tags that look like this: 
`<h1>This is an h1 element, enclosed in opening and closing p tags.</h1>`   
`<p>This is a paragraph element, enclosed in opening and closing p tags.</p>`   

#### HTML Document

HTML pages are defined as is shown below. The `<!DOCTYPE html>` and `<html>` tags tell the browser it is reading at html page. Everything in the head tags is metadata and won't show up on the page. The title element will show up on the tabs in the browser. This is also where to link the css file.

Everything in the body tag will show up on the page itself.

`<!DOCTYPE html>`  
&nbsp;&nbsp;&nbsp;&nbsp;`<html>`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`<head>`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`<title>My new website.</title>`   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`<link rel="stylesheet" href="style.css" />`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`</head>`   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`<body>`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`<p>This is a paragraph element, enclosed in opening and closing p tags.</p>`   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`</body>`   
&nbsp;&nbsp;&nbsp;&nbsp;`</html>`

#### CSS 

CSS stands for cascading style sheet and this a file where the style of the page is defined. This is where you set things like color, fonts and size of elements on the page.

HTML defines the structure and css defines the style. The block of code below, sets the text in the h1 element to be black and the p element to be red.

`h1 { color: black;
}`  
`p {
  color: red;
} `


##### Further tutorials:
* [Dealing with Files](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/Dealing_with_files)
* [HTML Basics](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics)
* [CSS Basics](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/CSS_basics)






