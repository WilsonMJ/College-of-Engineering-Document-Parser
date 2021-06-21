"""
Function for splitting a bulk PDF into smaller PDFs
"""


import PyPDF2
import sys
import re
import tempfile


def doc_splitter(docName):
    """Parses bulk PDF into individual PDFs named after the PID of the student

    Parameters
    ----------
    docName : str
        String containing the absolute or relative path to the bulk PDF to be
        parsed
    
    Returns
    -------
    str
        String containing the temporary output directory of the newly parsed 
        PDFs
    
    """        
    # Creating temporary directory
    tempdir = tempfile.mkdtemp()
    outputFolder = tempdir

    # create a pdf file object, pdf reader object, and pdfWriter object
    pdfFileObj = open(docName, 'rb') 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdfWriter = PyPDF2.PdfFileWriter()

    # get the number of pages in the file for reference
    maxPage = pdfReader.numPages

    sid = "" #predefine so can keep between loops

    #loop through every page
    for x in range(0,maxPage):
        # create a page object 
        pageObj = pdfReader.getPage(x) 
        
        # extract text from page
        page = pageObj.extractText()
        # need to remove \n and \t in search document to ensure number is continous string 
        searchPage = page.replace("\n","")
        searchPage = searchPage.replace("\t","")
        # find if has a sid and where starts
        pidStart = re.findall("90[0-9][0-9][0-9][0-9][0-9][0-9][0-9]", searchPage) 
        
        #if no matches found set to "" otherwise set to sidStart
        if(len(pidStart) == 0):
            sidStart = ""
        else:
            sidStart = pidStart[0]
                
        # current page has an sid
        if(sidStart != ""):
            sidOld = sid #save the old sid
            sid = sidStart #Copy sid for reference

            # split off previous pdf if not first
            if(sidOld != ""):
                # write the new pdf to <sid>.pdf
                with open(outputFolder + "/" + sidOld + ".pdf", "wb") as f:
                    pdfWriter.write(f)
                # clear the pdfWriter by replacing it
                pdfWriter = PyPDF2.PdfFileWriter()
        
        # add new page to the writer
        pdfWriter.addPage(pageObj)
        
        # need to write the last pdf
        if(x == maxPage-1):
            with open(outputFolder + "/" + sid + ".pdf", "wb") as f:
                    pdfWriter.write(f)

    # close the pdf file object 
    pdfFileObj.close()
    return tempdir
