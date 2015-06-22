#!/usr/bin/python

from flask import Flask, request, render_template
from flask_restful import Resource, Api
from md5 import md5
from copy import deepcopy

projects_data = [
  {
    'id': md5('sample').hexdigest(),
    'url': '/projects/' + md5('sample').hexdigest(),
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
    'url': '/projects/' + md5('sample2').hexdigest(),
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
api = Api(app)

@app.route("/tests.html")
def test():
  print(app.root_path)
  return render_template('tests.html')
  
@api.resource('/projects/')
class ProjectListAPI(Resource):
  def get(self):
    return {
      'items': [project_simplify(project) for project in projects_data]
    }

@api.resource('/projects/<string:project_id>')
class ProjectAPI(Resource):
  def get(self, project_id):
    return project_simplify(project_find(project_id))

@api.resource('/projects/<string:project_id>/build')
class ProjectBuildAPI(Resource):
  def post(self, project_id):
    return {
      'id': md5('sample-build-1').hexdigest(),
      'status': 'scheduled'
    }

@api.resource('/projects/<string:project_id>/resources')
class ResourceListAPI(Resource):
  def get(self, project_id):
    return {
      'items': project_find(project_id)['resources']
    }

@api.resource('/projects/<string:project_id>/resources/<string:resource_id>')
class ResourceAPI(Resource):
  def get(self, project_id, resource_id):
    return resource_find(project_id, resource_id)

@api.resource('/builds/')
class BuildListAPI(Resource):
  def get(self):
    return {
      'items': builds_data
    }

@api.resource('/builds/<string:build_id>')
class BuildAPI(Resource):
  def get(self, build_id):
    return build_find(build_id)

def project_simplify(project):
  return {
    'id': project['id'],
    'url': project['url'],
    'name': project['name']
  }

def project_find(project_id):
  return find(project_id, projects_data)

def find(element_id, collection):
  return next(element for element in collection if element['id'] == element_id)

def resource_find(project_id, resource_id):
  return next(resource for resource in project_find(project_id)['resources'] if resource['id'] == resource_id)

def build_find(build_id):
  return find(build_id, builds_data)

if __name__ == "__main__":
  app.run(debug=True)

