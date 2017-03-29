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
        self.s = requests.Session()
        self.sign_in()

    def sign_in(self):
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

                # ------------------------- Issues --------------------------

    def create_issue(self, summary, **kwargs):
        create_issue_url = self.API_URL + '/api/v1/projects/issues/create'
        required = {
            "token": self.token,
            "auth_token": self.auth_token,
            "summary": summary
        }
        required.update(kwargs)
        data = json.dumps(required)
        response = self._req('POST', create_issue_url, data)

    def delete_issue_by_id(self, issue_id):
        delete_issue_url = self.API_URL + '/api/v1/issues/'+ str(issue_id)
        data = json.dumps({
            "token": self.token,
            "auth_token": self.auth_token
        })
        response = self._req('DELETE', delete_issue_url, data)

    def delete_issue_by_id_in_project(self, issue_id):
        delete_issue_url = self.API_URL + '/api/v1/issues/pid' + str(issue_id)
        data = json.dumps({
                "token": self.token,
                "auth_token": self.auth_token
            })
        response = self._req('DELETE', delete_issue_url, data)

    def _req(self, method, url, data):
        if method == 'POST' or method == 'PUT' or method == 'DELETE':
            response = self.s.request(method=method, url=url, data=data, headers=self.headers)
            return response


                 # ------------------------- Organization --------------------------



                # ------------------------- Projects --------------------------