:markup:   restructuredtext
:language: it
:title:    Andamento temporale del Coronavirus Covid-19 in Italia
:created:  2020-03-07 20:17:53
:modified: $MODIFIED
:slug:     coronavirus_covid_19_italia
:category: science
:summary:  Questo articolo riporta l'andamento temporale dei dati del Ministero della Sanità
           diffusi dalla Protezione Civile, relativi all'epidemia di COVID-19
           che ha colpito l'Italia dal febbraio 2020. ...
:image:    corona_virus-480.jpg
:image_in_content: no
:authors:  Luciano De Falco Alfano
:published: yes
:evidence: yes

.. hic sunt leones


Andamento temporale del Coronavirus Covid-19 in Italia
========================================================

*Dati aggiornati al ${UPDATED}*.

Questo articolo riporta l'andamento temporale dei dati del Ministero della Sanità
diffusi dalla Protezione Civile 
relativi all'epidemia di COVID-19 che ha colpito l'Italia dal febbraio 2020.

Analisi grafica
-----------------

Qui di seguito graficamente la serie storica dei dati *cumulativi* relativi all'epidemia.
Nel grafico indico:

* i numeri dei casi contagiati (positivi);
* quelli, purtroppo, deceduti;
* ed infine i guariti.

.. image:: /media/images/204/dpc-covid19-ita-andamento-nazionale.png
   :height: 700 px
   :width:  900 px
   :scale: 75 %
   :align: center
   :alt:   COVID-19, Italia
   :name:  COVID-19, Italia

|

.. csv-table:: situazione nazionale - ultimo giorno

$DATA_TABLE_LAST
  
| 
| 

Invece, il seguente grafico mostra l'andamento temporale dei *casi totali*
per le sei regioni più colpite.

.. image:: /media/images/204/dpc-covid19-ita-regioni.most_hitted.png
   :height: 700 px
   :width:  900 px
   :scale: 75 %
   :align: center
   :alt:   COVID-19, Italia, regioni, andamento temporale
   :name:  COVID-19, Italia, regioni, andamento temporale

| 
| 

Se si desidera avere un'idea generale della diffusione del virus nelle diverse regioni,
il seguente istogramma mostra i casi totali per regione.

.. image:: /media/images/204/dpc-covid19-ita-regioni.png
   :height: 700 px
   :width:  900 px
   :scale: 75 %
   :align: center
   :alt:   COVID-19, Italia, regioni
   :name:  COVID-19, Italia, regioni

|

Qui di seguito la situazione numerica dell'ultimo giorno per le venti regioni:

.. csv-table:: situazione delle regioni - ultimo giorno

$RDATA_TABLE_LAST
  

|
|

Infine, qui di seguito riporto l'andamento temporale dei *nuovi casi giornalieri*
a livello nazionale

.. image:: /media/images/204/dpc-covid19-ita-andamento-nazionale.nuovi_positivi.png
   :height: 700 px
   :width:  900 px
   :scale: 75 %
   :align: center
   :alt:   COVID-19, Italia, regioni, andamento temporale nuovi casi giornalieri
   :name:  COVID-19, Italia, regioni, andamento temporale nuovi casi giornalieri

Questo grafico è quello controllato dagli esperti dell'ISS per capire l'andamento
dell'infezione. Ed in base a questo che ci dicono che abbiamo superato il *picco*
dei contagi. Che vuol dire questa affermazione? Il numero giornaliero di nuovi
contagi è la *velocità* di diffusione dell'infezione. Per le infezioni
si osserva che la velocità di diffusione ha un andamento che ricorda quello  presentato
da questo grafico, ripreso da `questo articolo di wikipedia <https://en.wikipedia.org/wiki/Pandemic>`_:

.. image::  https://upload.wikimedia.org/wikipedia/commons/9/90/Community_mitigation_%28cropped%29.jpg
   :height: 451 px
   :width:  800 px
   :align: center
   :alt:   pandemic
   :name:  pandemic
   
Avere superato il picco, significa avere scavalcato il massimo del grafico, e
procedere verso velocità di diffusione sempre inferiori.

