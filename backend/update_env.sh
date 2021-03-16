#!/bin/bash

# only works with bash not sh
#to use these environmental variables you must first source the .spenv file

key=$1
val=$2

envFileName="/home/pi/.spenv"

#check that neither argument is empty
if [ $key != "" ] && [ $val != "" ]
then
    #check if file exists
    if [ -e $envFileName ]
    then
    	echo "File exists. Editing existing file."

		while read l; do
			#check if the line includes the key
			if [[ ! $l == *"export ${key}="* ]]
			then
				echo "$l"
			fi
		done < $envFileName > ${envFileName}.tmp

		echo "export ${key}=${val}" >> ${envFileName}.tmp

		mv ${envFileName}.tmp $envFileName

    else
    	echo "File doesn't exists. Creating new file"
    	#dump variable into new file
	    echo "export ${key}=${val}" >> $envFileName
	fi
else
    echo "Missing key and/or value arguments."
fi


