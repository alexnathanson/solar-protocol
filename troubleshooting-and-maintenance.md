# Hardware Troubleshooting & Maintenance

## Best Practices

### Siting PV Module
* In the northern hemispher, above 23 degrees latitude, the sun will always be to the south. The ideal orientation for the PV module is facing south and tilted at the angle of latitude. For example, NYC is at 41 degrees north, so an optimal tilt will be at 41 degrees.
* Avoid obstructions that will shade the module particularly between 9am and 3pm.
* Vertical mounting, i.e. a 90 degree tilt, or flat mounting, i.e. 0 degree tilt, will work if need be but will cause decreased efficiency.

### Batteries
* Never mix batteries of different types, sizes, manufactures, or ages/ level of pre-existing use in the same circuit.
* Measure battery voltage with a multimeter prior to connecting it.
	*  A 12V sealed lead acid battery should read be between 12V and 13V. Closer to 12V it is about at 50%, which is the lowest it should be. Closer to 13V it is near 100%. Between 11V and 12V it has been depleted below the recommended depth of discharge. Under 11V it can be considered completely dead - you can use a grid powered battery charger to attempt to revive.
* Sealed lead acid batteries typically last 3-5 years, depending on how it was used and the environment it was in. If the battery is older than 3 years consider replacing it.
* Batteries types all have specific appropriate level of depth of discharge (DoD). This means that it shouldn't be depleted below this threshold. For lead acid batteries, the DoD is 50%.

### Wiring Order
Never have the PV module connected to the charge controller without the battery. It is always a good idea to measure the voltage of all components prior to connecting them.

* To install, connect the battery first, then connect the PV module
* To deinstall, disconnect the PV module first, then the battery
* The charge controller should turn on and function with only the battery connected

### Internet Connectivity

## Problem Identification

### No output
* Check charge controller output settings
* Measure output voltage with multimeter
* Check OCPD

### Unstable output
* Check battery health
* If battery voltage is below 12V, battery is too small for load and/or not enough sun for an extended period of time
	* Solution: Disconnect/turn off load and wait for a sunny day for it to recharge

### Battery doesn't hold charge
* If battery is older than 3 years old, consider replacing battery

## Troubleshooting By Graph

### Battery percentage drops off quickly once PV voltage drops
* Likely old or damaged battery