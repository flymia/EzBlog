#!/bin/bash

#Sourcing the settings file, to get variables
source config/settings

#Cutting out the title after the "title: " segment.
function gettitle () {
	echo $(cut -d ":" -f 2 <<< $(cat $1) | head -2 | awk 'NR!~/^(1)$/')
}

#Doing the same for the date
function getdate() {
	cut -d ":" -f 2 <<< $(cat $1) | head -3 | awk 'NR!~/^(1)$/' | tail -n +2
}

#...and the author
function getauthor() {
	cut -d ":" -f 2 <<< $(cat $1) | head -4 | awk 'NR!~/^(1)$/' | tail -n +3
}

#...and the content. This is printing out the contents auf POSTNUMBER.html
function getcontent() {
	htmlfile=$(echo $1 | cut -f 1 -d '.').html
	cat $ENCODED/$htmlfile
}

function search() {
    grep -r $ARTICLES/ -e '$1' | awk '{print $1}' | cut -d ":" -f 1 | uniq
}

#Doing that for the webserver, so that he knows the mime type to display
echo -e "Content-type: text/html\\n";


echo -e "<html>

<head>
<meta charset="utf-8"> <title>$BLOGTITLE - Index</title> 
<link rel="stylesheet" type="text/css" href="example.css">
</head>

<body>
<div id="title"><h1>$BLOGTITLE</h1></div>"

if [ "$SHOWSUBTITLE" = true ]; then
	echo -e '<div id="subtitle"><p>' $SUBTITLE '</p></div>';
fi

echo -e "<div id="wrapper">"

	for i in $(ls -t $ARTICLES);
		do
			counter=$((counter+1))
                        
			if [ "$counter" -ge "$SHOWPOSTS" ]; then
				echo -e '<a href="?=further">Weiter</a>';
				break
			else
                echo -e "<hr>"
                currentnumber=${i%%}
                currentart=$ARTICLES/${i%%}
                echo -e '<h2><div id="posttitle">'; gettitle $currentart;
                echo -e '</div></h2></u>
                <p>'
                
                if [ "$SHOWDATE" = true ]; then
                    echo -e '<div id="postdate">'
                    getdate $currentart
                    echo -e '</div>'
                fi
                
                if [ "$SHOWAUTHOR" = true ]; then
                    echo -e '<div id="postauthor"> <br /> From '
                    getauthor $currentart
                    echo -e '</div>';
                fi
                
                
                echo -e '</p>'			
                getcontent $currentnumber
                echo -e "<hr>"	
            fi

		done
echo -e "</div></body>

</html>"
