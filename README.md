# EasyQA Python 2 Client Library

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
# Methods
### Issues
#### Get issue
##### Get issues from project
```python
# get all issues from project
easyqa.get_issues()
```
##### Get issue by id
###### fields
[required]
- issue_id - Issue ID

```python
# get one issue by id
easyqa.get_issue_by_id(issue_id)

# get one issue by id in project
easyqa.get_issue_by_id_in_project(issue_id)
```

##### Create issue
###### fields
[required]
- summary - Issue summary

[optional]
- test_object_id - ID test object on site
- description - Issue description
- issue_type - Type of issue
- priority - Issue priority
- severity - Issue severity
- assigner_id - Issue assigner ID
- test.jpg - Name your upload image. Data type must be "jpg"
- test.mp4 - Name your upload video. Data type must be "mp4"

```python
# create one issue
easyqa.create_issue(summary, **kwargs)
```

###### examples
```python
# create one issue with optional fields
easyqa.create_issue(summary='Test', description='test description')
```
##### Update issue
###### fields
[required]
- issue_id - Issue ID
- summary - Issue summary

[optional]
- test_object_id - ID test object on site
- description - Issue description
- issue_type - Type of issue
- priority - Issue priority
- severity - Issue severity
- assigner_id - Issue assigner ID
- status_id - Status ID
- test.jpg - Name your upload image. Data type must be "jpg"
- test.mp4 - Name your upload video. Data type must be "mp4"

```python
# Update issue by id
easyqa.update_issue_by_id(issue_id, summary, **kwargs)
```

###### examples
```python
# update one issue with optional fields
easyqa.update_issue_by_id(issue_id=2, summary='Test', description='test description')

# update one issue by id in project with optional fields
easyqa.update_issue_by_id_in_project(issue_id=2, summary='Test', description='test description')
```

##### Delete issue
###### fields
[required]
- issue_id - Issue ID

###### examples
```python
# delete one issue
easyqa.delete_issue_by_id(issue_id=2)

# delete one issue by id in project
easyqa.delete_issue_by_id_in_project(issue_id=3)
```