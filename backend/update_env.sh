#!/bin/bash

#to use these environmental variables you must first source the .spenv file

key=$1
val=$2

flag=false

envFileName="/home/pi/.spenv"

#check that neither argument is empty
if [ $key != "" ] && [ $val != "" ]
then
    #check if file exists
    if [ -e $envFileName ]
    then
    	echo "File exists. Editing existing file."
    	#read file
		# while read p; do
		#   echo "$p"
		# done < $envFileName

		while read l; do
			#check if the line includes the key
			if [ $l == *"export $key"* ]
			then
		    	#echo ${l//abc/XYZ}
		    	echo "export " $key=$val 
		    	$flag=true
		    else 
		    	echo "$l"
		done < $envFileName > $envFileName.tmp

		mv /home/pi/$envFileName{.tmp,}

    	#if the environmental variable doesn't already exist in the file
    	if [ $flag == false]
    	then
    		echo "key doesn't already exist"
			echo "export " $key=$val >> $envFileName
		fi

    else
    	echo "File doesn't exists. Creating new file"
    	#dump variable into new file
	    echo "export " $key=$val >> $envFileName
	fi
else
    echo "Missing key and/or value arguments."
fi


