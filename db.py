"""
This module contains example code for basic SQLite usage.
Feel free to modify this file in any way.
"""
import sqlite3
import uuid


def get_db():
    """Connect to a sqlite database and turn on foreign key constraints."""
    conn = sqlite3.connect("globus_challenge.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    return c


def initialize_db():
    """
    Creates tables in the database if they do not already exist.
    Make sure to clean up old .db files on schema changes.
    """
    try:
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                project_id BINARY(16) PRIMARY KEY,
                project_name TEXT
            );
            """
        )

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                comment_id BINARY(16) PRIMARY KEY,
                project_id BINARY(16) NOT NULL,
                commenter_id BINARY(16) NOT NULL,
                commenter_username TEXT,
                message TEXT
            );
            """
        )

        db.connection.commit()
    except sqlite3.OperationalError:
        pass


def get_num_projects():
    """
    Example of a simple SQL query using SQLite
    """
    db = get_db()
    db.execute("SELECT COUNT(project_id) FROM projects")
    return db.fetchone()[0]

def insert_project(project_name):
    """
    Insert a new project
    """
    project_id = str(uuid.uuid4())
    db = get_db()
    query = f"INSERT INTO projects (project_id, project_name) VALUES ('{project_id}', '{project_name}')"
    db.execute(query)
    db.connection.commit()
    return project_id


def get_project_name(project_id):
    """
    Get project info
    """
    db = get_db()
    db.execute(f"SELECT project_name FROM projects WHERE project_id = '{project_id}'")
    return db.fetchone()[0]

def delete_project(project_id):
    """
    Delete the project with the uuid provided in the url. Any comments on the project should be deleted as well.
    """
    db = get_db()
    db.execute(f"DELETE FROM comments WHERE project_id = '{project_id}'")
    db.execute(f"DELETE FROM projects WHERE project_id = '{project_id}'")
    db.connection.commit()

def get_comments(project_id):
    """
    Get comments as dict
    """
    db = get_db()
    db.execute(f"SELECT comment_id, commenter_id, commenter_username, message FROM comments WHERE project_id = '{project_id}'")
    columns = [col[0] for col in db.description]
    return [dict(zip(columns, row)) for row in db.fetchall()]

def insert_comment(project_id, commenter_id, commenter_username, message):
    """
    Add a comment
    """

    comment_id = str(uuid.uuid4())

    db = get_db()
    query = f"INSERT INTO comments (comment_id, project_id, commenter_id, commenter_username, message) \
        VALUES ('{comment_id}', '{project_id}', '{commenter_id}', '{commenter_username}', '{message}')"
    db.execute(query)
    db.connection.commit()
    return comment_id