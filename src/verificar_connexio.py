"""
Script per verificar la connexió a MongoDB Atlas
i llistar les col·leccions disponibles.
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar variables des de .env si existeix
load_dotenv()

# Obtenir configuració de variables d'entorn
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "feb_db")


def verificar_connexio():
    """Verifica la connexió a MongoDB Atlas i mostra les col·leccions."""
    print(f"Connectant a MongoDB Atlas...")
    print(f"Base de dades: {MONGO_DB}")
    
    try:
        # Crear connexió
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        
        # Verificar connexió amb ping
        client.admin.command("ping")
        print("Connexió establerta correctament")
        
        # Llistar col·leccions
        col_leccions = db.list_collection_names()
        
        if not col_leccions:
            print("\nADVERTENCIA: No s'han trobat col·leccions a la base de dades.")
            print("  Hauràs de restaurar el backup primer.")
        else:
            print(f"\nCol·leccions trobades ({len(col_leccions)}):")
            for nom in col_leccions:
                count = db[nom].estimated_document_count()
                print(f"  - {nom}: {count:,} documents")
        
        client.close()
        print("\nVerificació completada")
        
    except Exception as e:
        print(f"\nError de connexió: {e}")
        print("\nComprova:")
        print("  1. Que la variable MONGO_URI està ben configurada")
        print("  2. Que la IP està permesa a Network Access d'Atlas")
        print("  3. Que l'usuari i contrasenya són correctes")


if __name__ == "__main__":
    verificar_connexio()
