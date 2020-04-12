:markup:   restructuredtext
:language: en
:title:    Time trend of Coronavirus Covid-19 outbreak in the world
:created:  2020-03-06 17:58:47
:modified: $MODIFIED
:slug:     coronavirus_covid_19_world
:category: science
:summary:  Questo articolo riporta l'andamento temporale dell'epidemia COVID-19 nel mondo
           secondo i dati diffusi dal 
           European Centre for Disease Prevention and Control (ECDC) ...
:image:    corona_virus-480.jpg
:image_in_content: no
:authors:  Luciano De Falco Alfano
:translation_of: Andamento temporale del Coronavirus Covid-19 nel mondo
:published: yes
:evidence:  yes

.. hic sunt leones


Time trend of Coronavirus Covid-19 outbreak in the world
==========================================================

*Data updated at ${UPDATED}*.

This article reports the temporal trend of the COVID-19 outbreak in the world
according to data released by the `European Center for Disease Prevention and Control <https://www.ecdc.europa.eu/en>`_.

The *European Center for Disease Prevention and Control* (ECDC) agency
publishes daily the data of the diffusion of the
`COVID-19 in the world <https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide>`_.

**Note**. I have not checked the ECDC data for the other countries, but about Italy
it reports data of the `Italian Civil Protection <https://github.com/pcm-dpc/COVID-19/tree/master/dati-amento-nazionale>`_,
with a delay of 24 hours.

Grafic analysis
-----------------

Below I report the graphics of the historical series of **cumulative** data
obtained by processing data published by ECDC.

Note that these are overall data, as ECDC does not publish the number of
healed, but, for every single day, only the number of new cases and deaths.

Consequently, adding the number of new cases day by day, it is possible
to get only the **total** number of people affected by the virus.

From the ECDC data, I aggregate them about European Union Countries, 
then I calculate the 10 countries that have the bigger number of
affected people. Below I indicate the time series
of the daily totals for these ten countries, as of January 14, 2020.

.. image:: /media/images/210/covid19-worldwide-${UPDATED}_1-10.png
   :height: 700 px
   :width:  900 px
   :scale: 85 %
   :align: center
   :alt:   COVID-19, World
   :name:  COVID-19, World
  
| 
| 
  
Instead, the following graph shows the trend of the overall cases,
starting from February 20, 2020, eliminating the data of the two most affected countries. Thereby
it is possible to better observe the trend in the latter period for the countries from the third to the tenth
placed among those most affected by the virus.

.. image:: /media/images/210/covid19-worldwide-${UPDATED}_3-10.png
   :height: 700 px
   :width:  900 px
   :scale: 85 %
   :align: center
   :alt:   COVID-19, World, without the most hitted country
   :name:  COVID-19, World, without the most hitted country

|
|

Finally, below, the situation for the 10 most affected countries member of the European Union.
Again starting from 20 February 2020.

.. image:: /media/images/210/covid19-worldwide-${UPDATED}_eu_1-10.png
   :height: 700 px
   :width:  900 px
   :scale: 85 %
   :align: center
   :alt:   COVID-19, Unione Europea
   :name:  COVID-19, Unione Europea


The data from which the graphs are derived can be consulted
at `this address </media/data/210/covid19-worldwide-${UPDATED}.csv>`_

Summary of situation on $UPDATED
------------------------------------------------------------------------

Hereafter a summary of the situation about the twenty most hitted countries
at the uate date of this article. Columns report:

* *date*, the date of the day;
* *cases*, the total number of cases on the indicated date: positive + healed + deceased;
* *death*, the total of the deceased on the indicated date;
* *death/cases*, the ratio between deaths and total cases;
* *cases/population*, the ratio between the total number of cases and the population;
* *death/population*, the ratio between the number of deaths and the population;
* *country*, the name of the country.

In the first table, European Union Countries are bundled.

.. csv-table:: situation of twenty most hitted countries on $UPDATED, EU Countries bundled

$DATA_TABLE

|
|

Instead, hereafter the European Union Countries are unbundled.

.. csv-table:: situation of twenty most hitted countries on $UPDATED, EU Countries unbundled

$DATA_TABLE_EU


Remarks
---------------------

The most recent remarks precede those temporally more dated.

*[March 31, 2020]* The speed with the US total case curve 
has soared is astounding. It seems the neglect with which
the US (not) faced the problem has brooded the epidemic
without detecting its presence for a long period
of time. Unfortunately, now there are consequences. 
Fortunately, at least for now, with a low percentage of deaths.

The total number of cases in France has exceeded that of IRAN. The latter
it is seeing a certain increase in infections, although not at the rate of the main ones
European countries: Italy, Spain, Germany, and France.

