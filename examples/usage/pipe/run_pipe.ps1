Start-Process pwsh -ArgumentList "-Command poetry run python .\echo.py --register"
Start-Process pwsh -ArgumentList "-Command poetry run python .\reverse.py --register"
Start-Process pwsh -ArgumentList "-Command poetry run python .\lower.py --register"