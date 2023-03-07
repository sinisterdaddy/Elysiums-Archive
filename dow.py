import pandas as pd
from geopy.geocoders import Nominatim
import geocoder as gc 
from cryptography.fernet import Fernet

class Encryptor():      #CLASS TO ENCRYPT AND DECRYPT USING FERNET ENCRYPTION

    def key_create(self):       #FUNCTION TO CREATE KEY FOR FERNET ENCRYPTION
        key = Fernet.generate_key()
        return key

    def key_write(self, key, key_name):     #FUNCTION TO WRITE KEY
        with open(key_name, 'wb') as mykey:
            mykey.write(key)

    def key_load(self, key_name):       #FUNCTION TO LOAD KEY
        with open(key_name, 'rb') as mykey:
            key = mykey.read()
        return key

    def file_encrypt(self, key, original_file, encrypted_file):     #FUNCTION TO ENCRYPT FILE
        
        f = Fernet(key)

        with open(original_file, 'rb') as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open (encrypted_file, 'wb') as file:
            file.write(encrypted)

    def file_decrypt(self, key, encrypted_file, decrypted_file):        #FUNCTION TO DECRYPT FILE
        
        f = Fernet(key)

        with open(encrypted_file, 'rb') as file:
            encrypted = file.read()

        decrypted = f.decrypt(encrypted)

        with open(decrypted_file, 'wb') as file:
            file.write(decrypted)

auth = False        #INITIALIZATION FOR CREDENTIALS AUTHENTICATION

user=input("Username: ")        #INPUTTING USERNAME
pas=input("Password: ")         #INPUTTING PASSWORD

dat=pd.read_csv('creds.csv')        #ITERATING THROUGH THE VALID CREDENTIALS
for i in dat.itertuples():
    if i[1]==user and i[2]==pas:        #VALIDATING USERNAME AND PASSWORD
        auth=True       #AUTHENTICATION SUCCESSFUL

geoLoc = Nominatim(user_agent="GetLoc")
locname = geoLoc.reverse("17.73222381494933, 83.32109617953489")       
area=locname.address        #COMPUTING LOCATION NAME (INCUBATION CENTER IN THIS CASE)
g=gc.ip('me')       #COMPUTING LOCATION FROM CURRENT IP-ADDRESS
cl=g.latlng     #SAVING LATITUDE AND LONGITUDE OF CURRENT IP-ADDRESS
ca=geoLoc.reverse("17.73222381494933, 83.32109617953489")       
c=ca.address        #SAVING LOCATION NAME FROM IP-ADDRESS

if c==area:       #CHECKING IF USER BELONGS TO REQUIRED LOCATION (VIT-AP IN THIS CASE)
    gauth=True
else:
    gauth=False

if auth==False:     #AUTHENTICATING CREDENTIALS
    print("CREDENTIALS AUTHENTICATION FAILED!")
    quit()
elif gauth==False:      #AUTHENTICATING GEO-LOCATION
    print("GEO-LOCATION AUTHENTICATION FAILED!")
    quit()
else:       #AUTHENTICATION SUCCESSFUL
    print("AUTHENTICATION SUCCESSFUL!")

encryptor=Encryptor()       #INSTANCE OF CLASS

mykey=encryptor.key_create()

encryptor.key_write(mykey, 'mykey.key')

loaded_key=encryptor.key_load('mykey.key')      #FUNCTION CALL TO LOAD KEY

encryptor.file_encrypt(loaded_key, 'datf.csv', 'enc.csv')

encryptor.file_decrypt(loaded_key, 'enc.csv', 'dec.csv')        #FUNCTION CALL TO DECRYPT DATA

data=pd.read_csv('dec.csv')     #ITERATING THROUGH DECRYPTED DATA
req=input("Enter Query: ")         #INPUTTING QUERY TO LOOKUP
fin=data[data['ENG_ID']==int(req)]      #SAVING FOUND DATA

if fin.empty:       #CHECKING IF DATA IS VALID(EXISTS)
    print("ENGAGEMENT ID INVALID!") 
else:
    print("ENGAGEMENT VALID!")
    print(fin)