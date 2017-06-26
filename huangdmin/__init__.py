#!encoding=utf-8

from __future__ import print_function

import os
import time

from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
from sqlalchemy import inspect

__version__ = 0.1
__author__ = 'huang'


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('huangAdmin.log', 'a', encoding='utf-8') as f:
        # 通过 file 参数可以把输出写入到文件 f 中
        print(dt, *args, file=f, **kwargs)


def fields_from_model(model, except_primary=False):
    m = inspect(model)
    fields = m.columns.keys()
    if except_primary:
        for p in m.primary_key:
            n = p.name
            fields.remove(n)
        return fields
    else:
        return fields


def table_name_from_model(model):
    n = model.__tablename__
    return n


class huangAdminException(Exception):
    pass


def make_model_mixin(db):

    class ModelMixin(object):
        def __repr__(self):
            class_name = self.__class__.__name__
            properties = (u'{0}=({1})'.format(k, v) for k, v in self.__dict__.items())
            return u'<{0}: \n{1}\n>'.format(class_name, '  \n'.join(properties))

        @classmethod
        def _ca_init(cls, form):
            item = cls()
            for k, v in form.items():
                setattr(item, k, v)
            return item

        def _ca_to_json(self):
            fields = fields_from_model(self.__class__)
            j = {k: getattr(self, k) for k in fields}
            return j

        def _ca_save(self):
            db.session.add(self)
            db.session.commit()

        def _ca_delete(self):
            db.session.delete(self)
            db.session.commit()

        @classmethod
        def _check(cls, form):
            uploaded_fields = form.keys()
            fields = fields_from_model(cls)
            return set(uploaded_fields).issubset(set(fields))

        @classmethod
        def create(cls, form):
            if cls._check(form):
                item = cls._ca_init(form)
                item._ca_save()
                return True
            else:
                return False

        def delete_filtered(self):
            pass

        @classmethod
        def _ca_get(cls, id):
            return cls.query.get(id)

        @classmethod
        def _ca_filter(cls, *args, **kwargs):
            try:
                return cls.query.filter_by(*args, **kwargs).all()
            except Exception as e:
                log(e)

        def _ca_update(self, form):
            assert type(form) is dict
            if self._check(form):
                for k, v in form.items():
                    setattr(self, k, v)
                self._ca_save()
            else:
                e = '{}:update----your form is wrong'.format(self.__class__.__name__)
                raise huangAdminException(e)

    return ModelMixin


def add_mixin(target_cls, mixin):
    bases = target_cls.__bases__
    # already has a mixin
    # if len(bases) == 2:
    #     raise huangAdminException('huangAdmin:add_mixin----Already has a mixin')
    # else:
    l = list(bases)
    l.append(mixin)
    new_bases = tuple(l)
    target_cls.__bases__ = new_bases


def sibling_dir(sibling_name):
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    d = '{}/{}'.format(parent_dir, sibling_name)
    return d


def json_response_error(msg=u'服务器出错了'):
    data = {
        'error': 1,
        'message': msg,
    }
    r = jsonify(data)
    return r


def json_response_ok(data, msg=''):
    data = {
        'error': 0,
        'message': msg,
        'data': data,
    }
    r = jsonify(data)
    return r


class HuangAdmin(object):

    def __init__(self, app, db, models, name='huangAdmin'):
        self.app = app
        self.db = db
        self.models = self.equip_mixin(models)
        self.blueprint = self.create_blueprint(name)
        self.model_dict = self._model_dict()

    def equip_mixin(self, models):
        mixin = make_model_mixin(self.db)
        for m in models:
            add_mixin(m, mixin)
        return models

    @classmethod
    def create_blueprint(cls, name):
        static_folder = sibling_dir('static')
        template_folder = sibling_dir('templates')
        b = Blueprint(name, __name__, static_folder=static_folder, template_folder=template_folder)
        return b

    def _model_dict(self):
        model_names = [table_name_from_model(m) for m in self.models]
        model_dict = dict(zip(model_names, self.models))
        return model_dict

    def init_app(self):
        self.add_jinja_ctx()
        self.add_views()
        self.app.register_blueprint(self.blueprint, url_prefix='/admin')

    def add_jinja_ctx(self):
        app = self.app

        @app.context_processor
        def jinja_ctx():
            model_names = self.model_dict.keys()
            return dict(model_names=model_names)

    def add_views(self):
        def index():
            return render_template('admin/base.html')

        def view_model():
            info = request.get_json()
            model_name = info.get('model')
            model = self.model_dict.get(model_name)
            fields = fields_from_model(model)
            data = [d._ca_to_json() for d in model.query.all()]
            return jsonify({
                'fields': fields,
                'data': data,
            })

        def add():
            info = request.get_json()
            model_name = info.pop('model')
            model = self.model_dict.get(model_name)
            r = model.create(info)
            return jsonify({
                'error': r,
            })

        def detail():
            info = request.get_json()
            model_name = info.get('model')
            model = self.model_dict.get(model_name)
            id = int(info.get('id'))
            d = model._ca_get(id)._ca_to_json()
            fields = fields_from_model(model)
            values = [d[k] for k in fields]
            return jsonify(values)

        def edit():
            info = request.get_json()
            model_name = info.pop('model')
            model = self.model_dict.get(model_name)
            id = int(info.get('id'))
            model._ca_get(id)._ca_update(info)
            return json_response_ok(True, u'编辑成功')

        def delete():
            info = request.get_json()
            model_name = info.get('model')
            model = self.model_dict.get(model_name)
            id = int(info.get('id'))
            model._ca_get(id)._ca_delete()
            return json_response_ok(True, u'删除成功')

        self.add_view('/', index)
        self.add_view('/model', view_model, methods=['POST'])
        self.add_view('/add', add, methods=['POST'])
        self.add_view('/detail', detail, methods=['POST'])
        self.add_view('/delete', delete, methods=['POST'])
        self.add_view('/edit', edit, methods=['POST'])

    def add_view(self, route, view_func, methods=None):
        if methods is None:
            methods = ['GET']
        assert type(methods) is list
        self.blueprint.add_url_rule(route, view_func.__name__, view_func=view_func, methods=methods)
