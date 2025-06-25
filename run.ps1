# run.ps1
$env:PORT = 8080
python -m uvicorn main:app --reload --port $env:PORT
