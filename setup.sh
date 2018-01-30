#!/bin/bash
echo -e 'Welcome to EzBlog! This will setup your blog! \n'

echo -n 'First tell us the name of your blog: '; read title;

echo -n 'Where should we generate the blog?'; read createdir;

echo -e 'Thanks, starting generation...\n';

mkdir $createdir/articles
mkdir $createdir/encoded
mkdir $createdir/config

cat << EOF
ARTICLES=articles/

ENCODED=encoded/

BLOGTITLE="$title"

SHOWPOSTS=12

SHOWAUTHOR=true

SHOWDATE=true
EOF  >> $createdir/config/settings
