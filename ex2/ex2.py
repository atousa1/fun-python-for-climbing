def isEng(string):
    for char in list(string):
        if char.isascii():
            return True
    return False

def Athlete_CheckInfo(*argv):

    from datetime import datetime

    report = True
    output = argv[0]
    # output = [row_num, pFirstName, pLastName, eFirstName, eLastName, ID_num, mob_num, jbirth, gbirth, province, edu, reg_fee, gym]
    message = 'everything is OK'

    row_num = output[0]
    pFirstName = output[1]
    pLastName = output[2]
    eFirstName = output[3]
    eLastName = output[4]
    ID_num = output[5]
    mob_num = output[6]
    jbirth = output[7]
    gbirth = output[8]              
    reg_fee = output[11]
    try:
        int(row_num)
    except ValueError:
        report = False
        message = 'rowNumber is not number'

    if isEng(pFirstName) or isEng(pLastName):
        report = False
        message = 'PersianFirstName or PersianLastName does not containg only Persian letters'

    if not pFirstName.isalpha() or not pLastName.isalpha():
        report = False
        message = 'PersianFirstName or PersianLastName does not contain only letters' 

    if not eFirstName.isalpha() or not eLastName.isalpha():
        report = False
        message = 'EnglishFirstName or EnglishLastName does not contain only letters'  

    try:
        int(ID_num)
    except ValueError:
        report = False
        message = 'ID number is not number'

    try:
        int(mob_num)
    except ValueError:
        report = False
        message = 'Mobile number is not number'

    try:
        datetime.strptime(jbirth, '%Y/%m/%d')
        datetime.strptime(gbirth, '%Y/%m/%d')
    except ValueError:
        report = False
        message = 'G(or J) date of Birth is not correct' 

    try:
        int(reg_fee)
    except ValueError:
        report = False
        message = 'Register Fee is not valid'

    return report, message


def import_Excel():
    import pandas as pd

    invalid_path = True
    while invalid_path == True:
        print('Please Enter Source Excel File Path:')
        excel_Filefolder = input()
        try:
            excelFile = pd.read_excel(excel_Filefolder, sheet_name= 0, header= 0)
            invalid_path = False
        except:
            print('Source File Path is Wrong or There is not such File')
            invalid_path = True
    return excelFile

class athletes:
    def __init__(self, info_list):
        self.row = info_list[0]
        self.pFirstName = info_list[1]
        self.pLastName = info_list[2]
        self.eFirstName = info_list[3]
        self.eLastName = info_list[4]
        self.ID_num = info_list[5]
        self.mob_num = info_list[6]
        self.jbirth = info_list[7]
        self.gbirth = info_list[8]
        self.province = info_list[9]
        self.edu = info_list[10]
        self.reg_fee = info_list[11]
        self.gym = info_list[12]

def assign_class(athlete_info_list):
    athlete = athletes(athlete_info_list)
    athlete_data = (athlete.row, athlete.pFirstName, athlete.pLastName, athlete.eFirstName, athlete.eLastName, athlete.ID_num,
                    athlete.mob_num, athlete.jbirth, athlete.gbirth, athlete.province, athlete.edu, athlete.reg_fee, athlete.gym)
    return athlete_data


### Loading Excel File ###
excel_file = import_Excel()
print(' -----------------\n', 'Excel File Loaded\n', '-----------------')

### Loading Competitors Data into Data Structure ###
num_athletes = excel_file.shape[0]
athletes_newstructure = []
counter = 0

print('Competitors Information is loading...\n-------------------------------------',)
for athlete_idx in range(0, num_athletes):

    athlete_info = excel_file.loc[athlete_idx]
    athlete_list = athlete_info.tolist()
    report, message = Athlete_CheckInfo(athlete_list)
    print('Reading', athlete_list[3], athlete_list[4], 'Info...')

    if report == True:
        athletes_newstructure.append(assign_class(athlete_list))
        print('+', athlete_list[3], athlete_list[4], 'added to database\n')
        counter += 1
    else:
        print('- ERROR:', message, 'for ' + athlete_list[3], athlete_list[4], '--> not added to database\n')


### Creating Database and Loading Data into it ###
def creat_SqliteDb(athletes_data):
    import sqlite3 as sq
    import numpy as np

    sq.register_adapter(np.int64, lambda val: int(val))
    conn = sq.connect('Competitors.db')
    c = conn.cursor()

    try:
        c.execute('''DROP TABLE info''')
    except sq.OperationalError:
        pass

    c.execute('''CREATE TABLE info (
                RowNumber INT,
                PersianFirstName text,
                PersianLastName text,
                EnglishFirstName text,
                EnglishLastName text,
                IDNumber INT,
                MobileNumber INT,
                JalaliBirth date,
                GregorianBirth date,
                Province text,
                Education text,
                RegisterFee REAL,
                Gym text)''')

    c.executemany('''INSERT INTO info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', athletes_data)
    # for row in c.execute('SELECT * FROM info'):
    #     print(row)
    conn.commit()
    conn.close()

creat_SqliteDb(athletes_newstructure)
print('------------------------------', '\n' + str(counter), 'Competitors Added to "info" Table in Competitors.db')
