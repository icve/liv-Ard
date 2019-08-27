# liv-Ard

[![Build Status](https://travis-ci.org/icve/liv-Ard.svg?branch=master)](https://travis-ci.org/icve/liv-Ard)

Source code that powers the Arduino in my living room.

## What does it do?
* collect room brightness data
* collect human activity data(with infered motion sensor)
* dispay animation / information on 8*8 LED matrix
* display network/server stats on LCD character display
* flash LED to notify events
* Control relay which provide power to a server (repurposed old laptop)
* Collect current sensor information (can compute instantaneous power draw of server)

## Architecture
All the sensors are connected to one Arduino Nano, a python script runs on the computer (Raspberry Pi) and
send commands through usb serial interface to control the Arduino Nano.

This architecture allows code to be written in Python which shortens development time.
At the same time, it allows the Raspberry pi to be swapped out in favorite of a more powerful server/computer.
(As long as the server has USB and can run Python, which is almost all computers)


## Testing and CI
[![Build Status](https://travis-ci.org/icve/liv-Ard.svg?branch=master)](https://travis-ci.org/icve/liv-Ard)

Most python functions has unit tests under hostscripts/test.
This project has travis CI set up to run these test cases.


## Demo


8*8 matrix animation:

![8*8 matrix](https://github.com/icve/liv-Ard/raw/master/docs/gifs/8_8matrix.gif "\\*-*/")

lcd showing server stats:

![lcd](https://github.com/icve/liv-Ard/raw/master/docs/gifs/lcd.gif ">_<")

ntp(Network Time Protocol) enabled digital clock :

![lcd](https://github.com/icve/liv-Ard/raw/master/docs/gifs/digital_clock.gif "_^_")


