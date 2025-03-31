#Betty Vuong
#1271673
from ctypes import *
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, Label
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.event import KeyboardEvent
from asciimatics.widgets.multicolumnlistbox import MultiColumnListBox
from datetime import datetime
import sys
import mysql.connector
import os
import ctypes

#for db
conn = None
cursor = None
dbUse = False

# connecting to backend
valid_file = {}

libPath = './libvcparser.so'

vclib = CDLL(libPath)

filesPath = "./cards"

#accessing all the file names for the folder path and placing into an array
file_names = os.listdir(filesPath)

#create a mock version of the c struct to pass data from python into c using ctypes

# duplicate the DateTime struct
class DateTime(Structure):
    _fields_ = [
        ("UTC", c_bool),
        ("isText", c_bool),
        ("date", c_char_p),
        ("time", c_char_p),
        ("text", c_char_p)
    ]

# duplicate property struct
class Property(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("group", c_char_p),
        ("parameters", c_void_p),
        ("values", c_void_p)
    ]

# Define the Card struct
class Card(Structure):
    _fields_ = [
        ("fn", POINTER(Property)),
        ("optionalProperties", ctypes.c_void_p),
        ("birthday", POINTER(DateTime)),
        ("anniversary", POINTER(DateTime))
    ]

# create a helper function for converting a regular Python string to a C string - i.e. a pointer to char
# the Python compiler can usually infer them, but this can be helpful - and will make yor code more readable
def makeCString(str):
    utf8Str = str.encode('utf-8')
    cStr = c_char_p(utf8Str) #c_char_p() is a Ctypes function for createing a value of type c_char_p
    return cStr

#wrapper code
create = vclib.createCard
prop_count = vclib.optionalPropCount
bdayStr = vclib.bdayToStr
anniStr = vclib.anniToStr
fnStr = vclib.fnToStr
pyToNewCard = vclib.pyToCard
editCard = vclib.pyEditCard
dtSql = vclib.dtToSQL
validateCardPtr = vclib.validateCard
delete = vclib.deleteCard

#setting up types for createCard()
#function parameters
create.argtypes = c_char_p, POINTER(POINTER(Card))
#function return
create.restype = c_int

#for validate
validateCardPtr.argtypes = [POINTER(Card)]
validateCardPtr.restype = c_int

#for delete
delete.argtypes = [POINTER(Card)]
delete.restype = None
#for optional prop count
prop_count.argtypes = [POINTER(Card)]
prop_count.restype = c_int

#for birthday to string
bdayStr.argtypes = [POINTER(Card)]
bdayStr.restype = c_char_p

#for anniversary to string
anniStr.argtypes = [POINTER(Card)]
anniStr.restype = c_char_p

#for full name to string
fnStr.argtypes = [POINTER(Card)]
fnStr.restype = c_char_p

#for create new contact
pyToNewCard.argtypes = [POINTER(POINTER(Card)), c_char_p, c_char_p]
pyToNewCard.restype = c_bool

#for edit contact
editCard.argtypes = [POINTER(Card), c_char_p, c_char_p]
editCard.restype = c_bool

#for anniversary to string
dtSql.argtypes = [POINTER(Card), c_bool]
dtSql.restype = c_char_p

class ContactModel():
    def __init__(self):
        return

