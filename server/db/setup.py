import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from db.config import DB_PARAMS

def create_database_if_not_exists():
    # Connect to the default 'postgres' database to create a new database
    conn_params = DB_PARAMS.copy()
    conn_params['database'] = 'postgres'
    
    try:
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_PARAMS['database']}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {DB_PARAMS['database']}")
            print(f"Database '{DB_PARAMS['database']}' created successfully.")
        else:
            print(f"Database '{DB_PARAMS['database']}' already exists.")
        
    except (Exception, psycopg2.Error) as error:
        print(f"Error while creating database: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def setup_database():
    create_database_if_not_exists()
    
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # Create LinkedIn table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS linkedin_posts (
                id SERIAL PRIMARY KEY,
                author TEXT,
                content TEXT,
                email TEXT,
                phone_number TEXT,
                UNIQUE (author, content)
            )
        ''')

        # Create Upwork table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS upwork_jobs (
                id SERIAL PRIMARY KEY,
                job_title TEXT,
                posted_on TEXT,
                description TEXT,
                job_data JSONB,
                link TEXT UNIQUE
            )
        ''')

        conn.commit()
        print("Database tables created successfully.")
    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed.")

if __name__ == "__main__":
    setup_database()