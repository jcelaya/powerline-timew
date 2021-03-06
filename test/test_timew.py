# vim:fileencoding=utf-8:noet

from subprocess import run
from time import sleep
from powerline_timew.segments import timew


class TestTimew:
    def delete_task(self, task):
        summary = timew.summary(task)
        while len(summary) > 1:
            id = summary[3].split()[3]
            run(['timew', 'delete', id])
            summary = timew.summary(task)

    def test_limit_expired(self):
        assert timew.limit_expired("8:00:00", "8:00:00")
        assert timew.limit_expired("8:00:00", "9:00:00")
        assert timew.limit_expired("8:00:00", "8:10:00")
        assert timew.limit_expired("8:00:00", "8:00:10")
        assert not timew.limit_expired("8:00:00", "7:00:00")
        assert not timew.limit_expired("8:10:00", "8:00:00")
        assert not timew.limit_expired("8:10:10", "8:10:00")

    def test_summary(self):
        task = 'foo'

        self.delete_task(task)
        assert len(timew.summary(task)) == 1
        run(['timew', 'start', task])
        assert len(timew.summary(task)) == 7
        run(['timew', 'stop'])
        run(['timew', 'continue'])
        assert len(timew.summary(task)) == 8
        self.delete_task(task)

    def test_time_today(self):
        task = 'foo'

        self.delete_task(task)
        time_today, running = timew.time_today(task)
        assert time_today is None
        assert not running
        run(['timew', 'start', task])
        time_today, running = timew.time_today(task)
        assert time_today is not None
        assert running
        run(['timew', 'stop'])
        time_today, running = timew.time_today(task)
        assert time_today is not None
        assert not running
        sleep(1)
        run(['timew', 'continue'])
        time_today, running = timew.time_today(task)
        assert time_today is not None
        assert running
        self.delete_task(task)

    def test_call(self):
        task = 'foo'

        self.delete_task(task)
        assert len(timew(None, task=task)) == 0
        run(['timew', 'start', task])
        segments = timew(None, task=task, limit='8:00:00')
        print(segments)
        assert len(segments) == 1
        segment = segments[0]
        assert 'contents' in segment
        assert 'highlight_groups' in segment
        assert len(segment['highlight_groups']) == 2
        assert segment['highlight_groups'][0] == 'timew_running'
        assert segment['highlight_groups'][1] == 'timew'

        segments = timew(None, task=task, limit='0:00:00')
        print(segments)
        assert len(segments) == 1
        segment = segments[0]
        assert 'contents' in segment
        assert 'highlight_groups' in segment
        assert len(segment['highlight_groups']) == 2
        assert segment['highlight_groups'][0] == 'timew_expired'
        assert segment['highlight_groups'][1] == 'timew'

        run(['timew', 'stop'])
        segments = timew(None, task=task, limit='8:00:00')
        print(segments)
        assert len(segments) == 1
        segment = segments[0]
        assert 'contents' in segment
        assert 'highlight_groups' in segment
        assert len(segment['highlight_groups']) == 2
        assert segment['highlight_groups'][0] == 'timew_paused'
        assert segment['highlight_groups'][1] == 'timew'
        self.delete_task(task)
