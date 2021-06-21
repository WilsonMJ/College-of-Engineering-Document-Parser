"""
Banner communication functions for uploading files to VT's document management
system
"""


import requests
import os
from requests_toolbelt import MultipartEncoder
import time
import shutil
from config import BANNER_ID, BANNER_PASSWORD, BANNER_TEST_CONNECTION_URL, BANNER_UPLOAD_URL


def fields_to_json(id, doctype, termcode):
    """Converts fields to a JSON object that complies with Banner's field specs

    Parameters
    ----------
    id : str
        Student ID number
    doctype : str
        Document type for uploaded file
    termcode : str
        Term code associated with uploaded file

    Returns
    -------
    str
        String containing a JSON formatted according to Banner's field
        specifications

    """
    json = "{\"TargetDoc\": null," \
				+ '"NewIndex":{"indexid":0, "values":[' \
				+ '{"FieldID": "field1", "FieldValue": "' + id + '"},' \
				+ '{"FieldID": "field3", "FieldValue": "' + doctype + '"},' \
				+ '{"FieldID": "field8", "FieldValue": "' + termcode + '"}],' \
				+ '"links": []},' \
				+ '"FromBatch": null, "BatchPageNum": 0, "IgnoreDuplicateIndex": true, "IgnoreDlsViolation": false}'
    
    return json


def test_connection():
    """Test connection with Banner system

    Useful for ensuring provided links and authorization credentials are valid
    before attempting to upload anything

    """
    with requests.Session() as s:
        s.auth = (BANNER_ID, BANNER_PASSWORD)
        s.headers.update({
            'Accept': 'application/vnd.emc.ax+json'
        })

        response = s.get(BANNER_TEST_CONNECTION_URL)

        print(response.status_code)
        print(response.headers)
        print(response.json())


def upload_file(file_name, id, doc_type, term_code):
    """Uploads file to VT's Banner system

    Parameters
    ----------
    file_name : str
        Relative or absolute file path of the file to be uploaded
    id : str
        Student ID to be associated with the file
    doc_type : str
        Document type to be associated with the file
    term_code : str
        Term code to be associated with the file

    Returns
    -------
    tuple (int, str)
        Either 200 and Success if upload successful, or the Student ID that
        was erroneous with a message indicating the error
    
    """
    with requests.Session() as s:
        s.auth = (BANNER_ID, BANNER_PASSWORD)

        m = MultipartEncoder(
            fields = {
                'data': (None, fields_to_json(id, doc_type, term_code), 'application/vnd.emc.ax+json; charset=utf-8'),
                'bin': (file_name, open(file_name, 'rb'), 'application/bin')
            }, boundary='--BOUNDARY--')

        response = s.post(BANNER_UPLOAD_URL, headers={
            'Accept': 'application/vnd.emc.ax+json',
            'Content-Type': m.content_type
        }, data=m.to_string())

        print(response.status_code)
        print(response.headers)
        print(response.json())

        if response.status_code == 200:
            return 200, 'Success'
        else:
            print(response.json()['Message'])
            return int(id), response.json()['Message']


def bulk_upload(folder_name, doc_type, term_code):
    """Uploads a bulk amount of PDFs to VT's Banner system

    Note
    ----
    It is expected that each file in the directory to be uploaded be named
    according to the student ID they are associated with. i.e. 905000001.pdf

    Parameters
    ----------
    folder_name : str
        String of the directory containing the multiple PDFs
    doc_type : str
        Document type to be associated with the batch of PDFs
    term_code : str
        Term code to be associated with the batch of PDFs

    Returns
    -------
    tuple (list, list, str)
        A tuple containing of list of successfully uploaded ID numbers, a list 
        of erroneous ID numbers, and string containing any error information if
        there were errors with term codes or document types
    
    """
    error_ids = []
    success_ids = []
    result_message = ''

    # Loop over each PDF in the directory
    for file_name in os.listdir(folder_name):

        student_id = file_name[0:-4]
        file_path = os.path.join(folder_name, file_name)

        print(file_path)
        print(student_id, doc_type, term_code)
        status_code, message = upload_file(file_path, student_id, doc_type, term_code)

        print(status_code)

        if status_code != 200:
            # Handle message for invalid term codes or document types
            if message == (doc_type + ' is not a valid user-defined value.'):
                result_message = 'Invalid Document Type'
                break
            elif message == (term_code + ' is not a valid user-defined value.'):
                result_message = 'Invalid Term Code'
                break
            error_ids.append(status_code)
        else:
            os.remove(file_path)
            success_ids.append(int(student_id))

    if result_message != '':
        shutil.rmtree(folder_name)

    return success_ids, error_ids, result_message