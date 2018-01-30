#!/bin/bash

source config/settings

for i in $(ls -t $ARTICLES);
	do
		htmlfile=$(echo ${i%%} | cut -f 1 -d '.').html
		currentfile=$ARTICLES/${i%%}
		pandoc $currentfile -o $ENCODED/$htmlfile
	done
