"""
Flask API for BDMParse's Angular frontend to communicate with to perform 
document functions, login functions, and administrative functions
"""


import os, json
from flask import Flask, request, send_file, session, redirect, url_for, abort
from flask_cors import CORS, cross_origin
from doc_splitter import doc_splitter
import tempfile
import shutil
import zipfile
import io
from werkzeug.utils import secure_filename
from cas import CASClient
import db
import banner
from doc_map import map_document_type
from config import VIRTUAL_MACHINE_HOSTNAME


app = Flask(__name__)
CORS(app, expose_headers=["x-suggested-filename"])

ALLOWED_EXTENSIONS = {'pdf'}

app.secret_key = ''

cas_client = CASClient(
    version=2,
    service_url= VIRTUAL_MACHINE_HOSTNAME + '/redirecting',
    server_url= ''
)

def allowed_file(filename):
    """Checks if the filename provided by the front-end is .pdf file
    
    Parameters
    ----------
    filename : str
        A string containing the filename of the file to be parsed
    
    Returns
    -------
    bool
        True if filename is a .pdf filename, false otherwise

    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_admin():
    """Checks whether current user accessing the API has admin privileges

    Returns
    -------
    bool
        True if user has admin privileges, false otherwise

    """
    print("In is_admin()")
    if is_logged_in() > 0: #Don't bother checking if not logged in
    #Check if user has admin privledges (>0)
        return True
    return False


def is_logged_in():
    """Checks whether user accessing the API is currently logged in

    Returns
    -------
    int
        User's role level with 0 being standard user, 1 being admin user if user
        is logged in, -1 otherwise to indicate not logged in.

    """
    #See if in session and get username
    print("In is_logged_in()")

    if 'username' in session:
        print("In is_logged_in() if statement")
        #See if valid username by checking each valid username w/ sessions username
        x = db.call_validate_user(session["username"])
        if len(x) > 0:
            print("is_logged_in() found valid user")
            return x[3]
        else:
            session.pop('username', None)
            print("is_logged_in() found invalid user")
    return -1


def is_valid_user(username):
    """Checks if username is a valid user of the web application

    Queries the database to determine if information exists for the username
    specified

    Parameters
    ----------
    username : str
        String of the username to check for existence in the database 
    
    Returns
    -------
    bool
        True if information for the user exists, false otherwise

    """
    x = db.call_validate_user(username)
    if len(x) == 0:
        return False
    else:
        return True


@app.route('/api/getuser')
def user_json():
    """Builds a JSON of the requested user information
    
    Note
    ----
    The GET request should contain the username in the query parameters as ```username```

    Returns
    -------
    JSON object
        A JSON object with the following format:

            {
                'username': username,
                'id': id according to the database,
                'role': Either admin or standard depending on the users database 
                        level,
                'college': College the user belongs to,
                'documentTypes': List of document types for that specific 
                                 college,
                'userList': List of users belonging to that college for admin 
                            functions,
                'termCodes': List of term codes for that specific college
            }
    
    """
    
    # Ensure user is logged in
    if is_logged_in() < 0:
        return 'User not logged in', 401
    
    #loop through all users to find the user
    username = request.args.get('username')

    x = db.call_validate_user(username)

    #return an empty json if user not in database
    if len(x) == 0:
        return json.dumps({
        'username':None,
        'id':None,
        'role':None,
        'college':None,
        'documentTypes':None,
        'userList':None,
        'termCodes':None
    }), 200, {'ContentType':'application/json'}
    else:
        #get all the other needed info
        #Check privilege level
        role = 'standard'
        userList = None
        if x[3] >= 1:
            role = 'admin'
            userList = [
                {
                    'id': user[0],
                    'username': user[1],
                    'role': 'standard' if user[2] == 0 else 'admin'
                } for user in db.call_get_users_by_college(x[2])]
        documentTypes = [
            {
                'id': document[0],
                'documentType': document[1]
            } for document in db.call_doc_types_by_college(x[2])]
        termCodes = [
            {
                'id': code[0],
                'termCode': code[1]
            } for code in db.call_get_term_codes_by_college(x[2])]
        return json.dumps({
            'username':username,
            'id':x[0],
            'role':role,
            'roleString':role,
            'college':x[2],
            'documentTypes': documentTypes,
            'userList':userList,
            'termCodes': termCodes
        }), 200, {'ContentType':'application/json'}


@app.route('/api/file/upload', methods=['POST'])
def parse():
    """Parses an uploaded bulk PDF file into separate PDFs based on PID

    Note
    ----
    The POST request should contain multipart form data consisting of a file
    with key ```fileKey``` and arguments for ```documentType``` and ```termCode```

    Returns
    -------
    JSON object
        Upon success the JSON object will be formatted as follows:

            {
                'total': The number of parsed PDFs,
                'num_success': The number of PDFs successfully uploaded to 
                               Banner,
                'num_error': The number of erroneous PIDs according to Banner,
                'successes': List of successful PIDs,
                'errors': List of erroneous PIDs,
                'file_path': String of file path containing erroneous pdfs for 
                             later download
            }
    
    str
        If the user is not logged in, a 403 code will be sent. 
        If the provided document type, term code, or file type are invalid a 500 code will be sent with an appropriate message
    
    """
    # Ensure user is logged in
    if is_logged_in() < 0:
        return 'User not logged in', 401

    if request.method == 'POST':

        file = request.files['fileKey']
        print('upload starting')
        print(request.get_json())
        print(request)

        document_type = map_document_type(request.args.get('documentType'))
        print(document_type)
        term_code = request.args.get('termCode')
        print(term_code)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = None

            # Make temporary directory
            with tempfile.TemporaryDirectory() as tempdirname:
                # Store pdf into temporary directory
                file.save(os.path.join(tempdirname, filename))

                # Call doc_splitter()
                output_directory = doc_splitter(os.path.join(tempdirname, filename)) 
                success, error, result = banner.bulk_upload(output_directory, document_type, term_code)
                
            if result == 'Invalid Term Code':
                return 'Invalid Term Code', 500
            elif result == 'Invalid Document Type':
                return "Invalid Document Type", 500

            if len(error) == 0:
                    shutil.rmtree(output_directory)
            else:
                file_path = output_directory

            return json.dumps({
                'total': len(success) + len(error),
                'num_success': len(success),
                'num_error': len(error),
                'successes': [str(id_number) for id_number in success],
                'errors': [str(id_number) for id_number in error],
                'file_path': file_path
            })
        
        else:
            return 'Invalid File Type', 500


@app.route('/api/file/download', methods=['POST'])
def zip_error_files():
    """Zips erroneous PID PDFs into a zipfile to be downloaded by the front-end

    Note
    ----
    The POST requests should contain parameters passed along in the format:

        {
            'params': {
                'file_path': String of directory containing erroneous files
            }
        }
    
    Returns
    -------
    zipfile
        A zipfile containing the parsed erroneous PDFs
    
    """
    # Ensure user is logged in
    if is_logged_in() < 0:
        return 'User not logged in', 401
        
    # Obtain file path from request params
    file_directory = request.get_json()['params']['file_path']

    # Create temporary data in memory for zipfile
    data = io.BytesIO()

    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in os.listdir(file_directory):
            print(os.path.join(file_directory, f_name))
            z.write(os.path.join(file_directory, f_name), arcname=f_name)
    
    data.seek(0)

    # Remove erroneous files off VM and remove temporary directory containing
    # them
    shutil.rmtree(file_directory)

    # Return zip file of parsed PDFs
    result = send_file(data, mimetype='application/zip', attachment_filename="parsed.zip", as_attachment=True)

    result.headers["x-suggested-filename"] = "parsed.zip"
    return result


@app.route('/api/login')
def login():
    """Ensures user is logged in and then redirects to parsing page OR redirects
    to CAS for login if not already logged in before CAS redirects here to check 
    again

    Note
    ----
    The GET request should containing the following arguments

        'next'
            The link to redirect to after CAS login
        'ticket'
            The ticket provided by CAS login

    Returns
    -------
    str
        CAS login URL if the user is not logged in yet, username if the user
        is logged in, empty string if the user is invalid

    """
    print('attempting login')
    print(session)
    #Check if user already logged in
    if'username' in session: #Can then compare username to database
        # Already logged in
        username = session['username']
        # session.pop('username', None) #DEBUGGING ONLY
        if is_valid_user(username):
            print("valid user w/ session")
            return username
        else:
            print("invalid user w/ session")
            session.pop('username', None)
            return VIRTUAL_MACHINE_HOSTNAME + '/login'

    #Not already logged in
    next = request.args.get('next')
    ticket = request.args.get('ticket')
    print('The ticket is', ticket)
    if not ticket:
        # No ticket, the request comes from user, send to CAS login
        cas_login_url = cas_client.get_login_url() # generates login URL w/ return page
        return cas_login_url

    #There is a ticket, the request come from CAS as callback
    #need to call 'verify_ticket()' to validate ticket and get user profile
    user, attributes, pgtiou = cas_client.verify_ticket(ticket)
    

    if not user:
        print("No user")
        session.pop('username', None)
        return VIRTUAL_MACHINE_HOSTNAME + '/login'
    else: # Login successfully, redirect according 'next' query parameter
        session['username'] = user
        print(user)
        if is_valid_user(user):
            print("New session w/ valid user")
            return user
        else:
            print("New session w/ invalid user")
            session.pop('username', None)
            return ''


@app.route('/api/logout')
def logout():
    """Forms call to CAS to logout and then performs call and will lead to 
    logout_callback

    Returns
    -------
    str
        The logout url to send the user to for logging out of CAS
    
    """
    print("Logging Out")
    print("Session was:", session)
    session.pop('username', None)
    print("Session now:", session)
    redirect_url = url_for('login', _external=True) #generates URL for endpoint after logout
    cas_logout_url = cas_client.get_logout_url() #gives CAS the URL for redirecting
    print("Redirect to", redirect_url, "after CAS logout using", cas_logout_url)
    return cas_logout_url # sends user to CAS logout which will return to endpoint


@app.route('/api/admin/addtype', methods=['POST'])
def add_type():
    """Adds a document type to the database

    Note
    ----
    The POST request should contain the following information:

        {
            'documentType': String of the new document type to be added,
            'collegeName': College to add the document type to
        }

    Aborts with a 403 error code if the user is not an admin.  This is used to
    protect against direct calls to the API from software such as Postman.

    Returns
    -------
    str
        The unique database ID of the newly added document type

    """
    if not is_admin():
        abort(403)

    if request.method == 'POST':

        tid = db.call_insert_document_type(request.get_json()['documentType'], request.get_json()['collegeName'])
        print(request.get_json())
        return str(tid)


@app.route('/api/admin/adduser', methods=['POST'])
def add_user():
    """Adds a new user based on their VT username to the database

    Note
    ----
    The POST request should contain the following information:

        {
            'role': 'admin' if to be added with admin priveleges, else 'standard',
            'username': VT username of user to be added,
            'college': College the new user belongs to
        }

    Aborts with a 403 error code if the user is not an admin.  This is used to
    protect against direct calls to the API from software such as Postman.

    Returns
    -------
    str
        The unique database ID of the newly added user

    """
    if not is_admin():
        abort(403)

    if request.method == 'POST':
        privilege_level = 0
        
        if request.get_json()['role'] == 'admin':
            privilege_level = 1

        uid = db.call_insert_user(request.get_json()['username'], privilege_level, request.get_json()['college'])
        print(request.get_json())
        return str(uid)

@app.route('/api/admin/addterm', methods=['POST'])
def add_term():
    """Adds a new term code to the database

    Note
    ----
    The POST request should contain the following information:

        {
            'termCode': String of the new term code to be added,
            'collegeName': College list to add the term code to
        }

    Aborts with a 403 error code if the user is not an admin.  This is used to
    protect against direct calls to the API from software such as Postman.

    Returns
    -------
    str
        The unique database ID of the newly added term code

    """ 
    if not is_admin():
        abort(403)

    if request.method == 'POST':
        tid = db.call_insert_term_code(request.get_json()['termCode'], request.get_json()['collegeName'])
        print(request.get_json())
        return str(tid)

@app.route('/api/admin/changerole', methods=['POST'])
def change_role():
    """Changes the role level of the user specified in the database

    Note
    ----
    The POST request should contain the following information:

        {
            'params': {
                'role': New role to set the user to,
                'user': VT username of the user to change
            }
        }

    Aborts with a 403 error code if the user is not an admin.  This is used to
    protect against direct calls to the API from software such as Postman.

    Returns
    -------
    JSON object
        JSON object with ```success: True``` and a 200 status code

    """ 
    if not is_admin():
        abort(403)

    if request.method == 'POST':
        print(request.get_json())

        role = request.get_json()['params']['role']
        level = 0

        if role == 'admin':
            level = 1

        db.call_change_user_privilege_level(request.get_json()['params']['user'], level)
        print(request.get_json())
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/api/admin/removetype', methods=['POST'])
def remove_type():
    """Deletes a document type from the database

    Note
    ----
    The POST request should contain the following information:

        {
            'params': {
                'id': Unique database ID of the document type,
            }
        }

    Aborts with a 403 error code if the user is not an admin.  This is used to
    protect against direct calls to the API from software such as Postman.

    Returns
    -------
    JSON object
        JSON object indicating successful deletion with a 200 status code

    """ 
    if not is_admin():
        abort(403)

    if request.method == 'POST':
        db.call_delete_document_type(int(request.get_json()['params']['id']))
        print(request.get_json())
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/api/admin/removeuser', methods=['POST'])
def remove_user():
    """Deletes a user from the database

    Note
    ----
    The POST request should contain the following information:

        {
            'params': {
                'id': Unique database ID of the user,
            }
        }

    Aborts with a 403 error code if the user is not an admin.  This is used to
    protect against direct calls to the API from software such as Postman.

    Returns
    -------
    JSON object
        JSON object indicating successful deletion with a 200 status code

    """ 
    if not is_admin():
        abort(403)

    if request.method == 'POST':
        db.call_delete_user(int(request.get_json()['params']['id']))
        print(request.get_json())
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/api/admin/removeterm', methods=['POST'])
def remove_term():
    """Deletes a term code from the database

    Note
    ----
    The POST request should contain the following information:

        {
            'params': {
                'id': Unique database ID of the term code,
            }
        }

    Aborts with a 403 error code if the user is not an admin.  This is used to
    protect against direct calls to the API from software such as Postman.

    Returns
    -------
    JSON object
        JSON object indicating successful deletion with a 200 status code

    """ 
    if not is_admin():
        abort(403)

    if request.method == 'POST':
        db.call_delete_term_code(int(request.get_json()['params']['id']))
        print(request.get_json())
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
