''' Contextual grep tool - search file(s) for a matching string and display the chunks of text surriounding it also.

    This tool is designed for quicker searching of chunks of files without having to open them in an editor and 
    do finds.

    Copyright Brian Elliott, 2011 <bdelliott@gmail.com>
'''

from optparse import OptionParser
import os
import sys

class ContextualGrep(object):
    def __init__(self, numlines):
        self.numlines = numlines
       
    def grep(self, pattern, files):

        # 1st check if all files exist:
        for f in files:
            if not os.path.exists(f):
                sys.exit("File %s does not exist." % f)

        for f in files:
            self.grepfile(pattern, f)
            
    def grepfile(self, pattern, file):
        ''' reads entire file into memory to search - could be made smarter for large files, but good enough
            for reading most text files. 
            
            note: won't find a pattern spanning multiple lines in the file
        '''
            
        f = open(file, "r")
        lines = f.readlines()
        f.close()

        num = len(lines)
        for i in range(num):
            l = lines[i]
            
            if l.find(pattern) != -1:
                # match
                start = max(0, i-self.numlines)
                end = min(i+self.numlines+1, num) 
                for j in range(start, end):
                    sys.stdout.write("%s:%d: %s" % (file, j, lines[j]))

                
                

if __name__=='__main__':
    
    parser = OptionParser()
    parser.usage = "python %prog pattern [files]"
    
    parser.add_option("-n", "--numlines", dest="numlines", help="Print AWS request URL",
                      default=5, action="store")
                      
    (opts, args) = parser.parse_args()

    if len(args) < 2:
        parser.print_usage()
        sys.exit("You must supply a search pattern and 1 or more files to search.")
        
    pattern = args.pop(0)
    files = args
        
    cg = ContextualGrep(opts.numlines)
    cg.grep(pattern, files)
