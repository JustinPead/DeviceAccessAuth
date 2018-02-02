SOFTWARE
installing raspbian
-download noobs
-insert micro sd card and format 
-extract noobs onto micro sd card
-install on pi with aid of mouse and keyboard

changing ip adress
-reinsert micro sd card in computer (do not format again)
-create ssh file (no extention) in boot drive of micro sd card
-insert sd card back into pi 							auto lo
										iface lo inet loopback
-type: 	sudo nano /etc/network/interfaces 
	
	into terminal and make following changes:

	auto eth0
	iface eth0 inet static
		address "insert ip here"
		netmask 255.255.255.0

	ctrl-x save and exit

(if that doesnt work the original ip is 169.254.162.119)

		
wifi working
-type:	sudo nano /etc/network/interfaces 

	into terminal and make following changes:

	auto wlan0
	iface wlan0 inet manuel
	ctrl-x save and exit

-then type:	sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
 		
		and make following changes:

		network={
        		ssid="eduroam"
        		scan_ssid=0
        		key_mgmt=WPA-EAP
       			pairwise=CCMP TKIP
        		group=CCMP TKIP
        		eap=PEAP
        		identity="01422682@wf.uct.ac.za"
        		password="NICE TRY …"
        		phase2="auth=MSCHAPv2"
			}



Updating everything
-sudo apt-get update 
-sudo apt-get upgrade

Installing modules
-to install modules type pip3 install "module name"
-install pyserial
-type :
    sudo apt-get install freetds-dev
    sudo apt-get install python3-dev
    pip3 install pymssql

Getting uct_info working
-create a log directory on the pi using mkdir command
-then:
import uct_info
uct_info.get_info_from_tag('0312AABBCC')

NB: Requires hex string input!

Returns a dictionary with person's info:
  * 'uct_id' (Staff/Student #)
  * 'title'
  * 'name'
  * 'surname'
  * 'affiliation' (Staff / Student)
  * 'status' (Card status - active or not)

Dependencies(installation mentioned above):

python: python3, pymssql (pip3 install pymssql)
linux: freetds-dev, python3-dev

GOOGLE SHEET INTERACTION

sudo pip install gspread
sudo pip install oauth2client

ADDITIONAL FILES
the client_secret.json.txt file for the google spreadsheet is needed for the google sheet interaction and is not included in the abover code
the uct_info.pyc python compression is needed for gathering the uct data, this is also not included in the above info

HARDWARE

RELAY
-a relay is a device that can be used to switch. 
-just connect the relay's ground and vcc to that of the pi.
-then connect the pin that is communicating with the pi (signal pin on the relay) to the pi. (in this case pin 7)
-use the noramlly open port of the relay.

LEDS (not used in this version)
-google the pinout of a pi in order to find out which pins to connect where.
-look at the location of the pins specified in the above code.
-get three leds and connect in a way so that they are each conrolled by and input signal at the base of a transistor. i.e. connect them to transistors with resistors etc.
-use a 1k resistor at the collector with the led and a 10k at the base input.
-place the signal from the pi at the base of the transistor.
-use the 5V pin of the pi as a power supply for the leds.

MAINS CONNECTION (be careful not to die)
-In the mains there are 3 wires live-brown , earth-green,neutral-blue
-the pi's power adapter is 2 prong and needs to be connected to live and neutral.
-the plug point needs to be connected to the power supply, but at the same its on/off state needs to be controlled by a relay module
-to do this one must connect the neutral and earth wires of both the power supply and the plug point and then connect the live wires of the sully and plug point through a switching relay that is controlled by the above code
-the neutral wire has to be connected to both the power supply of the pi and to the neutral wire of the plug point. Get a big enough terminal block to do this.
-The live wire from the supply needs to be connected directly to the pi's power supply so that it contatntly has power.
-this live wire also has to be connected to be connected to the live wire of the plug point, but the connection has to go through a relay in order for the switching of power to the plug point to be controlled.
-the earth wires of the supply and plug point can just be connected to each other normally.

CONECTING LCD
-the pin connections for the LCD to the pi is as follows (its run in 4-bit mode)
-The pins on the LCD should be labelled, google the pi pinout.
-VSS goes to GND
-VDD goes to 5V
-V0 (contrast) goes to the centre pin of a potentiometer (also connect one of the poteniometer ends to either ground or 5V (doesnt matter which)

-LCD_RS = 37 
-LCD_E  = 35
-LCD_D4 = 40
-LCD_D5 = 38
-LCD_D6 = 36
-LCD_D7 = 32 
-pin A goes to 5V 
-pin K goes to ground

CONECTING BUTTON
-connect on side of the button (google button pinout) to GND and the other to the signal that the pi transmits



