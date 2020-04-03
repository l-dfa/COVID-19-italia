:markup:   restructuredtext
:language: en
:title:    Time trend of Coronavirus Covid-19 in Italy
:created:  2020-03-07 20:17:53
:modified: $MODIFIED
:slug:     coronavirus_covid_19_italy
:category: science
:summary:  Questo articolo vuole riportare l'andamento temporale dei dati del Ministero della Sanità
           diffusi dalla Protezione Civile, relativi all'epidemia di COVID-19
           che ha colpito l'Italia dal febbraio 2020. ...
:image:    corona_virus-480.jpg
:image_in_content: no
:authors:  Luciano De Falco Alfano
:translation_of: Andamento temporale del Coronavirus Covid-19 in Italia
:published: yes
:evidence: yes

.. hic sunt leones


Time trend of Coronavirus Covid-19 in Italy
============================================

*Data updated at ${UPDATED}*.

This article reports the temporal trend of the data of the Italian Ministry of Health
released by the Civil Protection,
related to the COVID-19 epidemic that has hit Italy since February 2020.

Graphical analysis
-------------------

Below is the graph of the historical series of *cumulative* data relating to the epidemic.
In the graph I show:

* the numbers of infected cases (positive);
* those, unfortunately, deceased;
* and finally the healed.

.. image:: /media/images/204/dpc-covid19-ita-andamento-nazionale.en.png
   :height: 700 px
   :width:  900 px
   :scale: 75 %
   :align: center
   :alt:   COVID-19, Italy
   :name:  COVID-19, Italy

|

.. csv-table:: national status - last day

$DATA_TABLE_LAST
  
| 
| 

Instead, the following graph shows the time trend od *total cases* for
the six most hitted regions.

.. image:: /media/images/204/dpc-covid19-ita-regioni.most_hitted.en.png
   :height: 700 px
   :width:  900 px
   :scale: 75 %
   :align: center
   :alt:   COVID-19, Italia, regions, temporal trend
   :name:  COVID-19, Italia, regions, temporal trend

| 
| 

To have a general idea about the geographical distribution of the virus,
the following historam shows the total cases for every region.

.. image:: /media/images/204/dpc-covid19-ita-regioni.en.png
   :height: 700 px
   :width:  900 px
   :scale: 75 %
   :align: center
   :alt:   COVID-19, Italy, regions
   :name:  COVID-19, Italy, regions

|

Hereafter the figures about the twenty regions on the last day.

.. csv-table:: regions status - last day

$RDATA_TABLE_LAST
  
|
|

Finally, below I report the temporal trend of *new daily cases* regarding the
overall country.

.. image:: /media/images/204/dpc-covid19-ita-andamento-nazionale.nuovi_positivi.en.png
   :height: 700 px
   :width:  900 px
   :scale: 75 %
   :align: center
   :alt:   COVID-19, Italia, regioni, andamento temporale nuovi casi giornalieri
   :name:  COVID-19, Italia, regioni, andamento temporale nuovi casi giornalieri

This chart is the one checked by ISS experts to understand the trend
infection. And based on this they tell us that we have passed the *peak*
of the contagions. What does this statement mean? The daily number of new ones
contagion is the *speed* of spread of the infection. For infections
it is observed that the diffusion speed has a trend that recalls that presented
from this graph, taken from `this wikipedia article <https://en.wikipedia.org/wiki/Pandemic>`_:

.. image::  https://upload.wikimedia.org/wikipedia/commons/9/90/Community_mitigation_%28cropped%29.jpg
   :height: 451 px
   :width:  800 px
   :align: center
   :alt:   pandemic
   :name:  pandemic
   
Having exceeded the peak means having overtaken the maximum of the graph, and
proceed towards ever lower diffusion rates.

