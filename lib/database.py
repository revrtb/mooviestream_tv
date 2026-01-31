from flask_sqlalchemy import SQLAlchemy

# Create the database instance
db = SQLAlchemy(session_options={"autoflush": False}) 