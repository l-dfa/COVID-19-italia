
COVID-19-italia
================

This is an exercise to grab semi-automatically a bunch of data from the 
Internet, and use them to update a couple of articles the author wrote about
the Covid-19 outbreak in Italy and in the world.

It's developed using Python_ language and some libraries: Pandas_, Matplotlib_,
reStructuredtext_.

You can find a more exaustive explanation how all this stuff works `at this 
URL <https://luciano.defalcoalfano.it/blog/show/how_i_update_articles_about_coronavirus>`_.

Installation
------------------

To install [#]_:

* make an hosting directory, example: ``mkdir .\covid19-italia``
* make some auxiliary directories::

  cd .\covid19-italia
  mkdir data
  mkdir images
  mkdir world
  mkdir backup

* clone or download this project to the hosting directory
* create a python virtualenv environment: ``python - m venv venv``
* activate the environment: ``venv\Scripts\activate``
* rename utils_example.conf: ``ren utils_example.conf utils.conf`` 
* modify utils.conf contents as you wish;
* study the project listings;
* try it::

  python world.py
  python italy.py

License
------------

This work is distributed under a 
`CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/>`_
license.




------------------------------

.. _Python: http://www.python.org/
.. _Pandas: https://pandas.pydata.org/
.. _Matplotlib: https://matplotlib.org/

.. [#] These are for MS Windows. In Linux, please use the equivalent commands.