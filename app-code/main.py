import flask
from flask import Flask, render_template, send_from_directory
from code1 import analyze

folium_map = analyze()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    folium_map.save("C:\\Users\\fancy\Desktop\Class\\UN Armed Conflict\choropleth code\static\map.html")
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)