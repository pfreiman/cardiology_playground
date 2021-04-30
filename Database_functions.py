""" Function creates a new table 'ALL_ENTERED_CRITERIA_NAMES'
listing all previously used criteria"""

import sqlite3


def create_criteria_list_table():
    conn = sqlite3.connect('Patient_data.db')
    cur = conn.cursor()

    strsql = "PRAGMA table_info('Pt_Current_Status')"
    cur.execute(strsql)
    dataset = cur.fetchall()
    #   print(dataset)

    fields_list = []
    for row in dataset:
        field_name = row[1]
        fields_list.append(field_name)

    print("List of columns already in db: ", fields_list)
    sqlstr = """CREATE TABLE ALL_ENTERED_CRITERIA_NAMES ("Number"	
        INTEGER,	"Criteria_Name"	TEXT,	PRIMARY KEY("Number" AUTOINCREMENT)
        );"""
    cur.execute("DROP TABLE IF EXISTS 'ALL_ENTERED_CRITERIA_NAMES'")
    cur.execute(sqlstr)
    for item in fields_list:
        item = str(item)
        sqlstr = "INSERT INTO ALL_ENTERED_CRITERIA_NAMES (Criteria_Name) VALUES ('" + item + "')"
        print(item)
        print(sqlstr)
        cur.execute(sqlstr)
        conn.commit()
    conn.close()
    return fields_list


#  create_criteria_list_table()


"""This function validates user entry """

def Validate_entry(x):

    response = x.upper()

    if (response == 'Y') or (response == 'N') or (response.isnumeric() is True):
        entered_value = response
    else:
        print("Entry must be 'y' or 'n' or a number:")
        new_response = input(">>>  ")
        new_response = new_response.upper()
        if (new_response == 'Y') or (new_response == 'N') or (new_response.isnumeric() is True):
            entered_value = new_response
        else:
            entered_value = ""
            print("Unable to make valid entry.")

    # print("entry is:", entered_value)
    return entered_value


# def Validate_entry(x):
#     response = x.upper()
#     print("x is:", x)
#     print("response is:", response)
#
#     if (response == 'Y') or (response == 'N') or (response.isnumeric() is True):
#         entered_value = response
#     else:
#         print("Entry must be 'y' or 'n' or a number:")
#         response = input(">>>  ")
#         if (response == 'Y') or (response == 'N') or (response.isnumeric() is True):
#             entered_value = response
#         else:
#             entered_value = ""
#             print("Unable to make valid entry.")
#
#     print("entry is:", entered_value)
#     return entered_value



