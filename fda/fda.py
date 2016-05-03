#from django.contrib.auth import authenticate, login, logout
#import urllib.request
import requests, json, urllib, array
import urllib.request
from Crypto.Cipher import ARC4
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random

#import tkinter  #tkMessageBox
from tkinter import *
from tkinter import filedialog #must specify filedialog

def list_reports(user): #still being used
    if user == "":
        #print("heya form list_reports",user)
        exit()
    r2 = requests.get('http://127.0.0.1:8000/fda_index/', params={'username':user}) #Must NOT provide the username here but get it from request
    data = json.loads(r2.text)#may not be necessary
    #print(data)
    if data == '':
        print("There are no reports for you.")
        
    i = 0
    reports_list = []
    for f in data:
        file_dict = f['fields']
        report_name = file_dict['name'] #print all the lists
        #print(i, report_name)
        reports_list.append((i, report_name))
        i += 1
    return (reports_list,data) # this was data before

def filedownload(file_index): #deprecated: only works for one file
    resp = requests.get('http://127.0.0.1:8000/fda_index/', params={'username':user})
    resp_data = json.loads(resp.text)
    #print(resp_data)
    which_report = (resp_data[file_index])
    file_url = 'http://127.0.0.1:8000/media/' + which_report['fields']['path']
    print(file_url)
    
    download_file_url = which_report['fields']['path'].split('/')[1] #extract name
    print(download_file_url)
    
    with urllib.request.urlopen(file_url) as url:
        s = url.read()
    with open(download_file_url, 'wb') as code:
        code.write(s)

def encrypt_file(file, key): #deprecated
    cipher_gen = ARC4.new(key)
    try:
        file_reader = open(file, 'rb')
        hash = SHA256.new(file_reader.read()).digest()
        print("actual signature: ", hash)
        #file_writer = open(file, 'ab')
        #file_writer.write(hash) #append hash to file
        
        
        file_reader = open(file, 'rb')
        file_writer = open(file + ".enc", 'wb')
        for line in file_reader:
            enc_line = cipher_gen.encrypt(line)
            file_writer.write(enc_line)
            
        enc_hash = cipher_gen.encrypt(hash)#append hash to file
        file_writer.write(enc_hash)
        print("encrypted signature: ",enc_hash)

        #cipher_gen = ARC4.new(key)
        #dec_hash = cipher_gen.decrypt(enc_hash)
        #print("attempt to decrypt right after: ", dec_hash)
        
        file_reader.close()
        file_writer.close()
        return True
    except:
        print("Error opening file: %s!" % file)
        return False

def decrypt_file(file, key): #deprecated
    decipher = ARC4.new(key)
    try:
        if (file[-4:] != ".enc"):
            return None
    
        file_reader = open(file, 'rb')
        file_writer = open("DEC_" + file[0:-4], 'wb')
        
        file_length = len(file_reader.read())
        file_reader = open(file, 'rb') #reopens the file
        #print("file size", file_length)
        
        #another writer
        clear_signature = []
        while(True):
            b = file_reader.read(1)
            if b:
                dec_b = decipher.decrypt(b)
                if file_reader.tell() > file_length-32:
                    #print(dec_b)
                    #clear_signature += str(dec_b)
                    clear_signature.append(int.from_bytes(dec_b,'big'))
                    #print(clear_signature)
                else:
                    file_writer.write(dec_b)
            else:
                break
        
        #print((clear_signature))

        """
        file_reader2 = open("DEC_" + file,'rb')
        print("hi",file_reader2.tell())
        hash = SHA256.new(file_reader2.read()).digest()
        print(len(hash), hash)
        file_reader2.close()
        """
        
        file_writer.close()#the file is ready
        file_reader.close()
        
        return clear_signature
    except:
        return None


