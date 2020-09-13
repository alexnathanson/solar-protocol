# Troubleshooting & Maintenance

## Best Practices

### Battery health
Measure battery voltage with a multimeter prior to connecting it.
*  A 12V sealed lead acid Battery should read be between 12V and 13V. Closer to 12V it is about at 50%, which is the lowest it should be. Closer to 13V it is near 100%. Between 11V and 12V it has been depleted below the recommended depth of discharge. Under 11V it can be considered completely dead - you can use a grid powered battery charger to attempt to revive.

### Wiring order
Never have the PV module connected to the charge controller without the battery. It is always a good idea to measure the voltage of all components prior to connecting them.

* To install, connect the battery first, then connect the PV module
* To deinstall, disconnect the PV module first, then the battery
* The charge controller should turn on and function with only the battery connected

## Problem Identification

### No output or unstable output

<p>
No output

* Check charge controller output settings
* Check OCPD
* Measure output voltage with multimeter
</p>
<p>
Unstable output
* Check battery health
* If battery voltage is below 12V, battery is too small for load and/or not enough sun for an extended period of time
	* Solution: Disconnect load and wait for a sunny day for it to recharge
</p>

## Troubleshooting by graph