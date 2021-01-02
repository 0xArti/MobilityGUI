# Mobility with GUI
## The Goal
<h3 style="color:darkred">The Problem</h3>

While working you may not notice that you're sitting for too long without moving,
and you've spent hours in uncomfortable position, damaging you spinal health in the long term.
As for myself, if I wouldn't do any exercises for two weeks, I will start to suffer from pain and soreness in my neck and shoulders.


<h3 style="color:green">The Solution</h3>

A program that runs in the background and triggers a popup each 20 minutes (by default).\
The popup contains suggested exercises for you. And you should be honest and to them right away and don't cheat. If so, press the "Done" button.\
But, if you're in a meeting or can't do the exercises, you can click the "Ignore" button and save them for the next time (Windows only).
<br/><br/>

## Installation
Clone the git repository and install in _virtual environment_  
`pip install .`  
or for development  
`pip install -e .`   

You can test it by running `mobility` in your console.\
If you see a popup in the top-left side of the screen with exercises, then everything is correct.
<br/><br/> 


### Windows
Add environment variable which will point the to mobility package path.\
Create shortcut for `windows-mobility-auto.bat` and move it to your _Startup Folder_.\
The script launches VBS file and another BATCH file.\
  The VBS makes sure that the seconds BATCH runs invisible,\
  this way the user doesn't see the service and (can close from TaskMgr, etc...).\

Run the service.

Failed to run the service?\
Try:
* The service uses Win32 API (using pywin32)
    Make sure that:\
        you have `pythoncom38.dll` and `pywintypes38.dll` at
        `<python_path>\Lib\site-packages\win32` ,\
        `<python_path>\Lib\site-packages\win32\lib`
<br/><br/> 

### Linux
install:
    `sudo apt-get install python-tk gnome-screensaver`

create variable `MOBILITY_PATH` which should lead to the mobility package directory
 and set a crontab to run the script at interval (20 minutes by default)
```bash
crontab -e
# Add at the top of the file
export MOBILITY_PATH=<path_to_mobility_package>

# Add at the end of file
*/20 * * * * $MOBILITY_PATH/scripts/linux/linux-mobility.sh
```

If you encounter problems with running the mobility package in linux
you can save logs to a desiring file by adding `<path_to_log_file> 2>&1`

One drawback with the mobility package in linux is that it can't save the state of the exercises.
Unlike windows which runs the service in the background.

## Configuration
All the configuration is dynamically loaded,
so don't add / remove keys from it, it can make the code not run.

### Exercises
The exercises configuration consist from three elements:\
  Must:\
   set of exercises that it is your goal to complete each day.\
  Bonus:\
   set of exercises that it would be nice to complete.\
  Advanced:\
   set of exercises that used for certain goal (other day stay mobilized).\
   For example, to retain strength or increase flexibility.\
   By default (at least in windows), you will first finished the `must` exercises
and then move to the `bonus` exercises.

Exercises Metadata
* Each instance is adding one exercise by default. It could be change by increase 
  the `call` value.
* The `advanced` exercises are additional exercises that may summon randomly (10% by default).\
  but if you don't need the advanced exercises you could switch them off 
  by setting `advanced_enabled` to False.

Feel free to change, add or remove exercises to match your body.
Right now there are up to 80 non-advanced exercises!

### GUI
The GUI configuration is pretty solid,
If you change values, you should be familiar with the library PySimpleGUI.\
Either way, you should not change const configuration
(you will need to change the code source as well)

 ![plot](./assets/example_gui.png)
<br/><br/> 

## TODO
 * Add more types of exercises
 * Add more exercises
 * Add detailed exercises documentation 
 * Add dynamic configuration logic for delivering exercises,\
    * Creating template for some logics.       
