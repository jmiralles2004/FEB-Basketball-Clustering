# Scripts d'Automatització

Aquesta carpeta conté scripts per facilitar la configuració del projecte.

## Scripts disponibles

### 1. instal·lar_mongodb_tools.ps1
Descarrega i instal·la automàticament MongoDB Database Tools (mongorestore, mongodump, etc.)

**Ús:**
```powershell
.\scripts\instal·lar_mongodb_tools.ps1
```

**Què fa:**
- Descarrega MongoDB Database Tools v100.9.5
- Descomprimeix a la carpeta `mongodb-tools/`
- Comprova si ja està instal·lat abans de descarregar

### 2. restaurar_backup.ps1
Restaura el backup de la base de dades a MongoDB Atlas

**Prerequisits:**
1. Haver executat `instal·lar_mongodb_tools.ps1`
2. Tenir configurat el fitxer `.env` amb les credencials d'Atlas

**Ús:**
```powershell
.\scripts\restaurar_backup.ps1
```

**Què fa:**
- Llegeix la configuració del fitxer `.env`
- Restaura l'arxiu `2026-01-08_feb_db_bkp.archive` a Atlas
- Elimina col·leccions existents abans de restaurar (--drop)
- Demana confirmació abans de procedir

## Ordre d'execució recomanat

```powershell
# Pas 1: Instal·lar les eines (només la primera vegada)
.\scripts\instal·lar_mongodb_tools.ps1

# Pas 2: Configurar .env amb les credencials d'Atlas
# Copia .env.example a .env i edita'l amb les teves dades

# Pas 3: Restaurar el backup
.\scripts\restaurar_backup.ps1

# Pas 4: Verificar la connexió
.\.venv\Scripts\python.exe src\verificar_connexio.py
```

## Notes

- Els scripts només funcionen a Windows amb PowerShell
- MongoDB Database Tools s'instal·la localment al projecte (carpeta `mongodb-tools/`)
- No es puja a Git (està al `.gitignore`)
