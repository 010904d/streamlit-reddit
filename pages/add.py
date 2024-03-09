import streamlit as st
from google.cloud import firestore
import pandas as pd

db = firestore.Client.from_service_account_json("firestore-key.json")

def add_data(name, age, roll_no, marks, mobile_no):
    if name and age and roll_no and marks and mobile_no:
        doc_ref = db.collection("students")
        data = {
            "name": name,
            "age": age,
            "roll_no": roll_no,
            "marks": marks,
            "mobile_no": mobile_no
        }
        doc_ref.add(data)
        st.write("Data added successfully to Firestore!")
    else:
        st.write("Please enter all fields to add data to Firestore.")

def search_data(roll_no):
    if roll_no:
        doc_ref = db.collection("students").where("roll_no", "==", roll_no).get()
        if doc_ref:
            for doc in doc_ref:
                return doc.to_dict()
        else:
            st.write("No record found for the provided roll number.")
    else:
        st.write("Please enter a roll number to search.")
def display_all_students():
    students = []
    docs = db.collection("students").get()
    for doc in docs:
        students.append(doc.to_dict())
    if students:
        df = pd.DataFrame(students)
        st.write("All Students:")
        st.dataframe(df)
    else:
        st.write("No students found.")

def main():
    st.title("Student Data Management")

    tab_titles = ["Add Student", "Search Student", "Display"]
    tab1, tab2, tab3 = st.tabs(tab_titles)

    with tab1:
        st.write("Add Student Information:")
        name = st.text_input("Enter name:")
        age = st.number_input("Enter age:", min_value=0, max_value=150)
        marks = st.number_input("Enter marks:", min_value=0)
        mobile_no = st.text_input("Enter mobile number:")
        add = st.button("Add Data")
        if add:
            add_data(name, age, marks, mobile_no)

    with tab2:
        st.write("Search Student:")
        roll_no_search = st.text_input("Enter roll number to search:")

        search = st.button("Search Data")
        if search:
            search_result = search_data(roll_no_search)
            if search_result:
                st.write("Search Result:")
                df = pd.DataFrame([search_result])
                st.table(df)

    with tab3:            
        st.write("Display All Students:")
        display = st.button("Display All Students")
        if display:
            display_all_students()

if __name__ == "__main__":
    main()


