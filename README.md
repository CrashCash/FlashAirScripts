# FlashAirScripts
Python scripts to access a wi-fi enabled Toshiba FlashAir SD card

Toshiba FlashAir cards are SD cards that are accessible over wi-fi.

(This SD card has a wireless access point plus a CPU running a web server on
Linux. Isn't that amazing?)

This has been tested on Debian Linux with a W-04 version card

I have a Prusa i3 MK3 3D printer that's great, but it prefers to print from an
SD card. This necessitated a lot of physical swapping and frustration with
cheap USB card readers, and remembering to umount the card filesystem before
pulling it out.

I read
https://www.prusaprinters.org/easy-wireless-printing-with-flashair-sd-cards/
and it's an excellent starting point, but I'm a Linux guy, so I had to write
some scripts to talk to it.

It turns out that the webDAV support on this card is rather unreliable and
Linux webDAV clients are poor as well, but it's very good at HTTP
commands. These are documented at
https://www.flashair-developers.com/en/documents/api/

I wrote 3 scripts:

* **sdls**  - list the contents of the card

```
  % sdls
  Low_Pressure_Shaft_Aft_Rev_A.gcode           10,887,796
  Low_Pressure_Shaft_Connector_Rev_A.gcode        405,270
  Low_Pressure_Shaft_Front_Rev_A.gcode          9,462,366
  Nozzle_Cone.gcode                             9,946,598
  Nozzle_No_Supports.gcode                     31,395,785
  Stand.gcode                                  11,298,604
  ---------------------------------------- --------------
  Total In Use:                                73,396,419
  Remaining Space:                         31,920,488,448
  Free:                                            99.77%
```

* **sdput** - copy files from local storage to the card

  `sdput Nozzle_Cone.gcode LPT_Spool.gcode`

* **sdrm** - delete files from the card

  `sdrm` deletes all files

  `sdrm "*.gcode"` deletes all files with a "gcode" extension - note that you
  have to quote the glob to prevent it from being expanded locally by the
  shell

  `sdput Nozzle_Cone.gcode LPT_Spool.gcode` deletes the two given files

### Setting up the scripts

Copy this scripts to /usr/local/bin and mark them executable (`chmod a+x sdls sdrm sdput`)

Make sure Python 3.x and the requests package are installed through pip,
pipenv, apt-get, rpm or whatever. See
http://docs.python-requests.org/en/master/

You'll need to to change the **ip** variable at the top of each script to
reflect the address of the card on your network. You can either use the raw IP
address, or you can assign a hostname through your router.

### Setting up the card

Mount your card in your PC. The **config** configuration file is in the
**sd_wlan** directory.

Rename the file to something like "config.orig". Don't just delete it or
overwrite it, as you'll need to copy the values of several variables from it.

Copy my version of the file to this directory, and modify these values:

* **APPSSID** and **APPNETWORKKEY** are the name and password of your wireless
  network.  The card only does 2.4GHz, so it won't show up on a 5GHz system.
  It also doesn't tolerate blanks or non-ASCII characters in the network
  name. Note that APPNETWORKKEY becomes a row of asterisks after the first
  time the card connects successfully to the network.

* Copy the values of **CID** and **VERSION** from your old "config" file

Unmount the card and remove it from the reader. When you put it back in, it
should appear on the network, and you should see it from your router. Try
"sdls" to see if it communicates without errors.
