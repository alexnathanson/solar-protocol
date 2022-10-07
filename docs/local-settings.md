# Setting up your local node

## The Admin Console

Congratulations! If you've gotten this far you have installed your solar server. It is powered by solar power, accessible via http and ssh. These are the below steps for personalization and customization.

### Step 1: Change your admin password

This is the password for logging in to the backend of Solar Protocol. This portal will allow you to see system stats and add your own content to SP.

The default steward user names is **admin**. Contact one of the primary leads to receive a temporary password. Once you have logged in, click on your user name to change your password to something of your choosing. 

### Step 2: Add your info

### Step 3: Upload your site

**All URLs must be relative.**

* / will take you back to solarprotocol.net and not your root directory
* # will take you back to your root directory, so for example if you want to link to the midpoint on a the contact page, you would use this: contact.html#midpoint instead of simply #midpoint

File names:
* no spaces
* in some instances (that we are a little stumped by) files with underscore aren't routing properly. It is best to avoid underscores and use a dash or camel case instead
* no other irregular characters besides dashes

### Best practices

* small images
	* 72 dpi
* dithered images (see [power-saving.md](./power-saving.md) for more info)
