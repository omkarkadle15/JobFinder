import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv
from server.db.model.job_post_upwork_model import JobPostUpwork
from server.scraper.Upwork.util.link import extract_links
from server.scraper.Upwork.util.scheduler import job_data_extract

load_dotenv()

POSTGRESQL_URL = getenv("POSTGRESQL_URL")
if not POSTGRESQL_URL:
    raise ValueError("POSTGRESQL_URL environment variable is not set")

# Ensure the dialect is 'postgresql'
if POSTGRESQL_URL.startswith('postgres:'):
    POSTGRESQL_URL = 'postgresql' + POSTGRESQL_URL[8:]

try:
    engine = create_engine(POSTGRESQL_URL)
except ImportError:
    # If psycopg2 is not installed, try using psycopg2-binary
    try:
        from psycopg2cffi import compat
        compat.register()
        engine = create_engine(POSTGRESQL_URL)
    except ImportError:
        raise ImportError("Neither psycopg2 nor psycopg2-binary is installed. Please install one of them.")

Session = sessionmaker(bind=engine)
session = Session()

def __create_work_instance(data: dict) -> JobPostUpwork:
    """
    Create and return an instance of the Work class.
    """
    return JobPostUpwork(
        job_title=data["job_title"],
        posted_on=data["posted_on"],
        description=json.dumps(data["description"]),
        job_data=json.dumps(data["job_data"]),
        link=data["link"]
    )


def insert_data(data: dict) -> None:
    try:
        session.add(__create_work_instance(data=data))
        session.commit()
        print("Work instance inserted successfully.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")


def get_all() -> list[dict]:
    try:
        all_work = session.query(JobPostUpwork).all()
        work_list = [
            {
                "id": work.id,
                "job_title": work.job_title,
                "posted_on": work.posted_on,
                "description": work.description,
                "job_data": work.job_data,
                "link": work.link
            }
            for work in all_work
        ]
        return work_list

    except Exception as e:
        print(f"unable to fetch data: {e}")
    finally:
        session.close()


if __name__ == '__main__':
    data = {
        "job_title": "NEW.work.job_title",
        "posted_on": "work.posted_on",
        "description": "work.descriptionkuhdffiuehfe",
        "job_data": "work.job_data",
        "link": "work.link"
    }
    insert_data(data)
    print(get_all())
