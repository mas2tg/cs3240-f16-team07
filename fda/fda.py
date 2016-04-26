#from django.contrib.auth import authenticate, login, logout
#import urllib.request
import requests, json, urllib, array
import urllib.request
from Crypto.Cipher import ARC4
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random

def list_reports(user, password):
    r2 = requests.get('http://127.0.0.1:8000/fda_index/', params={'username':user}) #Must NOT provide the username here but get it from request
    data = json.loads(r2.text)#may not be necessary
    #print(data)
    if data == '':
        print("There are no reports for you.")
        
    i = 0
    for f in data:
        file_dict = f['fields']
        report_name = file_dict['name'] #print all the lists
        print(i, report_name)
        i += 1
    return data

def filedownload(file_index):
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

def encrypt_file(file, key):
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

def decrypt_file(file, key):
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




if __name__ == "__main__":
    URL = "http://localhost:8000/users/fda_login"
    URL_download = "http://localhost:8000/fda_index"
    client = requests.session()

    #====AUTHENTICATION====
    user = input("username: ")
    pwd = input("password: ")
    #user = 'marco' #DEBUG
    #pwd = 'marco' #DEBUG
    login = {'username':user,'password':pwd}
    r = client.post(URL, data=login)
    
    if r.text == "success": #If login is successful
        print("Welcome", login['username'])
        print()
    else:
        print("Login failed")
        exit()

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
