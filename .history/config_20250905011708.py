DB_CONFIG = {
    'dbname': 'it_business',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super_secure_key'
