# panoptes-timegen

### Setting up the environment 

#### Windows (Tested on Windows 10)
Download and extract the github repository. Say its at `\panoptes-timegen-master`. Open a new CMD window as administrator and do the following:

Make sure you already have python 3 installed and accessible from the command line as `python`.

* Step 1 : 
  * In the shell, run `pip3 install venv`
  * `python -m venv pan-tg`
This results in a new python virtual environment named `pan-tg` at `\panoptes-timegen-master\pan-tg`

* Step 2:
  * Activate the virtual environment by running the shell command: `pan-tg\Scripts\activate` from the `panoptes-timegen-master` directory.
  * Install the required python packages by running `pip3 install -r requirements.txt` 
  
#### Linux (Tested on Ubuntu 18.04)
Download and extract the github repository. Say its at `/panoptes-timegen-master`. Open a new terminal and navigate to this directory.

If you already have `pip3` and `venv` installed, skip Step 1. 
* Step 1 : In the terminal do: 
  * `sudo add-apt-repository universe`
  * `sudo apt-get install python3-pip python3-venv`
 
 
* Step 2 : Now start installing the required python pacakages by activating the virtual environment.
  * `python3 -m venv pan-tg` <br>
  * source `pan-tg/bin/activate`
  * `pip3 install -r requirements.txt`

Here `pan-tg` refers to the virtual environment where we run the code. Creating a virtual environment is recommended for this project.

That's it. The environment is setup now.

