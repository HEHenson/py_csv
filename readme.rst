========
Overview
========
The Python program in this git is python script written for a one-off project.  As it stands, it should be easily adaptable of the other similar projects.  This readme hopes to document the particular project but also suggest future improvements and potential for a framework but at least an easily modified set of routines.

This program address the need to have the ability to apply global edits to very large spreadsheets.  While it is true that the use of Python is not warranted for smaller spreadsheets, Python may be very useful for a number of reasons:

* File size - Although the original application may have started out small, through time the files have grown to the extent that visual interface is of limited value.
* Speed - Spreadsheet operations do not scale well. Calculations that may have been interactive at one time, become labourously slow.
* Weak Documentation - With a formal programing language, a user can be assured that a formula is uniformly applied.  With a spreadsheet an error in one cell may go unnoticed. Also the expression of formulas within a tiny cell can be highly error prone.
* Lack of control of updates - Spreadsheets update themselves in a haphazard fashion.  These problems can be further compounded with large linked spreadsheets.  A requirement of the current project is that this calculation be executable in terminal mode.  This allows very tight integration with the larger organizational workflow.

This document will first desribe the challenge posed by the client. Then an overview of the solution will be proposed. Then there will be a more detailed discussion that is targetted on the specific client. Then there will be an attempt to summarize the solution in a general fashion.

============
The Solution
============

The client had a large spreadsheet of 27 megabytes detailing interactions between various clients.  The goal was to classify these interactions by US state.  The actual formulae was complex, but easily managed in Python.  The solution was composed of two steps.

----------------------------------
Build Dictionary of Client Numbers
----------------------------------

A spreadsheet provided a listing of roughly 160,000 thousand client numbers and their associated states.  These were used to build a Python that allowed the mapping of client number to state.  This appears to have worked extremely well with very fast loading of the dictionary and lookup of the clients.  For the most part, the data appeared to be of high quality with very few of the records being identified as problematic.  It should be noted that problematic records were not included in the file.

---------------------------------------------
Create transactions file with new calculation
---------------------------------------------

Once the dictionary is loaded, then processing of the 27 megabyte file can begin.  However, the output csv file is first created.  In the main loop of this object each record is read in and new information is appended to create a larger output file.  In this process, no records are thrown out, although the ones with bad data are not used but marked as such. In fact the final column in the output file consists of an integer which is one of three values:

*  1 - Record contained the condition of interest to client
*  0 - Record did not contain condition
* -1 - Record could not be processed due to missing data.

===========
The Program
===========

A single Python file was created that contains three main sections:

* The dictionary class which provides rapid determination of the state.
* The main processing object that loops through the database of communications.
* The main program or script which allows the program to be wrong from a terminal in bash.

The package also includes a sample bash shell script that can execute the program.

--------------------
The dictionary class
--------------------

The class Find_Jur is created with the input of a function.  After some preprossing suggested by the client and evident from the data, a dictionary is created that allows for the very rapid identification of a client's state given their number.  The getstate function returns this state as a code given by the client.  If the state cannot be identified a empty string is provided.

-------------
The Main Loop
-------------

The Jur_File object contains the main loop to process the data. The processing is invoked by process_csv. 
The arguments are the dictionary class object, the output file, and an indicator the number of records to be processed. This allows for the selection of a small number of records for debugging purposes.

======================================
Final Thoughts and Future Improvements
======================================

This initial experiment completely justifies the use of Python to help manage very large spreadsheet databases.  Many of the possible improvements are evident from this initial attempt.  When the project was being planned, it was not known if the Panda's environment could have been used robustly in this situation.  However, if it was the case, further improvements would have been possible.

==============
Detailed Notes
==============

As always, the resolution of many detailed issues is crucial to completing the project.  Some of these issues are of importance only the the clients.  Others have genaral interest.

---------------
The Calculation
---------------

The calculation was performed in the getnewrow method.  It took the row from the original csv file and added four columns to it.  The first three give the state, and the fourth is an integer:

*  1 if the condition specified by client is true
*  0 if condition is known to be not tru
* -1 if record cannot be processed.

---------------------
The files as received
---------------------

* Note that current implementation does not handle spaces in file names well
* One file had unknown characters in the first 3 characters.  Note, substantial effort is required to bullet proof software against this.

---------------------------------
Particular to jurisdiction lookup
---------------------------------

* If jurisdiction could not be identified, then empty string is used.
* Numbers too short were rejected
* Numbers too long were truncated



