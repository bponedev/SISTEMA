from app import create_app

# Arquivo principal que inicia a aplicação Flask
# Mantido extremamente simples para evitar bugs.

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
