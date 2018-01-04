#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-02-23 00:19:06


import sys
import time
import socket
import inspect
import datetime
import traceback
from flask import render_template, request, json

try:
    import flask_login as login
except ImportError:
    from flask.ext import login

from pyspider.libs import utils, sample_handler, dataurl, sample_handler_spiderweb
from pyspider.libs.response import rebuild_response
from pyspider.processor.project_module import ProjectManager, ProjectFinder
from .app import app

default_task = {
    'taskid': 'data:,on_start',
    'project': '',
    'url': 'data:,on_start',
    'process': {
        'callback': 'on_start',
    },
}
default_script_spiderweb = inspect.getsource(sample_handler_spiderweb)


@app.route('/spiderweb/debug/<project>', methods=['GET', 'POST'])
def spiderweb_debug(project):
    print(request.values)
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script'])
    if info:
        script = info['script']
    else:
        script = (default_script_spiderweb
                  .replace('__DATE__', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                  .replace('__PROJECT_NAME__', project)
                  .replace('__START_URL__', request.values.get('start-url') or '__START_URL__')
                  .replace('__KEY_NAME__', request.values.get('key-name') or '__KEY_NAME__')
                  .replace('__KEY_TAG_SELECTOR__', request.values.get('key-tag-selector') or '__KEY_TAG_SELECTOR__')
                  .replace('__KEY_ATTR__', request.values.get('key-attr') or '__KEY_ATTR__')

                  .replace('__NEXTPAGE_NAME__', request.values.get('nextpage-name') or '__NEXTPAGE_NAME__')
                  .replace('__NEXTPAGE_TAG_SELECTOR__', request.values.get('nextpage-tag-selector') or '__NEXTPAGE_TAG_SELECTOR__')
                  .replace('__NEXTPAGE_ATTR__', request.values.get('nextpage-attr') or '__NEXTPAGE_ATTR__')
                  .replace('__PAGE_NUM__', request.values.get('page-num') or '__PAGE_NUM__')

                  .replace('__TITLE_TAG_SELECTOR__', request.values.get('title-tag-selector') or '__TITLE_TAG_SELECTOR__')
                  .replace('__TITLE_ATTR__', request.values.get('title-attr') or '__TITLE_ATTR__')

                  .replace('__CONTENT_TAG_SELECTOR__', request.values.get('content-tag-selector') or '__CONTENT_TAG_SELECTOR__')
                  .replace('__PUBLISH_TIME_NAME__', request.values.get('publish-time-name') or '__PUBLISH_TIME_NAME__')
                  .replace('__PUBLISH_TIME_TAG_SELECTOR__', request.values.get('publish-time-tag-selector') or '__PUBLISH_TIME_TAG_SELECTOR__')

                  .replace('__FILTER_WORDS__', request.values.get('filter-words') or ''))


    taskid = request.args.get('taskid')
    if taskid:
        taskdb = app.config['taskdb']
        task = taskdb.get_task(
            project, taskid, ['taskid', 'project', 'url', 'fetch', 'process'])
    else:
        task = default_task

    default_task['project'] = project
    return render_template("debug_spiderweb.html", task=task, script=script, project_name=project)

@app.route('/spiderweb/debug/<project>/get_script_save_run', methods=['GET', 'POST'])
def spiderweb_debug_get_script_save_run(project):
    print(request.values)
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script'])
    if info:
        script = info['script']
    else:
        script = (default_script_spiderweb
                  .replace('__DATE__', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                  .replace('__PROJECT_NAME__', project)
                  .replace('__START_URL__', request.values.get('start-url') or '__START_URL__')
                  .replace('__KEY_NAME__', request.values.get('key-name') or '__KEY_NAME__')
                  .replace('__KEY_TAG_SELECTOR__', request.values.get('key-tag-selector') or '__KEY_TAG_SELECTOR__')
                  .replace('__KEY_ATTR__', request.values.get('key-attr') or '__KEY_ATTR__')

                  .replace('__NEXTPAGE_NAME__', request.values.get('nextpage-name') or '__NEXTPAGE_NAME__')
                  .replace('__NEXTPAGE_TAG_SELECTOR__', request.values.get('nextpage-tag-selector') or '__NEXTPAGE_TAG_SELECTOR__')
                  .replace('__NEXTPAGE_ATTR__', request.values.get('nextpage-attr') or '__NEXTPAGE_ATTR__')
                  .replace('__PAGE_NUM__', request.values.get('page-num') or '__PAGE_NUM__')

                  .replace('__TITLE_TAG_SELECTOR__', request.values.get('title-tag-selector') or '__TITLE_TAG_SELECTOR__')
                  .replace('__TITLE_ATTR__', request.values.get('title-attr') or '__TITLE_ATTR__')

                  .replace('__CONTENT_TAG_SELECTOR__', request.values.get('content-tag-selector') or '__CONTENT_TAG_SELECTOR__')
                  .replace('__PUBLISH_TIME_NAME__', request.values.get('publish-time-name') or '__PUBLISH_TIME_NAME__')
                  .replace('__PUBLISH_TIME_TAG_SELECTOR__', request.values.get('publish-time-tag-selector') or '__PUBLISH_TIME_TAG_SELECTOR__')

                  .replace('__FILTER_WORDS__', request.values.get('filter-words') or ''))


    taskid = request.args.get('taskid')
    if taskid:
        taskdb = app.config['taskdb']
        task = taskdb.get_task(
            project, taskid, ['taskid', 'project', 'url', 'fetch', 'process'])
    else:
        task = default_task

    default_task['project'] = project
    # return render_template("debug_spiderweb.html", task=task, script=script, project_name=project)
    # projectdb = app.config['projectdb']
    # if not projectdb.verify_project_name(project):
    #     return 'project name is not allowed!', 400
    # script = request.form['script']
    project_info = projectdb.get(project, fields=['name', 'status', 'group'])
    if project_info and 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    if project_info:
        info = {
            'script': script,
        }
        if project_info.get('status') in ('DEBUG', 'RUNNING', ):
            info['status'] = 'CHECKING'
        projectdb.update(project, info)
    else:
        info = {
            'name': project,
            'script': script,
            'status': 'TODO',
            'rate': app.config.get('max_rate', 1),
            'burst': app.config.get('max_burst', 3),
        }
        projectdb.insert(project, info)

    rpc = app.config['scheduler_rpc']
    if rpc is not None:
        try:
            rpc.update_project()
        except socket.error as e:
            app.logger.warning('connect to scheduler rpc error: %r', e)
            return 'rpc error', 200

    return 'ok', 200

@app.before_first_request
def spiderweb_enable_projects_import():
    sys.meta_path.append(ProjectFinder(app.config['projectdb']))


@app.route('/spiderweb/debug/<project>/run', methods=['POST', ])
def spiderweb_run(project):
    start_time = time.time()
    try:
        task = utils.decode_unicode_obj(json.loads(request.form['task']))
    except Exception:
        result = {
            'fetch_result': "",
            'logs': u'task json error',
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
        return json.dumps(utils.unicode_obj(result)), \
            200, {'Content-Type': 'application/json'}

    project_info = {
        'name': project,
        'status': 'DEBUG',
        'script': request.form['script'],
    }

    if request.form.get('webdav_mode') == 'true':
        projectdb = app.config['projectdb']
        info = projectdb.get(project, fields=['name', 'script'])
        if not info:
            result = {
                'fetch_result': "",
                'logs': u' in wevdav mode, cannot load script',
                'follows': [],
                'messages': [],
                'result': None,
                'time': time.time() - start_time,
            }
            return json.dumps(utils.unicode_obj(result)), \
                200, {'Content-Type': 'application/json'}
        project_info['script'] = info['script']

    fetch_result = {}
    try:
        module = ProjectManager.build_module(project_info, {
            'debugger': True,
            'process_time_limit': app.config['process_time_limit'],
        })

        # The code below is to mock the behavior that crawl_config been joined when selected by scheduler.
        # but to have a better view of joined tasks, it has been done in BaseHandler.crawl when `is_debugger is True`
        # crawl_config = module['instance'].crawl_config
        # task = module['instance'].task_join_crawl_config(task, crawl_config)

        fetch_result = app.config['fetch'](task)
        response = rebuild_response(fetch_result)

        ret = module['instance'].run_task(module['module'], task, response)
    except Exception:
        type, value, tb = sys.exc_info()
        tb = utils.hide_me(tb, globals())
        logs = ''.join(traceback.format_exception(type, value, tb))
        result = {
            'fetch_result': fetch_result,
            'logs': logs,
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
    else:
        result = {
            'fetch_result': fetch_result,
            'logs': ret.logstr(),
            'follows': ret.follows,
            'messages': ret.messages,
            'result': ret.result,
            'time': time.time() - start_time,
        }
        result['fetch_result']['content'] = response.text
        if (response.headers.get('content-type', '').startswith('image')):
            result['fetch_result']['dataurl'] = dataurl.encode(
                response.content, response.headers['content-type'])

    try:
        # binary data can't encode to JSON, encode result as unicode obj
        # before send it to frontend
        return json.dumps(utils.unicode_obj(result)), 200, {'Content-Type': 'application/json'}
    except Exception:
        type, value, tb = sys.exc_info()
        tb = utils.hide_me(tb, globals())
        logs = ''.join(traceback.format_exception(type, value, tb))
        result = {
            'fetch_result': "",
            'logs': logs,
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
        return json.dumps(utils.unicode_obj(result)), 200, {'Content-Type': 'application/json'}


@app.route('/spiderweb/debug/<project>/save', methods=['POST', ])
def spiderweb_save(project):
    print(request.values)
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    script = request.form['script']
    project_info = projectdb.get(project, fields=['name', 'status', 'group'])
    if project_info and 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    if project_info:
        info = {
            'script': script,
        }
        if project_info.get('status') in ('DEBUG', 'RUNNING', ):
            info['status'] = 'CHECKING'
        projectdb.update(project, info)
    else:
        info = {
            'name': project,
            'script': script,
            'status': 'TODO',
            'rate': app.config.get('max_rate', 1),
            'burst': app.config.get('max_burst', 3),
        }
        projectdb.insert(project, info)

    rpc = app.config['scheduler_rpc']
    if rpc is not None:
        try:
            rpc.update_project()
        except socket.error as e:
            app.logger.warning('connect to scheduler rpc error: %r', e)
            return 'rpc error', 200

    return 'ok', 200

@app.route('/spiderweb/debug/<project>/get')
def spiderweb_get_script(project):
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script'])
    return json.dumps(utils.unicode_obj(info)), \
        200, {'Content-Type': 'application/json'}


@app.route('/spiderweb/blank.html')
def spiderweb_blank_html():
    return ""