Purtroppo l'andamento reale di una infezione è piuttosto diverso da quello 
di una curva teorica, ed è influenzato da molti fattori. Primo fra tutti
la possibilità di contrastare la diffusione. Nel grafico precedente si vede l'effetto
teorico del contenimento, che permette di posporre il picco e di abbassarlo:
lo scopo non è diminuire il numero di persone colpite [#]_, ma diluire i tempi
di espansione per evitare che le strutture sanitarie vadano in crisi.



Osservazioni
---------------------

Le osservazioni più recenti precedono quelle temporalmente più datate.

*[30 Marzo 2020]*: **forse** finalmente si può sperare. Osservando il grafico 
dell'andamento nazionale, 
si nota che la variazione dei positivi (il rettangolo in basso) è in diminuzione 
da 9 giorni, salvo un repentino singolo aumento il 25 Marzo. Statisticamente,
possiamo sperare che finalmente il lockdown stia producendo gli effetti
di contenimento dell'infezione che tutti ci auguriamo. 

*[30 Marzo 2020 - fine]*

*[18 Marzo 2020]* Riguardo *l'andamento nazionale*, sento la 
necessità di rimarcare il seguente fatto. Varie fonti d'informazione stanno
utilizzando il **totale generale dei dati giornalieri** del Ministero della Sanità
per rendere conto della variazione dell'epidemia.

Questo dato ci indica il numero **complessivo** di persone
colpite dal virus, sommando tre diverse grandezza: malati,
guariti e deceduti. Questo numero ci dà un'idea dell'impatto complessivo del
fenomeno. Può solo aumentare. E, quando tutto ciò finirà, assumerà un valore 
fisso: costante, pari al massimo valore raggiunto. La pendenza di questa curva
(ovvero la sua variazione giornaliera, utilizzata da molti media) ci dice se
diminuice la velocità con cui il virus impatta complessivamente il paese. Ma non
è l'indicatore giusto per misurare la virulenza dell'infezione.

Premetto: i dati relativi ad ognuno dei gruppi predetti sono preziosi.
L'analisi di ognuna di queste classi ci dice qualcosa
riguardo il modo in cui stiamo affrontano l'epidemia. Ad esempio, osservare come varia
il numero di guariti al giorno, a distanza di alcune settimane,ci può dire 
quanto sono efficaci le terapie adottate.

Ma il totale di queste tre grandezze è molto più articolato, e se l'analisi non
punta nella giusta direzione ci dà indicazioni fuorvianti.
Ricordate il concetto di sommare le mele con le pere,
che ci hanno insegnato alle elementari? Si tratta proprio di questo.

Per capire l'andamento dell'infezione, è necessario analizzare la dimensione del 
gruppo formato dalle persone infette, e solo queste. I guariti e i deceduti 
non sono più infetti. Entrambi questi casi sono *sconfitte* per il virus, che non
è più in grado i propagarsi utilizzandoli come vettori.

La dimensione del gruppo di persone infette è la linea rossa
nel riquadro superiore dell'andamento nazionale. Osservare la variazione della
pendenza di questa curva è particolarmente importante: ci dice la **velocità**
di diffusione del virus.

Anche il solo totale di persone infette (nota: non il totale
delle persone colpite: infetti+guariti+deceduti) è complesso da analizzare.
Consideriamo il fatto che ogni giorno a questa misura contribuiscono
le altre due classi: i guariti e i deceduti, che si sottraggono al numero di 
infetti. Mentre il numero di nuovi positivi si somma. La pendenza del totale
di persone infette è il risultato di queste tre grandezze, antagoniste tra loro.

Trovo fuorviante la dizione *nuovi_attualmente_positivi* che la Protezione Civile 
utilizza nelle sue tabelle dati. Nella mia analisi dei dati questa colonna si chiama
*variazione positivi* perché è la differenza tra il totale dei positivi del giorno
e il totale dei positivi del giorno precedente.

Il numero delle persone che entrano nel gruppo dei positivi per la prima volta,
ovvero i *nuovi attualmente positivi*, si può calcolare sommando alla
*variazione positivi* il numero di persone uscite dal gruppo: i guariti nel corso
della giornata e i deceduti nel corso della giornata. Se si effettua questa
operazione, in questo periodo si osserva un notevole aumento di nuovi positivi 
rispetto quanto indicato dalla Protezione Civile.

*[18 Marzo 2020 - fine]*


Provvedimenti del Governo Italiano
------------------------------------

* 22/03 divieto di spostamento tra comuni; chiusura delle attività produttive 
  non essenziali;
* 21/03 chiusura dei parchi pubblici e proibizione delle attività all'aperto;
* 16/03 misure economiche a sostegno di famiglie lavoratori e imprese;
* 14/03 accordo tra sindacati e associazioni di categoria per il 
  protocollo di sicurezza nei luoghi di lavoro;
* 11/03 integrazione alla relazione economica per un ulteriore ricorso
  all'indebitamento; chiusura delle attività commerciali al dettaglio 
  salvo alimentari, prima necessità, farmacie;
* 09/03 estensione al territorio nazionale del provvedimento del
  08/03; divieto di manifestazioni sportive e di assembramento;
* 08/03 per la Regione Lombardia e altre 14 Province limitazione agli spostamenti
  delle persone fisiche in ingresso e uscita dal territorio e dalle proprie 
  abitazioni;
* 04/03 - chiusura delle attività didattiche in tutto il territorio nazionale
* 25/02 divieto delle manifestazioni sportive
* 23/02 Quarantena per i Comuni di Codogno (Regione Lombardia) e limitrofi
  e per il comune di Vò (Regione Veneto);

Dati utilizzati
-----------------

Di seguito il dettaglio dei dati utilizzati per la generazione del grafico 
dell'andamento nazionale, estrapolato da questa
`sorgente dati <https://github.com/pcm-dpc/COVID-19/tree/master/dati-andamento-nazionale>`_
della Protezione Civile:

.. csv-table:: andamento nazionale

$DATA_TABLE

| 
| 

Note riguardo i dati dell'andamento nazionale (data nel formato: gg/mm del 2020):


* 29/03 - Dati  Emilia Romagna parziali (tamponi non aggiornati)
* 26/03 - Dati Piemonte parziali -50 deceduti (comunicazione tardiva)
* 18/03 - Dati Campania non aggiornati
* 18/03 - Dati Parma non aggiornati
* 17/03 - Dati Rimini non aggiornati
* 16/03 - Dati P.A. Trento e Puglia non pervenuti
* 11/03 - Dati Abruzzo non pervenuti
* 10/03 - Dati Lombardia parziali
* 07/03 - Dati Brescia +300 esiti positivi


Invece per l'andamento dei casi positivi nelle regioni negli ultimi quattro giorni
si sono utilizzati i seguenti dati (estratti da questa `ulteriore sorgente dati  <https://github.com/pcm-dpc/COVID-19/tree/master/dati-regioni>`_ della Protezione Civile)

.. csv-table:: andamento regionale

$RDATA_TABLE

Riferimenti
----------------

Tutti i dati utilizzati sono ottenuti dal `Ministero della Salute <http://www.salute.gov.it/portale/home.html>`_,  
tramite la `Protezione Civile <http://www.protezionecivile.gov.it/>`_:
un Dipartimento del `Consiglio dei Ministri <http://www.governo.it/>`_

Sino al 06 Marzo 2020 la Protezione Civile diffondeva i dati giornalmente tramite due
file in formato pdf. Uno riportava la situazione nazionale nel suo complesso,
l'altro indicava i casi per ogni singola provincia.

Dal 7 Marzo i dati sono diffusi tramite `una pagina web <http://opendatadpc.maps.arcgis.com/apps/opsdashboard/index.html#/b0c68bce2cce478eaac82fe38d4138b1>`_,
che riporta graficamente la situazione.

Inoltre, dalla stessa data, la Protezione Civile diffonde i dati dell'epidemia tramite Github agli indirizzi:

* `andamento nazionale <https://github.com/pcm-dpc/COVID-19/tree/master/dati-andamento-nazionale>`_;
* `andamento nelle regioni <https://github.com/pcm-dpc/COVID-19/tree/master/dati-regioni>`_;
* `andamento nelle province <https://github.com/pcm-dpc/COVID-19/tree/master/dati-province>`_.

---------------

.. [#] Il numero di persone infette è rappresentetato dall'area tra la curva del grafico e 
   la sua ascissa. 
