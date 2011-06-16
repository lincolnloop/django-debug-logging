from __future__ import with_statement
import sys

from django.test.client import Client
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Hit a list of urls in sequence so that the requests will be logged'
    args = "url_list [url_list ...]"
    
    def status_update(self, msg):
        if not self.quiet:
            print msg
    
    def status_ticker(self):
        if not self.quiet:
            sys.stdout.write('.')
            sys.stdout.flush()
    
    def handle(self, *url_lists, **options):
        verbosity = int(options.get('verbosity', 1))
        self.quiet = verbosity < 1
        self.verbose = verbosity > 1
        
        urls = []
        for url_list in url_lists:
            with open(url_list) as f:
                urls.extend([l.strip() for l in f.readlines()
                             if not l.startswith('#')])
        
        self.status_update('Beginning debug logging run...')
        
        for url in urls:
            try:
                self.client = Client()
                print url
                response = self.client.get(url)
            except KeyboardInterrupt, e:
                raise CommandError('Debug logging run cancelled.')
            except:
                if self.verbose:
                    self.status_update('\nSkipped %s because of an error'
                                       % url)
                    continue
            if response and response.status_code == 200:
                self.status_ticker()
            else:
                self.status_update('\nURL %s responded with code %s'
                                   % (url, response.status_code))
        self.status_update('done!\n')
