/*
* testing get procedures
*/
CALL getAllUsers();

CALL getUsersByCollege('College of Engineering');

CALL getAllDocumentTypes();

CALL getDocumentTypesByCollege('College of Engineering');

CALL getAllTermCodes();

CALL getTermCodesByCollege('College of Engineering');

CALL getAllColleges();


/*
* testing delete procedures
*/
CALL deleteUser('username', 'College of Engineering');
CALL getAllUsers();

CALL deleteTermCode('000001', 'College of Engineering');
CALL getAllTermCodes();

CALL deleteDocumentType('Scholarship', 'College of Engineering');
CALL getDocumentTypesByCollege('College of Engineering');

CALL deleteCollege('College of Engineering');
CALL getAllColleges();
CALL getAllUsers();
CALL getAllTermCodes();
CALL getDocumentTypesByCollege('College of Engineering');
