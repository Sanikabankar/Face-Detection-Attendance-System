# import streamlit as st
# import pandas as pd
# import time
# from datetime import datetime
# ts=time.time()
# date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
# timestamp=datetime.fromtimestamp(ts).strftime("%H-%M-%S")
# df=pd.read_csv("Attendance/Attendance_" + date + ".csv")
# st.dataframe(df.style.highlight_max(axis=0))



from flask import Flask, render_template_string
import pandas as pd
import time
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def show_attendance():
    # Get current date and timestamp
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    timestamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")

    # Ensure directory exists
    os.makedirs("Attendance", exist_ok=True)

    # File path
    file_path = f"Attendance/Attendance_{date}.csv"

    # Check if file exists
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        html_table = df.to_html(classes='table table-striped table-bordered', index=False)
        message = f"Attendance for {date}"
    else:
        # Create an empty file if not found
        df = pd.DataFrame(columns=["Name", "Time"])
        df.to_csv(file_path, index=False)
        html_table = df.to_html(classes='table table-striped table-bordered', index=False)
        message = f"No attendance found for {date}. Created a new empty file."

    # Simple HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Attendance Viewer</title>
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <style>
            body { padding: 20px; font-family: Arial, sans-serif; }
        </style>
    </head>
    <body>
        <h2>{{ message }}</h2>
        <div>{{ table|safe }}</div>
    </body>
    </html>
    """
    return render_template_string(html_template, table=html_table, message=message)

if __name__ == '__main__':
    app.run(debug=True)
