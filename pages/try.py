import streamlit as st
from google.cloud import firestore
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Initialize Firestore client
db = firestore.Client.from_service_account_json("firestore-key.json")

# Function to fetch student names and their attendance from Firestore
def get_student_data():
    students_ref = db.collection('students')
    students = {student.id: student.to_dict() for student in students_ref.stream()}
    return students

# Function to update attendance for a student on a given date
def update_attendance(student_id, date, status):
    student_ref = db.collection('students').document(student_id)
    student_data = student_ref.get().to_dict()
    
    if 'attendance' in student_data:
        attendance_data = student_data['attendance']
    else:
        attendance_data = {}
    
    # Ensure the status is case-insensitive and convert to uppercase
    status = status.upper()
    if status not in ['P', 'A']:
        st.error(f"Invalid attendance status '{status}' for student ID '{student_id}' on date '{date}'")
        return
    
    # Update or overwrite attendance for the given date
    attendance_data[date] = status
    
    # Calculate total classes attended and attendance percentage
    total_classes_attended = sum(1 for status in attendance_data.values() if status == 'P')
    total_classes = len(attendance_data)
    attendance_percentage = (total_classes_attended / total_classes) * 100 if total_classes > 0 else 0
    
    # Update student document in Firestore
    student_ref.update({
        'attendance': attendance_data,
        'total_classes_attended': total_classes_attended,
        'attendance_percentage': attendance_percentage
    })
    
    return total_classes_attended, attendance_percentage

# Function to add a new date to all students' attendance records
def add_new_date_to_all_students(date):
    students_ref = db.collection('students')
    students = students_ref.stream()
    
    for student in students:
        student_id = student.id
        student_data = student.to_dict()
        
        if 'attendance' in student_data:
            attendance_data = student_data['attendance']
        else:
            attendance_data = {}
        
        # Add the new date with a default value if it doesn't already exist
        if date not in attendance_data:
            attendance_data[date] = 'N/A'
        
        # Update student document in Firestore
        student_ref = db.collection('students').document(student_id)
        student_ref.update({
            'attendance': attendance_data
        })

# Streamlit app
def main():
    st.title('Student Attendance Tracker')
    
    # Initialize session state for date management
    if 'all_dates' not in st.session_state:
        st.session_state.all_dates = []
    if 'formatted_date' not in st.session_state:
        st.session_state.formatted_date = None
    if 'new_date_added' not in st.session_state:
        st.session_state.new_date_added = False
    if 'show_date_filters' not in st.session_state:
        st.session_state.show_date_filters = False

    # Get student data from Firestore
    students = get_student_data()
    
    if students:
        # Collect all dates for which there is attendance data
        all_dates = set()
        for student_data in students.values():
            all_dates.update(student_data.get('attendance', {}).keys())
        st.session_state.all_dates = sorted(all_dates)  # Sort dates for consistent column ordering
        
        # Streamlit input to add a new date
        st.write("### Add New Date")
        new_date = st.date_input("Select Date")
        add_date_button = st.button('Add New Date')
        
        if add_date_button:
            formatted_date = new_date.strftime('%Y-%m-%d')
            if formatted_date not in st.session_state.all_dates:
                add_new_date_to_all_students(formatted_date)
                st.session_state.all_dates.append(formatted_date)
                st.session_state.all_dates = sorted(set(st.session_state.all_dates))  # Ensure no duplicates and sort again
                st.session_state.new_date_added = True
            st.session_state.formatted_date = formatted_date
                
        # Checkbox to toggle "Show All Attendance"
        show_all = st.checkbox('Show All Attendance Records')

        # Checkbox to toggle "Add Filter?"
        if show_all:
            add_filter = st.checkbox('Add Filter?')

            # Only show date range filters if "Add Filter?" is checked
            if add_filter:
                # Add date range filter
                st.write("### Date Range Filter")
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")

                # Add a search button
                search_button = st.button('Search')

                # Fetch data based on the selected date range when the search button is clicked
                if search_button:
                    if start_date and end_date:
                        start_date_str = start_date.strftime('%Y-%m-%d')
                        end_date_str = end_date.strftime('%Y-%m-%d')
                        filtered_data = []
                        for student_id, student_data in students.items():
                            name = student_data['name']
                            attendance = student_data.get('attendance', {})
                            total_classes_attended = student_data.get('total_classes_attended', 0)
                            total_classes_marked = len(attendance)
                            attendance_percentage = student_data.get('attendance_percentage', 0)
                            
                            # Filter attendance data based on the selected date range
                            filtered_attendance = {date: status for date, status in attendance.items() if start_date_str <= date <= end_date_str}
                            
                            # Create a row with name, filtered attendance dates, total attended, and percentage
                            row = {"Name": name}
                            for date in filtered_attendance:
                                row[date] = filtered_attendance[date]
                            row["Total Attended"] = f"{total_classes_attended} / {total_classes_marked}"
                            row["Attendance Percentage"] = f"{attendance_percentage:.2f}%"
                            filtered_data.append(row)
                        
                        # Convert the filtered data to a DataFrame for display
                        filtered_df = pd.DataFrame(filtered_data)
                        
                        # Display the filtered attendance records
                        st.write("### Filtered Attendance Records")
                        st.dataframe(filtered_df)
                        
                        # Hide the "Show All Attendance Records" table when filters are applied
                        st.session_state.show_all = False
                    else:
                        st.warning("Please select both start and end dates for the search.")
        else:
            # Only display the table when "Show All Attendance" is checked
            st.write("Please check 'Show All Attendance Records' to display the table.")
        data = []
        for student_id, student_data in students.items():
            name = student_data['name']
            attendance = student_data.get('attendance', {})
            total_classes_attended = student_data.get('total_classes_attended', 0)
            total_classes_marked = len(attendance)
            attendance_percentage = student_data.get('attendance_percentage', 0)
            
            # Create a row with name, attendance dates, total attended, and percentage
            row = {"Student ID": student_id, "Name": name}
            for date in st.session_state.all_dates:
                if show_all or date == st.session_state.formatted_date:
                    row[date] = attendance.get(date, 'N/A')  # Default to 'N/A' if no attendance record for that date
            row["Total Attended"] = f"{total_classes_attended} / {total_classes_marked}"
            row["Attendance Percentage"] = f"{attendance_percentage:.2f}%"
            data.append(row)
        
        # Convert the data to a DataFrame for display
        df = pd.DataFrame(data)
        
        # Configure ag-Grid options
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_default_column(editable=True, groupable=True)
        gb.configure_grid_options(enableRangeSelection=True)
        gb.configure_selection(selection_mode='multiple', use_checkbox=True)
        gridOptions = gb.build()
        
        # Hide the Student ID column
        gridOptions['columnDefs'][0]['hide'] = True
        
        # Display the grid
        grid_response = AgGrid(
            df,
            gridOptions=gridOptions,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=True
        )
        
        updated_df = grid_response['data']
        selected_rows = grid_response['selected_rows']
        
        if st.button('Save Changes'):
            for i, row in updated_df.iterrows():
                student_id = row['Student ID']
                for date in st.session_state.all_dates:
                    if date in row and row[date] in ['P', 'A', 'p', 'a', 'N/A']:
                        status = row[date].upper()
                        if status in ['P', 'A']:  # Only update if the status is 'P' or 'A'
                            update_attendance(student_id, date, status)
            st.success('Changes saved successfully.')
        
        # Trick to force rerun when new date is added
        if st.session_state.new_date_added:
            st.experimental_rerun()
            st.session_state.new_date_added = False


# Run the Streamlit app
if __name__ == "__main__":
    main()



                




