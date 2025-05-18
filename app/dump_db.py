import os
import subprocess
from datetime import datetime

from dotenv import load_dotenv

from app.logger import get_logger

logger = get_logger(__name__)
load_dotenv()


def dump_postgres_db(output_dir="dumps"):
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    db_password = os.getenv("DB_PASSWORD")

    if not all([db_user, db_name, db_password]):
        logger.error("Missing DB_USER, DB_NAME or DB_PASSWORD in environment variables.")
        raise ValueError("Missing required DB credentials.")

    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_filename = f"{db_name}_dump_{timestamp}.sql"
    dump_filepath = os.path.join(output_dir, dump_filename)

    # Construct pg_dump command
    command = [
        "pg_dump",
        "-h", db_host,
        "-p", str(db_port),
        "-U", db_user,
        db_name
    ]
    logger.debug(f"Running command: {' '.join(command)}")

    # Set password in environment
    env = os.environ.copy()
    env["PGPASSWORD"] = db_password

    try:
        with open(dump_filepath, "w") as f:
            subprocess.run(command, stdout=f, check=True, env=env)
        logger.info(f"Dump created successfully at: {dump_filepath}")
    except subprocess.CalledProcessError as e:
        logger.error(f"pg_dump failed with error: {e}")
        raise
