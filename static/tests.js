/*module("project tests", {
  setup: function () {
    var me = this;

    this.url = '';
    this.apiToken = '';

    // authenticate
    var method = 'authenticate';
    var data = { email: 'tracky@tracky.net', password: '111111' };
    var type = 'POST';

    api_test(this.url + method, type, data, function (result) {
      ok(result.success, method + " method call failed");

      me.apiToken = result.data.apiToken;
      ok(me.apiToken.length == 32, "invalid api token");
    });
  }
});*/

function api_test(url, type, data, callback) {
  $.ajax({
    url: url,
    type: type,
    processData: false,
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    dataType: 'json',
    async: false,
    complete: function (result) {
      if (result.status == 0) {
        ok(false, '0 status - browser could be on offline mode');
      } else if (result.status == 404) {
        ok(false, '404 error');
      } else {
        callback($.parseJSON(result.responseText));
      }
    }
  });
}

function createCallUrl(method, params) {
  var callUrl = "/" + method;
  for (var p in params) {
    callUrl += "/" + params[p];
  }
  return callUrl;
}

module("project tests");

test("list projects", function () {
  var method = 'projects';
  var data = null;
  var type = 'GET';
  var params = [];
  var expected_project = {
    "id": "5e8ff9bf55ba3508199d22e984129be6",
    "name": "sample"
  }

  var call = createCallUrl(method, params);

  api_test(call, type, data, function (projects) {
    ok(projects, method + " method call");
    ok(projects.items.length >= 1, "projects has been returned");
    $.each(projects.items, function(index, project) {
      ok(project['id'], "valid project");
      ok(project['name'], "valid project");
    })
  });
});

test("build projects", function () {
  var method = 'projects/5e8ff9bf55ba3508199d22e984129be6/build';
  var data = {};
  var type = 'POST';
  var params = [];

  var call = createCallUrl(method, params);

  api_test(call, type, data, function (build) {
    ok(build, method + " method call");
  });
});
