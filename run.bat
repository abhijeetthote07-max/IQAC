@echo off
echo "Installing dependencies..."
"C:\Users\hp\AppData\Local\Programs\Python\Python314\python.exe" -m pip install -r requirements.txt
echo "Running the application..."
"C:\Users\hp\AppData\Local\Programs\Python\Python314\python.exe" app.py
