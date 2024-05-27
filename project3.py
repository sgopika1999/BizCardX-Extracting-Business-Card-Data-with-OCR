import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import mysql.connector


def image_to_text(path):
    input_img= Image.open(path)

    #converting image to array format
    image_array=np.array(input_img)

    reader=easyocr.Reader(['en'])
    text= reader.readtext(image_array , detail = 0)

    return text,input_img


def extracted_text(text_img):
    extract_dict= {"NAME":[], "DESIGNATION":[],"COMPANY_NAME":[], "CONTACT":[], "EMAIL":[],
                   "WEBSITE":[], "ADDRESS":[], "PINCODE":[]}
    extract_dict["NAME"].append(text_img[0])
    extract_dict["DESIGNATION"].append(text_img[1])

    for i in range(2, len(text_img)):
        if text_img[i].startswith("+") or (text_img[i].replace("-","").isdigit() and '-' in text_img[i]):
            extract_dict["CONTACT"].append(text_img[i])
        elif "@" in text_img[i] and ".com" in text_img[i]:
            extract_dict["EMAIL"].append(text_img[i])
        elif "WWW" in text_img[i] or "www" in text_img[i] or "Www" in text_img[i] or "wWw" in text_img[i] or "wwW" in text_img[i]:
            small=text_img[i].lower()
            extract_dict["WEBSITE"].append(small)

        elif "Tamil Nadu" in text_img[i] or "TamilNadu" in text_img[i] or text_img[i].isdigit():
            extract_dict["PINCODE"].append(text_img[i])

        elif re.match(r'^[A-Za-z]', text_img[i]):
            extract_dict["COMPANY_NAME"].append(text_img[i])

        else:
            remove_colon=re.sub(r'[,;]','',text_img[i])
            extract_dict["ADDRESS"].append(remove_colon)

    for key,value in extract_dict.items():
        if len(value)>0:
            concadenate= " ".join(value)
            extract_dict[key]=[concadenate]

        else:
            value = "NA"
            extract_dict[key]=[value]

    return extract_dict


st.set_page_config(page_title="Extracting Business Card Data with OCR",layout="wide")

st.header(":red[EXTRACTING BUSINESS CARD DATA WITH OCR]")

tab1, tab2 ,tab3,tab4= st.tabs(["HOME","UPLOAD & EXTRACT", "MODIFY","DELETE"])
default_option="HOME"

with tab1:
    col1,col2 = st.columns(2)
    with col1:
        st.image(Image.open("C:\\Users\\NANDHINI\\Downloads\\card1.jpg"), width=550)
        st.markdown("#### :red[**Technologies Used :**] Python, easy OCR, Streamlit, SQL, Pandas.")
    with col2:
        st.markdown("#### :red[**Overview :**] In this streamlit web app you can upload an image of a business card and extract relevant information from it using easyOCR. You can view, modify or delete the extracted data in this app. This app would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information.")


