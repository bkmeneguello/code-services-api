#!/usr/bin/python

from flask import Flask, jsonify
from md5 import md5
from copy import deepcopy

projects_data = [
  {
    'id': md5('sample').hexdigest(),
    'name': 'sample',
    'resources': [
      {
        'id': md5('/pom.xml').hexdigest(),
        'name': 'pom.xml',
        'path': '/'
      },
      {
        'id': md5('/src/').hexdigest(),
        'name': 'src',
        'path': '/src/'
      },
      {
        'id': md5('/src/Main.java').hexdigest(),
        'name': 'Main.java',
        'path': '/src/'
      }
    ]
  },
  {
    'id': md5('sample2').hexdigest(),
    'name': 'sample2'
  }
]

app = Flask(__name__)

@app.route("/")
def index():
  return jsonify({})

def project_simplify(project):
  return {
    'id': project['id'],
    'name': project['name']
  }

@app.route("/projects")
def projects():
  return jsonify({
    'items': [project_simplify(project) for project in projects_data]
  })

def project_find(project_id):
  return next(project for project in projects_data if project['id'] == project_id)

@app.route("/projects/<project_id>")
def project_get(project_id):
  return jsonify(project_simplify(project_find(project_id)))

@app.route("/projects/<project_id>/resources")
def resources(project_id):
  return jsonify({
    'items': project_find(project_id)['resources'] 
  })

def resource_find(project_id, resource_id):
  return next(resource for resource in project_find(project_id)['resources'] if resource['id'] == resource_id)

@app.route("/projects/<project_id>/resources/<resource_id>")
def resources_get(project_id, resource_id):
  return jsonify(resource_find(project_id, resource_id))

if __name__ == "__main__":
  app.run(debug=True)

