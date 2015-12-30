"""Tests for HTML pages"""

import requests

from ..utils import url_path_join as ujoin
from .. import orm

import mock
from .mocking import FormSpawner


def get_page(path, app, **kw):
    base_url = ujoin(app.proxy.public_server.host, app.hub.server.base_url)
    print(base_url)
    return requests.get(ujoin(base_url, path), **kw)

def test_root_no_auth(app, io_loop):
    print(app.hub.server.is_up())
    routes = io_loop.run_sync(app.proxy.get_routes)
    print(routes)
    print(app.hub.server)
    r = requests.get(app.proxy.public_server.host)
    r.raise_for_status()
    assert r.url == ujoin(app.proxy.public_server.host, app.hub.server.base_url, 'login')

def test_root_auth(app):
    cookies = app.login_user('river')
    r = requests.get(app.proxy.public_server.host, cookies=cookies)
    r.raise_for_status()
    assert r.url == ujoin(app.proxy.public_server.host, '/user/river')

def test_home_no_auth(app):
    r = get_page('home', app, allow_redirects=False)
    r.raise_for_status()
    assert r.status_code == 302
    assert '/hub/login' in r.headers['Location']

def test_home_auth(app):
    cookies = app.login_user('river')
    r = get_page('home', app, cookies=cookies)
    r.raise_for_status()
    assert r.url.endswith('home')

def test_admin_no_auth(app):
    r = get_page('admin', app)
    assert r.status_code == 403

def test_admin_not_admin(app):
    cookies = app.login_user('wash')
    r = get_page('admin', app, cookies=cookies)
    assert r.status_code == 403

def test_admin(app):
    cookies = app.login_user('river')
    u = orm.User.find(app.db, 'river')
    u.admin = True
    app.db.commit()
    r = get_page('admin', app, cookies=cookies)
    r.raise_for_status()
    assert r.url.endswith('/admin')

def test_spawn_redirect(app):
    cookies = app.login_user('wash')
    r = get_page('spawn', app, cookies=cookies)
    assert r.url.endswith('/wash')

def test_spawn_page(app):
    with mock.patch.dict(app.users.settings, {'spawner_class': FormSpawner}):
        cookies = app.login_user('jones')
        r = get_page('spawn', app, cookies=cookies)
        assert r.url.endswith('/spawn')
        assert FormSpawner.options_form in r.text

def test_spawn_form(app, io_loop):
    with mock.patch.dict(app.users.settings, {'spawner_class': FormSpawner}):
        base_url = ujoin(app.proxy.public_server.host, app.hub.server.base_url)
        cookies = app.login_user('jones')
        orm_u = orm.User.find(app.db, 'jones')
        u = app.users[orm_u]
        io_loop.run_sync(u.stop)
    
        r = requests.post(ujoin(base_url, 'spawn'), cookies=cookies, data={
            'bounds': ['-1', '1'],
            'energy': '511keV',
        })
        r.raise_for_status()
        print(u.spawner)
        print(u.spawner.user_options)
        assert u.spawner.user_options == {
            'energy': '511keV',
            'bounds': [-1, 1],
            'notspecified': 5,
        }

