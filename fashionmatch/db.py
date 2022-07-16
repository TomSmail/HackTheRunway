import psycopg2
import os
from psycopg2 import extras
from flask import current_app, g
from configparser import ConfigParser


def init_db():
    """Helper for init. Executes schema.sql"""
    db, cur = get_db()
    schema_path = os.path.join(os.getcwd(), 'sql/schema.sql')
    with current_app.open_resource(schema_path) as f:
        cur.execute(f.read())
    return cur.fetchone()['version']  # DB Version


def seed_db():
    """Helper for seed. Executes seed.sql"""
    db, cur = get_db()
    seed_path = os.path.join(os.getcwd(), 'sql/seed.sql')
    with current_app.open_resource(seed_path) as f:
        cur.execute(f.read())


def get_config(filename="database.ini", section="postgresql"):
    """Parses and gets database config from file"""
    parser = ConfigParser()
    parser.read(filename)

    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception("Section {0} not found".format(section))

    return db_config


def get_db():
    """Attempt to connect to database and attach to global app"""
    if ("db" not in g) or ("cur" not in g):
        db_config = get_config()
        g.db = psycopg2.connect(**db_config)  # db connection
        g.db.autocommit = True
        g.cur = g.db.cursor(cursor_factory=extras.DictCursor)  # operation cursor
    return g.db, g.cur


def close_db(e=None):
    """Close database connection"""
    cur = g.pop("cur", None)
    if cur is not None:
        cur.close()
    db = g.pop("db", None)
    if db is not None:
        db.commit()
        db.close()


def rollback_db(e=None):
    """Rollback database connection"""
    db = g.pop("db", None)
    if db is not None:
        db.rollback()
        db.close()
