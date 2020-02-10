# vim:fileencoding=utf-8:noet

import string
import re
from subprocess import PIPE, run

from powerline.segments import Segment, with_docstring


class TimewSegment(Segment):

    def summary(self, task):
        proc = run(['timew', 'summary', 'today', ':id', task], stdout=PIPE)
        return proc.stdout.decode('UTF-8').splitlines()

    def time_today(self, task):
        output = self.summary(task)
        if len(output) > 1:
            time = output[len(output) - 2].strip(string.whitespace)
            last_entry = output[len(output) - 4]
            pattern = re.compile('{} +[0-9:]+ +-'.format(task))
            running = pattern.search(last_entry) is not None
            return time, running
        return None, False

    def limit_expired(self, limit, time_today):
        for i, j in zip(limit.split(':'), time_today.split(':')):
            if int(i) < int(j):
                return True
            elif int(i) > int(j):
                return False
        return True

    def __call__(self, pl, task='work', limit='8:00:00'):
        time_today, running = self.time_today(task)
        if time_today is not None:
            if self.limit_expired(limit, time_today):
                group = 'timew_expired'
            elif not running:
                group = 'timew_paused'
            else:
                group = 'timew_running'
            return [
                {
                    'contents': time_today,
                    'highlight_groups': [group, 'timew']
                }
            ]
        return []


timew = with_docstring(TimewSegment(), '''
    Return the time worked so far in a particular task.
    ''')
