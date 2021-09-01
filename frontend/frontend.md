# Frontend

These files include:
* website styling (css) and content (html) that get served to site visitors
* admin console pages
* PHP api
* files for managing URL redirection 

## Admin

These pages needs some serious refactoring!!! (login to the admin console is managed by the files in backend/protect)


* index.php shows the most recent charge controller data for each device and displays the point of entry history. Currently, this is the 'network activity' page on the nav bar, but in the future there should be a different page for network activity with network stats and this page should probably be renamed 'solar activity' or something
* local.php shows graphs of charge controller data for the local device and displays the raw charge controller data in a table.
* settings/index.php allows the user to set local variables and network access passwords (these are the passwords for DNS & API calls)
* settings/local.php allows the user to upload and delete content for their personal page. This content is uploaded to the local/www directly outside of the solar protocol directory.
* settings/upload.php manages uploading the local content.
* user.php allows the user to changes their password. (this should maybe be moved to the backend/protect directly so all the admin password stuff is together)

## API

* api.php handles POST requests for sensitive/secure actions (predominantly servers on the network passing data back and forth to one another)
* chargecontroller.php handles GET requests for non-sensitive data that is open to the public
* index.html provides API documentation and an interface for exploring the publically available data. It can be found at <a href="http://solarprotocol.net/api/v1">http://solarprotocol.net/api/v1</a>
* chargeControllerExplorer.js makes the API calls from index.html. This API explorer is meant to demonstrate API calls, which is why it runs on JS.
* the contents of the sandbox directly have some examples of PHP password functions. These are not used for anything other than generating and testing new password. They operate completely independently from the rest of the project and are not needed for the project to run.

## Images

Contains images used in the site

## Redirect & .htaccess

These files route requests for files from the steward's personal site. It enables file distribution and clean/consistant URLs regardless of which server is the POE.

## HTML & CSS pages

These are the style and content pages that make up the solarprotocol.net website. These pages are updated periodically by the static site generator backend/createHTML/create_html.py 