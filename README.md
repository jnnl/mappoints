# MapPoints

![api](https://github.com/jnnl/mappoints/workflows/api/badge.svg)
![client](https://github.com/jnnl/mappoints/workflows/client/badge.svg)

MapPoints is a simple API that allows users to create, share and discuss geographic locations (points).

This project consists of two main parts: the API backend implementation and a web client demo.

_DISCLAIMER: this is an old, unsupported REST course project and shouldn't be used for anything serious._

## API

The API backend is implemented with [Django REST framework](https://www.django-rest-framework.org/).

A demo instance with a browsable API interface can be found in https://mappoints-api.herokuapp.com.
Please note the API uses a free Heroku dyno that will sleep after 30 minutes of inactivity so initial request(s) may take a while.

The API documentation can be found in https://mappoints.docs.apiary.io/.

Dependencies:
- Django
- Django REST Framework
- DRF Flex Fields
- DRF Nested Resources
- Django CORS Headers
- Django REST Framework JWT
- Furl
- for full list, see api/requirements.txt


### Databases
The default database is SQLite 3.
It is possible to use PostgreSQL 9.6+ as well (used in the Heroku demo instance).

NOTE: if you want to test/deploy with Postgres,
uncomment the postgres section in `api/mappoints/settings_dev.py` under `DATABASES`.
Don't forget to comment/delete the sqlite section above it as well.

### Local install
Prerequisites:
- Python 3.4 or above
- SQLite 3
- PostgreSQL 9.6 (optional)
```
# 1. Clone the repository
git clone https://github.com/jnnl/mappoints

# 2. Create a virtualenv (Python 3)
cd api
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations (if any)
python manage.py migrate

# 5. Start the development server
python manage.py runserver
```

### Testing
Prerequisites:
- Complete above installation steps up to step 4
```
# Collect static resources

python manage.py collectstatic

# Run tests

python manage.py test
```

## Client

A reference web client frontend is implemented with [Vue.js](https://vuejs.org).

A functional demo instance connected to the hosted API is available in https://mappoints.netlify.com.

Test users are available:
- username: user1, password: user1234
- username: user2, password: user1234
- username: user3, password: user1234


Dependencies:
- Vue.js
- Vuex
- Vue-Router
- Vue2-Leaflet
- Vue2-Leaflet-MarkerCluster
- Vue-Toasted
- Axios
- Lodash
- Bootstrap & Bootstrap-Vue
- Moment.js
- for full list see client/package.json

### Local install

Prerequisites:
- Node.js v10 or newer with npm v6 or newer
```
# 1. Clone the repository
git clone https://gitlab.com/jnnl/pwp-mappoints

# 2. Install dependencies
cd client
npm install

# 3. Start the development server
# If you want to use a local backend, change the API_URL constant in client/src/config/index.js.
npm run serve
```
