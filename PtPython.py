#!/usr/bin/python
import poster
import simplejson as json

import os
import re
import urllib
import urllib2
import uuid
import sys, getopt

class PtpImg:
    @staticmethod
    def Upload(logger, imagePath = None, imageUrl = None):
        # Get image extension from the URL and fall back to ptpimg.me's rehosting if it's not JPG or PNG.
        fileName, extension = os.path.splitext( imageUrl )
        extension = extension.lower()
        if ( extension != ".jpg" and extension != ".jpeg" and extension != ".png" ):
            raise Exception("Incompatible URL")

        return PtpImg.__UploadInternal( logger, None, imageUrl )

    @staticmethod
    def __UploadInternal(logger, imagePath = None, imageUrl = None):
        response = None

        encodedData = urllib.urlencode( { "urls": imageUrl } )
        headers = { "Content-Type": "application/x-www-form-urlencoded", "Content-Length": str( len( encodedData ) ) }
        request = urllib2.Request( "http://ptpimg.me/index.php?type=uploadv2&key=QT5LGz7ktGFVZpfFArVHCpEvDcC3qrUZrf0kP&uid=999999&url=c_h_e_c_k_p_o_s_t", encodedData, headers )
        result = urllib2.urlopen( request )
        response = result.read()

        # Response is JSON.
        # [{"status":1,"code":"8qy8is","ext":"jpg"}]
        jsonLoad = None
        try:
            jsonLoad = json.loads( response )
        except ( Exception, ValueError ):
            logger.exception( "Got exception while loading JSON response from ptpimg.me." )
            raise

        if ( jsonLoad is None ) or len( jsonLoad ) != 1:
            raise Exception("Got bad JSON response from ptpimg.me.")

        jsonLoad = jsonLoad[ 0 ]
        imageCode = jsonLoad[ "code" ]
        if ( imageCode is None ) or len( imageCode ) == 0:
            print( "Got bad JSON response from ptpimg.me: no image code." )

        imageExtension = jsonLoad[ "ext" ]
        if ( imageExtension is None ) or len( imageExtension ) == 0:
            print( "Got bad JSON response from ptpimg.me: no extension." )

        urlPath = "http://ptpimg.me/" + imageCode + "." + imageExtension
        print( urlPath )
        cmd = 'echo %s | tr -d "\n" | pbcopy' % urlPath
        os.system(cmd)

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:")
   except getopt.GetoptError:
      print 'PtPython.py -i <Image URL>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'PtPython.py -i <Image URL>'
         sys.exit()
      elif opt in ("-i"):
         inputfile = arg
         PtpImg.Upload(None, None, inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])