# Script per restaurar el backup a MongoDB Atlas
# Assegura't d'haver executat primer: .\instal·lar_mongodb_tools.ps1

$ErrorActionPreference = "Stop"

Write-Host "Restauració del backup a MongoDB Atlas" -ForegroundColor Cyan
Write-Host ""

# Comprovar si existeix .env
if (-not (Test-Path ".env")) {
    Write-Host "Error: No s'ha trobat el fitxer .env" -ForegroundColor Red
    Write-Host "  Copia .env.example a .env i configura les credencials" -ForegroundColor Yellow
    exit 1
}

# Llegir configuració de .env
$envContent = Get-Content ".env"
$mongoUri = ($envContent | Where-Object { $_ -match "^MONGO_URI=" }) -replace "^MONGO_URI=", ""
$mongoDb = ($envContent | Where-Object { $_ -match "^MONGO_DB=" }) -replace "^MONGO_DB=", ""

if ([string]::IsNullOrWhiteSpace($mongoUri) -or $mongoUri -match "<cluster>") {
    Write-Host "Error: MONGO_URI no està configurat correctament al fitxer .env" -ForegroundColor Red
    exit 1
}

Write-Host "Base de dades: $mongoDb" -ForegroundColor Gray
Write-Host ""

# Ruta a mongorestore
$mongorestore = "$PSScriptRoot\mongodb-tools\bin\mongorestore.exe"

# Comprovar si mongorestore existeix
if (-not (Test-Path $mongorestore)) {
    Write-Host "mongorestore no trobat" -ForegroundColor Red
    Write-Host "  Executa primer: .\instal·lar_mongodb_tools.ps1" -ForegroundColor Yellow
    exit 1
}

# Ruta al backup (carpeta data\backups)
$backupPath = "$PSScriptRoot\..\data\backups\2026-01-08_feb_db_bkp.archive\2026-01-08_feb_db_bkp.archive"

if (-not (Test-Path $backupPath)) {
    Write-Host "No s'ha trobat l'arxiu de backup: $backupPath" -ForegroundColor Red
    exit 1
}

Write-Host "Arxiu de backup: 2026-01-08_feb_db_bkp.archive" -ForegroundColor Gray
Write-Host ""
Write-Host "ATENCIO: Aquesta operació eliminarà les dades existents (--drop)" -ForegroundColor Yellow
Write-Host ""
$confirmation = Read-Host "Vols continuar? (S/N)"

if ($confirmation -ne "S" -and $confirmation -ne "s") {
    Write-Host "Operació cancel·lada" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Iniciant restauració..." -ForegroundColor Cyan
Write-Host ""

try {
    & $mongorestore --uri $mongoUri --archive=$backupPath --drop
    
    Write-Host ""
    Write-Host "Restauració completada!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Verifica les dades executant:" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\python.exe src\verificar_connexio.py" -ForegroundColor White
    
} catch {
    Write-Host ""
    Write-Host "Error durant la restauració: $_" -ForegroundColor Red
    exit 1
}
