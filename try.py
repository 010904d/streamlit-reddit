import streamlit as st
import pandas as pd
from google.cloud import firestore

db = firestore.Client.from_service_account_json("firestore-key.json")

def add_data(data):
    for index, row in data.iterrows():
        name = row['name']
        link = row['link']
        class_ = row['class']
        subject = row['subject']
        if name and link:
            doc_ref = db.collection("course").document(name)  # Use name as document ID
            data_dict = {
                "name": name,
                "link": link,
                "class": class_,
                "subject": subject
            }
            doc_ref.set(data_dict, merge=True)
            st.write(f"Data '{name}' added successfully to Firestore!")
        else:
            st.write("Please enter both name and link to add data to Firestore.")

def display_data():
    docs_ref = db.collection("course").stream()
    data_list = [doc.to_dict() for doc in docs_ref]
    df = pd.DataFrame(data_list)
    df_display = df[['name', 'class', 'subject', 'link']]  # Display 'name', 'class', 'subject', and 'link' columns
    st.dataframe(df_display)  # Display the DataFrame

def main():
    st.title("Add Data to Firestore")
    st.write("Enter multiple data entries:")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)
        if st.button("Add Data"):
            add_data(data)
        
    if st.button("Display Data"):
        display_data()

if __name__ == "__main__":
    main()













