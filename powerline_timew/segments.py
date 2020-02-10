# vim:fileencoding=utf-8:noet

import string
from subprocess import PIPE, run

from powerline.segments import Segment, with_docstring


class TimewSegment(Segment):

    def summary(self, task):
        proc = run(['timew', 'summary', 'today', ':id', task], stdout=PIPE)
        return proc.stdout.decode('UTF-8').splitlines()

    def limit_expired(self, limit, time_today):
        for i, j in zip(limit.split(':'), time_today.split(':')):
            if int(i) < int(j):
                return True
            elif int(i) > int(j):
                return False
        return True

    def __call__(self, pl, task='work', limit='8:00:00'):
        output = self.summary(task)
        if len(output) > 1:
            time_today = output[len(output) - 2].strip(string.whitespace)
            expired = self.limit_expired(limit, time_today)
            group = 'timew_expired' if expired else 'timew_unexpired'
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
