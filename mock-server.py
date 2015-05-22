#!/usr/bin/python

from flask import Flask, request, jsonify
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

builds_data = [
  {
    'id': md5('sample-build-1').hexdigest(),
    'status': 'scheduled'
  },
  {
    'id': md5('sample2-build-2').hexdigest(),
    'status': 'running'
  },
  {
    'id': md5('sample2-build-1').hexdigest(),
    'status': 'done'
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
  return find(project_id, projects_data)

def find(element_id, collection):
  return next(element for element in collection if element['id'] == element_id)

@app.route("/projects/<project_id>")
def project_get(project_id):
  return jsonify(project_simplify(project_find(project_id)))

@app.route("/projects/<project_id>/build", methods=['POST'])
def project_build(project_id):
  print(request.get_json(silent=True))
  return jsonify({
    'id': md5('sample-build-1').hexdigest(),
    'status': 'scheduled'
  })

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

@app.route("/builds")
def builds():
  return jsonify({
    'items': builds_data
  })

@app.route("/builds/<build_id>")
def build_get(build_id):
  return jsonify(build_find(build_id))

def build_find(build_id):
  return find(build_id, builds_data)

if __name__ == "__main__":
  app.run(debug=True)

