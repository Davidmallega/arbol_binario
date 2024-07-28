from app import create_app

# Crear una instancia de la aplicación Flask
app = create_app()

# Ejecutar la aplicación si este archivo es el punto de entrada
if __name__ == '__main__':
    app.run(debug=True)
