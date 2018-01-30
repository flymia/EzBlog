#!/bin/bash

source config/settings

function gettitle () {
	echo $(cut -d ":" -f 2 <<< $(cat $1) | head -2 | awk 'NR!~/^(1)$/')
}

function getdate() {
	cut -d ":" -f 2 <<< $(cat $1) | head -3 | awk 'NR!~/^(1)$/' | tail -n +2
}

function getauthor() {
	cut -d ":" -f 2 <<< $(cat $1) | head -4 | awk 'NR!~/^(1)$/' | tail -n +3
}

function getcontent() {
	htmlfile=$(echo $1 | cut -f 1 -d '.').html
	cat $ENCODED/$htmlfile
}

echo -e "Content-type: text/html\\n";

echo -e "<html>

<head>
<meta charset="utf-8">  
</head>

<body>
<h1>Testblog</h1>"

	for i in $(ls -t $ARTICLES);
		do
			counter=$((counter+1))
			echo -e "<hr>"
			currentnumber=${i%%}
			currentart=$ARTICLES/${i%%}
			echo -e "<h2><u>"; gettitle $currentart;
			echo -e '</h2></u>
			<p>'
			getdate $currentart
			
			echo -e '</p>'			
			getcontent $currentnumber
			echo -e "<hr>"	
		done
echo -e "</body>

</html>"
