# -*- coding: utf-8 -*-
from openerp import http, api
import json

def check_tokenOld(database, access_token):
    uid = http.request.session.authenticate(database, '', access_token)
    if uid:
        return api.Environment(http.request.cr, uid, http.request.context)


def check_token(database, login, password):
    uid = http.request.session.authenticate(database, login, password)
    if uid:
        return api.Environment(http.request.cr, uid, http.request.context)

def render_image(content, image_type='png'):
    headers = [('Content-Type', 'image/' + image_type)]
    return http.Response(content, headers=headers)


def render_json(model_dict):
    headers = [('Content-Type', 'application/json; charset=utf-8')]
    return http.Response(json.dumps(model_dict), headers=headers)


def render_template_json(template, context):
    headers = [('Content-Type', 'application/json; charset=utf-8')]
    return http.request.render(template, context, headers=headers)


def unauthorized(msg="Password error"):
    return http.Response(response=json.dumps({"error": msg}),
                         headers=[('Content-Type', 'application/json; charset=utf-8')],
                         status=401)


def not_found(msg="Resource not found"):
    return http.Response(response=json.dumps({"error": msg}),
                         headers=[('Content-Type', 'application/json; charset=utf-8')],
                         status=404)

def sendfile(filepath_or_fp, filename):
    print("*"*100)
    return http.send_file(filepath_or_fp, mimetype=None, as_attachment=True, filename=filename)

def bad_request(msg="Bad request"):
    return http.Response(response=json.dumps({"error": msg}),
                         headers=[('Content-Type', 'application/json; charset=utf-8')],
                         status=400)


def unprocessed(msg="cannot be processed"):
    return http.Response(response=json.dumps({"error": msg}),
                         headers=[('Content-Type', 'application/json; charset=utf-8')],
                         status=422)
