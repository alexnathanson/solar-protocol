# troubleshooting

## troubleshooting python - manual install

		pip install requests
		pip install pymodbus
		pip install pandas # (this should be refactored to not used pandas)  
		pip install numpy
		pip install jinja2
		pip install --upgrade Pillow
		sudo apt-get install libcairo2-dev
		pip install gizeh
		pip install webcolors

## troubleshooting numpy - reinstall

		sudo pip3 uninstall numpy
		sudo apt-get remove python3-numpy
		sudo pip3 install numpy
		sudo apt-get install libatlas-base-dev

## troubleshooting PIL

		sudo apt install libtiff5
		sudo apt-get install libopenjp2-7 # (unconfirmed)

## troubleshoot pymodbus - reinstall

		pip uninstall serial
		sudo pip uninstall serial
		pip uninstall pyserial
		sudo pip install pyserial
