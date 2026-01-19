from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
@app.route('/pbl0203')
def index():
    df = pd.read_csv('dataset/Iris.csv')
    data = df.head(20).to_dict(orient='records')
    columns = df.columns
    return render_template('index.html', data=data, columns=columns)

if __name__ == '__main__':
    app.run(debug=True)
