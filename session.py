# -*- coding: utf-8 -*-
import json
import requests


class Session(object):
    API_URL = 'http://qa_dashboard.test.thinkmobiles.com:8085'

    def __init__(self, login, password, project_token=None):
        self.headers = {'content-type': 'application/json'}
        self.auth_token = ''
        self.token = project_token
        self.login = login
        self.password = password
        self.sign_in()

    def sign_in(self):
        self.s = requests.Session()
        sign_in_url = self.API_URL + '/api/v1/sign_in'
        userdata = json.dumps({
                                "user": {
                                            "email": self.login,
                                            "password": self.password
                                        }
                              })
        response = self.s.post(sign_in_url, data=userdata, headers=self.headers)
        response = json.loads(response.content)
        self.auth_token = response['auth_token']


    def create_issue(self):
        pass
