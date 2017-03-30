# EasyQA Python 2 Client Library
[[ https://geteasyqa.com/wp-content/themes/easyqa_web/public/img/icons/ic_logo.svg | height = 40px ]]
This document describes Python 2 library that wraps EasyQA REST API.

# Installation
```sh
$ pip install easyqa
```
### Authenticating
```python
from easyqa.session import Session
easyqa = Session('email', 'password', 'project_token')
```

### Get issue
```python
# get one issue by id
easyqa.get_issue_by_id(4)

# get one issue by id in project
easyqa.get_issue_by_id_in_project(3)
```