Unfortunately, the actual course of an infection is quite different from that
of a theoretical curve, and it is influenced by many factors. First among all
the possibility of contrasting the diffusion. In the previous graph we see the theoretical effect
of containment, which allows to postpone the peak and to lower it:
the aim is not to decrease the number of affected people [#]_, but to dilute the time
expansion to prevent healthcare facilities from going into crisis.

Some remarks
---------------------

*[March 30, 2020]*: **maybe** finally we can hope. Looking at the chart below,
we note that the variation of the positives (the bottom rectangle) is decreasing
for 9 days, except for a sudden single increase on March 25th. Statistically,
we can hope that the lockdown is finally producing effects
to contain the outbreak.

*[March 30, 2020 - end]*



*[March 18th 2020]* About *the national trend*, I feel the
need to remark the following fact. Various sources of information are
using the **general total of daily data** of the Ministry of Health
to account for the change in the epidemic.

This number indicates the **total** number of people
affected by the virus, adding three different groups: sick,
healed and deceased. This quantity give us an idea of ​​the overall impact of
phenomenon. It can only increase. And when all this ends, it will take on a fixed 
value: constant, equal to the maximum value reached. The slope of this curve
(i.e. its daily variation, used by many news media) tells us if
the speed with which the virus impacts the country as a whole decreases. But 
it is not the right indicator to measure the virulence of the infection.

The data relating to each of the aforementioned groups are precious. The analysis of each of these classes
tells us something
about how we are dealing with the epidemic. For example, observe how it varies
the number of people healed per day, after a few weeks, can tell us
how the therapies adopted are effective.

But the total of these three quantities is much more articulated, and if the analysis is not
pointig in the right direction, it gives us misleading indications.
Remember the concept of adding apples with pears,
who taught us in elementary school? It is just that.

To understand the progress of the infection, it is necessary to analyze the size of the
group formed by infected people, and only these. The healed and the deceased
are no longer infected. Both of these cases are *defeats* for the virus, which is not
more able to propagate using them as vectors.

The size of the group of infected people is the red line
in the upper box of the national trend. To observe the variation of the
slope of this curve is particularly important: it tells us the **speed**
of spreading the virus.

Even just the total number of infected people (note: not the total
of people affected: infected + healed + deceased) is complex to analyze.
Consider the fact that every day the other two classes (heale and deceased)
contribute to this measure: they subtract to the number of
infected. While the number of new positives adds up. The slope of the total
of infected people is the result of these three quantities, antagonistic to each other.

I find misleading the term *new_currently_positive* that Civil Protection 
uses in its data tables. In my data analysis I call this column
*change of positives* because it is the difference between the total of the positives of the day
and the total of the positives from the previous day.

The number of people joining the positive group for the first time,
also known as the *new currently positive*, can be calculated by adding to the
*changes of positives* the number of people who left the group: the people healed during the course
of the day and the deceased during the day. If you do this
operation, in this period there is a notable increase in new positives
compliance with the provisions of the Civil Protection.

*[March 18th 2020 - end]*

Measures of the Italian Government
------------------------------------

* 22/03 ban on moving between municipalities; closure of not essential 
  production activities;
* 21/03 closing of public parks and prohibition of outdoor activities;
* 16/03 economic measures to support working families and businesses;
* 14/03 agreement between trade unions and trade associations for
  workplace safety protocol;
* 11/03 supplement to the economic report for a further appeal
  indebtedness; closure of retail businesses
  except food, basic necessities, pharmacies;
* 09/03 extension to the national territory of the provision of
  08/03; prohibition of sporting events and gatherings;
* 08/03 for the Lombardy Region and 14 other Provinces, limitation on travel
  of natural persons entering and leaving the territory and their own
  housing;
* 04/03 - closure of educational activities throughout the national territory
* 25/02 prohibition of sporting events
* 23/02 Quarantine for the Municipalities of Codogno (Lombardy Region) and neighboring
  and for the municipality of Vò (Veneto Region);

Used data
-----------------

The details of data used to generate the graph about the national trend are shown below
(copy of `this font <https://github.com/pcm-dpc/COVID-19/tree/master/dati-andamento-nazionale>`_ of Italian Civil Protection):

.. csv-table:: national trend

$DATA_TABLE

Notes about data regard the national trend:

* 29/03 - partial data from Emilia Romagna  (swabs not updated)
* 26/03 - partial data from Piemonte  -50 deaths (late comunication)
* 18/03 - data from Campania not updated
* 18/03 - data from Parma  not updated
* 17/03 - data from Rimini not updated
* 16/03 - no data from P.A. Trento and Puglia
* 11/03 - no data from Abruzzo
* March 10 2020 - partial data from Lombardia
* March 11 2020 - not received data from Abruzzo

Instead for the trend of positive cases in the regions in the last four days
we used the following data (extracted from this `data source  <https://github.com/pcm-dpc/COVID-19/tree/master/dati-regioni>`_ of Italian Civil Protection)

.. csv-table:: regional trend, last seven days every region

$RDATA_TABLE

References
-------------

All data here used are from `Ministero della Salute <http://www.salute.gov.it/portale/home.html>`_,  
by `Protezione Civile <http://www.protezionecivile.gov.it/>`_:
a Department of `Italian Government <http://www.governo.it/en>`_

Until 6th of March 2020, the Protezione Civile published data daily via two
pdf file. One reported the national situation as a whole,
and the other indicated the cases for each individual province.

Since the 7th of March, the data have been published through `a web page <http://opendatadpc.maps.arcgis.com/apps/opsdashboard/index.html#/b0c68bce2cce478eaac82fe38d4138b1>`_,
which graphically reports the situation.

Moreover, since the same date, Civil Protection spreads data about outbreak by Github, in Italian, at the links:

* national trend: `andamento nazionale <https://github.com/pcm-dpc/COVID-19/tree/master/dati-andamento-nazionale>`_;
* regional trend: `andamento nelle regioni <https://github.com/pcm-dpc/COVID-19/tree/master/dati-regioni>`_;
* provincial trend: `andamento nelle province <https://github.com/pcm-dpc/COVID-19/tree/master/dati-province>`_.

--------------

.. [#] The number of infected people is represented by the area between the curve of the graph and
   his abscissa.