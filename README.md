# System Process Visualization using arbor.js

### Just a basic Tree graph showing system processes and their owners

### Technologies used:

* SQLAlchemy

* arbor.js

* Tornado

* CoffeeScript

### To run the visualization:

`python server.py`

Will start an instance of the Tornado HTTP server on 127.0.0.1:8080

The process graph is merged every 5 seconds. If you kill or start a process it will disappear or show up on the graph.

The graph is very slow if you have a lot of processes.