Unfortunately, all deaths/cases ratios are worsening. Italy
has exceeded 11%, Spagna is over 8%. IRAN and France also exceeded 6%.
Only Germany has a percentage lower than 1%: I hope they
manage to keep it constant.

*[March 31, 2020 - end]*

*[March 26, 2020]* I added a table with summarizing data 
at the update date. This table has a column showing the ratio between
deaths and total number of positive cases.

The numbers in this column are conflicting. We have a mortality of
9.8% in Italy, 4% in China and 1.4% in USA. Without
mentioning 0.3% of Australia or Germany or Norway.

These gaps are excessive for
health systems that are qualitatively comparable. Even if you want
to account for Italy an excess of the population in old age.
I am convinced that here we have different data census criteria. Both for
define the positivity to the disease, which for the cause of death.

And I am convinced that the first thing to do is to impose a standard
of behavior among all nations. Otherwise monitoring does not make sense:
what has been done in a country cannot be analyzed and compared with what
made in another country. For example, I insist, look at the curve of
total cases of Iran; which for me is a big question mark. 

*[March 26, 2020 - end]*
 
*[March 20, 2020]* As of the writing date of this article we observe:

* as indicated by the constant trend of the China curve,
  this country is in a post-epidemic management phase; the new ones
  cases are very small, and largely, or totally, due
  to contagions of people from abroad;
* in Italy the infection is still in full development,
  as shown by the accentuated slope of the relative curve;
* just as Spain and as USA are in full diffusion;
  these even seem to have epidemic expansion rates
  higher than Italy;
* Korea is a surprise, because it has managed to contain quickly
  the expansion of the virus; from this country we would have to learn;
  it would not be bad to ask them for advice;
* Iran is strange; its curve, after the first trend polynomial (as usual),
  has now flattened similarly to a straight line; sign
  that the ongoing activities to fight outbreak are quite effective
  even if they can't completely block the virus from spreading;
  this too would be a case from which to learn something.

*[March 20, 2020 - end]*

 
And some considerations
---------------------------

This pandemic has made it clear more than ever that "*the whole world
is a village*". This old proverb wants to highlight as certain
behaviors are observable in all people. But now it
can mean literally: travel for pleasure or work weave
a spider web that envelops all humanity in the world.

In my opinion it is no coincidence that in Italy the diffusion took place
in the most industrially active regions: Lombardy, Emilia Romagna and Veneto.
They are the regions that have had the most contacts with industries in China, where
the first diffusion took place.

**Warning**, I'm not saying it's fault
of China, or that one should not trade with it. I am convinced that one
new epidemic could have developed in any other country
in the world. And if this country had been industrially active
(examples: Germany, France, USA, Brazil, UK, Italy, ...) then would be happened
exactly what we are experiencing now: from the country in question
(nation zero :-) would have spread to an industrial partner
(nation one ...) and then from here spread to the rest of the world.

So what must we do? Must we stop the trips, and bring the world back to a
Middle Ages made of feuds whose borders could be crossed
only for very serious reasons? (do we remember the film *We have just to cry*
of Benigni and Troisi? The tax collector
who asked: "Who are you? What are you wearing? How many are you? A florin!").

Whatever Trump says, I don't think that's a good idea. Also because 
at that time famine and disease were reaping victims, and I am
convinced that it was precisely because of the misery of physical resources and knowledge
imposed by this fragmentation which prevented mutual help and knowledge.

In a communication course that I attended some time ago, the teacher
start her teaching saying, "When you talk to someone, remind yourself:
his (or her) difference is your wealth."

This concept is central. Through the differences between people we discover
new ways of looking at things. And every time we discover something, the horizons
widen, improving ourselves and those around us. Expanding ours
ability and those of our neighbor.

So I think: travel is welcome, as an increasingly connected world,
and trade with everyone. But ... **we need to be ready**!

In 2015 a person, such Bill Gates, in one of his
`exposure to TED <https://www.youtube.com/watch?v=6Af6b_wyiwI>`_ said to be
convinced that the greatest risk to humanity is the possibility of a pandemic.
On that occasion Bill Gates proposed to organize the world with a model
health care which can react quickly around the world to counter
effectively an epidemic. And he concluded his speech saying "if we start
(to prepare) now, we can be ready for the next epidemic".

We didn't prepare. And now we pay the consequences, in economic terms
and, above all, of lost of lives.

From all this, will we be able to learn?

To finish: how do we get out? More than ever with a common effort. It is necessary
pool the resources of the different countries to bring them together where they are needed
more. I hear of people getting upset because they think that tampons
product in Italy were supplied to the USA. But, in turn, we Italians, 
did not scruple to buy sanitary ventilation systems
from Germany. An so? I insist, it is not by closing ourselves in our shield that
we will come out without harm. Well do the European Union if really it is going to organize
a reserve of sanitary materials to be used in countries with greater needs.
