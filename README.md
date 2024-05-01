# file-server
Welcome to the File Server project! This document serves as a guide to understand the purpose, functionality, and implementation details of this project.

## Project Objective
The objective of the File Server project is to provide Lizzy's business with a digital platform for distributing various documents, such as wedding cards, admission forms, and more, to users remotely. By creating this platform, Lizzy aims to scale her business efficiently. The platform will allow users to easily access and download documents, streamlining the distribution process.

## Key Features
### For Users (Customers)
1. **User Registration**: New users can effortlessly register by providing necessary details (Email and Password).
2. **User Login**: Registered  users can securely log in to the platform using (Email and Password).
3. **Reset Password**: Users can reset their password when they can not remember
4. **Feed Page**: Authenticated users have access to a feed page where they can view a list of files available for download.
5. **Search Functionality**: Authenticated users can search for specific files within the file server.
6. **Send Files**: Authenticated Users can send files to an email address through the platform.
7. **Change Password**: Authenticated Users can change their password.
8. **Delete Account** User can delete his or her account


## For Admin
1. **File Management**: Admin have the capability to upload files to the server along with titles and descriptions.
2. **Delete Files**: Admin can delete file 
3. **Analytics**: Admin can view analytics such as the number of downloads and the number of emails sent for each file.

## Language and Libraries
Python 
Django 
Javascript
Html
css
## Usage Guidelines
1. **Clone the Repository:**
   ```bash
   https://github.com/BINAH25/file-server.git
   cd file-server

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install the requires packages:**
   ```bash
   cd document_distribution
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser 
   python manage.py runserver
   
