## A platform for remote execution of Python code on a Raspberry Pi, to power a Makeblock Orion

## Setup instructions

### On your PC

#### Prerequisites

- Python 3 (on your PC)
- [PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html) (instructions differ for Windows and Linux)

I've personally found more success in using Linux, since installing PyGObject on Windows can be troublesome.

#### Setting up the Raspberry Pi
1. Unzip the files to a folder.
2. Open a command prompt, and issue the following commands:
    - `sudo apt-get install python2`
	- `sudo pip install future`
	- `sudo pip install megapi`
3. Connect the Makeblock Orion via USB to the Raspberry Pi.
4. Create a file named `connect.txt`. Inside this file should be the IP address of your PC.
5. Run `python2 client.py`

#### Use instructions (on your PC)

1. Unzip the files to a folder.
2. Open a command prompt
3. Run `python3 server.py`
4. You will need the IP of your Raspberry Pi. Use the same IP that you use to SSH into the Raspberry Pi.
5. The IP goes into the text bar above.
6. You can write your program in the provided text space. Alternatively, you may open a pre-written script with the "Open file" button.
7. Click "Upload to robot and start" to upload your program to the robot and start the program.
8. To stop the program, click "Stop".

## Available readings
The following readings are available:
- `lf`: The line follower reading. `0` indicates a white reading, `1` a black reading.
- `dist`: The distance sensor reading.

## Available APIs
- `motor.turn_right`
- `motor.turn_left`
- `motor.forward`
- `motor.m1`: Direct acccess to motor M1
- `motor.m2`: Direct acccess to motor M2

## Currently unsupported features
- Additional Python methods