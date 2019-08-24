# panoptes-timegen

### Setting up the environment 

#### Linux (Tested on Ubuntu 18.04)
Download and extract the github repository. Say its at `/panoptes-timegen-master`. Open a new terminal and navigate to this directory.

If you already have `pip3` and `venv` installed, skip Step 1. 
* Step 1 : In the terminal do: 
  * `sudo add-apt-repository universe`
  * `sudo apt-get install python3-pip python3-venv`
  * `python3 -m venv pan-tg` <br>

Here `pan-tg` refers to the virtual environment where we run the code. Creating a virtual environment is recommended for this project.   
* Step 2 : Now start installing the required python pacakages by activating the virtual environment.
  * source `pan-tg/bin/activate`
  * `pip3 install -r requirements.txt`

That's it. The environment is setup now.

