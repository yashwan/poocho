from dotenv import dotenv_values

config = dotenv_values(".env")
JWT_SECRET = config["JWT_SECRET_KEY"]

