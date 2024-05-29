import streamlit as st
from google.cloud import firestore
import pandas as pd

db = firestore.Client.from_service_account_json("firestore-key.json")

def get_students_names():
    try:
        docs = db.collection("students").get()
        names = [doc.to_dict()["name"] for doc in docs]
        return names
    except Exception as e:
        st.error(f"Error occurred while fetching student names: {str(e)}")

def add_marks(name, marks_1, marks_2, marks_3, marks_4):
    if name:
        try:
            doc_ref = db.collection("students").where("name", "==", name).get()
            for doc in doc_ref:
                doc_id = doc.id
                data = {
                    "marks_1": marks_1,
                    "marks_2": marks_2,
                    "marks_3": marks_3,
                    "marks_4": marks_4,
                    "total_marks": marks_1 + marks_2 + marks_3 + marks_4
                }
                db.collection("students").document(doc_id).update(data)
            st.write("Marks added successfully to Firestore!")
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
    else:
        st.warning("Please select a student name to add marks.")

def display_student_marks(name):
    if name:
        try:
            doc_ref = db.collection("students").where("name", "==", name).get()
            for doc in doc_ref:
                student = doc.to_dict()
                data = {
                    "Name": [student['name']],
                    "Marks 1": [student.get('marks_1', 'N/A')],
                    "Marks 2": [student.get('marks_2', 'N/A')],
                    "Marks 3": [student.get('marks_3', 'N/A')],
                    "Marks 4": [student.get('marks_4', 'N/A')],
                    "Total Marks": [student.get('total_marks', 'N/A')]
                }
                df = pd.DataFrame(data)
                st.write("Student Marks:")
                st.table(df)
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
    else:
        st.warning("Please select a student name to display marks.")

def main():
    st.title("Student Marks Management")

    tab_titles = ["Display","Add Marks"]
    tab1, tab2 = st.tabs(tab_titles)
    
    with tab2:
        st.write("Add Marks:")
        student_names = get_students_names()
        selected_names = st.multiselect("Select Student Names:", student_names)
        marks_1 = st.number_input("Enter Marks 1:", min_value=0)
        marks_2 = st.number_input("Enter Marks 2:", min_value=0)
        marks_3 = st.number_input("Enter Marks 3:", min_value=0)
        marks_4 = st.number_input("Enter Marks 4:", min_value=0)
        
        add_marks_button = st.button("Add Marks")
        if add_marks_button:
            for name in selected_names:
                add_marks(name, marks_1, marks_2, marks_3, marks_4)

    with tab1:
        st.write("Display Student Marks:")
        student_names = get_students_names()
        selected_name = st.selectbox("Select Student Name:", student_names)
        
        display_marks_button = st.button("Display Marks")
        if display_marks_button:
            display_student_marks(selected_name)

if __name__ == "__main__":
    main()


