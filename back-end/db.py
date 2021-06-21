"""
Functions for calling stored procedures of a MySQL database
"""


from mysql.connector import MySQLConnection, Error
from config import DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD


def call_validate_user(username):
    """Calls validateUser stored procedure

    Parameters
    ----------
    username : str
        String of the username to validate

    Returns
    -------
    tuple (int, str, str, int)
        Tuple containing the unique database ID of the user, the username,
        the college name the user belongs to, and the privelege level to
        indicate if the user has admin privileges or not.  The tuple is empty
        if the user does not exist in the database.
    
    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [username]

        user_info = []

        cursor.callproc('validateUser', args)
        for result in cursor.stored_results():
            user_info = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if len(user_info) > 0:
        return user_info[0]
    else:
        return ()


def call_change_user_privilege_level(username, privilege_level):
    """Calls changeUserPrivelegeLevel stored procedure

    Parameters
    ----------
    username : str
        Username of user who's privelege level to change
    privilege_level : int
        int of new privilege level for the user 0 = standard, 1 = admin
    
    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [username, privilege_level]

        cursor.callproc('changeUserPrivilegeLevel', args)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def call_insert_user(username, privilege_level, college):
    """Calls insertUser stored procedure

    Parameters
    ----------
    username : str
        String of the user's username
    privilege_level : int
        int of the new user's privilege level, 0 = standard, 1 = admin
    college : str
        String of the college the new user belongs to

    Returns
    -------
    int
        Unique database ID of newly added user

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [username, privilege_level, college]

        cursor.callproc('insertUser', args)
        conn.commit()

        for result in cursor.stored_results():
            uid = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return uid[0][0]


def call_insert_college(college):
    """Calls insertCollege stored procedure

    Parameters
    ----------
    college : str
        String of the new college to be added, i.e. 'College of Engineering'

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [college]

        cursor.callproc('insertCollege', args)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
   

def call_insert_document_type(doc_type, college):
    """Calls insertDocumentType stored procedure

    Parameters
    ----------
    doc_type : str
        String of new document type to be added, i.e. 'N-NEW DOC TYPE'
    college : str
        String of college to add document type to

    Returns
    -------
    int
        Unique database ID of newly added document type

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [doc_type, college]

        cursor.callproc('insertDocumentType', args)
        conn.commit()

        for result in cursor.stored_results():
            did = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return did[0][0]


def call_insert_term_code(term_code, college):
    """Calls insertTermCode stored procedure

    Parameters
    ----------
    term_code : str
        String of term code to be added
    college : str
        String of college to add new term code to

    Returns
    -------
    int
        Unique database ID of newly added term code

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [term_code, college]

        cursor.callproc('insertTermCode', args)
        conn.commit()

        for result in cursor.stored_results():
            tid = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    
    return tid[0][0]


def call_delete_term_code(tid):
    """Calls deleteTermCode stored procedure

    Parameters
    ----------
    tid : int
        Integer of unique ID corresponding to term code to be deleted

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [tid]

        cursor.callproc('deleteTermCode', args)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def call_delete_document_type(did):
    """Calls deleteDocumentType stored procedure

    Parameters
    ----------
    did : int
        Integer of unique ID corresponding to document type to be deleted

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [did]

        cursor.callproc('deleteDocumentType', args)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def call_delete_user(uid):
    """Calls deleteUser stored procedure

    Parameters
    ----------
    uid : int
        Integer of unique ID corresponding to user to be deleted

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [uid]
        
        cursor.callproc('deleteUser', args)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def call_delete_college(cid):
    """Calls deleteCollege stored procedure

    Parameters
    ----------
    cid : int
        Integer of unique ID corresponding to college to be deleted

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [cid]

        cursor.callproc('deleteCollege', args)
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def call_get_all_users():
    """Calls getAllUsers stored procedure

    Returns
    -------
    list
        List of tuples with each tuple containing 
        (unique DB ID as int, username as string, privilegeLevel as int)

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        cursor.callproc('getAllUsers')

        for result in cursor.stored_results():
            people = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return people


def call_get_users_by_college(college):
    """Calls getUsersByCollege stored procedure

    Parameters
    ----------
    college : str
        String of college to retrieve a list of users from

    Returns
    -------
    list
        List of tuples with each tuple containing 
        (unique DB ID as int, username as string, privilegeLevel as int)

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [college]

        cursor.callproc('getUsersByCollege', args)
        for result in cursor.stored_results():
            users = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return users


def call_get_all_doc_types():
    """Calls getUsersByCollege stored procedure

    Returns
    -------
    list
        List of tuples with each tuple containing
        (unique DB ID as int, document type as string)
    
    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        cursor.callproc('getAllDocumentTypes')
        for result in cursor.stored_results():
            doc_types = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return doc_types


def call_doc_types_by_college(college):
    """Calls getDocumentTypesByCollege stored procedure

    Parameters
    ----------
    college : str
        String of college to get document types from

    Returns
    -------
    list
        List of tuples with each tuple containing
        (unique DB ID as int, document type as string)

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [college]

        cursor.callproc('getDocumentTypesByCollege', args)
        for result in cursor.stored_results():
            doc_types = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return doc_types


def call_get_all_term_codes():
    """Calls getAllTermCodes stored procedure

    Returns
    -------
    list
        List of tuples with each tuple containing
        (Unique DB ID as int, term code as string)

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        cursor.callproc('getAllTermCodes')
        for result in cursor.stored_results():
            term_codes = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    
    return term_codes


def call_get_term_codes_by_college(college):
    """Calls getTermCodesByCollege stored procedure

    Parameters
    ----------
    college : str
        String of college to get term codes from

    Returns
    -------
    list
        List of tuples with each tuple containing
        (Unique DB ID as int, term code as string)

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        args = [college]

        cursor.callproc('getTermCodesByCollege', args)
        for result in cursor.stored_results():
            term_codes = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return term_codes


def call_get_all_colleges():
    """Calls getAllColleges stored procedure

    Returns
    -------
    list
        List of tuples with each tuple containing
        (College name as string)

    """
    try:
        conn = MySQLConnection(user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST,
                                database=DB_DATABASE)
        cursor = conn.cursor()

        cursor.callproc('getAllColleges')
        for result in cursor.stored_results():
            colleges = result.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return colleges