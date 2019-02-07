import os
import time
import requests
import operator
import secrets
import json as JSON
import requests
from app import app
from google.protobuf.json_format import MessageToJson
from google.cloud import vision

class ImageAnalyser:
    _region = 'westeurope'
    _url = "https://{}.api.cognitive.microsoft.com/vision/v2.0/analyze".format(_region)
    _ms_key = app.config['MS_VISION_KEY']
    _google_key = app.config['GOOGLE_VISION_KEY']
    _maxNumRetries = 2

    def __init__(self):
        pass

    def analyse_with_google_vision(self, urlImage):
        """
        Method that fetches all relevant textual features produced by the Google Vision image analysis API

        Parameters:
        urlImage: Image's url
        """

        if not self._google_key:
            return None

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        params = (
            ('key', self._google_key),
        )

        data = '{"requests":[{"image":{"source":{"imageUri":"' + urlImage + '"}},"features":[{"type":"WEB_DETECTION"},{"type":"LABEL_DETECTION"},{"type":"FACE_DETECTION"},{"type":"LANDMARK_DETECTION"},{"type":"LOGO_DETECTION"},{"type":"SAFE_SEARCH_DETECTION"},{"type":"IMAGE_PROPERTIES"},{"type":"PRODUCT_SEARCH"},{"type":"TEXT_DETECTION"}]}]}'

        response = requests.post('https://vision.googleapis.com/v1/images:annotate', headers=headers, params=params, data=data)

        return JSON.dumps(response.json())

    def analyse_with_ms_vision(self, urlImage):
        """
        Method that fetches all relevant textual features produced by the MS Vision image analysis API

        Parameters:
        urlImage: Image's url
        """

        if not self._ms_key:
            return None

        # API parameters for recognition found in:
        # https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1fa
        params = { 'visualFeatures' : 'Description,Tags,Categories,Faces,ImageType,Color,Adult', 'details' : 'Celebrities,Landmarks' }

        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = self._ms_key
        headers['Content-Type'] = 'application/json'

        json = { 'url': urlImage }
        data = None

        result = self.process_request(json, data, headers, params )

        return JSON.dumps(result)

    def process_request(self, json, data, headers, params):
        """
        Method to process requests to the API

        Parameters:
        json: Contains image url
        data: Set to none - used for image uploading
        headers: Used to pass the key information and the data type request
        """

        retries = 0
        result = None

        while True:
            response = requests.request( 'post', self._url, json = json, data = data, headers = headers, params = params )
            if response.status_code == 429:
                print( "Message: %s" % ( response.json() ) )

                if retries <= self._maxNumRetries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print( 'Error: failed after retrying!' )
                    break

            elif response.status_code == 200 or response.status_code == 201:

                if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                    result = None
                elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                    if 'application/json' in response.headers['content-type'].lower():
                        result = response.json() if response.content else None
                    elif 'image' in response.headers['content-type'].lower():
                        result = response.content
            else:
                print( "Error code: %d" % ( response.status_code ) )
                print( "Message: %s" % ( response.json() ) )

            break

        return result