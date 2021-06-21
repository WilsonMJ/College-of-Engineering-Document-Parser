"""
Function for mapping non-Banner compliant document types to Banner compliant
ones
"""


from banner import upload_file
from config import DOC_TYPE_STANDARD_SET, DOC_TYPE_MAPPINGS


def map_document_type(input_string):
    """Maps provided input to banner compliant document type if one exists

    Parameters
    ----------
    input_string : str
        String of document type to be mapped if necessary or able to
    
    Returns
    -------
    str
        String of newly mapped banner compliant document type if possible or
        the original string to allow for untracked additions of new document
        types that haven't been added to DOC_TYPE_STANDARD_SET

    """
    upper_input = input_string.upper()

    if upper_input in DOC_TYPE_STANDARD_SET:
        return upper_input
    
    for doc_type in DOC_TYPE_MAPPINGS:
        if upper_input in DOC_TYPE_MAPPINGS:
            return doc_type

    return input_string