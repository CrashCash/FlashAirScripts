# FlashAirScripts
Python scripts to access a wi-fi enabled Toshiba FlashAir SD card

Toshiba FlashAir cards are SD cards that are accessible over wi-fi.
(This SD card has a wireless access point plus a CPU running a webserver on
Linux. Isn't that amazing?)

This has been tested on Debian Linux with a W-04 version card

I have a Prusa i3 MK3 3D printer that's great, but it prefers to print from an
SD card. This necessitated a lot of physical swapping and frustration with
cheap USB card readers, and remembering to umount the card filesystem before
pulling it out.

I read
https://www.prusaprinters.org/easy-wireless-printing-with-flashair-sd-cards/
and it's an excellent startning point, but I'm a Linux guy, so I had to write
some scripts to talk to it.

It turns out that the webDAV support on this card is rather unreliable and
Linux webDAV clients are poor as well, but it's very good at HTTP
commands. These are documented at
https://www.flashair-developers.com/en/documents/api/

I wrote 3 scripts:

* sdls  - list the contents of the card
* sdput - copy files from local storage to the card

  sdput Nozzle_Cone.gcode LPT_Spool.gcode

* sdrm - delete files from the card

### Setting up the scripts

Copy this scripts to /usr/local/bin and mark them executable (`chmod a+x sdls sdrm sdput`)

Make sure Python 3.x and the requests package are installed through pip,
pipenv, apt-get, rpm or whatever. See
http://docs.python-requests.org/en/master/

You'll need to to change the **ip** variable at the top of each script to
reflect the addess of the card on your network. You can either use the raw IP
address, or you can assign a hostname through your router.

### Setting up the card

Mount your card in your PC. The **CONFIG** configuration file is in the
**SD_WLAN** directory, which are hidden in Windows.

Rename the file to something like CONFIG.BAK.

Copy my version of the file to this directory, and modify these values:

* **APPSSID** and **APPNETWORKKEY** are the name and password of your wireless
  network.  The card only does 2.4GHz, so it won't show up on a 5GHz system.
  It also doesn't tolerate blanks or non-ASCII characters in the network name
  (even though they're legal)

* Copy **CID** and **VERSION** from your old CONFIG file

Unmount the card and remove it from the reader. When you put it back in, it
should appear on the network, and you should see it from your router. Try sdls
to see if it communicates without errors.
