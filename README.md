# EzBlog
EzBlog is the smallest and simplest blogging software written in Bash.

## Installation

1. Configure CGI to work on your webserver - this is mandatory!
2. Install pandoc
3. Upload the files to a web directory
4. Navigate to index.cgi

## Requirements
* Bash
* pandoc
```
sudo apt install pandoc

sudo pacman -S pandoc

sudo dnf install pandoc
```
* Webserver, that is able to do CGI

# Usage
* Add article using the example article (Markdown syntax!)
* Compile the articles using the compile.sh script
* Have a look at the webpage
