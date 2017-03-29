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
        self._sign_in()

    def _sign_in(self):
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
    def get_issue(self):
        get_issue_url = self.API_URL + '/api/v1/issues?' + 'token='+self.token + '&auth_token='+self.auth_token,
        return self._req('GET', get_issue_url)

    def get_issue_by_id(self, issue_id):
        get_issue_url = self.API_URL + '/api/v1/issues/'+ issue_id + '?token=' + self.token + '&auth_token=' + self.auth_token,
        return self._req('GET', get_issue_url)

    def get_issue_by_id_in_project(self, issue_id):
        get_issue_url = self.API_URL + '/api/v1/issues/pid' + issue_id + '?token=' + self.token + '&auth_token=' + self.auth_token,
        return self._req('GET', get_issue_url)

    def create_issue(self, summary, **kwargs):
        create_issue_url = self.API_URL + '/api/v1/projects/issues/create'
        required = {
            "token": self.token,
            "auth_token": self.auth_token,
            "summary": summary
        }
        required.update(kwargs)
        data = json.dumps(required)
        return self._req('POST', create_issue_url, data)

    def update_issue_by_id(self,issue_id, summary, **kwargs):
        update_issue_url = self.API_URL + '/api/v1/issues/'+ str(issue_id)
        required = {
            "token": self.token,
            "auth_token": self.auth_token,
            "summary": summary
        }
        required.update(kwargs)
        data = json.dumps(required)
        return self._req('PUT', update_issue_url, data)

    def update_issue_by_id_in_project(self,issue_id, summary, **kwargs):
        update_issue_url = self.API_URL + '/api/v1/issues/pid'+ str(issue_id)
        required = {
            "token": self.token,
            "auth_token": self.auth_token,
            "summary": summary
        }
        required.update(kwargs)
        data = json.dumps(required)
        return self._req('PUT', update_issue_url, data)

    def delete_issue_by_id(self, issue_id):
        delete_issue_url = self.API_URL + '/api/v1/issues/'+ str(issue_id)
        data = json.dumps({
            "token": self.token,
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_issue_url, data)

    def delete_issue_by_id_in_project(self, issue_id):
        delete_issue_url = self.API_URL + '/api/v1/issues/pid' + str(issue_id)
        data = json.dumps({
                "token": self.token,
                "auth_token": self.auth_token
            })
        return self._req('DELETE', delete_issue_url, data)

    def _req(self, method, url, data=None):
        if method == 'POST' or method == 'PUT' or method == 'DELETE':
            return self.s.request(method=method, url=url, data=data, headers=self.headers)

        return self.s.request(method=method, url=url)


                 # ------------------------- Organization --------------------------
    def get_organizations(self):
        get_organizations_url = self.API_URL + '/api/v1/organizations' + '?auth_token=' + self.auth_token
        return self._req('GET', get_organizations_url)

    def show_organization(self, id):
        show_organizations_url = self.API_URL + '/api/v1/organizations/' + id + '?auth_token=' + self.auth_token
        return self._req('GET', show_organizations_url)

    def create_organization(self, title, description=None):
        create_organization_url = self.API_URL + '/api/v1/organizations/'
        data = json.dumps({
            "organization":{
                "title": title,
                "description": description
            },
            "auth_token": self.auth_token
        })
        return self._req('POST', create_organization_url, data)

    def update_organization(self, id, title=None, description=None):
        create_organization_url = self.API_URL + '/api/v1/organizations/' + id
        data = json.dumps({
            "organization": {
                "title": title,
                "description": description
            },
            "auth_token": self.auth_token
        })
        return self._req('PUT', create_organization_url, data)

    def delete_organization(self, id):
        delete_organization_url = self.API_URL + '/api/v1/organizations/' + id
        data = json.dumps({
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_organization_url, data)



                # ------------------------- Projects --------------------------
    def get_projects(self):
        get_projects_url = self.API_URL + '/api/v1/projects' + '?auth_token=' + self.auth_token
        return self._req('GET', get_projects_url)

    def show_project(self, id):
        show_project_url = self.API_URL + '/api/v1/projects/' + id + '?auth_token=' + self.auth_token
        return self._req('GET', show_project_url)

    def create_project(self, org_id, title):
        create_project_url = self.API_URL + '/api/v1/projects/'
        data = json.dumps({
            "organization_id": org_id,
            "project":{
                "title": title
            },
            "auth_token": self.auth_token
        })
        return self._req('POST', create_project_url, data)

    def update_project(self, id, title=None):
        update_project_url = self.API_URL + '/api/v1/projects/' + id
        data = json.dumps({
            "project":{
                "title": title
            },
            "auth_token": self.auth_token
        })
        return self._req('PUT', update_project_url, data)

    def delete_project(self, id):
        delete_project_url = self.API_URL + '/api/v1/projects/' + id
        data = json.dumps({
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_project_url, data)