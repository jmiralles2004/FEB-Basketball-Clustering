# Script per instal·lar MongoDB Database Tools
# Descarrega i configura mongorestore i altres eines necessàries

$ErrorActionPreference = "Stop"

Write-Host "Instal·lant MongoDB Database Tools..." -ForegroundColor Cyan

# Configuració
$version = "100.9.5"
$url = "https://fastdl.mongodb.org/tools/db/mongodb-database-tools-windows-x86_64-$version.zip"
$toolsDir = "$PSScriptRoot\mongodb-tools"
$zipFile = "$PSScriptRoot\mongodb-tools.zip"

# Crear directori si no existeix
if (-not (Test-Path $toolsDir)) {
    New-Item -ItemType Directory -Path $toolsDir | Out-Null
}

# Comprovar si ja està instal·lat
if (Test-Path "$toolsDir\bin\mongorestore.exe") {
    Write-Host "MongoDB Database Tools ja està instal·lat" -ForegroundColor Green
    Write-Host "  Ubicació: $toolsDir\bin" -ForegroundColor Gray
    exit 0
}

# Descarregar
Write-Host "Descarregant MongoDB Database Tools v$version..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri $url -OutFile $zipFile -UseBasicParsing
    Write-Host "Descàrrega completada" -ForegroundColor Green
} catch {
    Write-Host "Error en la descàrrega: $_" -ForegroundColor Red
    exit 1
}

# Descomprimir
Write-Host "Descomprimint..." -ForegroundColor Yellow
try {
    Expand-Archive -Path $zipFile -DestinationPath $toolsDir -Force
    
    # Moure els binaris a l'arrel de mongodb-tools
    $extractedFolder = Get-ChildItem -Path $toolsDir -Directory | Select-Object -First 1
    Move-Item -Path "$($extractedFolder.FullName)\bin" -Destination "$toolsDir\bin" -Force
    Remove-Item -Path $extractedFolder.FullName -Recurse -Force
    
    Write-Host "Descompressió completada" -ForegroundColor Green
} catch {
    Write-Host "Error en la descompressió: $_" -ForegroundColor Red
    exit 1
}

# Netejar ZIP
Remove-Item -Path $zipFile -Force

Write-Host ""
Write-Host "Instal·lació completada!" -ForegroundColor Green
Write-Host ""
Write-Host "Eines disponibles a: $toolsDir\bin" -ForegroundColor Cyan
Write-Host "  - mongorestore.exe" -ForegroundColor Gray
Write-Host "  - mongodump.exe" -ForegroundColor Gray
Write-Host "  - mongoexport.exe" -ForegroundColor Gray
Write-Host "  - mongoimport.exe" -ForegroundColor Gray
Write-Host ""
Write-Host "Pots restaurar el backup executant:" -ForegroundColor Yellow
Write-Host "  .\restaurar_backup.ps1" -ForegroundColor White
