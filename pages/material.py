import streamlit as st
import pandas as pd
from google.cloud import firestore
from streamlit_card import card

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
        # Check if the 'link' key exists in the document before including it
        if 'link' in data:
            subjects_data[subject].append({"name": data["name"], "class": data["class"], "link": data["link"]})
        else:
            subjects_data[subject].append({"name": data["name"], "class": data["class"]})

    return subjects_data



def main():
    st.title("Study Material Management")
    tab_titles = ["STUDY MATERIAL", "add data"]
    tab1, tab2 = st.tabs(tab_titles)

    with tab2:
        st.write("### Add Data")
        name = st.text_input("Name")
        link = st.text_input("Link")
        class_ = st.text_input("Class")
        subject = st.text_input("Subject")
        if st.button("Add"):
            add_data(name, link, class_, subject)

    with tab1:
        subjects_data = display_data()
        st.write("### Study Material")
        if subjects_data:
            for subject, data in subjects_data.items():
                st.subheader(subject)
                for item in data:
                    card_title = f"Name: {item['name']}"
                    card_content = f"Class: {item['class']}\n[Link]({item['link']})"
                    hasClicked = card(
                        title=card_title,
                        text=card_content,
                        url=item['link']  # Make the card clickable
                    )


if __name__ == "__main__":
    main()






