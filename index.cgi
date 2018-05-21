#!/usr/bin/env bash

#Sourcing the settings file, to get variables
source config/settings

#Getting the search term, if there is one
searchterm=${get[s]}

#If the user entered a search term the search boolean is set either to false or true
if [ -z "$searchterm" ]; then
    search=false
else
    search=true
fi

#Cutting out the title after the "title: " segment.
gettitle() {
	head -5 $1 | grep '^title: ' | cut -d ':' -f 2
}

#Doing the same for the date
getdate() {
	head -5 $1 | grep '^date: ' | cut -d ':' -f 2
}

#...and the author
getauthor() {
	head -5 $1 | grep '^author: ' | cut -d ':' -f 2
}

#...and the content. This is printing out the contents auf POSTNUMBER.html
getcontent() {
	cat "$ENCODED/$1.html"
}

#Main search function using a simple recursive grep
search() {
    grep -ri $ARTICLES/ -e $1 | eval "awk '//{print \$1}'" | cut -d ":" -f 1 | uniq
}

#Doing that for the webserver, so that it knows, which MIME type to display
echo -e 'Content-type: text/html\n'

echo '<!doctype html>

<html>

<head>
<meta charset="utf-8"> <title>'"$BLOGTITLE"' - Index</title>
<link rel="stylesheet" type="text/css" href="styles/'"$STYLESHEET"'">
</head>

<body>
<div id="title"><h1><a href="index.cgi">'"$BLOGTITLE"'</a></h1></div>'

#If the subtitle option is enabled, we show it.
if [ "$SHOWSUBTITLE" = true ]; then
	echo '<div id="subtitle"><p>'"$SUBTITLE"'</p></div>'
fi

#If the search option is enabled, we show the search form
if [ "$SHOWSEARCH" = true ]; then
    echo '<div id="search"><form action="index.cgi?s=" method="GET">
            <input type="text" name="s" placeholder="'"$SEARCHTEXT"'"/>
            <input type="submit" value="'"$SEARCHBUTTONTEXT"'">
            </form></div>'
fi

echo '<div id="wrapper">'

    if [ "$search" = true ]; then

        results=$(search "$searchterm")
        results=($results)

        if [ ${#results[@]} -eq 0 ]; then
            echo '<div id="error">No results for ' $searchterm 'found.<hr>'
        else
            echo '<div class="blogpost">'
            for i in ${results[@]}
                do
                    ((counter++))

                    if [ "$counter" -gt "$SHOWPOSTS" ]; then
                        echo '<a href="/?start=10">Weiter</a>'
                        break
                    else
                        echo '<hr>'
                        rawnumber=${i%%.md}
                        rawnumber=${rawnumber##*/}
                        echo '<h2 class="posttitle"><a href="viewarticle.cgi?article='"$rawnumber"'">'
                        gettitle "$i"
                        echo '</a></h2>'

                        if [ "$SHOWDATE" = true ]; then
                            echo '<div id="postdate">'
                            getdate "$i"
                            echo '</div>'
                        fi

                        if [ "$SHOWAUTHOR" = true ]; then
                            echo '<div id="postauthor"> <br> From '
                            getauthor "$i"
                            echo '</div>'
                        fi

                        getcontent "$rawnumber"
                        echo '<hr></div>'
                    fi
            done
        fi



    else
    	for i in $(ls -t "$ARTICLES");
		do
			((counter++))

			if [ "$counter" -gt "$SHOWPOSTS" ]; then
				echo '<a href="/?start=10">Weiter</a>'
				break
			else
                echo '<div class="blogpost">'
                currentart="$ARTICLES/$i"
                rawnumber=${i%%.md}
                rawnumber=${rawnumber##*/}
                echo '<h2 class="posttitle"><a href="viewarticle.cgi?article='"$rawnumber"'">'
                gettitle "$currentart"

                echo '</a></h2>
                <p>'

                if [ "$SHOWDATE" = true ]; then
                    echo '<div id="postdate">'
                    getdate "$currentart"
                    echo '</div>'
                fi

                if [ "$SHOWAUTHOR" = true ]; then
                    echo '<div id="postauthor"> <br> From '
                    getauthor "$currentart"
                    echo '</div>'
                fi

                getcontent "$rawnumber"
                echo '<hr></div>'
            fi

		done
    fi


echo '</div>'

if [ "$SHOWCREDITS" = true ]; then
	echo '<div id="credits">Made using <a href="https://github.com/flymia/EzBlog">EzBlog</a>.</div>'
fi

echo '</body>

</html>'
