from flask.views import MethodView, View
import flask
import glob, json

class ProcReadView(MethodView):
    def __init__(self, path):
        self.path = path

    def get(self, uuid, fd):
        path = "%s/%s/%s" % (self.path, uuid, fd)

        resp = flask.make_response(file(path).read(), 200)
        resp.headers['Content-Type'] = 'text/plain'

        return resp

class ProcView(MethodView):
    def __init__(self, path):
        self.path = path

    def get(self, uuid):
        path = "%s/%s/state.json" % (self.path, uuid)

        resp = flask.make_response(file(path).read(), 200)
        resp.headers['Content-Type'] = 'application/json'

        return resp

class ProcListView(View):
    def __init__(self, path):
        self.path = path

    def dispatch_request(self):
        objects = {
            'results': []
        }

        for info in glob.glob("%s/*/state.json" % (self.path)):
            data = json.loads(file(info).read())
            data['uuid'] = info[-47:-11]

            objects['results'].append(data)

        r = flask.make_response(json.dumps(objects))
        r.headers['Content-Type'] = 'application/json'

        return r