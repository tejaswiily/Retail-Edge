import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Flask

from flask import Flask, render_template, request
import os
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Process the file and generate the graph
        try:
            plot_graph(filepath)
            return render_template('result.html', image_url='static/graph.png')
        except Exception as e:
            return f"An error occurred: {e}"

def plot_graph(filepath):
    df = pd.read_csv(filepath)
    columns = df.columns

    # Clear previous graph
    plt.clf()

    if len(columns) == 2:
        # Bar Graph
        x, y = columns
        df.plot(kind='bar', x=x, y=y, legend=False)
    else:
        # Line Graph
        df.plot(kind='line', legend=True)

    # Save the graph
    plt.xlabel('Index')
    plt.ylabel('Values')
    plt.title('Generated Graph')
    plt.savefig('static/graph.png')

if __name__ == '__main__':
    app.run(debug=True)
