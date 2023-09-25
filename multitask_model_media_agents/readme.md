# Media Multitasking

## Summary

[Media Multitasking](https://www.sciencedirect.com/topics/psychology/media-multitasking), which can either occur when two types of media are being used simultaneously or when a type of screen media is being used while doing another task (i.e., completing homework and eating dinner), can pose many difficulties to children’s everyday lives (Wallis, 2010). 

In this research, we are planning to figure out the mechanism which lies under the normal facts.

One thing need to be addressed is that this model is built on: agent-media, environment-people.
## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press ``run``.

## Files

* ``multitask_model/cell.py``: Defines the behavior of an individual cell, which can be in two states: DEAD or ALIVE.
* ``multitask_model/model.py``: Defines the model itself, initialized with a random configuration of alive and dead cells.
* ``multitask_model/portrayal.py``: Describes for the front end how to render a cell.
* ``multitask_model/server.py``: Defines an interactive visualization.
* ``run.py``: Launches the visualization

## Optional

*  ``multitask_model/app.py``: can be used to run the simulation via the streamlit interface.
* For this some additional packages like ``streamlit`` and ``altair`` needs to be installed.
* Once installed, the app can be opened in the browser using : ``streamlit run app.py``


## Further Reading
TBC.
