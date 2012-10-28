#!/bin/bash

THEME_DIR=./theme/*
DIR=$1

shift

for THEME in $THEME_DIR
do

	for ARG in $*
	do
		PATH=$THEME/image/$DIR
		if [ ! -d $PATH ]; then
			/bin/mkdir $PATH	
		fi
		/bin/cp $ARG $THEME/image/$DIR
	done

done
