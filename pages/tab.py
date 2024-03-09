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
        doc_ref.add(data)
        st.write("Data added successfully to Firestore!")
    else:
        st.write("Please enter both name and link to add data to Firestore.")

def display_data():
    doc_ref = db.collection("course")
    docs = doc_ref.stream()
    data_dict = {}

    for doc in docs:
        data = doc.to_dict()
        subject = data["subject"]
        if subject not in data_dict:
            data_dict[subject] = []
        data_dict[subject].append(data)
    return data_dict

    

def main():
    st.title("study material management")
    tab_titles=["add data","study material"]
    tab1,tab2=st.tabs(tab_titles)

    with tab1:
        st.write("### Add Data")
        name = st.text_input("Name")
        link = st.text_area("Link")
        class_ = st.text_input("Class")
        subject = st.text_input("Subject")
        if st.button("Add"):
            add_data(name, link, class_, subject)
    with tab2:
        st.write("### Study Material")
        data_dict = display_data()
        if tab2:
            tab_labels = list(data_dict.keys())
            selected_tab = st.tabs(tab_labels)
            selected_subject_data = data_dict[selected_tab]
            table_data = []
        for idx, data in enumerate(selected_subject_data, start=1):
            table_data.append([idx, data["name"], data["class"], data["link"]])

        df = pd.DataFrame(table_data, columns=["Serial No", "Name", "Class", "Link"])

        def make_clickable(link):
            return f"[Link]({link})"

        df['Link'] = df['Link'].apply(make_clickable)

        markdown = df.to_markdown(index=False)
        st.markdown(markdown, unsafe_allow_html=True)
if __name__ == "__main__":
    main()




