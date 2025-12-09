import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

# Load environment variables for environment-specific DB configuration.
load_dotenv()

# Database configuration (defaults support local Docker development).
dbconfig = {
    "host": os.getenv("MYSQL_HOST", "mariadb"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DATABASE", "x_app"),
    "user": os.getenv("MYSQL_USER", "x_user"),
    "password": os.getenv("MYSQL_PASSWORD", "x_password"),
}

# Connection pool improves performance and avoids creating a new DB
# connection on every request (common best practice in Flask apps).
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)

def db():
    """
    Returns a connection from the global pool.
    All services use this function to ensure consistent and efficient DB access.
    """
    return connection_pool.get_connection()
