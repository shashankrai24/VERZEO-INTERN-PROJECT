from flask import *
import pyrebase
import tone
import os
import sys
from PIL import Image 
import PIL 
config = {
     "apiKey": "AIzaSyBmD7OqXCv4XvVdrR4XMulhpgs-rWMZYdk",
    "authDomain": "verzeo-project.firebaseapp.com",
    "databaseURL": "https://verzeo-project-default-rtdb.firebaseio.com",
    "projectId": "verzeo-project",
    "storageBucket": "verzeo-project.appspot.com",
    "messagingSenderId": "423643052111",
    "appId": "1:423643052111:web:0a293b5f479d76908a123a",
    "measurementId": "G-07G7ZJCY1G"
}
firebase = pyrebase.initialize_app(config)
db= firebase.database()
storage=firebase.storage()
app = Flask(__name__)



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        nam=request.form['name1']
        numb=request.form['num']
        que=request.form['query1']
        string = "queryfolder/" + nam
        storage.child(string).put({"name":nam , "phone number":numb , "query":que})
        db.child("querybox").child(numb).push({"name":nam , "phone number":numb , "query":que})
        return render_template('contact.html')
    return render_template('contact.html')
    
   

@app.route("/img",methods=['GET','POST'])
def img():
    if request.method == 'POST':
        img=request.files['image']
        ur=request.form['url']
        if ur:
            try:
                ans=tone.detector(ur)
                ur1 = "static\image4.png" 
                ur4 = "static\image5.png"
                storage.child("images/ans1.png").put(ur1)
                storage.child("images/ans2.png").put(ur4)
                ur2=storage.child("images/ans1.png").get_url(None)
                colorbar=storage.child("images/ans2.png").get_url(None)
                return render_template('ans.html',url=ur,ans1=ans[0],url2=ur2,col=colorbar)
            except:
                return render_template('error.html',upload="UPLOAD UNSUCCESFULL TRY DOWNLOADING THE IMAGE AND THEN UPLOAD")
        else:
            storage.child("images/ans.jpg").put(img)
            uri=storage.child("images/ans.jpg").get_url(None)
            ans=tone.detector(uri)
            ur1 = "static\image4.png" 
            ur4 = "static\image5.png"
            storage.child("images/ans1.png").put(ur1)
            storage.child("images/ans2.png").put(ur4)
            ur2=storage.child("images/ans1.png").get_url(None)
            colorbar=storage.child("images/ans2.png").get_url(None)
            return render_template('ans.html',ans1=ans[0],url=uri,url2=ur2,col=colorbar)   
    return render_template('imgclass.html')



if __name__ == '__main__':
    app.run(debug=True)