class LoginView(Frame):
    def __init__(self, screen, model):
        super(LoginView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Login",
                                          reduce_cpu=True)
        self._model = model

        layout = Layout([200], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Username:", "user"))
        layout.add_widget(Text("Password:", "pass"))
        layout.add_widget(Text("DB name:", "db"))

        #error ui

        layout3 = Layout([1])
        self.add_layout(layout3)
        self.error_label = Label("", height = 3)
        layout3.add_widget(self.error_label)

        #options ui
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _ok(self):
        self.save()
        uName = self.data["user"]
        passwd = self.data["pass"]
        dbname = self.data["db"]
        # uName = "bvuong"
        # passwd = "1271673"
        # dbname = "bvuong"
        #connect to db
        try:
            global conn, cursor, dbUse
            conn = mysql.connector.connect(host="dursley.socs.uoguelph.ca", database = dbname,user=uName, password=passwd)
            # configure SQL to automatically immediately commit every change (insert/update/delete)
            conn.autocommit = True
            # prepare a cursor object using cursor() method
            cursor = conn.cursor()
            #create the db tables
            createTable = "CREATE TABLE IF NOT EXISTS FILE(file_id INT AUTO_INCREMENT PRIMARY KEY, file_name VARCHAR(60) NOT NULL, last_modified DATETIME, creation_time DATETIME NOT NULL )"
            try:
                cursor.execute(createTable)
            except mysql.connector.Error as err:
                self.error_label.text = "Something went wrong {}".format(err)
                return
            create_contact_table = "CREATE TABLE IF NOT EXISTS CONTACT(contact_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(256) NOT NULL, birthday DATETIME, anniversary DATETIME, file_id INT NOT NULL, FOREIGN KEY (file_id) REFERENCES FILE(file_id) ON DELETE CASCADE )"
            try:
                cursor.execute(create_contact_table)
            except mysql.connector.Error as err:
                self.error_label.text = "Something went wrong {}".format(err)
                return

        except mysql.connector.Error as err:
            self.error_label.text = "something went wrong when trying to access the database: {}".format(err)
            return
        
        #iterating and calling the backend for the card pointers
        global valid_file, dbUse
        for i in file_names:
            file_name = "cards/"+i
            file_name = makeCString(file_name)
            #create malloc for createCard()
            cardptr = POINTER(Card)()
            createCode = create(file_name, byref(cardptr))
            if createCode == 0 and cardptr:
                #extract information for the database
                vcard = cardptr.contents #dereference
                validCode = validateCardPtr(byref(vcard))
                #validate code
                if validCode != 0:
                    delete(byref(vcard))
                    continue #cont since its invalid
                #create dictionary for the pointer to file
                valid_file[i] = vcard #keep file name and pointer for use
                fn = fnStr(byref(vcard))
                fn = fn.decode('utf-8')
                birthday = dtSql(byref(vcard), True)
                anniversary = dtSql(byref(vcard), False)
                if birthday is not None:
                    birthday = birthday.decode('utf-8')
                if anniversary is not None:
                    anniversary = anniversary.decode('utf-8')

                #db populating
                #for file table
                findFile = "SELECT * FROM FILE WHERE file_name = %s"
                try:
                    cursor.execute(findFile, (i,))
                    file_result = cursor.fetchone()
                    #insert new file
                    if not file_result:
                        file_name_py = "cards/"+i
                        #convert the epoch output to date time in sql
                        file_time = os.path.getmtime(file_name_py)
                        file_time = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
                        insertFile = "INSERT INTO FILE (file_name, last_modified, creation_time) VALUES (%s, %s, %s)"
                        try:
                            cursor.execute(insertFile, (i, file_time, file_time))
                        except mysql.connector.Error as err:
                            self.error_label.text = "Something went wrong {}".format(err)
                            return
                        #for contact table
                        #retrieve the id for the file created
                        file_db_id = cursor.lastrowid
                        contactInsert = "INSERT INTO CONTACT (name, birthday, anniversary, file_id) VALUES (%s, %s, %s, %s)"
                        try:
                            cursor.execute(contactInsert, (fn, birthday, anniversary, file_db_id))
                        except mysql.connector.Error as err:
                            self.error_label.text = "Something went wrong {}".format(err)
                            return
                    else:
                        file_db_id = file_result[0] if file_result else None
                        if file_db_id:
                            updateContact = "UPDATE CONTACT SET name = %s, birthday = %s, anniversary = %s WHERE file_id = %s"
                            try:
                                cursor.execute(updateContact, (fn, birthday, anniversary, file_db_id))
                            except mysql.connector.Error as err:
                                self.error_label.text = "Something went wrong {}".format(err)
                                return
                        else:
                            self.error_label.text = "Something went wrong {}".format(err)
                            return
                    dbUse = True
                except mysql.connector.Error as err:
                   self.error_label.text ="Something went wrong {}".format(err)
                   return
        raise NextScene("Main")

    def _cancel(self):
        self.save()
        global valid_file, dbUse
        dbUse = False
        for i in file_names:
            file_name = "cards/"+i
            file_name = makeCString(file_name)
            #create malloc for createCard()
            cardptr = POINTER(Card)()
            createCode = create(file_name, byref(cardptr))

            if createCode == 0 and cardptr:
                #extract information for the database
                vcard = cardptr.contents #dereference
                validCode = validateCardPtr(byref(vcard))
                if validCode != 0:
                    delete(byref(vcard))
                    continue
                #create dictionary for the pointer to file
                valid_file[i] = vcard #keep file name and pointer for use
                
        raise NextScene("Main")
    
    #for esc feature
    def process_event(self, event):
        self.save()
        if isinstance(event, KeyboardEvent):
            if event.key_code == -1 or event.key_code == 27:
                self._cancel()
            elif event.key_code == 10:
                self._ok()
        return super(LoginView, self).process_event(event)

class ListView(Frame):

    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3, 
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="vCard List")
        self._model = model
        global valid_file

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            [(file,file) for file in valid_file.keys()],
            name="contacts",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit)
        self._edit_button = Button("Edit", self._edit)
        self._queries = Button("DB queries", self._query)
        layout = Layout([200], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Create", self._create), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._queries, 2)
        layout2.add_widget(Button("Exit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        global valid_file
        self._edit_button.disabled = valid_file is None
        self._queries.disabled = dbUse is False
        #self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        global valid_file
        self._list_view.options = [(file,file) for file in valid_file.keys()]
        self._list_view.value = new_value

    def _create(self):
        # self._model.current_id = None
        raise NextScene("Create Contact")

    def _edit(self):
        self.save()
        self._model.current_id = self._list_view.value
        raise NextScene("Edit Contact")

    #@staticmethod
    def _quit(self):
        global valid_file
        for i, card in valid_file.items():
            delete(byref(card))
        #remember to drop tables as well
        if dbUse is True:
            # cursor.execute("drop table CONTACT")
            # cursor.execute("drop table FILE")
            cursor.close()    
            conn.close()
        raise StopApplication("User pressed quit")

    def _query(self):
        self.save()
        self._model.current_id = None
        raise NextScene("DB")
    
    #populate list on gui
    def _addList(self):
        self.save()
        self._model.current_id = self.data["contacts"]
    
    #for esc feature
    def process_event(self, event):
        self.save()
        if isinstance(event, KeyboardEvent):
            if event.key_code == -1 or event.key_code == 27:
                self._quit()
        return super(ListView, self).process_event(event)



class EditView(Frame):
    global conn, cursor, dbUse, valid_file
    def __init__(self, screen, model):
        super(EditView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="vCard Details",
                                          reduce_cpu=True)
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([200], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("File Name: ", "filename", readonly=True))
        layout.add_widget(Text("Contact:", "contact", readonly = False))
        layout.add_widget(Text("Birthday:", "birthday", readonly=True))
        layout.add_widget(Text("Anniversary:", "anniversary", readonly=True))
        layout.add_widget(Text("Other properties:", "other", readonly=True))

        #error ui
        layout3 = Layout([1])
        self.add_layout(layout3)
        self.error_label = Label("", height = 3)
        layout3.add_widget(self.error_label)

        #options ui
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(EditView, self).reset()
        #get file name and pointer for other calls
        file_name = self._model.current_id
        file_path = "cards/" + file_name
        #find the value in dictionary
        cardptr = valid_file[file_name]
        op_prop_count = prop_count(byref(cardptr))
        bday = bdayStr(byref(cardptr))
        bday = bday.decode('utf-8')
        anni = anniStr(byref(cardptr))
        anni = anni.decode('utf-8')
        fn = fnStr(byref(cardptr))
        fn = fn.decode('utf-8')
        self.data = {"filename": self._model.current_id, "other": str(op_prop_count), 
            "birthday": bday, "anniversary": anni, "contact": fn}


    def _ok(self):
        self.save()
        file_name = self.data["filename"]
        contact = self.data["contact"]

        #validate
        if len(file_name) == 0:
            self.error_label.text = "File Name is empty!"
            return
        
        contact_stripped = contact.replace(" ", "")
        if len(contact_stripped) == 0:
            self.error_label.text = "Contact is empty!"
            return
        
        #validate file name
        #ending
        if file_name.endswith(".vcf") == False and file_name.endswith(".vcard") == False:
            self.error_label.text = "File Name is the wrong type! Must be '.vcf' or '.vcard'"
            return
        
        #updating the struct, files, and db
        c_file_name = "cards/"+file_name
        c_file_name= makeCString(c_file_name)
        c_contact = makeCString(contact)
        cardptr = valid_file[file_name] #get pointer
        #call function to make changes
        edit = editCard(byref(cardptr), c_contact, c_file_name)
        if edit == False:
            self.error_label.text = "Changes cannot be made to the Card."
            return
        
        #update db
        if dbUse is True:
            findFile = "SELECT * FROM FILE WHERE file_name = %s"
            try:
                cursor.execute(findFile, (file_name,))
                file_result = cursor.fetchone()
                #update db
                file_db_id = file_result[0] if file_result else None
                if file_db_id:
                    updateContact = "UPDATE CONTACT SET name = %s WHERE file_id = %s"
                    try:
                        cursor.execute(updateContact, (contact, file_db_id))
                    except mysql.connector.Error as err:
                        self.error_label.text = "Something went wrong {}".format(err)
                        return
                    #update modification time
                    modTime = os.path.getmtime("cards/"+file_name)
                    modTime = datetime.fromtimestamp(modTime).strftime('%Y-%m-%d %H:%M:%S')
                    updateFile = "UPDATE FILE SET last_modified = %s WHERE file_id = %s"
                    try:
                        cursor.execute(updateFile, (modTime, file_db_id))
                    except mysql.connector.Error as err:
                        self.error_label.text = "Something went wrong {}".format(err)
                        return
                else:
                    self.error_label.text = "Something went wrong {}".format(err)
                    return
            except mysql.connector.Error as err:
                self.error_label.text = "Something went wrong {}".format(err)
                return
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")
    
    # for esc feature
    def process_event(self, event):
        self.save()
        if isinstance(event, KeyboardEvent):
            if event.key_code == -1 or event.key_code == 27: #esc
                raise NextScene("Main")
            elif event.key_code == 10: #enter
                self._ok()
        return super(EditView, self).process_event(event)

class ContactView(Frame):
    global conn, cursor, dbUse, valid_file
    def __init__(self, screen, model):
        super(ContactView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="vCard Details",
                                          reduce_cpu=True)
        self._model = model
        
        # Create the form for displaying the list of contacts.
        layout = Layout([200], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("File Name: ", "filename"))
        layout.add_widget(Text("Contact:", "contact"))
        layout.add_widget(Text("Birthday:", "birthday", readonly = True))
        layout.add_widget(Text("Anniversary:", "anniversary", readonly = True))
        layout.add_widget(Text("Other properties:", "other", readonly = True))

        #error ui
        layout3 = Layout([1])
        self.add_layout(layout3)
        self.error_label = Label("", height = 3)
        layout3.add_widget(self.error_label)

        #bottom button layout
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()
        
    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ContactView, self).reset()

    def _ok(self):
        self.save()
        # self._model.update_current_contact(self.data)
        file_name = self.data["filename"]
        contact = self.data["contact"]
        #validate
        file_name_stripped = file_name.replace(" ", "")
        if len(file_name_stripped) == 0:
            self.error_label.text = "File Name is empty!"
            return
        
        contact_stripped = contact.replace(" ", "")
        if len(contact_stripped) == 0:
            self.error_label.text = "Contact is empty!"
            return
        file_stripped = file_name.replace(".vcard", "")
        if len(file_stripped) == 0:
            self.error_label.text = "File Name is empty, there's only the extension"
            return
        file_stripped = file_name.replace(".vcf", "")
        if len(file_stripped) == 0:
            self.error_label.text = "File Name is empty, there's only the extension"
            return
        #validate file name
        #ending
        if file_name.endswith(".vcf") == False and file_name.endswith(".vcard") == False:
            self.error_label.text = "File Name is the wrong type! Must be '.vcf' or '.vcard'"
            return

        #file duplicates
        for key in valid_file:
            if key == file_name:
                self.error_label.text = "File Name exists!"
                return
        
        # create new pointer, write to card, and validate
        card_ptr = POINTER(Card)()
        c_file_name = "cards/"+file_name
        c_file_name= makeCString(c_file_name)
        c_contact = makeCString(contact)
        validNewCard = pyToNewCard(byref(card_ptr), c_file_name, c_contact)
        if validNewCard == False:
            self.error_label.text = "New contact cannot be created, please try again."
            return
        else:
            #add to dictionary
            card_ptr = card_ptr.contents #dereference
            valid_file[file_name] = card_ptr
        if dbUse is True:
            #update the db with the new addition
            file_name_py = "cards/"+file_name
            #convert the epoch output to date time in sql
            file_time = os.path.getmtime(file_name_py)
            file_time = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
            insertFile = "INSERT INTO FILE (file_name, last_modified, creation_time) VALUES (%s, %s, %s)"
            try:
                cursor.execute(insertFile, (file_name, file_time, file_time))
            except mysql.connector.Error as err:
                self.error_label.text = "Something went wrong {}".format(err)
                return
            #for contact table
            #retrieve the id for the file created
            file_db_id = cursor.lastrowid
            contactInsert = "INSERT INTO CONTACT (name, birthday, anniversary, file_id) VALUES (%s, %s, %s, %s)"
            try:
                cursor.execute(contactInsert, (contact, None, None, file_db_id))
            except mysql.connector.Error as err:
                self.error_label.text = "Something went wrong {}".format(err)
                return
        
        #reset label
        self.error_label.text = ""
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")
    
    #for esc feature
    def process_event(self, event):
        self.save()
        if isinstance(event, KeyboardEvent):
            if event.key_code == -1 or event.key_code == 27:
                raise NextScene("Main")
            elif event.key_code == 10:
                self._ok()
        return super(ContactView, self).process_event(event)


class DBView(Frame):
    global conn, cursor, dbUse, valid_file
    def __init__(self, screen, model):
        super(DBView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="DB Query View")
        layout = Layout([200], fill_frame=True)
        self.add_layout(layout)

        # self.feedback = Label("", height = screen.height // 3)
        # layout.add_widget(self.feedback)

        self.table = MultiColumnListBox(height = screen.height // 3, options = [], columns = [12, 25, 25, 25, 45],name = 'results_table', add_scroll_bar = True)
        layout.add_widget(self.table)

        #error ui
        layout3 = Layout([1])
        self.add_layout(layout3)
        self.error_label = Label("", height = 3)
        layout3.add_widget(self.error_label)

        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Display All Contacts", self._display_all), 0)
        layout2.add_widget(Button("Find Contacts Born in June", self._June), 1)
        layout2.add_widget(Button("Cancel", self._cancel), 2)
        self.fix()

    def _display_all(self):
        self.save()
        displayQuery = "SELECT CONTACT.contact_id, CONTACT.name, CONTACT.birthday, CONTACT.anniversary, FILE.file_name FROM CONTACT JOIN FILE ON CONTACT.contact_id = FILE.file_id ORDER BY CONTACT.name"
        try:
            cursor.execute(displayQuery)
            tables = cursor.fetchall()
            table = []
            query_table = []
            table.append(("Contact ID", "Name", "Birthday", "Anniversary", "File Name"))
            #format the query results for the multilist column format
            for row in tables:
                table.append((str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))
            
            for i, row in enumerate(table):
                query_table.append((row, i))
            self.table.options = query_table

            #query results and feedback
            #get total count of records in each table
            fileQuery = "SELECT COUNT(file_id) FROM FILE"
            fileCount = []
            contactCount = []
            try:
                cursor.execute(fileQuery)
                fileCount = cursor.fetchone()
            except mysql.connector.Error as err:
                self.error_label.text = "Something went wrong {}".format(err)
                return
            
            contactQuery = "SELECT COUNT(contact_id) FROM CONTACT"
            try:
                cursor.execute(contactQuery)
                contactCount = cursor.fetchone()
            except mysql.connector.Error as err:
                self.error_label.text = "Something went wrong {}".format(err)
                return
            message = "Database has " + str(fileCount[0]) + " files and " + str(contactCount[0]) + " contacts"
            if not tables:
                message = message + "\nDatabase is empty, there are no contacts"
            self.error_label.text = message
        except mysql.connector.Error as err:
            self.error_label.text = "Something went wrong {}".format(err)
        return

    def _June(self):
        self.save()
        displayQuery = "SELECT CONTACT.name, CONTACT.birthday FROM CONTACT JOIN FILE ON CONTACT.contact_id = FILE.file_id WHERE MONTH(CONTACT.birthday) = 6 ORDER BY DATEDIFF(CONTACT.birthday, FILE.last_modified)/365"
        try:
            cursor.execute(displayQuery)
            tables = cursor.fetchall()
            table = []
            query_table = []
            #format the query results for the multilist column format
            table.append(("Contact", "Birthday", "", ""))
            for row in tables:
                table.append((str(row[0]), str(row[1]), "", "", ""))
            
            for i, row in enumerate(table):
                query_table.append((row, i))
            self.table.options = query_table

            #query results and feedback
            #get total count of records in each table
            fileQuery = "SELECT COUNT(file_id) FROM FILE"
            fileCount = []
            contactCount = []
            try:
                cursor.execute(fileQuery)
                fileCount = cursor.fetchone()
            except mysql.connector.Error as err:
                self.error_label.text = "Something went wrong {}".format(err)
                return
            
            contactQuery = "SELECT COUNT(contact_id) FROM CONTACT"
            try:
                cursor.execute(contactQuery)
                contactCount = cursor.fetchone()
            except mysql.connector.Error as err:
                self.error_label.text = "Something went wrong {}".format(err)
                return
            message = "Database has " + str(fileCount[0]) + " files and " + str(contactCount[0]) + " contacts"
            if not tables:
                message = message + ("\nNo contacts born in June are in the database")
            self.error_label.text = message
        except mysql.connector.Error as err:
            self.error_label.text = "Something went wrong {}".format(err)
        return

    def _cancel(self):
        self.save()
        raise NextScene("Main")
    #for esc feature
    def process_event(self, event):
        self.save()
        if isinstance(event, KeyboardEvent):
            if event.key_code == -1 or event.key_code == 27:
                self._cancel()
        return super(DBView, self).process_event(event)
    
def demo(screen, scene):
    global dbUse, conn, cursor
    scenes = [
        Scene([LoginView(screen, contacts)], -1, name="Login"),
        Scene([ListView(screen, contacts)], -1, name="Main"),
        Scene([ContactView(screen, contacts)], -1, name="Create Contact"),
        Scene([DBView(screen, contacts)], -1, name = "DB"),
        Scene([EditView(screen, contacts)], -1, name="Edit Contact"),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


contacts = ContactModel()
last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene