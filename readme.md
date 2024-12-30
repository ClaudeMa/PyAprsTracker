***PyAPRSTraccker*** is an experimental APRS tracker.

The tracker uses either a TNC modem in KISS mode or a KISS TCP connection (Direwolf, Soundmodem, etc.).

**Installation**

Install the python3-venv and pip modules for your distribution, e.g. Debian and derivatives.

sudo apt install python3.venv python3-pip

In the sources folder, create a virtual environment.

python -m venv .venv

**Activate the virtual environment**

source .venv/bin/activate

**Install the required modules**

pip install -r requirements.txt

**Program settings**

Edit the config.py file. Enter your callsign and the TNC connection parameters.
Modify the GPS parameters

**Running the programme**

python aprstracker.py


