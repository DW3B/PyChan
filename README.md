PyChan
======

A simple read-only API wrapper for 4chan. 

Example Usage:

```python
import pychan

chan = pychan.PyChan()
board = chan.select_board('wg')

for thread in board.get_threads():
    thread.get_posts()
```


