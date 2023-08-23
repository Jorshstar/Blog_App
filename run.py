from flaskblog import create_app

app = create_app()


# Running the app only if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)  # Running the app in debug mode
