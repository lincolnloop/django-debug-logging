from django.conf import settings
from debug_toolbar.panels.timer import TimerDebugPanel


class TimerLoggingPanel(TimerDebugPanel):
    """Extends the Timer debug panel to enable logging."""
    
    def get_stats(self):
        """
        Taken from the beginning of TimerDebugPanel's 'content' method.
        """
        utime = 1000 * self._elapsed_ru('ru_utime')
        stime = 1000 * self._elapsed_ru('ru_stime')
        vcsw = self._elapsed_ru('ru_nvcsw')
        ivcsw = self._elapsed_ru('ru_nivcsw')
        minflt = self._elapsed_ru('ru_minflt')
        majflt = self._elapsed_ru('ru_majflt')
        
        return utime, stime, vcsw, ivcsw, minflt, majflt
    
    def process_response(self, request, response):
        response = super(TimerLoggingPanel, self).process_response(
            request, response)
        
        if getattr(settings, 'DEBUG_LOGGING_CONFIG', {}).get('ENABLED', False):
            utime, stime, vcsw, ivcsw, minflt, majflt = self.get_stats()
            stats = {
                'timer_utime': utime,
                'timer_stime': stime,
                'timer_cputime': (utime + stime),
                'timer_total': self.total_time,
                'timer_vcsw': vcsw,
                'timer_ivcsw': ivcsw,
            }
            request.debug_logging_stats.update(stats)
        
        return response
