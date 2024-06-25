# LiFePO4 with Epever AN Series

While Epever advertises LiFePO4 battery charging for their AN series charge controllers, it does not automatically detect that battery chemistry and the settings for LiFePO4 when you manually identify the battery type aren't perfect.

If you are using a LiFePO4 battery with the Epever AN series charge controller, you must manually make a number of changes to the settings. Always consult the manufacturer's manual for your specific battery to identify precise settings. The settings below are to be taken as general guidance only.

## EPever Dongle

A wifi or bluetooth dongle is required to connect to the Solar Guardian app.

### Wifi Dongle
The instructions suggest that the wifi password is the 22 digit number located on the box and on the sticker on the dongle itself. That password didn't work for me. If it doesn't work for you try this password, which did work for me. `12345678`

### Bluetooth Dongle

We have not tested the Bluetooth Dongle.

## Minimal Installation Requirements

This is a general approach to setting an Epever charge controller to properly charge a LiFePO4 battery. Refer to your battery manufacturer documentation for precise settings.

1) Battery Control Parameters

If you're OK with the EPever defaults for LiFePO4, set battery type to LiFePO4. This is a generic and imperfect default for this type of battery. I found that you need to set battery rated voltage before this option appears in  the battery type menu.

If you're not OK with the default settings, set battery type to USER and refer to you battery manufacturer's documentation for guidance. These are the settings I used with a Expert Power LiFePO4 battery. Because this charge controller isn't actually suited for LiFePO4, I'm not 100% sure these settings are ideal.

Note that if your settings don't conform to this Epever rule, you'll get an error message: `Over Voltage Disconnect Voltage > Charging Limit Voltage (Absorption) ≥ Equalize Charging Voltage ≥ Boost Charging Voltage ≥ Float Charging Voltage > Boost Voltage Reconnect.`

* Battery Type: User
* Overvoltage Disconnect Voltage: 14.8
* Charging Limit Voltage: 14.4
* Overvoltage Recovery Voltage: 14.4
* Equalization Charging Voltage: 14.4 (We don't actually want an equalization charge but it still needs to be set here. See below.)
* Bulk Charging Voltage: 14.4
* Float Charging Voltage: 13.8
* Bulk Voltage Recovery Voltage: 13.2
* Low Voltage Recovery Voltage: 12.6

2) Battery Parameter Settings
* Set Battery Capacity to your battery capacity
* I set Boost Charge Time to 120. The max charge rate of my battery is .5C, which translates to 120 min. (1C is a fully charge in 60 min)
* Set Equalize Charging Time to 0. This is particularly important because LiFePO4 batteries can be damaged if an equalization charge is applied.
* Set battery temperature limits to your manufacture's spec.