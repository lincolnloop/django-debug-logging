from __future__ import with_statement
from datetime import datetime
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
        from django.conf import settings
        from debug_logging.models import TestRun
        from debug_logging.utils import (get_project_name, get_hostname,
                                         get_revision)
        
        verbosity = int(options.get('verbosity', 1))
        self.quiet = verbosity < 1
        self.verbose = verbosity > 1
        
        # Create a TestRun object to track this run
        filters = {}
        panels = settings.DEBUG_TOOLBAR_PANELS
        if 'debug_logging.panels.identity.IdentityLoggingPanel' in panels:
            filters['project_name'] = get_project_name()
            filters['hostname'] = get_hostname()
        if 'debug_logging.panels.revision.RevisionLoggingPanel' in panels:
            filters['revision'] = get_revision()
        
        # Check to see if there is already a TestRun object open
        existing_run = TestRun.objects.filter(end__isnull=True, **filters)
        if existing_run:
            # If so, close it so that we can open a new one
            existing_run.end = datetime.now()
            existing_run.save()
        
        filters['start'] = datetime.now()
        test_run = TestRun(**filters)
        test_run.save()
        
        urls = []
        for url_list in url_lists:
            with open(url_list) as f:
                urls.extend([l.strip() for l in f.readlines()
                             if not l.startswith('#')])
        
        self.status_update('Beginning debug logging run...')
        
        client = Client()
        
        for url in urls:
            try:
                response = client.get(url)
            except KeyboardInterrupt, e:
                # Close out the log entry
                test_run.end = datetime.now()
                test_run.save()
                
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
        
        # Close out the log entry
        test_run.end = datetime.now()
        test_run.save()
        
        self.status_update('done!\n')
