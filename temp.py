# Python program that runs a GUI that allows the user to choose a file from their computer and then displays the contents of the file in a text box.
import tkinter as tk
import tkinter.filedialog as fd
import csv
import datetime
import os

def generate_dummy_csv():
    # Generate a dummy CSV file for testing.
    with open('dummy.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['student.firstName', 'student.lastName', 'student.birthdate', 'student.grade', 'pcontact.email', 'contacts.firstName', 'contacts.lastName', 'contacts.email', 'contacts.householdPhone'])
        writer.writeheader()
        writer.writerow({'student.firstName': 'John', 'student.lastName': 'Doe', 'student.birthdate': '01/01/2000', 'student.grade': '10', 'pcontact.email': 'johndoe@test.com', 'contacts.firstName': 'Jane', 'contacts.lastName': 'Doe', 'contacts.email': 'janedoe@parent.com', 'contacts.householdPhone': '123-456-7890'})
        writer.writerow({'student.firstName': 'John', 'student.lastName': 'Doe', 'student.birthdate': '01/01/2000', 'student.grade': '9', 'pcontact.email': 'johndoe@test.com', 'contacts.firstName': 'Jim', 'contacts.lastName': 'Doe', 'contacts.email': 'jimdoe@parent.com', 'contacts.householdPhone': '123-456-7891'})
        writer.writerow({'student.firstName': 'Jimmy', 'student.lastName': 'Roe', 'student.birthdate': '01/01/2000', 'student.grade': '11', 'pcontact.email': 'jimmyroe@test.com', 'contacts.firstName': 'Janet', 'contacts.lastName': 'Roe', 'contacts.email': 'janetroe@parent.com', 'contacts.householdPhone': '123-456-7898'})

def open_file():
    file_path = fd.askopenfilename()
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Create a new list to hold the updated rows.
        # Write any errors to text_area

        
        updated_rows = []
        num_guardians = {}

        # Iterate through the rows.
        for row in rows:
            # Check if the email address is already in the list of updated rows.
            if row['pcontact.email'] in [r['Student Email'] for r in updated_rows]:
                # If the email address is already in the list, find the index of the row with the matching email address.
                index = [r['Student Email'] for r in updated_rows].index(row['pcontact.email'])
                # Check if the guardian is already in the row
                if row['contacts.firstName'] in updated_rows[index].values() and row['contacts.lastName'] in updated_rows[index].values() and row['contacts.email'] in updated_rows[index].values():
                    continue
                # Increment the number of guardians for the student.
                num_guardians[row['pcontact.email']] += 1
                # Combine the parent/guardian names from the current row with the parent/guardian names from the row
                num_guardian = num_guardians[row['pcontact.email']]
                updated_rows[index]['Guardian ' + str(num_guardian) + ' First Name'] = row['contacts.firstName']
                updated_rows[index]['Guardian ' + str(num_guardian) + ' Last Name'] = row['contacts.lastName']
                updated_rows[index]['Guardian ' + str(num_guardian) + ' Email'] = row['contacts.email']
                updated_rows[index]['Guardian ' + str(num_guardian) + ' Phone Number (Optional)'] = row['contacts.householdPhone']
            else:
                # If the email address is not already in the list, add the row to the list.
                # First, update birthday format from MM/DD/YYYY to YYYY-MM-DD.
                new_row = {}
                birthday = row['student.birthdate']
                #birthday = datetime.datetime.strptime(birthday, '%m/%d/%Y').strftime('%Y-%m-%d')
                new_row['Student Birthday'] = birthday
                new_row['Student First Name'] = row['student.firstName']
                new_row['Student Last Name'] = row['student.lastName']
                new_row['Student Email'] = row['pcontact.email']
                new_row['Student Grade'] = row['student.grade']
                new_row['Guardian 1 First Name'] = row['contacts.firstName']
                new_row['Guardian 1 Last Name'] = row['contacts.lastName']
                new_row['Guardian 1 Email'] = row['contacts.email']
                new_row['Guardian 1 Phone Number (Optional)'] = row['contacts.householdPhone']
                # Next, add the row to the updated rows list.
                updated_rows.append(new_row)
                # Add the email address to the list of email addresses.
                num_guardians[row['pcontact.email']] = 1

        # Create a new file name for the updated CSV file.
        output_file = os.path.splitext(file_path)[0] + '_updated.csv'

        # Open the output file and write the updated rows to the file.
        new_fieldnames = ["Student First Name", "Student Last Name", "Student Email", "Student Grade", "Student Birthday"]
        max_num_guardians = max(num_guardians.values())
        for i in range(1, max_num_guardians + 1):
            new_fieldnames.append('Guardian ' + str(i) + ' First Name')
            new_fieldnames.append('Guardian ' + str(i) + ' Last Name')
            new_fieldnames.append('Guardian ' + str(i) + ' Email')
            new_fieldnames.append('Guardian ' + str(i) + ' Phone Number (Optional)')
        with open(output_file, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=new_fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

        print('The updated CSV file has been saved to {}.'.format(output_file))
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, 'The updated CSV file has been saved to {}.'.format(output_file))
    except Exception as e:
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, 'An error occurred: {}'.format(str(e)))
        
generate_dummy_csv()
root = tk.Tk()
root.title('File Reader')

text_area = tk.Text(root)
text_area.pack()

open_button = tk.Button(root, text='Open File', command=open_file)
open_button.pack()

# Add an exit button to close the application.
exit_button = tk.Button(root, text='Exit', command=root.quit)
exit_button.pack()

root.mainloop()