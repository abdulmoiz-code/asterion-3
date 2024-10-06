from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

# Load the CSV data once when the app starts
DATA_FRAME = pd.read_csv('nasa.csv')

# Convert the 'Close Approach Date' to datetime for filtering
DATA_FRAME['Close Approach Date'] = pd.to_datetime(DATA_FRAME['Close Approach Date'], errors='coerce')

# HTML template with NASA theme
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- Responsive design -->
    <title>Nasa Data Filter</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 20px;
            padding: 20px;
            background-image: url('https://t3.ftcdn.net/jpg/02/38/16/94/360_F_238169477_Daonex5XsbOWLdcL0x8IcQ91RCJGubDy.jpg');
            background-size: cover;
            color: #f2f2f2;
        }
        h1 {
            color: #FFD700;
            text-shadow: 2px 2px 4px #000000;
        }
        form {
            margin-bottom: 20px;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }
        input[type="text"] {
            padding: 10px;
            margin: 5px 0;
            width: calc(100% - 22px);
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            padding: 10px 15px;
            background-color: #FFD700;
            color: #000;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #FFC107;
        }
        .data {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
            background-color: rgba(255, 255, 255, 0.9);
            overflow-x: auto; /* Allow horizontal scrolling */
            display: block; /* Make table scrollable on small screens */
        }
        .data th, .data td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }
        .data th {
            background-color: #007BFF;
            color: black;
        }
        .error {
            color: #FF4500;
            margin-top: 10px;
        }
    </style>
</head>
<body style='color:black;'>
    <h1>Nasa Data Filter</h1>
    <form method="post">
        <label for="value">Enter Value:</label>
        <input type="text" name="value" placeholder="e.g., 3703080 or a name" required>
        <input type="submit" value="Filter Data">
    </form>

    {% if tables %}
        <h2 style='color:white;'>Filtered Data</h2>
        {% for table in tables %}
            {{ table | safe }}
        {% endfor %}
    {% endif %}
    
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def filter_data():
    tables = []
    error = None

    if request.method == 'POST':
        value = request.form.get('value')

        # Ensure the input value is a string and not empty
        if not isinstance(value, str) or not value.strip():
            error = "Please enter a valid value."
        else:
            # Filter the DataFrame, ensuring we handle NaN values
            filtered_data = DATA_FRAME[DATA_FRAME.apply(
                lambda row: row.astype(str).fillna('').str.contains(value, case=False).any(), axis=1
            )]

            # Debugging: Print the shape of the filtered data
            print(f"Filtered data shape: {filtered_data.shape}")

            if not filtered_data.empty:
                tables.append(filtered_data.to_html(classes='data', index=False))
            else:
                error = f"No data found for the value '{value}'."

    return render_template_string(HTML_TEMPLATE, tables=tables, error=error)

if __name__ == '__main__':
    app.run(debug=True)
