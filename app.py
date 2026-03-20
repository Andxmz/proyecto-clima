import requests
import os
from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
app = Flask(__name__)

@app.route("/")
def inicio():
    return redirect("/clima")

@app.route("/clima")
def tit():
    return render_template("clima.html")

@app.route("/resultado", methods=["POST"])
def resultado():
    ciudad = request.form["ciudad"]
    api_key = "d42be6595ee4cd4f7c7b3a37020e919b"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    respuesta = requests.get(url)
    datos = respuesta.json()
    url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={api_key}&units=metric&lang=es"
    datos_forecast = requests.get(url_forecast).json() 
    probabilidad = datos_forecast['list'][0]['pop'] * 100

    manana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    probabilidades_manana = []

    for bloque in datos_forecast['list']:
     if bloque['dt_txt'].startswith(manana):
        probabilidades_manana.append(bloque['pop'] * 100)
     if probabilidades_manana:
      prob_manana = max(probabilidades_manana)
     else:
      prob_manana = 0


    

    if probabilidad == 0:
         mensaje_lluvia = "No se esperan lluvias ☀️"
    elif probabilidad <= 30:
         mensaje_lluvia = "Poca probabilidad de lluvia 🌤️"
    elif probabilidad <= 60:
         mensaje_lluvia = "Probabilidad moderada de lluvia 🌦️"
    else:
         mensaje_lluvia = "Alta probabilidad de lluvia 🌧️"
 
    return render_template("resultado.html",
    ciudad=datos['name'],
    temperatura=datos['main']['temp'],
    clima=datos['weather'][0]['description'],
    humedad=datos['main']['humidity'],
    probabilidad=probabilidad,
    mensaje_lluvia=mensaje_lluvia,
    prob_manana=prob_manana
)

@app.route("/about")
def sobre():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))