"""
This module contains example code for Flask usage.
Feel free to modify this file in any way.
"""
import json

from auth import introspect_token
from db import (
    get_num_projects, 
    initialize_db, 
    insert_project, 
    get_comments, 
    get_project_name,
    delete_project,
    insert_comment
)

from flask import Flask, Response, request

app = Flask(__name__)
initialize_db()


@app.route("/", methods=["GET"])
def example():
    """
    Basic example of GET to / using Flask
    Does not handle missing or invalid Access Tokens
    """
    if request.method == "GET":
        # get bearer token from auth header
        auth_header = request.headers.get("authorization")
        access_token = auth_header[len("Bearer ") :]

        # get username and num_projects to respond with
        token_info = introspect_token(access_token)
        user_info = token_info["user_info"]
        username = user_info["username"]
        num_projects = get_num_projects()

        # respond
        response_dict = {
            "message": (
                "Hello {}, there are {} projects in the database!".format(
                    username, num_projects
                )
            )
        }
        return Response(
            json.dumps(response_dict), status=200, mimetype="application/json"
        )

@app.route("/projects", methods=["POST"])
def create_project():
    """
    Create a project, and respond with the new project's information.
    """
    # get bearer token from auth header
    auth_header = request.headers.get("authorization")
    access_token = auth_header[len("Bearer ") :]
    
    # get username and num_projects to respond with
    token_info = introspect_token(access_token)
    user_info = token_info["user_info"]
    username = user_info["username"]
    user_id = user_info["user_id"]

    project_name = request.json.get('project_name', '')
    project_id = insert_project(project_name)
    # respond
    response_dict = {
        "project_id": project_id,
        "owner_id": user_id,
        "owner_username": username,
        "project_name": project_name,
        "comments": get_comments(project_id)
    }

    return Response(
        json.dumps(response_dict), status=200, mimetype="application/json"
    )


@app.route("/projects/<project_id>", methods=["GET", "DELETE"])
def project(project_id):
    # get bearer token from auth header
    auth_header = request.headers.get("authorization")
    access_token = auth_header[len("Bearer ") :]
    
    # get username and num_projects to respond with
    token_info = introspect_token(access_token)
    user_info = token_info["user_info"]
    username = user_info["username"]
    user_id = user_info["user_id"]

    """
    Get information on the project with the uuid provided in the url.
    """
    
    project_name = get_project_name(project_id)

    response_dict = {
        "project_id": project_id,
        "owner_id": user_id,
        "owner_username": username,
        "project_name": project_name,
        "comments": get_comments(project_id)
    }

    if request.method == "DELETE":
        delete_project(project_id)

    return Response(
        json.dumps(response_dict), status=200, mimetype="application/json"
    )

@app.route("/projects/<project_id>/comments", methods=["POST"])
def add_comment(project_id):
    # get bearer token from auth header
    auth_header = request.headers.get("authorization")
    access_token = auth_header[len("Bearer ") :]
    
    # get username and num_projects to respond with
    token_info = introspect_token(access_token)
    user_info = token_info["user_info"]
    username = user_info["username"]
    user_id = user_info["user_id"]

    message = request.json.get('message', '')
    comment_id = insert_comment(project_id, user_id, username, message)

    response_dict = {
        "comment_id": comment_id,
        "commenter_id": user_id,
        "commenter_username": username,
        "message": message
    }
    return Response(
        json.dumps(response_dict), status=200, mimetype="application/json"
    )



if __name__ == "__main__":
    app.run()
