import ioc
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):

        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/services.yml" % path, container_builder)
        loader.load("%s/resources/config/responders.yml" % path, container_builder)

        container_builder.parameters.set('shirka.web.public.dir', config.get('public_dir', "%s/resources/public" % path))
        container_builder.parameters.set('shirka.bot.name', config.get('bot.name', 'Shirka'))
        container_builder.parameters.set('shirka.bot.email', config.get('bot.email', 'no-reply@nowhere'))
        container_builder.parameters.set('shirka.bot.url', config.get('bot.url', 'http://nowhere'))

        container_builder.parameters.set('shirka.web.api.base_url', config.get('api.base_url', ''))

        if not config.get('data_dir', False):
            raise Exception("Please configure the data_dir settings")

        container_builder.parameters.set('shirka.data.dir', config.get('data_dir', False))

    def pre_build(object, container_builder, container):
        """
        Configure Flask instance and Twisted
        """
        definition = container_builder.get('ioc.extra.flask.app')

        base_url = container_builder.parameters.get('shirka.web.api.base_url')
        definition.method_calls.append([
            'add_url_rule', 
            ['%s/process' % base_url],
            {'view_func': ioc.component.Reference('shirka.flask.view.shirka_proc_list')}
        ])

        definition.method_calls.append([
            'add_url_rule', 
            ['%s/process/<id>' % base_url],       
            {'view_func': ioc.component.Reference('shirka.flask.view.shirka_proc_view')}
        ])

        definition.method_calls.append([
            'add_url_rule', 
            ['%s/process/<id>/<fd>' % base_url], 
            {'view_func': ioc.component.Reference('shirka.flask.view.shirka_proc_read_view')}
        ])


        definition = container_builder.get('ioc.extra.twisted.reactor')
        definition.method_calls.append([
            'listenTCP', 
            ['%ioc.extra.flask.app.port%', ioc.component.Reference('shirka.twisted.web.site')],
            {}
        ])


