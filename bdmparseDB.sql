create table Colleges(
   cid INT NOT NULL AUTO_INCREMENT,
   collegeName VARCHAR(50) NOT NULL,
   PRIMARY KEY ( cid )
);

create table TermCodes(
   tid INT NOT NULL AUTO_INCREMENT,
   termCode VARCHAR(10) NOT NULL,
   collegeID INT NOT NULL,
   PRIMARY KEY ( tid ),
   FOREIGN KEY ( collegeID ) REFERENCES Colleges(cid)
   ON DELETE CASCADE
);

create table DocumentTypes(
   did INT NOT NULL AUTO_INCREMENT,
   documentType VARCHAR(100) NOT NULL,
   collegeID INT NOT NULL,
   PRIMARY KEY ( did ),
   FOREIGN KEY ( collegeID ) REFERENCES Colleges(cid)
   ON DELETE CASCADE
);

create table Users(
   uid INT NOT NULL AUTO_INCREMENT,
   username VARCHAR(50) NOT NULL,
   privilegeLevel INT NOT NULL,
   collegeID INT NOT NULL,
   PRIMARY KEY ( uid ),
   FOREIGN KEY ( collegeID ) REFERENCES Colleges(cid)
);

/*
* On Valid User: Query returns privilege level
* On Invalid User: Query returns the empty set
*/
delimiter //
create procedure validateUser(
   in param_username VARCHAR(50)
)
begin
select U.uid, U.username, C.collegeName, U.privilegeLevel
from Users U, Colleges C
where U.username = param_username and U.collegeID = C.cid;
end //
delimiter ;

/*
* updates the privalege level of a valid user
*/
delimiter //
create procedure changeUserPrivilegeLevel(
   in param_username VARCHAR(50),
   in param_privalegeLevel INT
)
begin 
update Users
set privilegeLevel = param_privalegeLevel
where username = param_username;
end //
delimiter ;

/*
* Allows for inserting a new user into the database
*/
delimiter //
create procedure insertUser(
   in param_username VARCHAR(50),
   in param_privilegeLevel INT,
   in param_collegeName VARCHAR(50)
)
begin
SET @resultCollegeID := (SELECT cid FROM Colleges 
WHERE collegeName = param_collegeName);

INSERT INTO Users (username, privilegeLevel, collegeID)
VALUES (param_username, param_privilegeLevel, @resultCollegeID);

SELECT U.uid
FROM Users U
WHERE U.username = param_username;
end //
delimiter ;

/*
* Allows for inserting a college into the database
*/
delimiter //
create procedure insertCollege(
   in param_collegeName VARCHAR(50)
)
begin
INSERT INTO Colleges (collegeName)
VALUES(param_collegeName);
end //
delimiter ;

/*
* Allows for inserting a document types into the database
*/
delimiter //
create procedure insertDocumentType(
   in param_documentType VARCHAR(100),
   in param_collegeName VARCHAR(50)
)
begin
SET @resultCollegeID := (SELECT cid FROM Colleges 
WHERE collegeName = param_collegeName);

INSERT INTO DocumentTypes (documentType, collegeID)
VALUES(param_documentType, @resultCollegeID);

SELECT did
FROM DocumentTypes
WHERE documentType = param_documentType and collegeID = @resultCollegeID;
end //
delimiter ;

/*
* Allows for inserting a term code into the database
*/
delimiter //
create procedure insertTermCode(
   in param_termCode VARCHAR(10),
   in param_collegeName VARCHAR(50)
)
begin
SET @resultCollegeID := (SELECT cid FROM Colleges 
WHERE collegeName = param_collegeName);

INSERT INTO TermCodes (termCode, collegeID)
VALUES(param_termCode, @resultCollegeID);

SELECT tid
FROM TermCodes
WHERE termCode = param_termCode and collegeID = @resultCollegeID;
end //
delimiter ;

/*
* Allows for deleting a document type from the database
*/
delimiter //
create procedure deleteTermCode(
   in param_tid INT
)
begin
DELETE FROM TermCodes 
WHERE tid = param_tid;
end //
delimiter ;

/*
* Allows for deleting a document type from the database
*/
delimiter //
create procedure deleteDocumentType(
   in param_did INT
)
begin
DELETE FROM DocumentTypes 
WHERE did = param_did;
end //
delimiter ;

/*
* Allows for deleting a user from the database
*/
delimiter //
create procedure deleteUser(
   in param_uid INT
)
begin
DELETE FROM Users U
WHERE U.uid = param_uid;
end //
delimiter ;

/*
* Allows for deleting a college from the database
*/
delimiter //
create procedure deleteCollege(
   in param_cid INT
)
begin
DELETE FROM TermCodes
WHERE collegeID = param_cid;

DELETE FROM DocumentTypes
WHERE collegeID = param_cid;

DELETE FROM Users
WHERE collegeID = param_cid;

DELETE FROM Colleges
WHERE cid = param_cid;
end //
delimiter ;

/*
* select from users, returns username, uid, and whether they are an admin
*/
delimiter //
create procedure getAllUsers()
begin
SELECT U.uid, U.username, U.privilegeLevel FROM Users U;
end //
delimiter ;

/*
* select from users, returns username, uid, and whether they are an admin
* allows for query by college
*/
delimiter //
create procedure getUsersByCollege(
   in param_collegeName VARCHAR(50)
)
begin
SET @resultCollegeID := (SELECT cid FROM Colleges 
WHERE collegeName = param_collegeName);

SELECT U.uid, U.username, U.privilegeLevel FROM Users U
INNER JOIN Colleges C
ON (U.collegeID = C.cid)
WHERE U.collegeID = @resultCollegeID;
end //
delimiter ;

/*
* select from users, returns username, uid, and whether they are an admin
*/
delimiter //
create procedure getAllDocumentTypes()
begin
SELECT did, documentType FROM DocumentTypes;
end //
delimiter ;

/*
* select from document types, returns document types, did
* allows for query by college
*/
delimiter //
create procedure getDocumentTypesByCollege(
   in param_collegeName VARCHAR(50)
)
begin
SELECT D.did, D.documentType FROM DocumentTypes D
INNER JOIN Colleges C
ON (D.collegeID = C.cid)
WHERE C.collegeName = param_collegeName;
end //
delimiter ;

/*
* select from users, returns username, uid, and whether they are an admin
*/
delimiter //
create procedure getAllTermCodes()
begin
SELECT tid, termCode FROM TermCodes;
end //
delimiter ;

/*
* select from termCodes, returns document types, did
* allows for query by college
*/
delimiter //
create procedure getTermCodesByCollege(
   in param_collegeName VARCHAR(50)
)
begin
SELECT T.tid, T.termCode FROM TermCodes T
INNER JOIN Colleges C
ON (T.collegeID = C.cid)
WHERE C.collegeName = param_collegeName;
end //
delimiter ;

/*
* select from users, returns username, uid, and whether they are an admin
*/
delimiter //
create procedure getAllColleges()
begin
SELECT collegeName FROM Colleges;
end //
delimiter ;
