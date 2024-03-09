import streamlit as st
import pandas as pd
from google.cloud import firestore
import webbrowser

db = firestore.Client.from_service_account_json("firestore-key.json")

def add_data(name, link, class_, subject):
    if name and link:
        doc_ref = db.collection("course")
        data = {
            "name": name,
            "link": link,
            "class": class_,
            "subject": subject
        }
        doc_ref.add(data)  # Changed `set` to `add`
        st.write("Data added successfully to Firestore!")
    else:
        st.write("Please enter both name and link to add data to Firestore.")

def main():
    st.title("Add Data to Firestore")
    name = st.text_input("Enter Name:")
    link = st.text_input("Enter Link:")
    class_ = st.text_input("Enter class:")
    subject = st.text_input("Enter subject name:")
    
    if st.button("Add Data"):  # Moved the condition inside `main`
        add_data(name, link, class_, subject)

if __name__ == "__main__":
    main()
