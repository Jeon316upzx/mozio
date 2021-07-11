# Mozio 

# Mozio test LIVE - https://mozio-test1.herokuapp.com/

## Description:

As Mozio expands internationally, we have a growing problem that many transportation suppliers we'd like to integrate cannot give us concrete zipcodes, cities, etc that they serve. To combat this, we'd like to be able to define custom polygons as their "service area" and we'd like for the owners of these shuttle companies to be able to define and alter their polygons whenever they want, eliminating the need for mozio employees to do this boring grunt work.

### INSTALLATION AND LOCAL SETUP

```
Clone the repo
$ virtualenv -p python3 venv      # Create virtualenv
$ source venv/bin/activate        # Activate virtualenv
$ pip install -r requirements.txt # Install python modules
Edit database settings in project/settings.py
$ python manage.py migrate
```

   - VIEW PROJECT DOCUMENTATION HERE :
     https://documenter.getpostman.com/view/11299064/Tzm6nwLv