with tab2:
    img = st.file_uploader("Upload the Image",type=["png","jpg","jpeg"])

    if img is not None:
        st.image(img,width=300)
        text_image,input_img=image_to_text(img)

        text_dict=extracted_text(text_image)

        if text_dict:
            st.success("DATA EXTRACTED")

        df=pd.DataFrame(text_dict)

        st.dataframe(df)

        button_1=st.button("upload to database")

        if button_1:

            
            try:
                # Database connection
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="bizcard"
                )
                mycursor = mydb.cursor(buffered=True)

                create_query1 = '''
                    CREATE TABLE IF NOT EXISTS bizcard.project (
                        NAME varchar(225),
                        DESIGNATION varchar(225),
                        COMPANY_NAME varchar(225),
                        CONTACT varchar(225),
                        EMAIL varchar(225),
                        WEBSITE text,
                        ADDRESS text,
                        PINCODE varchar(225)
                    )'''
                mycursor.execute(create_query1)
                mydb.commit()  # Ensure table creation is committed

                # Inserting data
                insert_query1 = '''
                    INSERT INTO bizcard.project (
                        NAME, DESIGNATION, COMPANY_NAME, CONTACT, EMAIL, WEBSITE, ADDRESS, PINCODE
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
                datas = df.values.tolist()[0]
                mycursor.execute(insert_query1, datas)
                mydb.commit()  # Ensure data insertion is committed

                st.success("Uploaded to database successfully")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                mycursor.close()
                mydb.close()
            
with tab3:
    
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bizcard")
    print(mydb)
    mycursor = mydb.cursor(buffered=True)

    select_query="select * from project" 
    mycursor.execute(select_query)
    table=mycursor.fetchall()
    table1=pd.DataFrame(table,columns=("NAME","DESIGNATION","COMPANY_NAME","CONTACT","EMAIL","WEBSITE",
                                        "ADDRESS","PINCODE"))
    col1,col2=st.columns(2)
    with col1:
        selected_name = st.selectbox("select the name", table1["NAME"])

    st.markdown("## Alter the data here")

    df_3 = table1[table1["NAME"]== selected_name]

    if not df_3.empty:
    
        df_4 = df_3.copy()


        col1, col2 = st.columns(2)
        with col1:
            mo_name = st.text_input("Name", df_3["NAME"].iloc[0])
            mo_desi = st.text_input("Designation", df_3["DESIGNATION"].iloc[0])
            mo_comp = st.text_input("Company_name", df_3["COMPANY_NAME"].iloc[0])
            mo_cont = st.text_input("Contact", df_3["CONTACT"].iloc[0])

            df_4["NAME"] = mo_name
            df_4["DESIGNATION"] = mo_desi
            df_4["COMPANY_NAME"] = mo_comp
            df_4["CONTACT"] = mo_cont

        with col2:
            mo_email = st.text_input("Email", df_3["EMAIL"].iloc[0])
            mo_website = st.text_input("Website", df_3["WEBSITE"].iloc[0])
            mo_address = st.text_input("Address", df_3["ADDRESS"].iloc[0])
            mo_pincode = st.text_input("Pincode", df_3["PINCODE"].iloc[0])

            df_4["EMAIL"] = mo_email
            df_4["WEBSITE"] = mo_website
            df_4["ADDRESS"] = mo_address
            df_4["PINCODE"] = mo_pincode   
        

        
        button_3 = st.button("modify")

        if button_3:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bizcard")
            print(mydb)
            mycursor = mydb.cursor(buffered=True)

            update_query = f"UPDATE project SET DESIGNATION=%s, COMPANY_NAME=%s, CONTACT=%s, EMAIL=%s, WEBSITE=%s, ADDRESS=%s, PINCODE=%s WHERE NAME='{selected_name}'"

            updated_data = df_4.iloc[0].tolist()[1:]  
            mycursor.execute(update_query, updated_data)
            mydb.commit()

            st.write(df_4)  
            st.success("MODIFIED SUCCESSFULLY")    
    else:
        st.warning("No data found for the selected name.")
            
with tab4:
    mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="bizcard")
    print(mydb)
    mycursor = mydb.cursor(buffered=True)

    
    select_query="SELECT NAME FROM project"
    mycursor.execute(select_query)
    table1=mycursor.fetchall()
    mydb.commit()

    names=[]

    for i in table1:
        names.append(i[0])

    name_select=st.selectbox("select the name", names,key="name_select_unique_key")

    
    st.write(f" ### You have selected :red[**{name_select}'s**] card to delete")
        
    remove=st.button("Yes,Delete")

    if remove:
        mycursor.execute(f"DELETE FROM PROJECT WHERE NAME = '{name_select}' ")
        mydb.commit()
        st.warning("DELETED")
        st.success(f":red[**{name_select}'s**] Business card information deleted from database.")

            
            








