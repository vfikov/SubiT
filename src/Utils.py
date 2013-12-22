#!/usr/bin/python
import httplib
import urllib
import os
import tempfile
import re
import gzip
import zipfile
from StringIO import StringIO 
import uuid
import sys
import time

import UserAgents
import Logs 

INFO_LOGS = Logs.LOGS.INFO
WARN_LOGS = Logs.LOGS.WARN
DIRC_LOGS = Logs.LOGS.DIRECTION

class HttpRequestTypes:
    GET  = 'GET'  #Retrieve only
    POST = 'POST' #Post data (Retrieve Optional)
    HEAD = 'HEAD' #Check response (same response as get, but without the data)


#===============================================================================
# performs http request, url-> the url without the domain, type-> GET/POST
# retry is needed for subtitle downloading. in some cases, the download 
# is corrupted, with some bytes missing, with this method, it's working
#===============================================================================
def performrequest( domain, url, data, type, more_headers, retry = False ):
    httpcon = httplib.HTTPConnection( domain )
    headers = {}
    #each packet we send will have this params (good for low-profile)
    if not retry:
        headers =   {
                        'Connection'        : r'keep-alive',
                        'User-Agent'        : UserAgents.getAgent(), #The Fake User Agent
                        'X-Requested-With'  : r'XMLHttpRequest',
                        'Content-Type'      : r'application/x-www-form-urlencoded',
                        'Accept'            : r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset'    : r'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding'   : r'gzip,deflate,sdch',
                        'Accept-Language'   : r'en-US,en;q=0.8',
                        'Cache-Control'     : r'max-age=0'
                    }
    else:
        headers =   {
                        'User-Agent'        : UserAgents.getAgent() #The Fake User Agent
                    }
    
    #in case of specifiyng more headers
    if ( len(more_headers) ):
        headers.update(more_headers)

    httpcon.request( type, url, data, headers )     
    
    if retry:
        return httpcon.getresponse( ).read()
    else:
        return gzip.GzipFile(fileobj=StringIO(httpcon.getresponse( ).read())).read().replace('\r\n', '')

#===============================================================================
# Downloand the file from the given url, and saves it at the given location
# domain    = domain name
# url       = url inside the domain
# path      = directory in which the subtitle will be saved (after extraction), leave empty for current dir)
# file_name = name to give to the subtitle file after extraction. 
#    note: will use the original name if: 
#        a. file_name is empty 
#        b. there is more then one file in the archive
# 
# in case of success, returns true, else false
#===============================================================================
def getfile(domain, url, path, file_name):
    #temp location for the zip file
    file_location       = os.path.abspath(path)
    dst_file            = os.path.join(file_location, file_name)
    defaultextraction   = lambda zf: zf.extractall( file_location )
    
    writelog( INFO_LOGS.STARTING_SUBTITLE_DOWNLOAD_PROCEDURE )
    writelog(INFO_LOGS.DESTINATION_DIRECTORY_FOR_SUBTITLE % file_location)
    
    for retry in range(0,2):
        response    = performrequest( domain, url, '', 'GET', '', retry )
        random_name = os.path.join( tempfile.gettempdir(), str(uuid.uuid4()) + '.zip' ) 
        if (len(response)):       
            try:
                open(random_name, 'wb').write( response )

                with zipfile.ZipFile(random_name, 'r') as zfile:
                    try:
                        #if we have one file in the zip
                        if len(zfile.namelist()) == 1:
                            file_name_in_archive = zfile.namelist()[0]
                            open(dst_file, 'wb').write(zfile.open(file_name_in_archive).read())
                            writelog( INFO_LOGS.SUCCESSFULL_EXTRACTION_FROM_ARCHIVE )
                        else:
                            writelog( INFO_LOGS.GOT_SEVERAL_FILES_IN_THE_ARCHIVE )
                            defaultextraction(zfile)
                            writelog( INFO_LOGS.SUCCESSFULL_EXTRACTION_FROM_ARCHIVE )
                    except:
                        writelog( WARN_LOGS.FAILED_SPECIAL_EXTRACTION_OF_SUBTITLE )
                        defaultextraction(zfile)
                        writelog( INFO_LOGS.SUCCESSFULL_EXTRACTION_FROM_ARCHIVE )
                break #We wont do another iteration if we get success
            except:
                writelog( WARN_LOGS.FAILED_EXTRACTING_SUBTITLE_FILE_FROM_ARCHIVE )
                if not retry: #at first try
                    writelog( INFO_LOGS.TRYING_ANOTHER_METHOD_FOR_DOWNLOADING_SUB )
        else:
            writelog(WARN_LOGS.FAILED_DOWNLOADING_SUBTITLE_ARCHIVE)
            
    writelog(INFO_LOGS.FINISHED_SUBTITLE_DOWNLOAD_PROCEDURE)
        
        
    try:
        os.remove(random_name)
        return True
    except:
        time.sleep(1)
        try:
            os.remove(random_name)
            return True
        except:
            writelog( WARN_LOGS.FAILED_TEMP_ZIP_FILE_REMOVAL )
            return False
                

#===============================================================================
# Query the content and returns list of all result, in case of multi-group pattern, 
# will return a list of tuples (tuple for each group)
#===============================================================================
def getregexresults( pattern, content ):
    c_pattern = re.compile( pattern )
    return re.findall( c_pattern, content )

HELP_ARGS = ['/?', '?', '--help', 'help']


def printhelp():
    print ''
    print 'SubiT - Auto Subtitles Downloader'
    print 'Usage: SubiT.exe [moviename | filename] [Directory]'
    print ''
    print 'moviename: movie name'
    print 'filename:  name of movie file, with extension'
    print 'Directory: destination directory for storing the subtitle,'
    print '           omitting this parameter will keep original subtitle filename'
    raw_input()
    sys.exit()
	
#params[0] is Dir
#params[1] is filename without ext    
def parseargs():
    params = ['','']

    if len(sys.argv) > 1:
        if sys.argv[1].lower() in HELP_ARGS: 
            printhelp()
        elif len(sys.argv) == 2:
            if os.path.isfile(sys.argv[1]):
                params = list(os.path.split(sys.argv[1]))
                params[1] = os.path.splitext(params[1])[0] #File name without ext
            elif os.path.isdir(sys.argv[1]):
                params[0] = sys.argv[1]
        else:
            printhelp()
    return params

def askuserforname():
    moviename = askuser( DIRC_LOGS.INSERT_MOVIE_NAME_FOR_QUERY, False )
    if(len(moviename) == 0):
        sys.exit()
    return moviename

GuiInstance = None

#Basic function to print messages (modification will be done later)
def writelog( message ):
    GuiInstance.writelog( message )

def askuser( question, canempty, withdialog=False ):
    return GuiInstance.getuserinput(question, canempty, withdialog)
    
def setmoviechoices( choices, message ):     
    GuiInstance.setmoviechoices(choices, message)
    
def setversionchoices( choices, message ):
    return GuiInstance.setversionchoices(choices, message)

def getselection( type ):
    return GuiInstance.getselection( type )
