Write-Host "Running isort..." -ForegroundColor Cyan
python -m isort --settings-file .\.isort.cfg .
if ($LASTEXITCODE -ne 0) {
    Write-Host "isort failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Running black..." -ForegroundColor Cyan
python -m black --config .\.black .
if ($LASTEXITCODE -ne 0) {
    Write-Host "black failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Running flake8..." -ForegroundColor Cyan
python -m flake8 --config .flake8 .
if ($LASTEXITCODE -ne 0) {
    Write-Host "flake8 found issues!" -ForegroundColor Red
    exit 1
}

Write-Host "All checks passed!" -ForegroundColor Green