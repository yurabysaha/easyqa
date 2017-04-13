# -*- coding: utf-8 -*-
import json
import requests


class Session(object):
    DEFAULT_URL = 'https://app.geteasyqa.com'

    def __init__(self, login, password, base_url=DEFAULT_URL, project_token=None):
        self.headers = {'content-type': 'application/json'}
        self.base_url = base_url
        self.auth_token = ''
        self.token = project_token
        self.login = login
        self.password = password
        self.s = requests.Session()
        self._sign_in()

    def _sign_in(self):
        sign_in_url = self.base_url + '/api/v1/sign_in'
        userdata = json.dumps({
            "user": {
                "email": self.login,
                "password": self.password
            }
        })
        response = self.s.post(sign_in_url, data=userdata, headers=self.headers)
        response = json.loads(response.content)
        self.auth_token = response['auth_token']

    def _req(self, method, url, data=None, files=None):
        if method == 'POST' or method == 'PUT' or method == 'DELETE':
            if not files:
                return self.s.request(method=method, url=url, data=data, headers=self.headers, files=files)
            else:
                return self.s.request(method=method, url=url, data=data, files=files)
        return self.s.request(method=method, url=url)

        # ------------------------- Issues --------------------------

    def get_issues(self):
        get_issue_url = self.base_url + '/api/v1/issues?' + 'token=' + self.token + '&auth_token=' + self.auth_token
        return self._req('GET', get_issue_url)

    def get_issue_by_id(self, issue_id):
        get_issue_url = self.base_url + '/api/v1/issues/' + str(
            issue_id) + '?token=' + self.token + '&auth_token=' + self.auth_token
        return self._req('GET', get_issue_url)

    def get_issue_by_id_in_project(self, issue_id):
        get_issue_url = self.base_url + '/api/v1/issues/pid' + str(
            issue_id) + '?token=' + self.token + '&auth_token=' + self.auth_token
        return self._req('GET', get_issue_url)

    def create_issue(self, summary, **kwargs):
        create_issue_url = self.base_url + '/api/v1/projects/issues/create'
        required = {
            "token": self.token,
            "auth_token": self.auth_token,
            "summary": summary
        }
        required.update(kwargs)
        data = json.dumps(required)
        if 'file' in kwargs:
            issue = json.loads(self._req('POST', create_issue_url, data).content)
            attach = json.loads(self.create_issue_attachment(issue['id'], kwargs['file']).content)
            issue['attachments'].append(attach)
            return issue

        return self._req('POST', create_issue_url, data)

    def update_issue_by_id(self, issue_id, summary, **kwargs):
        update_issue_url = self.base_url + '/api/v1/issues/' + str(issue_id)
        required = {
            "token": self.token,
            "auth_token": self.auth_token,
            "summary": summary
        }
        required.update(kwargs)
        data = json.dumps(required)
        if 'file' in kwargs:
            issue = json.loads(self._req('POST', update_issue_url, data).content)
            attach = json.loads(self.create_issue_attachment(issue['id'], kwargs['file']).content)
            issue['attachments'].append(attach)
            return issue
        return self._req('PUT', update_issue_url, data)

    def update_issue_by_id_in_project(self, issue_id, summary, **kwargs):
        update_issue_url = self.base_url + '/api/v1/issues/pid' + str(issue_id)
        required = {
            "token": self.token,
            "auth_token": self.auth_token,
            "summary": summary
        }
        required.update(kwargs)
        data = json.dumps(required)
        return self._req('PUT', update_issue_url, data)

    def delete_issue_by_id(self, issue_id):
        delete_issue_url = self.base_url + '/api/v1/issues/' + str(issue_id)
        data = json.dumps({
            "token": self.token,
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_issue_url, data)

    def delete_issue_by_id_in_project(self, issue_id):
        delete_issue_url = self.base_url + '/api/v1/issues/pid' + str(issue_id)
        data = json.dumps({
            "token": self.token,
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_issue_url, data)

        # ------------------------- Attachment --------------------------

    def create_issue_attachment(self, issue_id, attach_file):
        create_issue_attachment_url = self.base_url + '/api/v1/issues/' + str(issue_id) + '/attachments'
        required = {
            "token": self.token,
            "auth_token": self.auth_token
        }
        upload_file = [('attachment', (attach_file, open(attach_file, 'rb')))]
        return self._req('POST', create_issue_attachment_url, data=required, files=upload_file)

    def delete_attachment(self, attachment_id):
        delete_attachment_url = self.base_url + '/api/v1/attachments/' + str(attachment_id)
        data = json.dumps({
            "token": self.token,
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_attachment_url, data)

        # ------------------------- Organization --------------------------

    def get_organizations(self):
        get_organizations_url = self.base_url + '/api/v1/organizations' + '?auth_token=' + self.auth_token
        return self._req('GET', get_organizations_url)

    def show_organization(self, id):
        show_organizations_url = self.base_url + '/api/v1/organizations/' + str(id) + '?auth_token=' + self.auth_token
        return self._req('GET', show_organizations_url)

    def create_organization(self, title, description=None):
        create_organization_url = self.base_url + '/api/v1/organizations/'
        data = json.dumps({
            "organization": {
                "title": title,
                "description": description
            },
            "auth_token": self.auth_token
        })
        return self._req('POST', create_organization_url, data)

    def update_organization(self, id, title=None, description=None):
        create_organization_url = self.base_url + '/api/v1/organizations/' + str(id)
        data = json.dumps({
            "organization": {
                "title": title,
                "description": description
            },
            "auth_token": self.auth_token
        })
        return self._req('PUT', create_organization_url, data)

    def delete_organization(self, id):
        delete_organization_url = self.base_url + '/api/v1/organizations/' + str(id)
        data = json.dumps({
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_organization_url, data)

        # ------------------------- Projects --------------------------

    def get_projects(self):
        get_projects_url = self.base_url + '/api/v1/projects' + '?auth_token=' + self.auth_token
        return self._req('GET', get_projects_url)

    def show_project(self, id):
        show_project_url = self.base_url + '/api/v1/projects/' + str(id) + '?auth_token=' + self.auth_token
        return self._req('GET', show_project_url)

    def create_project(self, org_id, title):
        create_project_url = self.base_url + '/api/v1/projects/'
        data = json.dumps({
            "organization_id": str(org_id),
            "project": {
                "title": title
            },
            "auth_token": self.auth_token
        })
        return self._req('POST', create_project_url, data)

    def update_project(self, id, title=None):
        update_project_url = self.base_url + '/api/v1/projects/' + str(id)
        data = json.dumps({
            "project": {
                "title": title
            },
            "auth_token": self.auth_token
        })
        return self._req('PUT', update_project_url, data)

    def delete_project(self, id):
        delete_project_url = self.base_url + '/api/v1/projects/' + str(id)
        data = json.dumps({
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_project_url, data)

        # ------------------------- Roles --------------------------

    def get_roles(self, organization_id):
        get_roles_url = self.base_url + "/api/v1/organizations/" + str(organization_id) + \
                        "/roles?auth_token=" + self.auth_token
        return self._req('GET', get_roles_url)

    def show_role(self, id):
        show_role_url = self.base_url + "/api/v1/roles/" + str(id) + "?auth_token=" + self.auth_token
        return self._req('GET', show_role_url)

    def create_organization_role(self, organization_id, user_id, role='user'):
        # Role in organization. Must be "user" or "admin"
        create_organization_role_url = self.base_url + '/api/v1/organizations/' + str(organization_id) + '/roles'
        data = json.dumps(
            {
                "role": role,
                "user_id": str(user_id),
                "auth_token": self.auth_token
            }
        )
        return self._req('POST', create_organization_role_url, data)

    def create_project_role(self, organization_id, user_id, role='tester'):
        # Role in project. Must be "developer", "tester", "viewer" or "project_manager"
        create_project_role_url = self.base_url + '/api/v1/organizations/' + str(organization_id) + '/roles'
        data = json.dumps(
            {
                "role": role,
                "user_id": str(user_id),
                "token": self.token,
                "auth_token": self.auth_token
            }
        )
        return self._req('POST', create_project_role_url, data)

    def update_project_role(self, id, role='tester'):
        # Role in project. Must be "developer", "tester", "viewer" or "project_manager"
        update_project_role_url = self.base_url + '/api/v1/roles/' + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "role": role,
                "auth_token": self.auth_token
            }
        )
        return self._req('PUT', update_project_role_url, data)

    def delete_role(self, id):
        delete_role_url = self.base_url + '/api/v1/roles/' + str(id)
        data = json.dumps({
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_role_url, data)

        # ------------------------- Test Cases --------------------------

    def get_test_cases(self, test_module_id):
        get_test_cases_url = self.base_url + "/api/v1/test_modules/" + str(test_module_id) + "/test_cases?token=" + self.token +\
                        "&auth_token=" + self.auth_token
        return self._req('GET', get_test_cases_url)

    def show_test_case(self, id):
        show_test_case_url = self.base_url + "/api/v1/test_cases/" + str(id) + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', show_test_case_url)

    def create_test_case(self, test_module_id, title,  **kwargs):
        create_test_case_url = self.base_url + "/api/v1/test_modules/" + str(test_module_id) + "/test_cases"
        required ={
                "token": self.token,
                "test_case": {
                    "title": title
                },
                "auth_token": self.auth_token
            }
        required["test_case"].update(kwargs)
        data = json.dumps(required)
        return self._req('POST', create_test_case_url, data)

    def update_test_case(self, test_module_id, title, **kwargs):
        update_test_case_url = self.base_url + "/api/v1/test_cases/" + str(test_module_id)
        required = {
            "token": self.token,
            "test_case": {
                "title": title
            },
            "auth_token": self.auth_token
        }
        required["test_case"].update(kwargs)
        data = json.dumps(required)
        return self._req('PUT', update_test_case_url, data)

    def delete_test_case(self, id):
        delete_test_case_url = self.base_url + '/api/v1/test_cases/' + str(id)
        data = json.dumps({
            "token": self.token,
            "auth_token": self.auth_token
        })
        return self._req('DELETE', delete_test_case_url, data)

        # ------------------------- Statuses --------------------------

    def get_statuses(self):
        get_statuses_url = self.base_url + "/api/v1/statuses?" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', get_statuses_url)

    def show_statuses(self, id):
        show_statuses_url = self.base_url + "/api/v1/statuses/" + str(
            id) + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', show_statuses_url)

    def create_status(self, name):
        create_status_url = self.base_url + '/api/v1/statuses'
        data = json.dumps(
            {
                "token": self.token,
                "status_object": {
                    "name": name
                },
                "auth_token": self.auth_token
            }
        )
        return self._req('POST', create_status_url, data)

    def update_status(self, id, name):
        update_status_url = self.base_url + '/api/v1/statuses/' + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "status_object": {
                    "name": name
                },
                "auth_token": self.auth_token
            }
        )
        return self._req('PUT', update_status_url, data)

    def delete_status(self, id):
        delete_status_url = self.base_url + '/api/v1/statuses/' + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "auth_token": self.auth_token
            }
        )
        return self._req('DELETE', delete_status_url, data)

        # ------------------------- Test Modules --------------------------

    def get_test_modules(self, test_plan_id):
        get_test_modules_url = self.base_url + "/api/v1/test_plans/" + test_plan_id + "/test_modules?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', get_test_modules_url)

    def show_test_module(self, id):
        show_test_module_url = self.base_url + "/api/v1/test_modules/" + str(
            id) + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', show_test_module_url)

    def create_test_module(self, test_plan_id, title, description='', parent_id=None):
        create_test_module_url = self.base_url + '/api/v1/test_plans/' + test_plan_id + "/test_modules"
        data = json.dumps(
            {
                "token": self.token,
                "test_module": {
                    "title": title,
                    "description": description,
                    "parent_id": parent_id
                },
                "auth_token": self.auth_token
            }
        )
        return self._req('POST', create_test_module_url, data)

    def update_test_module(self, id, title, description='', parent_id=None):
        update_test_module_url = self.base_url + '/api/v1/test_modules/' + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "test_module": {
                    "title": title,
                    "description": description,
                    "parent_id": parent_id
                },
                "auth_token": self.auth_token
            }
        )
        return self._req('PUT', update_test_module_url, data)

    def delete_test_module(self, id):
        delete_test_module_url = self.base_url + '/api/v1/test_modules/' + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "auth_token": self.auth_token
            }
        )
        return self._req('DELETE', delete_test_module_url, data)

        # ------------------------- Test Plan --------------------------

    def get_test_plans(self):
        get_test_modules_url = self.base_url + "/api/v1/test_plans" + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', get_test_modules_url)

    def show_test_plan(self, id):
        get_test_modules_url = self.base_url + "/api/v1/test_plans/" + str(id) + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', get_test_modules_url)

    def create_test_plan(self, title, description=''):
        create_test_plans_url = self.base_url + "/api/v1/test_plans"
        data = json.dumps(
            {
                "token": self.token,
                "test_plan": {
                    "title": title,
                    "description": description,
                },
                "auth_token": self.auth_token
            }
        )
        return self._req('POST', create_test_plans_url, data)

    def update_test_plan(self, id, title, description=''):
        create_test_plans_url = self.base_url + "/api/v1/test_plans/" + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "test_plan": {
                    "title": title,
                    "description": description,
                },
                "auth_token": self.auth_token
            }
        )
        return self._req('PUT', create_test_plans_url, data)

    def delete_test_plan(self, id):
        delete_test_plan_url = self.base_url + '/api/v1/test_plans/' + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "auth_token": self.auth_token
            }
        )
        return self._req('DELETE', delete_test_plan_url, data)

        # ------------------------- Test Objects --------------------------

    def get_test_objects(self):
        get_test_objects_url = self.base_url + "/api/v1/test_objects?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', get_test_objects_url)

    def show_test_object(self, id):
        show_test_object_url = self.base_url + "/api/v1/test_objects/" + str(
            id) + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', show_test_object_url)

    def create_test_object_link(self, link):
        create_test_object_url = self.base_url + '/api/v1/test_objects'
        data = json.dumps(
            {
                "token": self.token,
                "link": link,
                "auth_token": self.auth_token
            }
        )
        return self._req('POST', create_test_object_url, data)

    def create_test_object_file(self, build_file):
        create_test_object_file_url = self.base_url + '/api/v1/test_objects'
        data = {
                "token": self.token,
                "auth_token": self.auth_token
            }

        qwerty = {"file": ('build.apk', open(build_file, 'rb'), 'application/vnd.android.package-archive')}
        return self.s.request('POST', url=create_test_object_file_url, data=data, files=qwerty)

    def delete_test_object(self, id):
        delete_test_object_url = self.base_url + '/api/v1/test_objects/' + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "auth_token": self.auth_token
            }
        )
        return self._req('DELETE', delete_test_object_url, data)

        # ------------------------- Test Runs --------------------------

    def get_test_runs(self):
        get_test_runs_url = self.base_url + "/api/v1/test_runs" + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', get_test_runs_url)

    def show_test_run(self, test_run_id):
        get_test_run_url = self.base_url + "/api/v1/test_runs/" + str(test_run_id) + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', get_test_run_url)

    def create_test_run(self, title, **kwargs):
        create_test_run_url = self.base_url + '/api/v1/test_runs'
        required = {
                "token": self.token,
                "test_run": {
                    "title": title,
                },
                "auth_token": self.auth_token
            }
        required.update(kwargs)
        data = json.dumps(required)
        return self._req('POST', create_test_run_url, data)

    def update_test_run(self, id, title, **kwargs):
        update_test_run_url = self.base_url + '/api/v1/test_runs/' + str(id)
        required = {
                "token": self.token,
                "test_run": {
                    "title": title,
                },
                "auth_token": self.auth_token
            }
        required.update(kwargs)
        data = json.dumps(required)
        return self._req('PUT', update_test_run_url, data)

    def delete_test_run(self, id):
        delete_test_run_url = self.base_url + '/api/v1/test_runs/' + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "auth_token": self.auth_token
            }
        )
        return self._req('DELETE', delete_test_run_url, data)

        # ------------------------- Test Run Results --------------------------

    def get_test_run_results(self, test_run_id):
        get_test_run_results_url = self.base_url + "/api/v1/test_runs/" + str(test_run_id) + "/test_run_results" + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', get_test_run_results_url)

    def show_test_run_result(self, test_run_result_id):
        get_test_run_result_url = self.base_url + "/api/v1/test_run_results/" + str(test_run_result_id) + "?token=" + self.token + "&auth_token=" + self.auth_token
        return self._req('GET', get_test_run_result_url)

    # def create_test_run_result(self, test_run_id, test_case_id, result_status=None):
    #     create_test_run_result_url = self.base_url + '/api/v1/test_runs/' + str(test_run_id) + '/test_run_results'
    #     data = json.dumps(
    #         {
    #             "token": self.token,
    #             "test_run_result": {
    #                 "result_status": result_status,
    #                 "test_case_id": test_case_id
    #             },
    #             "auth_token": self.auth_token
    #         }
    #     )
    #     return self._req('POST', create_test_run_result_url, data)

    def update_test_run_result(self, test_run_results_id, test_case_id=None, result_status=None):
        update_test_run_result_url = self.base_url + '/api/v1/test_run_results/' + str(test_run_results_id)
        data = json.dumps(
            {
                "token": self.token,
                "test_run_result": {
                    "result_status": result_status,
                    "test_case_id": test_case_id
                },
                "auth_token": self.auth_token
            }
        )
        return self._req('PUT', update_test_run_result_url, data)

    def delete_test_run_result(self, id):
        delete_test_run_result_url = self.base_url + '/api/v1/test_run_results/' + str(id)
        data = json.dumps(
            {
                "token": self.token,
                "auth_token": self.auth_token
            }
        )
        return self._req('DELETE', delete_test_run_result_url, data)