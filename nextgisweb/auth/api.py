# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from pyramid.httpexceptions import HTTPForbidden

from ..models import DBSession
from .models import User, Group


def user_cget(request):
    request.require_administrator()
    return map(lambda o: o.serialize(), User.query())


def user_cpost(request):
    request.require_administrator()
    obj = User(system=False)
    obj.deserialize(request.json_body)
    obj.persist()

    DBSession.flush()
    return dict(id=obj.id)


def user_iget(request):
    request.require_administrator()
    obj = User.filter_by(id=request.matchdict['id']).one()
    return obj.serialize()


def user_iput(request):
    request.require_administrator()
    obj = User.filter_by(id=request.matchdict['id']).one()
    obj.deserialize(request.json_body)
    return dict(id=obj.id)


def group_cget(request):
    request.require_administrator()
    return map(lambda o: o.serialize(), Group.query())


def group_cpost(request):
    request.require_administrator()
    obj = Group(system=False)
    obj.deserialize(request.json_body)
    obj.persist()

    DBSession.flush()
    return dict(id=obj.id)


def group_iget(request):
    request.require_administrator()
    obj = Group.filter_by(id=request.matchdict['id']).one()
    return obj.serialize()


def group_iput(request):
    request.require_administrator()
    obj = Group.filter_by(id=request.matchdict['id']).one()
    obj.deserialize(request.json_body)
    return dict(id=obj.id)


def register(request):
    if not request.env.auth.settings_register:
        raise HTTPForbidden("Anonymous registration is not allowed!")

    # For self-registration only certain attributes of the user are required
    rkeys = ('display_name', 'description', 'keyname', 'password')
    src = request.json_body
    data = dict()
    for k in rkeys:
        if k in src:
            data[k] = src[k]

    # Add groups automatically assigned on registration
    data['member_of'] = map(
        lambda group: group.id,
        Group.filter_by(register=True))

    obj = User(system=False)
    obj.deserialize(data)
    obj.persist()

    DBSession.flush()
    return dict(id=obj.id)


def setup_pyramid(comp, config):
    config.add_route('auth.user.collection', '/api/component/auth/user/') \
        .add_view(user_cget, request_method='GET', renderer='json') \
        .add_view(user_cpost, request_method='POST', renderer='json')

    config.add_route('auth.user.item', '/api/component/auth/user/{id}') \
        .add_view(user_iget, request_method='GET', renderer='json') \
        .add_view(user_iput, request_method='PUT', renderer='json')

    config.add_route('auth.group.collection', '/api/component/auth/group/') \
        .add_view(group_cget, request_method='GET', renderer='json') \
        .add_view(group_cpost, request_method='POST', renderer='json')

    config.add_route('auth.group.item', '/api/component/auth/group/{id}') \
        .add_view(group_iget, request_method='GET', renderer='json') \
        .add_view(group_iput, request_method='PUT', renderer='json')

    config.add_route('auth.register', '/api/component/auth/register') \
        .add_view(register, request_method='POST', renderer='json')
