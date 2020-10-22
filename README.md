# Rattlesnake

Rattlesnake is a program designed to create an alarm when an object is within a specific proximity.
It will produce a different pitch depending on the distance.


The system was designed for a sentor which would:
Input a distance from 0-10 meters, for a 10m input the tone will be low, 500Hz, for a
distance of 0 the tone will be 2.5kHz.

## Usage
To setup for the standard conditions you must first set up the preferences on the command line,
```console
python3 cli.py
  --min-distance 0
  --max-distance 10
  --min-frequency 500
  --max-frequency 2.5kHz
```
During runtime, use these commands to adjust the output
```console
    on : Plays the tone
    off: Stops the tone
    f# : The frequency
    d# : The distance from the sensor
    v# : The volume (0 - 9)

    0  : exit (or ^c)
```
