"""First function gets the list of criteria to be used and adds
any needed new columns to the main pt data database.

Second function gets the headings for each criterion from the database
and sets up a dictionary.
Then retrieves entry input from available data in
the database, and prompts user to enter the remaining values.
Then updates the database and then updates the dictionary.
Returns a completed dictionary of criteria items:values.
"""

import sqlite3

from Database_functions import Validate_entry

LastName = input("Enter Last Name:")
reference_list = input("Enter Criteria List:")


""" This function adds any new criteria items as a column
 to the main patient db"""


def add_new_column_for_new_db_field(reference_list):
    conn = sqlite3.connect('Patient_data.db')
    cur = conn.cursor()

    #  list all the fields already in the large data base

    strsql = "PRAGMA table_info('Pt_Current_Status')"
    cur.execute(strsql)
    dataset = cur.fetchall()
    #   print(dataset)

    fields_list = []
    for row in dataset:
        field_name = row[1]
        fields_list.append(field_name)

    #  print("List of columns already in db: ", fields_list)
    #  return fields_list

    # next, check if the field in the current criteria list is in the large db

    #  next section brings the criteria list into program from db

    criteria_list = []  # this is the list of criteria currently being evaluated

    # table_selected = input("Enter the name of the Criteria List:")
    select_text = 'SELECT Criterion FROM ' + reference_list
    cur.execute(select_text)
    dataset = cur.fetchall()
    # print(dataset)

    for row in dataset:
        criteria_list.append(row[0])
    #  print(criteria_list)

    # now check the criteria list against the fields list in the large db and
    # make a list of the new fields

    new_fields = []
    for item in criteria_list:
        if item not in fields_list:
            new_fields.append(item)
        else:
            continue
    #  print('Fields list already in pt database:', fields_list)
    #  print('New columns to be added to database:', new_fields)

    # next, add new columns to the Pt_Current_Status db for all new fields

    for item in new_fields:
        item = str(item)
        sqlstring = 'ALTER TABLE Pt_Current_Status ADD COLUMN ' + item
        #  print(sqlstring)
        cur.execute(sqlstring)

    conn.commit()
    conn.close()
    print("Database column headings updated.")


"""Function pulls in available data from database and then updates
the dictionary values, asks user to input missing data and then 
updates the database and the dictionary values. 
Returns the completed dictionary"""


def pull_in_available_data(LastName, reference_list):
    conn = sqlite3.connect('Patient_data.db')
    cur = conn.cursor()

    #  next section brings the criteria list into program
    criteria_list = []  # this is the list of criteria which are keys for the dictionary
    criteria_dict = {}  # this is the dictionary of (criteria) keys:values
    missing_items_list = []

    # table_selected = input("Enter the name of the Criteria List:")
    select_text = 'SELECT Criterion FROM ' + reference_list

    cur.execute(select_text)
    dataset = cur.fetchall()
    # print(dataset)

    for row in dataset:
        criteria_list.append(row[0])
        # print("Criteria list is:, ", criteria_list)
    for item in criteria_list:
        strsql = 'SELECT ' + item + ' FROM Pt_Current_Status WHERE NameLast = ? '
        cur.execute(strsql, (LastName,))
        dataset = cur.fetchone()
        # print("Retrieved values: ", str(dataset))
        criteria_dict.update({item: str(dataset[0])})
        #  print(criteria_dict)
        #  print("For pt " + LastName + ", " + item + "=: " + str(dataset[0]))

        # if (dataset[0]) == "":
        #      missing_items_list.append(item)

        field_value = str(dataset[0])  # eliminate the Null entries
        field_value = field_value.upper
        if (field_value != 'Y') and (field_value != 'N'):
            missing_items_list.append(item)
        # print("Missing items:", LastName, missing_items_list)

    if len(missing_items_list) > 0:
        print("""\n\nSome items are missing from the database.
            Enter the required information.""")
        # print("Missing items:", missing_items_list)

    # this next section will let user enter the missing data and update the database:

    for criteria in missing_items_list:
        user_input = input("\n\nEnter value for " + criteria + "  (must be 'y' or 'n' or a number): ")
        entry = Validate_entry(user_input)
        print("Database will be updated.")

        #  Update the large pt database

        strsql = 'UPDATE Pt_Current_Status SET ' + criteria + ' = ? WHERE NameLast = ? '
        #  print(strsql)
        cur.execute(strsql, (entry, LastName))
        conn.commit()

        """update the entries dictionary and return the final
         updated dictionary"""

    for item in criteria_list:
        strsql = 'SELECT ' + item + ' FROM Pt_Current_Status WHERE NameLast = ? '
        cur.execute(strsql, (LastName,))
        dataset = cur.fetchone()
        #  print("Retrieved values: ", str(dataset))
        criteria_dict.update({item: str(dataset[0])})
        #  print(criteria_dict)

    # print("Entered dictionary values are:", criteria_dict)
    conn.close()
    return criteria_dict


add_new_column_for_new_db_field(reference_list)

completed_entries = pull_in_available_data(LastName, reference_list)

print("\n\nFinal summary:\n\nLast Name is:", LastName)
print("\n\n Final dictionary:", completed_entries)


