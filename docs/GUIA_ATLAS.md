# Guia: Restauració del Backup a MongoDB Atlas

Aquesta guia explica pas a pas com restaurar la còpia de seguretat de la base de dades a MongoDB Atlas.

## Prerequisits

### 1. Clúster de MongoDB Atlas
- Accedeix a [MongoDB Atlas](https://cloud.mongodb.com/)
- Crea un compte (o inicia sessió)
- Crea un nou clúster gratuït (M0) si no en tens cap

### 2. Configuració del Clúster

#### Crear un usuari de base de dades:
1. Al menú lateral: **Database Access**
2. Clica **Add New Database User**
3. Tria autenticació per usuari/contrasenya
4. Defineix usuari (exemple: `feb_user`) i contrasenya (guarda-la!)
5. Assigna rol: **Atlas admin** o **Read and write to any database**
6. Clica **Add User**

#### Permetre l'accés de xarxa:
1. Al menú lateral: **Network Access**
2. Clica **Add IP Address**
3. Opcions:
   - **Recomanat**: Afegir la teva IP actual
   - **Temporal per proves**: Afegir `0.0.0.0/0` (tots els IPs - ATENCIO: només per desenvolupament!)
4. Clica **Confirm**

### 3. Instal·lar MongoDB Database Tools

Necessites `mongorestore` per pujar el backup:

1. Descarrega des de: https://www.mongodb.com/try/download/database-tools
2. Tria la versió per **Windows** (format ZIP)
3. Descomprimeix el fitxer
4. (Opcional) Afegeix la carpeta `bin` al PATH de Windows

## Restaurar el Backup

### Obtenir l'URI de connexió

1. Al teu clúster d'Atlas, clica **Connect**
2. Selecciona **Shell**
3. Copia l'URI (format: `mongodb+srv://<usuari>:<contrasenya>@cluster.mongodb.net`)
4. Substitueix `<usuari>` i `<contrasenya>` pels teus valors

### Executar la restauració

Obre PowerShell i executa (substitueix els valors):

```powershell
# Navega fins al projecte
cd C:\Users\holaq\Desktop\FEB-Basketball-Clustering

# Executa mongorestore (substitueix <usuari>, <contrasenya> i <cluster>)
mongorestore --uri "mongodb+srv://<usuari>:<contrasenya>@<cluster>.mongodb.net" ^
  --archive="2026-01-08_feb_db_bkp.archive\2026-01-08_feb_db_bkp.archive" ^
  --drop
```

**Nota**: L'opció `--drop` elimina col·leccions existents abans de restaurar.

### Si vols canviar el nom de la base de dades:

```powershell
mongorestore --uri "mongodb+srv://<usuari>:<contrasenya>@<cluster>.mongodb.net" ^
  --archive="2026-01-08_feb_db_bkp.archive\2026-01-08_feb_db_bkp.archive" ^
  --nsFrom="NOM_ANTIC.*" ^
  --nsTo="feb_db.*" ^
  --drop
```

## Verificar la Restauració

### Opció 1: Des de l'interfície d'Atlas

1. Al teu clúster, clica **Browse Collections**
2. Hauries de veure la base de dades `feb_db`
3. I les col·leccions:
   - `partits`
   - `FEB3_players_shots`
   - `FEB3_players_statistics`
   - `FEB3_teams_statistics`

### Opció 2: Amb el script Python

1. Copia `.env.example` a `.env`:
   ```powershell
   cp .env.example .env
   ```

2. Edita `.env` i omple amb les teves credencials:
   ```
   MONGO_URI=mongodb+srv://feb_user:la_teva_contrasenya@cluster123.mongodb.net
   MONGO_DB=feb_db
   ```

3. Executa el script de verificació:
   ```powershell
   .\.venv\Scripts\python.exe src\verificar_connexio.py
   ```

Si tot ha anat bé, veuràs el llistat de col·leccions i el nombre de documents.

## Treballar en Equip

Per compartir l'accés amb els teus companys:

1. Crea un usuari per cada company a **Database Access**
2. Comparteix l'URI de connexió (que cada un usi el seu usuari/contrasenya)
3. Cada company crea el seu propi fitxer `.env` local amb les seves credencials

**IMPORTANT**: No pugis el fitxer `.env` a GitHub! Està al `.gitignore` per seguretat.

## Recursos

- [Documentació de mongorestore](https://www.mongodb.com/docs/database-tools/mongorestore/)
- [MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/)
