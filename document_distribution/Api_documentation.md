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
  - [USER REGISTRATION](#user-registration)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [EMAIL VERIFICATION](#email-verification)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [CHANGE PASSWORD](#change-password)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [RESET PASSWORD](#reset-password)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [RESET PASSWORD CODE VERIFICATION](#reset-password-code-verification)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [LOGOUT](#logout)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [DELETE ACCOUNT](#delete-account)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)

- [FILES](#files)
  - [UPLOAD FILES](#upload-files)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [GET ALL UPLOADED FILES](#get-all-uploaded-files)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [GET FILE](#get-file)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [DOWNLOAD FILE](#download-file)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [DELETE FILE](#delete-file)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [SEARCH FOR FILE](#search-for-file)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [SEND FILE VIA EMAIL](#send-file-via-email)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
   
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

## USER REGISTRATION

### Request Information

| Method | URL                                      |
| ------ | -----------------------------------------|
| POST   | http://127.0.0.1:8000/api/auth/register/ |

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

| Code | Message                                  |
| ---- | ---------------------------------------- |
| 400  | "Password Must be at least 4 characters" |
| 400  | "Invalid email address format"           |
| 400  | "IEmail Already Exist"                   |
| 400  | "Error sending email: {e}, try again"    |
| 400  | "this field is required "                |

### Successful Response Example

```
{
  "status": "success",
  "detail": "email verification code send",
  "data": {
    "email_address": "lbinah@st.ug.edu.gh"
  }
}
```

## EMAIL VERIFICATION

### Request Information

| Method | URL                                      |
| ------ | -----------------------------------------|
| POST   | http://127.0.0.1:8000/api/auth/verify/   |

### Header

| Type         | Property Name    |
| ------------ | ---------------- |
| Allow        | POST, OPTION     |
| Content-Type | Application/Json |
| Vary         | Accept           |

### JSON Body

| Property Name | type   | required | Description                         |
| ------------- | ------ | -------- | ----------------------------------- |
| code          | String | true     | code sent to user email address     |

### Error Responses

| Code | Message                            |
| ---- | -----------------------------------|
| 400  | "the code is required"             |
| 400  | "The code must be numeric"         |
| 400  | "Invalid or Wrong Code Entered"    |

### Successful Response Example

```
{
  "user": {
    "email_address": "lbinah@st.ug.edu.gh"
  },
  "permission": [],
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNDkwMDE1MiwiaWF0IjoxNzE0ODEzNzUyLCJqdGkiOiJjNzlkYTUxYWI1NWI0ZTU0OTVmMjhmYmYzZDk5NDg0NSIsInVzZXJfaWQiOjEwfQ.IQOSNgFuNHbCWf9O-5_PJDJ13xuGEeKiZuldfaSEo-Q",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0ODE0MDUyLCJpYXQiOjE3MTQ4MTM3NTIsImp0aSI6Ijg0MjM4ZDI4MjExYzRiMDliZDUzZGMzMjRlMDczMmMwIiwidXNlcl9pZCI6MTB9.CsUfGAA4yJBfucNedO6dUtX5YkIILo_UtwwnZ78tIok"
}
```

## CHANGE PASSWORD

### Request Information

| Method | URL                                             |
| ------ | ------------------------------------------------|
| POST   | http://127.0.0.1:8000/api/auth/change-password/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |

### JSON Body

| Property Name     | type   | required | Description                         |
| -------------     | ------ | -------- | ----------------------------------- |
| current_password  | String | true     | user current password               |
| new_password      | String | true     | user new  password                  |

### Error Responses

| Code | Message                                       |
| ---- | ----------------------------------------------|
| 400  | "Password Must be at least 4 characters"      |
| 400  | "wrong current password"                      |
| 401  | "Authentication credentials were not provided"|
| 400  | "change password failed"                      |
| 400  | "some field were not provided"                |

### Successful Response Example

```
{
  "status": "success",
  "detail": "Password changed successfully"
}
```

## RESET PASSWORD

### Request Information

| Method | URL                                             |
| ------ | ------------------------------------------------|
| POST   | http://127.0.0.1:8000/api/auth/reset-password/  |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |

### JSON Body

| Property Name     | type   | required | Description                         |
| -------------     | ------ | -------- | ----------------------------------- |
| email_address     | String | true     | email address of the user           |

### Error Responses

| Code | Message                                |
| ---- | ---------------------------------------|
| 400  | "Error sending email: {e}, try again"  |
| 400  | "User Not Found"                       |
| 400  | "some field were not provided"         |

### Successful Response Example

```
{
  "status": "success",
  "detail": "Password Reset Verification Code Sent to Email",
  "data": {
    "email_address": "lbinah@st.ug.edu.gh"
  }
}
```

## RESET PASSWORD CODE VERIFICATION

### Request Information

| Method | URL                                                  |
| ------ | -----------------------------------------------------|
| POST   | http://127.0.0.1:8000/api/auth/reset-password-done/  |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |

### JSON Body

| Property Name     | type   | required | Description                         |
| -------------     | ------ | -------- | ----------------------------------- |
| code              | String | true     | code sent to the user email         |
| new_password      | String | true     | user new password                   |

### Error Responses

| Code | Message                                                |
| ---- | -------------------------------------------------------|
| 400  | "The code must be numeric"                             |
| 400  | "Password Must be at least 4 characters"               |
| 400  | "some field were not provided"                         |
| 400  | "Invalid or Wrong Password Verification Code Entered"  |

### Successful Response Example

```
{
  "status": "success",
  "detail": "Password Reset Successfully"
}
```

##  LOGOUT

### Request Information

| Method | URL                                     |
| ------ | ----------------------------------------|
| POST   | http://127.0.0.1:8000/api/auth/logout/  |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication token |

### JSON Body

| Property Name     | type   | required | Description           |
| -------------     | ------ | -------- | ----------------------|
| refresh           | String | true     | refresh token         |

### Error Responses

| Code | Message                                        |
| ---- | -----------------------------------------------|
| 400  | "Error logging out"                            |
| 400  | "Authentication credentials were not provided" |

### Successful Response Example

```
{
  "detail": "Successfully logged out."
}
```


##  DELETE ACCOUNT

### Request Information

| Method    | URL                                            |
| ------    | -----------------------------------------------|
| DELETE    | http://127.0.0.1:8000/api/auth/delete-account/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication token |


### Error Responses

| Code | Message                                        |
| ---- | -----------------------------------------------|
| 404  | "User Not Found"                            |
| 400  | "Authentication credentials were not provided" |

### Successful Response Example

```
{
    "status": "success",
    "detail": "User Account Deleted  Successfully",
}
```


# Files

## UPLOAD FILES

### Request Information

| Method | URL                                         |
| ------ | --------------------------------------------|
| POST   | http://127.0.0.1:8000/api/file/upload-file/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |

### JSON Body

| Property Name     | type   | required | Description                     |
| -------------     | ------ | -------- | --------------------------------|
| title             | String | true     | title of the file               |
| description       | String | true     | descrisption of the file        |
| type              | String | true     | the type of file (eg,PDF,JPG)   |
| file              | file   | true     | the file to be uploded          |

### Error Responses

| Code | Message                                              |
| ---- | -----------------------------------------------------| 
| 401  | "Authentication credentials were not provided"       |
| 403  | "You do not have permission to perform this action"  |
| 400  | "some field were not provided"                       |

### Successful Response Example

```
 {
  "status": "success",
  "detail": "File Uploaded Successfully"
}
```

## GET ALL UPLOADED FILES

### Request Information

| Method | URL                                           |
| ------ | ----------------------------------------------|
| GET    | http://127.0.0.1:8000/api/file/get-all-files/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |


### Error Responses

| Code | Message                                              |
| ---- | -----------------------------------------------------| 
| 401  | "Authentication credentials were not provided"       |

### Successful Response Example

```
 {
  "status": "success",
  "detail": [
    {
      "id": 8,
      "uploaded_by": {
        "email_address": "admin@gmail.com"
      },
      "title": "Hall Registration",
      "description": "Akuafo Hall",
      "type": "PDF",
      "file": "/media/files/hall.pdf",
      "downloads": 0,
      "emails_sent": 0,
      "created_at": "2024-05-05T17:12:07.413115Z"
    },
    {
      "id": 7,
      "uploaded_by": {
        "email_address": "admin@gmail.com"
      },
      "title": "louis",
      "description": "seyram",
      "type": "PDF",
      "file": "/media/files/files_7eI58CV.pdf",
      "downloads": 4,
      "emails_sent": 2,
      "created_at": "2024-05-03T12:17:28.583979Z"
    },
    {
      "id": 2,
      "uploaded_by": {
        "email_address": "admin@gmail.com"
      },
      "title": "Final Year Project",
      "description": "Before actually sending your email, you need to set up for it. So, let’s add some lines to the settings.py file of your Django app.",
      "type": "PDF",
      "file": "/media/files/dbm.2011.16.pdf",
      "downloads": 1,
      "emails_sent": 3,
      "created_at": "2024-04-30T20:07:53.370747Z"
    }
  ]
}
```

## GET FILE

### Request Information

| Method    | URL                                              |
| ------    | -------------------------------------------------|
| GET       | http://127.0.0.1:8000/api/file/get-file/file_id/ |
| Example   | http://127.0.0.1:8000/api/file/get-file/7/       |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |



### Error Responses

| Code | Message                                              |
| ---- | -----------------------------------------------------| 
| 401  | "Authentication credentials were not provided"       |
| 404  | "File Not Found"                                     |

### Successful Response Example

```
{
  "status": "success",
  "detail": {
    "id": 7,
    "uploaded_by": {
      "email_address": "admin@gmail.com"
    },
    "title": "louis",
    "description": "seyram",
    "type": "PDF",
    "file": "/media/files/files_7eI58CV.pdf",
    "downloads": 4,
    "emails_sent": 2,
    "created_at": "2024-05-03T12:17:28.583979Z"
  }
}
```

## DOWNLOAD FILE

### Request Information

| Method    | URL                                                   |
| ------    | ------------------------------------------------------|
| GET       | http://127.0.0.1:8000/api/file/download-file/file_id/ |
| Example   | http://127.0.0.1:8000/api/file/download-file/8/       |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |



### Error Responses

| Code | Message                                              |
| ---- | -----------------------------------------------------| 
| 401  | "Authentication credentials were not provided"       |
| 404  | "File Not Found"                                     |

### Successful Response Example

```
![alt text](image.png)
```

## DELETE FILE

### Request Information

| Method    | URL                                                 |
| ------    | ----------------------------------------------------|
| DELETE    | http://127.0.0.1:8000/api/file/delete-file/file_id/ |
| Example   | http://127.0.0.1:8000/api/file/delete-file/6/       |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |



### Error Responses

| Code | Message                                              |
| ---- | -----------------------------------------------------| 
| 401  | "Authentication credentials were not provided"       |
| 403  | "You do not have permission to perform this action"  |
| 404  | "File Not Found"                                     |

### Successful Response Example

```
{
  "status": "success",
  "detail": "File Deleted Successfully"
}
```

## SEARCH FOR FILE

### Request Information

| Method | URL                                         |
| ------ | --------------------------------------------|
| POST   | http://127.0.0.1:8000/api/file/search-file/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |

### JSON Body

| Property Name | type   | required | Description                         |
| ------------- | ------ | -------- | ------------------------------------|
| keyword       | String | true     | Enter keyword to search for file    |

### Error Responses

| Code | Message                                         |
| ---- | ------------------------------------------------|
| 400  | "this field is required "                       |
| 401  | "Authentication credentials were not provided"  |
| 404  | "File Not Found"                                |

### Successful Response Example
```
{
  "status": "success",
  "detail": [
    {
      "id": 7,
      "uploaded_by": {
        "email_address": "admin@gmail.com"
      },
      "title": "louis",
      "description": "seyram",
      "type": "PDF",
      "file": "/media/files/files_7eI58CV.pdf",
      "downloads": 4,
      "emails_sent": 2,
      "created_at": "2024-05-03T12:17:28.583979Z"
    }
  ]
}
```


## SEND FILE VIA EMAIL

### Request Information

| Method | URL                                                 |
| ------ | ----------------------------------------------------|
| POST   | http://127.0.0.1:8000/api/file/send-file-via-email/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |

### JSON Body

| Property Name | type   | required | Description                         |
| ------------- | ------ | -------- | ------------------------------------|
| email_address | String | true     | Email Address to send the file to   |
| file_id       | String | true     | the id of the file to be sent       |

### Error Responses

| Code | Message                                         |
| ---- | ------------------------------------------------|
| 400  | "this field is required "                       |
| 400  | "Invalid email address format "                 |
| 400  | "Error sending email try again "                |
| 401  | "Authentication credentials were not provided"  |
| 404  | "File Not Found"                                |

### Successful Response Example
```
{
  "status": "success",
  "detail": "File sent to lbinah@st.ug.edu.gh Successfully"
}
```