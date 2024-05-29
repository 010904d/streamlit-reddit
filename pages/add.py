import streamlit as st
from google.cloud import firestore
import pandas as pd

db = firestore.Client.from_service_account_json("firestore-key.json")

def get_max_roll_no():
    try:
        docs = db.collection("students").order_by("roll_no", direction=firestore.Query.DESCENDING).limit(1).get()
        for doc in docs:
            max_roll_no = doc.to_dict()["roll_no"]
            return int(max_roll_no) if max_roll_no else 0
    except Exception as e:
        st.error(f"Error occurred while fetching max roll number: {str(e)}")

def add_data(name, contact_no, age, class_, program, guardian_name, guardian_contact):
    if name and contact_no and age and class_ and program  and guardian_name and guardian_contact:
        try:
            max_roll_no = get_max_roll_no()
            roll_no = max_roll_no + 1
                
            doc_ref = db.collection("students")
            data = {
                "name": name,
                "roll_no": roll_no,
                "contact_no": contact_no,
                "age": age,
                "class": class_,
                "program": program,
                "guardian_name": guardian_name,
                "guardian_contact": guardian_contact
            }
            doc_ref.add(data)
            st.write("Data added successfully to Firestore!")
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
    else:
        st.warning("Please enter all fields to add data to Firestore.")


def search_data(name):
    if name:
        try:
            docs = db.collection("students").where("name", "==", name).get()
            if docs:
                students = []
                for doc in docs:
                    students.append(doc.to_dict())
                return students
            else:
                st.warning("No record found for the provided name.")
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
    else:
        st.warning("Please enter a name to search.")

def display_all_students():
    try:
        students = []
        docs = db.collection("students").get()
        for doc in docs:
            students.append(doc.to_dict())
        if students:
            df = pd.DataFrame(students)
            df = df[['roll_no', 'name', 'age','class', 'contact_no', 'program',  'guardian_name', 'guardian_contact']]
            st.write("All Students:")
            st.dataframe(df)
        else:
            st.warning("No students found.")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")

def main():
    st.title("Student Data Management")

    tab_titles = ["Display", "Search Student", "Add Student"]
    tab1, tab2, tab3 = st.tabs(tab_titles)

    with tab1:
        st.write("Display All Students:")
        display_all_students()

    with tab2:
        st.write("Search Student:")
        name_search = st.text_input("Enter name to search:")

        search = st.button("Search Data")
        if search:
            search_result = search_data(name_search)
            if search_result:
                st.write("Search Result:")
                df = pd.DataFrame(search_result)
                st.table(df)

    with tab3:
        st.write("Add Student Information:")
        name = st.text_input("Enter name:")
        contact_no = st.text_input("Enter contact number:")
        age = st.number_input("Enter age:", min_value=0, max_value=150)
        class_ = st.text_input("Enter class:")
        program = st.text_input("Enter program:")
        guardian_name = st.text_input("Enter guardian name:")
        guardian_contact = st.text_input("Enter guardian contact number:")
        
        add = st.button("Add Data")
        if add:
            add_data(name, contact_no, age, class_, program, guardian_name, guardian_contact)

if __name__ == "__main__":
    main()






