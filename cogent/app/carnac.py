#!/usr/bin/env python

from cogent.app.util import CommandLineApplication,\
    CommandLineAppResult, ResultPath
from cogent.app.parameters import Parameter,FlagParameter,Parameters

__author__ = "Shandy Wikman"
__copyright__ = "Copyright 2007-2009, The Cogent Project"
__contributors__ = ["Shandy Wikman"]
__license__ = "GPL"
__version__ = "1.4"
__maintainer__ = "Shandy Wikman"
__email__ = "ens01svn@cs.umu.se"
__status__ = "Development"

class Carnac(CommandLineApplication):
    """Application controller for Carnac RNAfolding application

    Info at:
    http://bioinfo.lifl.fr/carnac/index.html

     Options:
     -a   Inhibit the energy correction that is automatically
          performed to create the initial set of potential
          stems. By default, the energy correction depends of the
          GC percentage of each sequence.

     -c   Eliminate sequences that are too similar. The similarity
          treshold is 98%.

     -h   Add hairpins that are present only in one sequence to
          the initial set of potential stems (may be time and space
          demanding).
     """
    #Limitation
    #if -c is turned on and file is deleted error in file handling in _get_result_paths
    _parameters = {
        '-c':FlagParameter(Prefix='-',Name='c',Value=False), 
        '-a':FlagParameter(Prefix='-',Name='a'),
        '-h':FlagParameter(Prefix='-',Name='h')}
    _command = 'carnac'
    _input_handler='_input_as_string'
    

    def _get_result_paths(self,data):
        """Specifies the paths of output files generated by the application
        
        data: the data the instance of the application is called on
        
        Carnac produces it's output to a .ct, .eq, to the location of input file
        and .out files located in the same folder as the program is run from. 
        graph and align file is also created.
        You always get back: StdOut,StdErr, and ExitStatus

        """
        result={}
        name_counter = 0
        seq_counter = 0
        ones='00'
        tens='0'
        count=''
        if not isinstance(data,list):
            #means data is file
            path=str(data)
            data=open(data).readlines()
        else: #data input as lines
            #path=''.join([self.WorkingDir,self._input_filename.split('/')[-1]])
            path = ''.join(['/tmp/', self._input_filename.split('/')[-1]])
        for item in data:
            if item.startswith('>'):
                name_counter += 1
                if name_counter < 10:
                    count=ones             
                if name_counter > 9:
                    count=tens
                if name_counter > 99:
                    count=''
                name = item.strip('>\n')
            else:
                nr=name_counter
                
                result['ct%d' % nr] =\
                    ResultPath(Path=('%s%s%d.ct' % (path,count,nr)))
                result['eq%d' % nr] =\
                    ResultPath(Path=('%s%s%d.eq' % (path,count,nr)))
                result['out_seq%d' % nr] = \
                    ResultPath(Path=(''.join([self.WorkingDir,'Z_%s%d.%s.out'% \
                        (count,nr,name)])))

            result['graph'] =\
                ResultPath(Path=(self.WorkingDir+'graph.out'))
            result['align'] =\
                ResultPath(Path=(self.WorkingDir+'alignment.out'))

        return result 