def login_gui():
    URL = "http://localhost:8000/users/fda_login"
    URL_download = "http://localhost:8000/fda_index"
    client = requests.session()

    user = e1.get()
    pwd = e2.get()

    #====DEBUG====
    #user = 'admin'
    #pwd = 'admin'
    #====END OF DEBUG ====
    
    login = {'username':user,'password':pwd}
    r = client.post(URL, data=login)
    global username #bad practice
    username =""
    #print("hello")
    if r.text == "success": #If login is successful
        message_gui("Welcome" +" "+ login['username']+"!") #TODO: implement dialogue box
        username = user
        
        top.destroy()
        
    else:
        message_gui("Login failed")

def get_creator_gui(index):
    r2 = requests.get('http://127.0.0.1:8000/fda_creator/', params={'index':index})
    return r2.text

def get_folder_gui(index):
    r2 = requests.get('http://127.0.0.1:8000/fda_folder/', params={'index':index})
    return r2.text
    

def display_details_gui(app, data, file_index, list_detail):
    #print(file_index)
    #print(data)
    which_report = data[file_index]
    #print(which_report)
    """
    i=0
    for var in list_detail:
        list_thin
        var.set(field)#query data with file index
        i+=1
    """
    field_labels = ['name', 'folder', 'description', 'longDescription',
                    'creator', 'time', 'private', 'encrypted']
    i=0
    #for field in which_report['fields']:
    while(i<8):
        
        if i == 4:
            creator = get_creator_gui(which_report['fields'][field_labels[i]])
            #print(creator)
            #field = which_report['fields'][field_labels[i]]
            list_detail[i].set(creator)
            i+=1
            continue
        
        if i == 1:
            if which_report['fields'][field_labels[i]] != None:
                folder = get_folder_gui(which_report['fields'][field_labels[i]])
                #field = which_report['fields'][field_labels[i]]
                list_detail[i].set('folder')
                i+=1
                continue
        
        field = which_report['fields'][field_labels[i]]
        list_detail[i].set(field )#which_report['fields'][field])
        #print(field,":",which_report['fields'][field])
        #Label(root, text=field+":").grid(row=i, column=3)
        #Label(root, text=which_report['fields'][field]).grid(row=i, column=4)
        i+=1
    return
    

def display_files_gui(app,report_name, listbox, data, file_index, list_detail):

    display_details_gui(app,data,file_index, list_detail)
    
    URL_FILES = "http://localhost:8000/fda_attachments"
    r = requests.get(URL_FILES, params={'report_name':report_name})
    data = json.loads(r.text)
    #print(data)
    
    if data == '':
        print("There are no files.")
        
    i = 0
    attachments_list = []

    """
    while i<5:
        Label(app).grid(row=i+2,column=1).grid_remove()
        i+=1
    i=0
    """
    
    for f in data:
        attach_dict = f['fields']
        attach_name = attach_dict['path']
        #print(i, attach_name)
        #Label(app, text=attach_name).grid(row=i+2, column=1)
        attachments_list.append((i, attach_name))
        i += 1

    #listBox was instantiated in main and now should only be updated
    listbox.delete(0,END)# clears listbox
    
    i=0
    for attach in attachments_list:
        #print(attach)
        listbox.insert(i+1, attachments_list[i][1][12:]) 
        i+=1
    listbox.grid(row=2,column=1) #.grid() updates the listbox
    
        
    return attachments_list

"""
def list_box_gui(app, attachments_list):
    i=0
    list1 = Listbox(app)
    for attach in attachments_list:
        print(attach)
        list1.insert(i+1, attachments_list[i][1])
        i+=1
    list1.grid(row=2,column=1)
"""
def download_gui(list, file_tuple):
    

    #print("====from download_gui:", file_tuple)
    if file_tuple == ():
        #print("No messages were selected")
        return #TODO: implement message to the user

    file_name = list.get(file_tuple[0])
    #print(file_name)
    file_url = 'http://127.0.0.1:8000/media/attachments/' + file_name
    #print(file_url)
    
    #download_file_name = file_name.split('/')[1] #extract name
    #print(download_file_url)
    
    with urllib.request.urlopen(file_url) as url:
        s = url.read()
    #with open(file_name, 'wb') as code:
    #    code.write(s)

    file_writer = filedialog.asksaveasfile(mode='wb', title="Download", initialfile = file_name)
    file_writer.write(s)
    message_gui("Done!")
        
