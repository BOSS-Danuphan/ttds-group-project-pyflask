# Real-time image content search
Text Technologies for Data Science Group Assignment 2018/19

Web app: https://ttds-group-project.herokuapp.com/

## Setting up
##### Clone the repo
```
git clone https://github.com/BOSS-Danuphan/ttds-group-project-pyflask.git
cd ttds-group-project-pyflask
```
##### Initialize a virtualenv
```
# For Windows (cmd)
C:\ttds-group-project-pyflask>.\venv\Scripts\activate.bat
(venv) C:\ttds-group-project-pyflask>

# For Linux
$ source venv/bin/activate
(venv) $
```
##### Install the dependencies
```
(venv) $ pip install -r requirements.txt
```
##### Leave virualenv
```
# For Windows (cmd)
(venv) C:\ttds-group-project-pyflask>deactivate
C:\ttds-group-project-pyflask>

# For Linux
(venv) $ deactivate
$
```
## Development
##### Add local Environment variables
```
$ cp .env-example .env
```
Available configurations:
* `SECRET_KEY`: Application secret key
* `APP_SETTINGS`: can be `config.ProductionConfig` (default, for production), `config.StagingConfig`, `config.DevelopmentConfig` (for local development), `config.TestingConfig`
* `DATETIME_FORMAT`: Display datetime format (default: "%Y-%m-%d %H:%M:%S")
* `INDEXFILE_PATH`: Path to index file (default: "myindex.txt")

#### Start project
```
(venv) $ python app.py
```
