from getngrams import runQuery
from time import sleep
import os

def fail_nohits(filename):
    """ Returns True if there are no hits at all for any words in 'filename'.
    """

    # open file for reading
    o = open(filename,'rU')

    first = o.readline()

    # if the first like looks like this, there were no hits.
    if first == 'year\n':
        return True
    return False

def getngrams_wrapper(queries):
    """ A wrapper for "getngrams.py", which takes care of a few defaults,
    and also makes sure we do not download files again if we already have them.
    It also has a short sleep interval to make sure we don't hurt the google servers
    (or let them know what we are doing).

    : 
    Returns: 
    filenem(str)

    NOTE: see: https://github.com/econpy/google-ngrams for the full documentation to 'getngrams'.

    NOTE: I think this program may be violating some copyright things... :/

    """

    # set a handfull of parameter to some nice default values
    corpus = "eng_2012"
    startYear = "1800"
    endYear = "2008"
    smoothing = "1"
    word_case_flag = "caseInsensitive"
    print_flag = "noprint"

    filename = ("-").join([
        queries, corpus, startYear,
        endYear, smoothing, word_case_flag
    ])
    filename += ".csv"

    # remove spaces from filename (as in original script)
    filename = filename.replace(" ","")

    print("Checking: {0}".format(filename))

    # check if the file 'filename', exists, and if not, run 'getngrams.runQuery'.
    if os.path.exists(filename):
        print "Data exists as: {0}".format(filename)
    else:
        argumentString = ("-corpus={corpus} "
                          "-startYear={startYear} "
                          "-endYear={endYear} "
                          "-smoothing={smoothing} "
                          "-{word_case_flag} "
                          "-{print_flag} "
                          "{queries}".format(
                              queries=queries,
                              corpus=corpus,
                              startYear=startYear,
                              endYear=endYear,
                              smoothing=smoothing,
                              word_case_flag=word_case_flag,
                              print_flag=print_flag,
                              )
                          )
        try:
            # do nothing for 1 second, we don't want to hurt the google servers
            sleep(1)
            runQuery(argumentString)
        except:
            print('An error occurred running Marcs Wrapper.')

        # check and clean 0 values
        if fail_nohits(filename):
            try:
                os.remove(filename)
            except:
                pass
            raise Exception(
                    "There were no hits for '{0}'. Aborting!".format(queries)
                    )
    return filename
