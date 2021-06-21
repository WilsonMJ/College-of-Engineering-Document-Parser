# How to debug flask API with Gunicorn
## Step 1
Stop currently running gunicorn service
```
sudo systemctl stop bdmparse
```

## Step 2
Activate virtual environment for python packages
```
cd back-end
source venv/bin/activate
```

You should see `(venv)` as the prompt

## Step 3
Start gunicorn manually with error and access logs being printed to terminal
```
gunicorn --access-logfile - --error-logfile - --workers=8 -b 127.0.0.1:5000 api:app
```

## Step 4
When done debugging, restart gunicorn service
```
sudo systemctl start bdmparse
```

and ensure service is running
```
sudo systemctl status bdmparse
```

## Step 5
Deactivate virtual environment
```
deactivate
```