def message_gui(message):
    toplevel = Toplevel()
    label1 = Label(toplevel, text=message)
    label1.grid(row=0, sticky = 'E'+'W'+'N'+'S')
    button_ok = Button(toplevel, text='OK', command=toplevel.destroy)
    button_ok.grid(row=1)

def get_password_gui(command):
    global dialogue #this is horrible programming practice
    dialogue = Tk()
    dialogue.title('Input password')
    #Label(dialogue, text='New filename:').grid(row=0)
    Label(dialogue, text="Password:").grid(row=1)
    Button(dialogue, text='OK',
           command= command
           ).grid(row=2)
    global e99 #should use classes instead
    #global e_name
    e99 = Entry(dialogue)
    e99.grid(row=1, column=1)

    """
    e_name = Entry(dialogue)
    e_name.insert(0, "default")
    e_name.grid(row=0,column=1)
    """
    dialogue.mainloop()
    #return key

def encrypt_gui():

    key = e99.get()
    dialogue.destroy() #kill widget. Again, horrible programming practice. Use objects instead
    file_reader = filedialog.askopenfile(mode='rb') #this is a stream

    cipher_gen = ARC4.new(key)
    
    hash = SHA256.new(file_reader.read()).digest()
    print("actual signature: ", hash)
        
    file_reader.seek(0)
    old_name_list = (file_reader.name).split("/")
    old_name = old_name_list[len(old_name_list) - 1]
    #print(old_name)
                                        
                                        
    file_writer = open(old_name + ".enc", 'wb')
    for line in file_reader:
        enc_line = cipher_gen.encrypt(line)
        file_writer.write(enc_line)
            
    enc_hash = cipher_gen.encrypt(hash) # append hash to file
    file_writer.write(enc_hash)
    print("encrypted signature: ",enc_hash)

    """
    toplevel = Toplevel()
    label1 = Label(toplevel, text='Done!')
    label1.grid(row=0)
    button_ok = Button(toplevel, text='OK', command=toplevel.destroy)
    button_ok.grid(row=1)
    """
    message_gui("Done!")
    #toplevel.mainloop()

    return

def decrypt_gui(): #must take original input signature? 
    file_reader = filedialog.askopenfile(mode='rb') #this is a stream

    key = e99.get()
    dialogue.destroy()
    decipher = ARC4.new(key)

    #TODO: must check if a file is encrypted!
    #if (file[-4:] != ".enc"):
 #       return
    
    #file_writer = open("DEC_" + file[0:-4], 'wb')
    old_name_list = (file_reader.name).split("/")
    old_name = old_name_list[len(old_name_list) - 1]
    file_writer = open("DECRYPTED_" + old_name[0:-4], 'wb') #TODO: dialogue box??
    
    file_length = len(file_reader.read())
    file_reader.seek(0)
    #print("file size", file_length)
    
    #another writer
    clear_signature = []
    while(True):
        b = file_reader.read(1)
        if b:
            dec_b = decipher.decrypt(b)
            if file_reader.tell() > file_length-32:
                #print(dec_b)
                #clear_signature += str(dec_b)
                clear_signature.append(int.from_bytes(dec_b,'big'))
                #print(clear_signature)
            else:
                file_writer.write(dec_b)
        else:
            break
        
        #print((clear_signature))

        """
        file_reader2 = open("DEC_" + file,'rb')
        print("hi",file_reader2.tell())
        hash = SHA256.new(file_reader2.read()).digest()
        print(len(hash), hash)
        file_reader2.close()
        """
        
    file_writer.close()#the file is ready
    file_reader.close()
    
    
    #global signature = clear_signature #TODO: must check signature
    compare_signature(clear_signature, old_name)

    return
        
