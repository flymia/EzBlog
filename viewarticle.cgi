#!/usr/bin/env bash

#Sourcing the settings file, to get variables
source config/settings

toview=${get[article]}

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
	htmlfile=$(echo $1 | cut -f 1 -d '.').html
	cat $ENCODED/$htmlfile
}

function search() {
    grep -ri $ARTICLES/ -e '$1' | awk '{print $1}' | cut -d ":" -f 1 | uniq
}

#Doing that for the webserver, so that he knows the mime type to display
echo -e "Content-type: text/html\\n";

echo "<html>

<head>
<meta charset="utf-8"> <title>$BLOGTITLE - Viewing article</title>
<link rel="stylesheet" type="text/css" href="styles/$STYLESHEET">
</head>

<body>
<div id="title"><h1><a href="index.cgi">$BLOGTITLE</a></h1></div>"

if [ "$SHOWSUBTITLE" = true ]; then
	echo '<div id="subtitle"><p>' $SUBTITLE '</p></div>';
fi

#If the search option is enabled, we show the search form
if [ "$SHOWSEARCH" = true ]; then
    echo '<div id="search"><form action="index.cgi?s=" method="GET">
            <input type="text" name="s" placeholder="'$SEARCHTEXT'"/>
            <input type="submit" value="'$SEARCHBUTTONTEXT'">
            </form></div>';
fi

echo "<div id="wrapper">"
                echo '<div class="blogpost">'
                currentnumber=$toview
                currentart=$ARTICLES/$toview.md

                echo '<h2>'; gettitle $currentart;
                echo '</div></h2></u>
                <p>'

                if [ "$SHOWDATE" = true ]; then
                    echo '<div id="postdate">'
                    getdate $currentart
                    echo '</div>'
                fi

                if [ "$SHOWAUTHOR" = true ]; then
                    echo '<div id="postauthor"> <br /> From '
                    getauthor $currentart
                    echo '</div>';
                fi


                echo '</p>'
                getcontent $currentnumber
                echo '<hr></div>'
echo "</div>"

if [ "$SHOWCREDITS" = true ]; then
        echo '<div id="credits">Made using <a href="https://github.com/flymia/EzBlog">EzBlog</a>.</div>'
fi

echo '</body>

</html>'
