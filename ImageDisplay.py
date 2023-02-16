from flask import Flask, request, render_template
import pyodbc
from datetime import datetime, timedelta
from azure.storage.blob import generate_container_sas, ContainerSasPermissions


server = 'tcp:my-server01.database.windows.net'
database = 'My-db'
username = 'sxg6912'
password = 'PoiuytrewQ@239'
#driver= '{ODBC Driver 17 for SQL Server}'
account_name = "assign1"
account_key = "LRQ7KMFLfj76yCbLIdfF0VeLYyrNvkTWPi35Xt6vumz/XmL74jiUCeTzvSahTMKVTrN/N5AwqXm9+AStsZurlQ=="
container_name = "assgn-pics"



app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template("frontendpage.html")


@app.route('/', methods=['POST'])
def my_form():

    variable = request.form['Student Name']
    cnxn = pyodbc.connect(
		'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    cursor.execute(f"SELECT * FROM [dbo].[datan]")
    row = cursor.fetchall()
    print(row[0][0])
    #i=0
    found = False
    print(variable)
    for i in range(len(row)):
        l = list(row[i])
        if(variable in l):
            found = True
            break
    if(found == True and row[i][3] != None):
        urlpath = get_img_url(row[i][3])
        return displayimage(urlpath, row[i])

    else:
        return render_template("ImgNotFound.html")

def get_img_url(varname):
    container_sas_token = generate_container_sas(
        account_name="assign1",
        container_name="assgn-pics",
        account_key="LRQ7KMFLfj76yCbLIdfF0VeLYyrNvkTWPi35Xt6vumz/XmL74jiUCeTzvSahTMKVTrN/N5AwqXm9+AStsZurlQ==",
        permission=ContainerSasPermissions(read=True)
    )
    blob_url_with_container_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/" + varname
    print(blob_url_with_container_sas_token)
    return blob_url_with_container_sas_token


@app.route("/")
def displayimage(path, rowdata):
    img_url = path
    data = list(rowdata)
    print(data)
    return render_template('showimage.html', img_url_with_sas_token=img_url, studentname = data[0], studentclass = data[1], studentincome = data[2], studentcomments = data[4])


#@app.route('/login')
#def login():
#	return "<h1>Welcome</h1>"

#if _name_ == "_main_":
app.run()