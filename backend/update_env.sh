#!/bin/sh

#to use these environmental variables you must first source the .spenv file

key=$1
val=$2

envFileName="/home/pi/.spenv"

#check that neither argument is empty
if [ $key != "" ] && [ $val != "" ]
then
    #check if file exists
    if [-e $envFileName]
    then
    	#read file
		while read p; do
		  echo "$p"
		done < $envFileName
    	#if the environmental variable doesn't already exist
    	echo "export " $key=$val >> $envFileName
    else
    	#dump variable into new file
	    echo "export " $key=$val >> $envFileName
	fi
else
    echo "Missing key and/or value arguments."
fi


