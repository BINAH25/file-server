# **FILE SERVER BACKEND API DOCUMENTATION**
<!-- TOC -->
- [**FILE SERVER APPLICATION BACKEND  API DOCUMENTATION**]
- [Accounts](#accounts)
  - [LOGIN](#login)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [CURATOR LOGIN](#curator-login)




# Accounts
## LOGIN

### Request Information

| Method | URL                                   |
| ------ | ------------------------------------- |
| POST   | http://127.0.0.1:8000/api/auth/login/ |

### Header

| Type         | Property Name    |
| ------------ | ---------------- |
| Allow        | POST, OPTION     |
| Content-Type | Application/Json |
| Vary         | Accept           |

### JSON Body

| Property Name | type   | required | Description                  |
| ------------- | ------ | -------- | ---------------------------- |
| email_address | String | true     | The email address of user    |
| password      | String | true     | The password of user         |

### Error Responses

| Code | Message                             |
| ---- | ----------------------------------- |
| 400  | "Invalid Credential"                |
| 400  | "this field is required "           |
| 404  | "User Not Found"                    |

### Successful Response Example

```
{
  "user": {
    "email_address": "admin@gmail.com"
  },
  "permission": [
    "add_blacklistedtoken",
    "add_codeemail",
    "add_contenttype",
    "add_file",
    "add_file",
    "add_group",
    "add_logentry",
    "add_outstandingtoken",
    "add_permission",
    "add_session",
    "add_user",
    "change_blacklistedtoken",
    "change_codeemail",
    "change_contenttype",
    "change_file",
    "change_group",
    "change_logentry",
    "change_outstandingtoken",
    "change_permission",
    "change_session",
    "change_user",
    "delete_blacklistedtoken",
    "delete_codeemail",
    "delete_contenttype",
    "delete_file",
    "delete_file",
    "delete_group",
    "delete_logentry",
    "delete_outstandingtoken",
    "delete_permission",
    "delete_session",
    "delete_user",
    "edit_file",
    "view_blacklistedtoken",
    "view_codeemail",
    "view_contenttype",
    "view_file",
    "view_file",
    "view_group",
    "view_logentry",
    "view_outstandingtoken",
    "view_permission",
    "view_session",
    "view_user"
  ],
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNDg4OTQyOSwiaWF0IjoxNzE0ODAzMDI5LCJqdGkiOiI4Mjg2ZGUxZTEyNDQ0ZTIzYjA1Yzg5YTJiMWYzNmJlOCIsInVzZXJfaWQiOjF9.-fS2fWQIFe5r7l-qTDBP9BGspeA3zNJIg37pG0jHG1w",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0ODAzMzI5LCJpYXQiOjE3MTQ4MDMwMjksImp0aSI6IjI3MjMwOWNlOTNlYTRhM2ZhNGRlNWY5MjE5OTUwOGJlIiwidXNlcl9pZCI6MX0.zj7n4Nd-Kd4Ix5MgIPrpWSLIksy1WGhXk-gWBEB8404"
}
```