import psycopg2
import json
from server.db.config import DB_PARAMS

class LinkedInPost:
    @staticmethod
    def insert(author, content, email, phone_number):
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO linkedin_posts (author, content, email, phone_number) VALUES (%s, %s, %s, %s)",
                (author, content, email, phone_number)
            )
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            print(f"Duplicate post detected for {author}. Skipping.")
        except (Exception, psycopg2.Error) as error:
            conn.rollback()
            print(f"Error inserting post into database: {error}")
        finally:
            cursor.close()
            conn.close()

class UpworkJob:
    @staticmethod
    def insert(job_title, posted_on, description, job_data, link):
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO upwork_jobs (job_title, posted_on, description, job_data, link) VALUES (%s, %s, %s, %s, %s)",
                (job_title, posted_on, description, json.dumps(job_data), link)
            )
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            print(f"Duplicate job detected for {link}. Skipping.")
        except (Exception, psycopg2.Error) as error:
            conn.rollback()
            print(f"Error inserting job into database: {error}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all():
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM upwork_jobs")
            return cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print(f"Error retrieving jobs from database: {error}")
            return []
        finally:
            cursor.close()
            conn.close()