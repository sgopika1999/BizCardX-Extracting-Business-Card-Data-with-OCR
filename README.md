# BizCardX-Extracting-Business-Card-Data-with-OCR

__#Introduction__

BizCardX-Extracting Business Card Data with OCR Bizcard Extraction is a Python application built with Streamlit, EasyOCR, OpenCV, regex function, and MySQL database. It allows users to extract information from business cards and store it in a MySQL database for further analysis. The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.

__#Overview__

In this streamlit web app, you can upload an image of a business card and extract relevant information such as name, designation, company, contact details, location etc from it using easyOCR. You can view, modify or delete the extracted data in this app. This app would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information.

__#1. Tools Installed__

-Virtual Studio code
        
-Python 3.11.3 or higher
        
-MySQL

__#2. Required Libraries__

-streamlit, easyocr, mysql-connector,python, pandas

__#3. Import Libraries__

__#Image handling libraries__

-import easyocr

__#File handling libraries__

-import os

-import re

__#SQL library__

-import mysql.connector as sq

__#Pandas__

-import pandas as pd

__#Dashboard libraries__

-import streamlit as st

-from streamlit_option_menu import option_menu

__#4. ETL and EDA Process__
__# a) Extracting the data__

-Extract the particular business card data by using easyocr.

__# b) Transforming the data__

-After the extraction process, the text data extracted is converted into a structured data in the form of dataframe

__#c) Loading data__

-After the transformation process, the data in the form of dataframe is stored in the MySQL database

__# d) Visualizing, Updating, deleting the data__

-The extracted data can be visualized in the form of dataframe.

-The data can also be updated, modified and deleted from the database.

__#User Guide__

__# Step 1. Home__

-It provides a brief overview of the project and the tools required for the project.

__# Step 2. Upload and Extract__

-In this tab, Browse a a business card file (image) using browse file button and upload the image in upload here section. 
-The image will be processed, required data will be collected. 
-The processed image will appear with collected data in the text format.
-Upoad the data to MySQL by clicking upload to MySQL button.
-The fetched data will appear in the form of data frame.

__# Step 3. Modify__

-In this page, we can alter the data collected from a business card, uplaod the modified data to the SQL database and then we can view the modified data as well.
-Similarly, we can delete the data from MySQL database.
