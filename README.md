# FlashAirScripts
Python scripts to access a wi-fi enabled Toshiba FlashAir SD card

Toshiba FlashAir cards are SD cards that are accessible over wi-fi.

(This SD card has a wireless access point plus a CPU running a web server on
Linux. Isn't that amazing?)

This has been tested on Debian Linux with a W-04 version card. Only W-03 and
W-04 cards are compatible.

I have a Prusa i3 MK3 3D printer that's great, but it prefers to print from an
SD card. This necessitated a lot of physical swapping and frustration with
cheap USB card readers, and remembering to umount the card filesystem before
pulling it out.

It turns out that the webDAV support on this card is rather unreliable and
Linux webDAV clients are poor as well, but it's very good at HTTP
commands. These are documented at
https://www.flashair-developers.com/en/documents/api/

### I wrote 4 scripts:

* **sdls**  - list the contents of the card

```
  % sdls
  Directory: /
  Binder_Spool_Clip_v1-0.gcode        410,730 401.10 KB
  Shim.gcode                          313,291 305.95 KB
  filament_clip.gcode                 702,319 685.86 KB
  ---------------------------- -------------- ---------
  Dir Total:                        1,426,340   1.36 MB
  Used:                             1,638,400   1.56 MB  0.01%
  Free:                        31,992,512,512  29.80 GB 99.99%
```

* **sdput** - copy files from local storage to the card

  `sdput Nozzle_Cone.gcode LPT_Spool.gcode`

  To create a directory, you just specify it, and if it doesn't exist, it will
  be created. You can only do one level at a time.

  `sdput -d gcode LPT_Spool.gcode` creates the "gcode" directory and puts the
  "LPT_Spool.gcode" file in it.

  `sdput -d dir1/dir2 diary.txt` will fail if "dir1" doesn't already exist.

* **sdrm** - delete files/directories from the card

  A directory must be empty before it can be deleted.

  `sdrm "*.gcode"` deletes all files with a "gcode" extension in the current
  directory - note that you have to quote the glob to prevent it from being
  expanded locally by the shell.

  `sdrm Nozzle_Cone.gcode LPT_Spool.gcode` deletes the two given files.

* **sdtree** - display tree of files/directories from the card

```
├─ arm.gcode
├─ body.gcode
├─ dir1
│  ├─ aaa
│  ├─ bbb
│  ├─ dir2
│  │  ├─ dir3
│  │  │  ├─ dir4
│  │  │  │  └─ xxx
│  │  │  ├─ file3
│  │  │  └─ test
│  │  ├─ dirxxx
│  │  ├─ diryyy
│  │  └─ file2
│  └─ file1
├─ head.gcode
├─ leg-1.gcode
├─ leg-2.gcode
└─ robot.gcode
```

### The scripts take optional arguments:

`-a ADDRESS, --address ADDRESS` specifies the address of the card on your
network. You can either use the raw IP address, or you can usually assign a
hostname through your router.

`-d DIRECTORY, --directory DIRECTORY` specifies the working directory.

`-h, --help` displays help.

These are saved to a configuration file (~/.flashair) so you don't have to
retype them constantly. This means you only need to specify the card address
once, and it's remembered. This also means the current working directory
"sticks" across invocations as well.

### Setting up the scripts

Copy these scripts to /usr/local/bin and mark them executable

`chmod a+x sdls sdrm sdput sdtree`

Copy flashair.py to somewhere in sys.path, such as /usr/lib/python3/dist-packages

Make sure Python 3.x and the requests package are installed through pip,
pipenv, apt-get, rpm or whatever. See
http://docs.python-requests.org/en/master/

### Setting up the card

Mount your card in your PC. The **config** configuration file is in the
**sd_wlan** directory.

Rename the file to something like "config.orig". Don't just delete it or
overwrite it, as you'll need to copy the values of several variables from it.

Copy my version of the file to this directory, and modify these values:

* **APPSSID** and **APPNETWORKKEY** are the name and password of your wireless
  network.  The card only does 2.4GHz, so it won't show up on a 5GHz system.
  It tolerates blanks but it doesn't accept non-ASCII characters in the
  network name. Note that APPNETWORKKEY becomes a row of asterisks after the
  first time the card connects successfully to the network.

* Copy the values of **CID** and **VERSION** from your old "config"
  file. Don't screw these up, as you'll have to reinitialize your card with
  the buggy and annoying Toshiba software.

Unmount the card and remove it from the reader. When you put it back in, it
will use the new configuration, so it should appear on the network. You should
see it on your router's list of attached devices. Try "sdls" to see if it
communicates without errors.

### Warning

Do not upload the same filename that is currently being printed, even if the
file itself is identical. The printer will crash.