def compare_signature(signature,name):
    
    with open("DECRYPTED_"+name[:-4], 'rb') as file_reader:
        hash = SHA256.new(file_reader.read()).digest()
    #print("hash:   ", str.encode(str(hash)))
    
    corrupted = False
    j = 0
    if signature:
        for h in hash:
            #print(int(h), signature[j])#DEBUG
            if(int(h) != signature[j]):
                corrupted = True
                break
            j += 1
            
        if (not corrupted):
            #print("Done!")
            message_gui("Done!")
        else:
            message_gui("The file was corrupted or the file's password is incorrect")
    else:
        message_gui("An error has occurred decrypting your file!")

    

    

if __name__ == "__main__":
    #global username
    #username = ""
    #==== LOGIN APP ====
    
    top = Tk() #top is the login application window
    top.title("Login Safecollab")
    #top.pack()

    Label(top, text="Username").grid(row=0)
    Label(top, text="Password").grid(row=1)

    e1 = Entry(top)
    e2 = Entry(top, show="*")

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    submit_button = Button(top)
    submit_button['text'] = "Submit"
    submit_button.grid(row=3)
    submit_button['command'] = login_gui #pass function without parenthesis
    #submit_button.pack(side='top')

    exit_button = Button(top)
    exit_button['text'] = "Exit"
    exit_button['command'] = top.quit
    exit_button.grid(row=3, column=1)
    
    top.mainloop()

    #print(username) #global variable declared after the loop! Woot! 
    user = username#e1.get()#save user to query reports later
    #print("from main",user)
    
    #user = 'admin' #ERASE ME
    
    #==== MAIN APP ====
    root = Tk() #main application window
    root.title("Safecollab")
    
    menu = Menu(root)
    root.config(menu=menu)

    file = Menu(menu)
    file.add_command(label='Download', command=lambda:download_gui( list1, list1.curselection() ))
    file.add_command(label='Encrypt...', command=lambda:get_password_gui(encrypt_gui))
    file.add_command(label='Decrypt...', command=lambda:get_password_gui(decrypt_gui))
    file.add_command(label='Exit', command=exit)
    menu.add_cascade(label='File',menu=file)
    
    
    #Label(root, text="SAFECOLLAB").grid(row=0)
    reports_label = Label(root, text="Reports")
    reports_label.grid(row=1)
    reports_label.configure(bg='grey',padx=20)
    attachments_label = Label(root, text="Attachments")
    attachments_label.grid(row=1, column=1, sticky='E')
    attachments_label.configure(bg="#808080",padx=47)
    detail_label = Label(root, text="Detail")
    detail_label.grid(row=1, column=3, sticky='E'+'W',columnspan=2)
    detail_label.configure(bg="grey",padx=47)

    list1 = Listbox(root) #instantiate listBox
    list1.grid(row=2,column=1, columnspan=2, rowspan=20)


    
    #reports fields
    Label(root, text='name:').grid(row=2, column=3, sticky = 'W')
    Label(root, text='folder:').grid(row=3, column=3, sticky = 'W')
    Label(root, text='description:').grid(row=4, column=3, sticky = 'W')
    Label(root, text='longDescription:').grid(row=5, column=3,sticky = 'W')
    Label(root, text='creator:').grid(row=6, column=3,sticky = 'W')
    Label(root, text='time:').grid(row=7, column=3,sticky = 'W')
    Label(root, text='private:').grid(row=8, column=3,sticky = 'W')
    Label(root, text='encrypted:').grid(row=9, column=3,sticky = 'W')

    #instantiate labels because they will be updated later!
    #also save them in a list
    list_detail_fields = []
    i=0
    while(i<10):
        #print(field,":",which_report['fields'][field])
        #Label(root, text=field+":").grid(row=i, column=3)
        v = StringVar()
        l = Label(root, text="", textvariable=v)
        list_detail_fields.append(v)
        l.grid(row=i+2, column=4, sticky = 'W')
        i+=1

    report_tuple = list_reports(user)
    report_list = report_tuple[0]
    report_data = report_tuple[1]
    i=2
    for report in report_list:
       # print(report[1])
        b = Button(root, text=report[1], command=lambda report=report, i=i:display_files_gui(root,report[1],list1,report_data,i-2,list_detail_fields))
        b.grid(row=i, column=0, sticky = 'E') #must use default parameter to avoid late-binding
        b.configure(width=10)
        i+=1

 

    root.mainloop()
    
    

    #====AUTHENTICATION====
    #user = input("username: ")
    #pwd = input("password: ")
    #user = 'marco' #DEBUG
    #pwd = 'marco' #DEBUG

    exit() #ERASE THIS

    print("Commands:")
    print('"v" - View reports')
    print('"d" - View a report\'s detail')
    print('"do" - Download report\'s files')
    print('"e" - Encrypt a file in the current folder')
    print('"dc" - Decrypt a file')
    print('"h" - Help')
    print('"q" - Quit\n')

    data = list_reports(user, pwd)
    while(1):
        command = input("What would you like to do?")
        #command = 'dc' #DEBUG
        
        #====LIST REPORTS====
        if command == 'v':
            data = list_reports(user, pwd) #refresh reports data
            
        #====DETAILS====
        if (command == 'd'):
            while(True):
                file_index = int(input("Select report to view (use its number):"))
                if file_index >= len(data):
                    print("Not a valid number...")
                    continue
                print()
                """
                for f in data:
                    file_dict = f['fields']
                    if which_report == file_dict['name']:
                        for field in file_dict:
                            print(field,":",file_dict[field])
                        not_found=False
"""
                

                which_report = data[file_index]
                for field in which_report['fields']:
                    print(field,":",which_report['fields'][field])
                break

       
        #====DOWNLOAD====
        if command == 'do':
            which_report = int(input("Select a report (using its number) to download:"))
            filedownload(which_report)
        

        #====ENCRYPTION====
        if command == 'e':
            file_name = input("Enter filename including extension:")
            enc_key = input("Enter a password for the file:")
            if encrypt_file(file_name,enc_key):
                print("Done!")
            else:
                print("An error has occurred encrypting your file!")

        #====DECRYPTION====
        if command == 'dc':
            file_name = input("Enter filename including extension:")
            if file_name == "": #MUST HANDLE I/O
                pass
            enc_key = input("Enter the file's password:")
            
            #file_name = "marco.png.enc"
            #enc_key = "123"
            
            signature = decrypt_file(file_name,enc_key)
            #print(signature)

            
            with open("DEC_"+file_name[:-4], 'rb') as file_reader:
                hash = SHA256.new(file_reader.read()).digest()
            #print("hash:   ", str.encode(str(hash)))
            
            corrupted = False
            j = 0
            if signature:
                for h in hash:
                    #print(int(h), signature[j])#DEBUG
                    if(int(h) != signature[j]):
                        corrupted = True
                        break
                    j += 1
                    
                if (not corrupted):
                    print("Done!")
                else:
                    print("The file was corrupted...")
            else:
                print("An error has occurred decrypting your file!")
                        
            
                #print(file_dict)

        """# Tried passing a request with current session to avoid passing username in the script
        req = requests.Request('GET', URL_download)#create request
        prep_req = req.prepare()#prepare request
        resp=client.send(prep_req)
        print(resp.text)
        """
        if command == 'h':
            print("Commands:")
            print('"v" - View reports')
            print('"d" - View a report\'s detail')
            print('"do" - Donwnload report\'s files')
            print('"e" - Encrypt a file in the current folder')
            print('"dc" - Decrypt a file')
            print('"h" - Help')
            print('"q" - Quit\n')
        if command == 'q':
            break

        print()
