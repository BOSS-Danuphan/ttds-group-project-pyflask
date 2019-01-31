# Real-time image content search
Text Technologies for Data Science Group Assignment 2018/19

Web app: https://ttds-group-project.herokuapp.com/

## Setting up
##### Clone the repo
```
git clone https://github.com/BOSS-Danuphan/ttds-group-project-pyflask.git
cd ttds-group-project-pyflask
```
### For Frontend client
##### Install the dependencies
```
$ npm install
```
### For Backend service
##### Initialize a virtualenv
```
# For Windows (cmd)
C:\ttds-group-project-pyflask>.\venv\Scripts\activate
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
##### Add local Environment variables (For backend service)
```
$ cp .env-example .env
```
Available configurations:
* `SECRET_KEY`: Application secret key
* `APP_SETTINGS`: can be `config.ProductionConfig` (default, for production), `config.StagingConfig`, `config.DevelopmentConfig` (for local development), `config.TestingConfig`
* `DATETIME_FORMAT`: Display datetime format (default: "%Y-%m-%d %H:%M:%S")
* `INDEXFILE_PATH`: Path to index file (default: "myindex.txt")
* `INDEX_WRITER`: Options are FileWriter, AzureBlobWriter, or blank (None). Default is None.
* `TWITTER_CONSUMER_KEY`: Twitter consumer key
* `TWITTER_CONSUMER_SECRET`: Twitter consumer secret
* `TWITTER_ACCESS_TOKEN_KEY`: Twitter access key
* `TWITTER_ACCESS_TOKEN_SECRET`: Twitter access secret
* `MS_VISION_KEY`: Microsoft Vision API key
* `KEEP_ALIVE` (for scheduler job): '1' run ping job, otherwise '0' (default)
* `PING_EVERY_X_MINUTES` (for scheduler job): run ping job itself every X minutes (according to `KEEP_ALIVE`)
* `DOMAIN_URL` (for scheduler job): Domain url
* `AZURE_BLOB_ACCOUNT` = 'Azure blob storage account name'
* `AZURE_BLOB_KEY` = 'Azure blob strage account key'
#### Start project in development
##### Run frontend client independently
```
$ cd client
$ npm start
```
##### Run backend service independently
```
(venv) $ python run.py
```
##### Run both frontend client and backend service together
* Run project as a single service
i.e. backend service will serve frontend minified files (result from build command of create-react-app)
```
(venv) $ npm run dev
```
* Alternatively, run project as 2 separated services
i.e. frontend client and backend service
```
(venv) $ npm run dev:separated
```
#### Start project in production
```
(venv) $ npm run prod
```