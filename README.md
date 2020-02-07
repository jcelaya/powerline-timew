# Powerline segment for timew

Powerline segment to show time spent today in a particular task.

## Setup

Add the following segment to your shell prompt / tmux bar / powerline-enabled app:

    {
        "function": "powerline_timew.timew",
        "args": {
            "task": "work"
        }
    }

And a highlight group called `timew` to `powerline/colorschemes/defaut.conf`, e.g.:

    {
        "groups": {
            "timew": { "fg": "white", "bg": "gray3", "attrs": ["bold"] }
        }
    }
