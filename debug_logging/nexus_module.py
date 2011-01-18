import nexus


class DebugLoggingModule(nexus.NexusModule):
    home_url = 'index'
    name = 'debug-logging'
    
    def get_title(self):
        return 'Django Debug Logging'
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        
        urlpatterns = patterns('',
            url(r'^$', self.as_view(self.index), name='index'),
        )
        
        return urlpatterns
    
    def render_on_dashboard(self, request):
        return self.render_to_string('nexus/debug_logging/dashboard.html', {
            'title': 'Django Debug Logging',
        })
    
    def index(self, request):
        return self.render_to_response("nexus/debug_logging/index.html", {
            'title': 'Django Debug Logging',
        }, request)

nexus.site.register(HelloWorldModule, 'hello-world')
