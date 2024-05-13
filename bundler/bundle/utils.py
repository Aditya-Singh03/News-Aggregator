from dotenv import dotenv_values

config = dotenv_values(".env")

IMGUR_CLIENT_ID = config["IMGUR_CLIENT_ID"]
