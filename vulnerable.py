import os

def funcion_segura():
    # 1. REMEDIACIÓN VULNERABILIDAD: Nunca hardcodear contraseñas.
    # Usamos variables de entorno (environment variables).
    password_segura = os.environ.get("DB_PASSWORD", "no_configurada")
    
    # 2. REMEDIACIÓN CODE SMELL: Eliminada la variable inútil.
    
    # 3. REMEDIACIÓN BUG LÓGICO: Arreglado el orden del 'return' para no dejar código muerto.
    if password_segura != "no_configurada":
        print("Autenticación configurada de forma segura.")
        return True
        
    print("Falta configurar la variable de entorno de la contraseña.")
    return False

if __name__ == "__main__":
    funcion_segura()
