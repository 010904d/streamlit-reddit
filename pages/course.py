import streamlit as st
import pandas as pd
from google.cloud import firestore

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
        doc_ref.add(data)
        st.write("Data added successfully to Firestore!")
    else:
        st.write("Please enter both name and link to add data to Firestore.")

def display_data():
    doc_ref = db.collection("course")
    docs = doc_ref.stream()
    subjects_data = {}  # Use a dictionary to store data for each subject
    for doc in docs:
        data = doc.to_dict()
        subject = data["subject"]
        if subject not in subjects_data:
            subjects_data[subject] = []
        subjects_data[subject].append(data)

    return subjects_data

def display_subject_data(subjects_data):
    st.write("### Study Material")
    if subjects_data:
        tab_labels = list(subjects_data.keys())
        selected_tab = st.selectbox("Select Subject", tab_labels)
        selected_subject_data = subjects_data[selected_tab]
        table_data = []
        for idx, data in enumerate(selected_subject_data, start=1):
            table_data.append([idx, data["name"], data["class"], data["link"]])

        df = pd.DataFrame(table_data, columns=["Serial No", "Name", "Class", "Link"])

        def make_clickable(link):
            return f"[Link]({link})"

        df['Link'] = df['Link'].apply(make_clickable)

        markdown = df.to_markdown(index=False)
        st.markdown(markdown, unsafe_allow_html=True)

def main():
    st.title("Study Material Management")
    tab_titles=["Add Data", "Study Material"]
    tab1, tab2 = st.tabs(tab_titles)

    with tab1:
        st.write("### Add Data")
        name = st.text_input("Name")
        link = st.text_input("Link")
        class_ = st.text_input("Class")
        subject = st.text_input("Subject")
        if st.button("Add"):
            add_data(name, link, class_, subject)

    with tab2:
        subjects_data = display_data()
        display_subject_data(subjects_data)

if __name__ == "__main__":
    main()


