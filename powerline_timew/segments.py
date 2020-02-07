# vim:fileencoding=utf-8:noet

import os
import string
from subprocess import PIPE, Popen

from powerline.segments import Segment, with_docstring


class TimewSegment(Segment):

    def execute(self, pl, task):
        pl.debug('Executing command: timew summary today %s' % task)

        git_env = os.environ.copy()
        git_env['LC_ALL'] = 'C'

        proc = Popen(['timew', 'summary', 'today', task], stdout=PIPE,
                     stderr=PIPE, env=git_env)
        out, err = [item.decode('utf-8') for item in proc.communicate()]

        if out:
            pl.debug('Command output: %s' % out.strip(string.whitespace))
        if err:
            pl.debug('Command errors: %s' % err.strip(string.whitespace))

        return out.splitlines()

    def __call__(self, pl, task='work'):
        pl.debug('Running timew for task %s' % task)

        output = self.execute(pl, task)
        if len(output) > 1:
            return output[len(output) - 2].strip(string.whitespace)
        return []


timew = with_docstring(TimewSegment(), '''
    Return the time worked so far in a particular task.
    ''')
