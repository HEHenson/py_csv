# APT sorter 
# Created for UP work project
# 2017 May

import sys,os

import csv

class Find_Jur(object):
    """Provides ability to determine juridiction from phone number"""
    def __init__(self,thefilename:str, maindir: str="", subdir: str=""):
        # number of records found
        self.cendir = maindir
        self.recno = 0
        self.probno = 0
        self.fndjurfile = None
        self.fndfilename = thefilename
        self.jurdic = {}
        self.fileOK = self.opencsv(subdir)
    def opencsv(self,subdir: str):
        """ Open cvs file."""
        # need to open subdirectory
        retval = False
        if(subdir != ""):
            os.chdir('..')
            os.chdir(subdir)
        print("Loading numbers to zipcode dictionary {0} in {1} ".format(self.fndfilename,os.getcwd()))
        with open(self.fndfilename) as csvfile:
            try:
                jurreader = csv.reader(csvfile,quoting=csv.QUOTE_ALL)
            except:
                print("difficulty reading file")
            for row in jurreader:
                # skip header
                if self.recno == 0:
                    self.recno += 1
                    continue
                try:
                    thenum = int(row[2])
                    thest = row[0]
                    self.jurdic[thenum] = thest
                    self.recno += 1
                except:
                    self.probno += 1
                    if self.probno > 2 and self.probno < 5:
                        print("could not process",row)
                        print("parsed as {0} and {1}".format(thenum,thest))
        if self.recno == 0:
            print("Could not code lookup file {0}".format(self.jurfilename))
            print("Here are the available files")
            print(os.listdir()) 
        else:
            print("{0} entries in dictionary with problems {1} encountered".format(self.recno,self.probno))
            retval = True
        os.chdir(self.cendir)
        return retval  
    def getstate(self,thenum :str)->str:
        """ Looks up state associated with phone number.
        :Args: phonenumber
        :Results: string indicating state.  None is return if it cannot found.
        """
        # only need first six digits after leading one
        if len(thenum) == 0:
            return ""
        if thenum[0] == '1':
            searchstr = thenum[1:7]
        else:
            searchstr = thenum[0:6]
        if len(searchstr) != 6:
            return ""
        try:
            searchint = int(searchstr)
        except:
            return ""
        try:
            thestate = self.jurdic[searchint]
        except:
            thestate = ""
        return thestate

class Jur_File(object):
    """ Jurisdiction File Object"""
    def __init__(self,thefilename:str, maindir: str, subdir: str=""):
        # number of records found
        self.cendir = maindir
        self.recno = 0
        #: the number of output records
        self.outno = 0
        self.numones = 0
        self.numzeros = 0
        self.nummones = 0
        self.thedict = None
        self.jurfile = None
        self.jurfilename = thefilename
        self.juroutfile = None
        self.juroutfilename = ""
        self.fileOK = self.opencsv(subdir)      
    def opencsv(self,subdir: str)->bool:
        """ Open cvs file."""
        # need to open subdirectory
        retval = False
        if(subdir != ""):
            os.chdir('..')
            os.chdir(subdir)
        print("Processing {0} in {1} ".format(os.getcwd(),self.jurfilename) )
        try:
            thefile = open(self.jurfilename)
            self.jurfile = csv.reader(thefile)
            print("openned ",self.jurfilename)
            retval = True
        except:
            self.jurfile = None
        if not retval:
            print("Could not open jurisdiciton file {0}".format(self.jurfilename))
            print("Here are the available files")
            print(os.listdir())            
        os.chdir(self.cendir)
        return retval
    def process_csv(self,thedict:dict, outfile:str,maxrec:int = -1):
        """ This will create a new csv that is the same as input
        plus four new columns
        :Args: 
          thedict - dictionary to classify records
          outfile - output file
          maxrec - maximum number of records to be process, negative = no limit
        """
        print(80*'=')
        self.thedict = thedict
        self.juroutfilename = outfile
        try:
            self.juroutfile = open(self.juroutfilename,'w')
        except:
            print("Could not create output file")
            return self.outno
        juroutwriter = csv.writer(self.juroutfile)
        self.outno = 0
        
        for therow in self.jurfile:
            if self.outno == 0:
                # create header file
                newrow = therow + ['','ani_st','dnis_st','lrn_st','result']
                juroutwriter.writerow(newrow)
                self.outno += 1
                continue
            self.outno += 1
            if maxrec > 0 and self.outno > maxrec :
                break # for now
            newrow = self.getnewrow(therow)
            juroutwriter.writerow(newrow)
        self.juroutfile.close()
                
    def getnewrow(self,therow:list)->list:
        """This will create a new row."""
        # None will be converted to empty string
        ani_st = self.thedict.getstate(therow[1])
        dnis_st = self.thedict.getstate(therow[2])
        lrn_st = self.thedict.getstate(therow[3])
        
        result = 1
        
        if ani_st == "" or dnis_st == "" or lrn_st == "":
            result = -1
        elif ani_st == dnis_st:
            result = 0
        elif lrn_st != ani_st and lrn_st != dnis_st :
            result = 0
        else:
            result = 1
        
        # update stats
        if result == 1:
            self.numones += 1
        elif result == 0:
            self.numzeros += 1
        else:
            self.nummones +=  1           
            
            
        newrow = therow + [ani_st,dnis_st,lrn_st,result]
        return newrow
            

    
if __name__ == '__main__':
    """ Script to allow excecution from the command line"""
    if(len(sys.argv) != 4):
        print("Please enter 3 arguments:")
        print(4*' ','Jurisdiciton file ',)
        print(4*' ','linebyline file')
        print(4*' ','output file')
        sys.exit() 
    
    # save main directory as a global variable
    cendir = os.getcwd()   
    print("Executing program in {0}".format(cendir))
    
    print("about to load dictionary {0}".format(sys.argv[1]))
    thedict = Find_Jur(sys.argv[1],cendir)
    print("successfully loaded dictionary of {0} zipcodes".format(thedict.recno))
    thejur= Jur_File(sys.argv[2],cendir)
    thejur.process_csv(thedict,sys.argv[3])    
    print("Program successfully completed with {0} records processed".format(thejur.outno))
    print("There were:")
    print("    {0} Records for which the condition held".format(thejur.numones))
    print("    {0} Records for which it did not hold".format(thejur.numzeros))
    print("    {0} Records that could not be processed".format(thejur.nummones))