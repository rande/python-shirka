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

        self.build_flowdock_consumer(config, container_builder)

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


    def build_flowdock_consumer(self, config, container_builder):
        if not config.get('flowdock'):
            return

        flowdock = config.get_dict('flowdock')

        container_builder.parameters.set('shirka.flowdock.user.token', flowdock.get_dict('user_token'))
        defaults = {
            'organisation': False,
            'name': False,
            'token': False,
            'responders': []
        }

        for name, parameters in flowdock.get_dict('channels').all().iteritems():
            d = defaults.copy()
            
            d.update(parameters.all())

            container_builder.parameters.set('shirka.flowdock.%s.organisation' % name, d['organisation'])
            container_builder.parameters.set('shirka.flowdock.%s.name' % name, d['name'])
            container_builder.parameters.set('shirka.flowdock.%s.token' % name, d['token'])

            flowdockId = "shirka.flowdock.%s" % name
            loggerId = "shirka.consumer.flowdock.%s.logger" % name
            consumerId = "shirka.consumer.flowdock.%s" % name

            container_builder.add(flowdockId, ioc.component.Definition('flowdock.FlowDock', [], {
                'api_key': d['token'],
                'app_name': name,
                'project': d['name'],
            }))

            container_builder.add(loggerId, ioc.component.Definition('logging.getLogger', [consumerId]))

            container_builder.add(consumerId, ioc.component.Definition('shirka.consumers.FlowDockConsumer', [
                ioc.component.Reference('shirka.bot'),
                d['token'],
                [(responderId, ioc.component.Reference(responderId)) for responderId in d['responders']],
                ioc.component.Reference(flowdockId),
            ], {
                'logger': ioc.component.Reference(loggerId)
            }))
