#!/bin/bash
# Script to simply use a pre-existing script on many linux and OS X systems to
# prettyfy a JSON file provided through STDIN, sending the output to STDOUT. While
# this can be easily used from the command line, BBEDIT users can also place it in 
# the ~/Library/Application Support/BBEdit/Text Filters directory to add it as a
# BBEDIT text filter that can be used to accomplish the same task within BBEDIT. 
# Thanks to Scott's Weblog - http://blog.scottlowe.org/2013/11/11/making-json-output-more-readable-with-bbedit/ - for this hint. 

python -m json.tool
