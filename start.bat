@echo off
echo =======================================================
echo Azure AI Foundry: Environment Setup and Authentication
echo =======================================================
echo.

echo [1/4] Installing required Python dependencies...
pip install -r requirements.txt
echo.

echo [2/4] Clearing old Azure CLI accounts and token cache...
call az account clear
echo.

echo [3/4] Disabling Windows Azure Authentication Broker...
call az config set core.enable_broker_on_windows=false
echo.

echo [4/4] Opening browser for Azure Login...
call az login
echo.

echo =======================================================
echo ✅ Setup Complete! You can now run your Python scripts.
echo =======================================================
pause