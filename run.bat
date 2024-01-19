@echo off
set EXT=csv

set /P log=output logfile(0:false, 1: true)? 

if %log% == 1 (
    @set /P filename=Please input a file name: 
    scrapy crawl mailarchive --logfile %filename%.%EXT% -O out.%EXT%
    
) else if %log% == 0 (
    scrapy crawl mailarchive -O out.%EXT%
)