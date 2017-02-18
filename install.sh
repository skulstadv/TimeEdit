#!/bin/bash
# Installs dependencies of TimeEdit.py
if [ "$(id -u)" != "0" ]; then
	echo "Must be run as ROOT"
	exit 1
else
	apt-get -qq update
	apt-get -qqy install python-pip python-dev build-essential xvfb chromium-chromedriver
	pip install selenium pyvirtualdisplay
	printf "\n\nFinishing...\nDo you want to add the script to crontab? [y/n]: "
	read ANSWER
	if [[ "$ANSWER" == "y" ]]; then
		printf "Generating reservation for 15 days ahead in. Will run and book every MON-SAT \n"
		printf "Type username to run job as (can be found HERE@computer:~$): "
		read USERNAME
		printf "Type your feide username: "
		read FUSERNAME
		printf "Type your feide password: "
		read FPASSWORD
		printf "Type room number [A266, A267, A268, A269, A270, A062]: "
		read ROOM
		printf "Reservation start-time in format HH:MM [08:00]: "
		read START
		printf "Reservation end-time in format HH:MM [18:00]: "
		read END
		printf "Are you in timezone GMT+1? Type 'y' for GMT+1 and 'n' for GMT [y/n]: "
		read TIMEZONE
		if [[ "$TIMEZONE" == "y" ]]; then
			TIMEZONE="23"
		else 
			TIMEZONE="22"
		fi
		echo "58 "$TIMEZONE" * * 0-5 "$USERNAME" python $PWD/TimeEdit.py "$FUSERNAME" "$FPASSWORD" "$ROOM" "$START" "$END"" | tee -a /etc/crontab
		printf "Added to crontab.\n"
	fi
	printf "All done.\n"
fi
