'''
Code created by Matt Richardson 
for details, visit:  http://mattrichardson.com/Raspberry-Pi-Flask/inde...
'''
from flask import Flask, render_template, request
import datetime
import db

app = Flask(__name__)

@app.route("/")
def welcome():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")

   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   
   return render_template('index.html', **templateData)

@app.route("/updateTemperature", methods=["GET", "POST"])
def updateTemp():


   if request.method == "POST":
      temperature = request.form.get('temperature')

      print(g)

      db.storeTemperature(temperature)
      db.checkDatabase()

      templateData = {
         # 'temp': temperature
      }

   return render_template('index.html', **templateData)



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=99, debug=True)