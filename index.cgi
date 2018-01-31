#!/bin/bash

#Sourcing the settings file, to get variables
source config/settings

#Getting the search term, if there is one
searchterm=${get[s]}


if [ -z "$searchterm" ]; then
    search=false
else
    search=true
fi

#Cutting out the title after the "title: " segment.
function gettitle () {
	head -5 $1 | grep title | cut -d ':' -f 2
}

#Doing the same for the date
function getdate() {
	head -5 $1 | grep date | cut -d ':' -f 2
}

#...and the author
function getauthor() {
	head -5 $1 | grep author | cut -d ':' -f 2
}

#...and the content. This is printing out the contents auf POSTNUMBER.html
function getcontent() {
	htmlfile=$(echo $1 | xargs -L 1 basename | cut -f 1 -d '.').html
	cat $ENCODED/$htmlfile
}

function search() {
    grep -ri $ARTICLES/ -e $1 | eval "awk '//{print \$1}'" | cut -d ":" -f 1 | uniq
}

#Doing that for the webserver, so that he knows the mime type to display
echo -e "Content-type: text/html\\n";


echo -e "<html>

<head>
<meta charset="utf-8"> <title>$BLOGTITLE - Index</title> 
<link rel="stylesheet" type="text/css" href="example.css">
</head>

<body>
<div id="title"><h1><a href="index.cgi">$BLOGTITLE</a></h1></div>"

#If the subtitle option is enabled, we show it.
if [ "$SHOWSUBTITLE" = true ]; then
	echo -e '<div id="subtitle"><p>' $SUBTITLE '</p></div>';
fi

#If the search option is enabled, we show the search form
if [ "$SHOWSEARCH" = true ]; then
    echo -e '<div id="search"><form action="index.cgi?s=" method="GET">
            <input type="text" name="s" placeholder="'$SEARCHTEXT'"/>
            <input type="submit" value="'$SEARCHBUTTONTEXT'">
            </form></div>';
fi
        
echo -e "<div id="wrapper">"

    if [ "$search" = true ]; then
     
        results=$(search $searchterm)
        resultloop=$(echo $results| tr " " "\n")
        
        if [ -z "$results" ]; then
            echo -e "<hr><div id="error">No results for found.";
        else
            echo -e "<hr>"
            while read line;
                do 
                    counter=$((counter+1))
                                
                    if [ "$counter" -ge "$SHOWPOSTS" ]; then
                        echo -e '<a href="/?start=10">Weiter</a>';
                        break
                    else
                        echo -e "<hr>"
                        currentnumber=${line}
                        currentart=${line}
                        rawnumber=$(echo $currentnumber | xargs -L 1 basename | cut -f 1 -d '.')
                        echo -e "<h2><div id="posttitle"><a href="viewarticle.cgi?article=$rawnumber">"; gettitle $currentart;

                        echo -e '</a></div></h2></u>
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
            done < <(echo "$resultloop")
        fi
        


    else
    	for i in $(ls -t $ARTICLES);
		do
			counter=$((counter+1))
                        
			if [ "$counter" -ge "$SHOWPOSTS" ]; then
				echo -e '<a href="/?start=10">Weiter</a>';
				break
			else
                echo -e "<hr>"
                currentnumber=${i%%}
                currentart=$ARTICLES/${i%%}
                rawnumber=$(echo $currentnumber | cut -f 1 -d '.')
                echo -e "<h2><div id="posttitle"><a href="viewarticle.cgi?article=$rawnumber">"; gettitle $currentart;

                echo -e '</a></div></h2></u>
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
    fi
    

echo -e "</div></body>

</html>"
