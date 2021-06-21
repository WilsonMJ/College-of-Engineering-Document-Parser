# File Structure
## front-end
Angular project built using `ng build --prod`.

If desired to serve locally for development, use `ng serve`.

## config
Contains the necessary files for configuring nginx and gunicorn as system services on the hosting virtual machine as well as a self-signed certificate that will be copied to their proper locations during setup.

## back-end
Python backend that uses Flask to provide Angular frontend with endpoints for running scripts. 

Also contains a ```requirements.txt``` which is used in to install python dependencies into a virtual environment on set up and ```db_init.py``` which is used to initialize MySQL database with initial users, document types, and term codes.  

Both of these files can be seen used in ```setup.sh```

### back-end/html
Contains `.html` files of each python module that can be opened in a web browser for easier reading of documentation.

Also contains ```backend.py``` which is an overall PDF form of mentioned HTML files.

### bdmparseDB.sql
Contains statements for creating tables in the existing MySQL database and stored procedures to be used for communicating with the database.

### exampleProcedureCalls.sql
Contains example procedure calls of the stored procedures provided by ```bdmparseDB.sql```

### How_To_Use.pdf
Contains a walkthrough for general usage of the application.

# Setup
1. Clone the repository with the https link into the home folder
2. Setup mySql using [Digital Ocean walkthrough](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-centos-7)

    2a. Once finished with the setup enter into the db
    ```
    sudo mysql -u root -p
    ```
    NOTE YOU NEED TO CHANGE THE PASSWORD IN THE ```config.py``` TO THE PASSWORD YOU SET JUST NOW
    2b. Run the following commands

    Create database
    ```
    create database insert_db_name_here;
    ```
    NOTE YOU MUST CHANGE THE DATABASE NAME IN ```config.py``` TO WHAT YOU JUST NAMED THE DATABASE
    
    Source SQL procedure file
    ```
    source /home/admin/CoED-M-Document-Parser/bdmparseDB.sql;
    ```
3. Update hostname in ```config.py```

4. Update ```db_init.py``` with initial users of college being added, their roles, and any initial term codes desired. These values will be located in the following variables
    ```
    COLLEGE
    INITIAL_USERS
    INITIAL_TERM_CODES
    ```

5. Give setup shell script privileges
    ```
    chmod u+x setup.sh
    ```
6. Run the script with super user privileges this will take a while
    ```
    sudo ./setup.sh
    ```
7. Then check the status of nginx and gunicorn after the script is done. You should see that both are running.
    ```
    sudo systemctl status nginx
    sudo systemctl status bdmparse
    ```

    6a. If nginx fails to start, error logs are located at ```/var/log/nginx/error.log```

    6b. If gunicorn fails to start, please follow the provided ```debug_flask.md``` to restart gunicorn manually and capture realtime logging.
8. At this point the project should be running and you should be able to access the app at the hostname you defined in the ```config.py```

Currently the server is setup using self-signed certificates. These credentials are located in
    ```
    /etc/ssl/certs/nginx-selfsigned.crt
    /etc/ssl/private/nginx-selfsigned.key
    ```

Upon switching to an official certificate and key, the locations of these official credentials will need to be updated in ```/etc/nginx/nginx.conf``` on lines **53** and **54** that currently appear as so.

```
ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
ssl_certificate_key	/etc/ssl/private/nginx-selfsigned.key;
```