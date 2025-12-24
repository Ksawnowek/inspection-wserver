param(
    [string]$ServiceName = "InspectionApi",
    # UWAGA: Skoro używasz venv, ścieżka powinna prowadzić do python.exe W ŚRODKU venv!
    [string]$PythonExe = "C:\InspectionApp\backend\venv\Scripts\python.exe",
    [string]$AppDir = "C:\InspectionApp\backend",
    [int]$Port = 8001,
    [string]$NssmPath = "C:\ProgramData\chocolatey\bin\nssm.exe"
)


$ErrorActionPreference = "Stop"

# 1. Sprawdzenie NSSM
if (!(Test-Path $NssmPath)) { 
    Write-Error "NSSM nie został znaleziony w: $NssmPath"; 
    exit 1 
}

# 2. Tworzenie folderu na logi
$LogDir = Join-Path $AppDir "logs"
if (!(Test-Path $LogDir)) {
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
}

# 3. Argumenty startowe
# Używamy modułu uvicorn, wskazujemy hosta i port
$Args = "-m uvicorn app.main:app --host 0.0.0.0 --port $Port"

Write-Host "Instalowanie usługi $ServiceName..." -ForegroundColor Cyan

# 4. Konfiguracja NSSM
& "$NssmPath" install $ServiceName "$PythonExe" "$Args"
& "$NssmPath" set $ServiceName AppDirectory "$AppDir"
& "$NssmPath" set $ServiceName Start SERVICE_AUTO_START
& "$NssmPath" set $ServiceName AppStdout "$LogDir\stdout.log"
& "$NssmPath" set $ServiceName AppStderr "$LogDir\stderr.log"

# 5. Uruchomienie
& "$NssmPath" start $ServiceName

Write-Host "Gotowe! Usługa powinna działać." -ForegroundColor Green