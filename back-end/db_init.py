"""
Initializes database with college, initial users and privelege levels, term 
codes, and requested document types. TO BE RUN ONLY ONCE FOR EACH COLLEGE.
"""


from config import DOC_TYPE_STANDARD_SET
import db

################################################################################
# CONFIGURATION SETTINGS FOR INITIAL DATABASE                                  #
################################################################################

# College to be using this instance of BDMParse
COLLEGE = 'College of Engineering'

# List of tuples separated by commas of PIDs for initial users and their roles
# in the form ('pid_username', role) where roles correspond to following
# integers:
# Administrator = 1
# Standard User = 0

# i.e. INITIAL_USERS = [('fakeuser1', 0), ('fakeuser2', 1)]
# fakeuser1 will be a standard user without admin privileges and fakeuser2
# will have admin privileges
INITIAL_USERS = [('user1', 1), ('user2', 1), ('user3', 1), ('user4', 1)]

# List of comma-separated strings denoting initial term codes to be added to database
INITIAL_TERM_CODES = ['202101', '202106']

################################################################################
# Database Initialization Script                                               #
################################################################################

# Add college
db.call_insert_college(COLLEGE)

# Add users
for user in INITIAL_USERS:
    db.call_insert_user(user[0], user[1], COLLEGE)

# Add term codes
for term_code in INITIAL_TERM_CODES:
    db.call_insert_term_code(term_code, COLLEGE)

# Add document types
for doc_type in DOC_TYPE_STANDARD_SET:
    db.call_insert_document_type(doc_type, COLLEGE)