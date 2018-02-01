#!/bin/bash

source config/settings


#THE LIVE COMPILE FUNCTION IS NOT READY YET! BUGGY!
case "$1" in 
  "--live")
        inotifywait -m $ARTICLES/ -e create -e moved_to -e moved_from -e delete |
            while read path action file; do
                echo "The file '$file' changed! Taking actions..."             
                
                if [ ! -f $file ]; then
                    echo "Deleted an article! Deleting html file..."
                    htmlfile=$(echo $file | cut -f 1 -d '.').html
                    
                    rm $ENCODED/$htmlfile
                    
                    break
                else
                    echo "File $file was added. Compiling..."
                
                    htmlfile=$(echo $file | cut -f 1 -d '.').html
                    currentfile=$ARTICLES/$file
                    pandoc $currentfile -o $ENCODED/$htmlfile  
                fi
                
                echo "Completed! Watching ..."
                echo
            done
    ;;
  "--recompile")
        echo "Recompiling every article!"
        
        rm -rf $ENCODED/*
        
        for i in $(ls -t $ARTICLES);
            do
                htmlfile=$(echo ${i%%} | cut -f 1 -d '.').html
                currentfile=$ARTICLES/${i%%}
                pandoc $currentfile -o $ENCODED/$htmlfile
        done
        echo "Okay, done!"
    ;;
  *)
        for i in $(ls -t $ARTICLES);
            do
                htmlfile=$(echo ${i%%} | cut -f 1 -d '.').html
                currentfile=$ARTICLES/${i%%}
                pandoc $currentfile -o $ENCODED/$htmlfile
        done
    ;;
esac

if [[ "$RSS" == true ]] && [ "$RSSFILE" ]; then
	blogurl="http$([[ "$HTTPSENABLED" == true ]] && echo -n s)://$VHOST/"
	
	echo '<?xml version="1.0" encoding="UTF-8"?>' > "$RSSFILE"
	
	echo '
		<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
		
		<channel>
			<title>'"$BLOGTITLE"'</title>
			<link>'"$blogurl"'</link>
			<lastBuildDate>'"$(date -R)"'</lastBuildDate>
			<atom:link href="'"${blogurl}$RSSFILE"'" rel="self" type="application/rss+xml" />
	' >> "$RSSFILE"
	
	if [[ "$SHOWSUBTITLE" == true ]] && [ "$SUBTITLE" ]; then
		echo "<description>$SUBTITLE</description>" >> "$RSSFILE"
	fi
	
	[[ "$SHOWCREDITS" == true ]] && echo '<generator>EzBlog</generator>' >> "$RSSFILE"
	
	ls -1t "$ARTICLES" | head -"$SHOWRSSPOSTS" | while read i; do
		mdhead="$(head -5 "$ARTICLES/$i")"
		rawnumber="${i%%.md}"
		
		echo '<item>' >> "$RSSFILE"
		echo "<title>$(grep '^title: ' <<< "$mdhead" | cut -d: -f2)</title>" >> "$RSSFILE"
		echo "<link>${blogurl}viewarticle.cgi?article=$rawnumber</link>" >> "$RSSFILE"
		echo "<guid>${blogurl}viewarticle.cgi?article=$rawnumber</guid>" >> "$RSSFILE"
		
		if [[ "$SHOWDATE" == true ]]; then
			date="$(grep '^date: ' <<< "$mdhead" | cut -d: -f2)"
			rfc2822date="$(date -Rd "${date//-/\/}")"
			echo "<pubDate>$rfc2822date</pubDate>" >> "$RSSFILE"
		fi
		
		[[ "$SHOWAUTHOR" == true ]] && echo "<title>$(grep '^author: ' <<< "$mdhead" | cut -d: -f2)</title>" >> "$RSSFILE"
		
		echo "<description><![CDATA[$(<$ENCODED/$rawnumber.html)]]></description>" >> "$RSSFILE"
		
		echo '</item>' >> "$RSSFILE"
	done
	
	echo '
			</channel>
		</rss>
	'  >> "$RSSFILE"
fi
