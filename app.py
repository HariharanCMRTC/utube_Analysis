from flask import Flask,render_template,request
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contact",methods = ["GET","POST"])
def contactus():
    if request.method == "POST":
        fname = request.form.get("fullname")
        pno = request.form.get("phone")
        email = request.form.get("email")
        addr = request.form.get("address")
        msg = request.form.get("message")
        conn = sqlite3.connect("youtube.db")
        curr = conn.cursor()
        curr.execute(f'''INSERT INTO CONTACT VALUES("{fname}","{pno}","{email}","{addr}","{msg}")''')
        conn.commit()
        return render_template("message.html")
    else:
        return render_template('contact.html')
    
@app.route("/analytics")
def analytical():
    return render_template("analytics.html")

with open("Model.pickle","rb") as model_file:
    model = pickle.load(model_file)

@app.route("/predictor",methods = ["GET","POST"])
def predictor():
    if request.method == "POST":
        nview = request.form.get("views")
        dislike = request.form.get("dislikes")
        comment = request.form.get("comments")
        genre  =request.form.get("genre")
        prediction = model.predict([[float(nview),float(dislike),float(comment),float(genre)]])
        
        return render_template("message1.html",prediction=prediction[0])    
    else:
        return render_template("predictor.html")


if __name__ == "__main__":
    app.run(debug = True)