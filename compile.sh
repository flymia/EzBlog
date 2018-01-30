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
