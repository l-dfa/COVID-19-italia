:markup:   restructuredtext
:language: it
:title:    Andamento temporale del Coronavirus Covid-19 nel mondo
:created:  2020-03-06 17:58:47
:modified: $MODIFIED
:slug:     coronavirus_covid_19_mondo
:category: science
:summary:  Questo articolo riporta l'andamento temporale dell'epidemia COVID-19 nel mondo
           secondo i dati diffusi dal 
           European Centre for Disease Prevention and Control (ECDC) ...
:image:    corona_virus-480.jpg
:image_in_content: no
:authors:  Luciano De Falco Alfano
:published: yes
:evidence:  yes

.. hic sunt leones


Andamento temporale del Coronavirus Covid-19 nel mondo
========================================================

*Dati aggiornati al ${UPDATED}*.

Questo articolo riporta l'andamento temporale dell'epidemia COVID-19 nel mondo
secondo i dati diffusi dal `European Centre for Disease Prevention and Control <https://www.ecdc.europa.eu/en>`_.

L'agenzia *European Centre for Disease Prevention and Control* (ECDC)
pubblica giornalmente i dati della diffusione del 
`COVID-19 nel mondo <https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide>`_.

**Nota**. Non ho controllato per gli altri paesi, ma per l'Italia i dati della ECDC
riportano quelli della `Protezione Civile italiana <https://github.com/pcm-dpc/COVID-19/tree/master/dati-andamento-nazionale>`_,
con un ritardo di 24 ore.

Analisi grafica
-----------------

Qui di seguito riporto la grafica della serie storica dei dati **cumulativi** 
elaborati dalla pubblicazione della ECDC.

Si noti che questi sono dati complessivi, in quanto ECDC non pubblica il numero di 
guariti, ma, per ogni singolo giorno,  solo il numero di nuovi casi e i decessi.

Di conseguenza, sommando giorno per giorno il numero di nuovi casi, è possibile
ottenere solo il numero **complessivo** di persone colpite dal virus.

Dai dati di ECDC aggrego i numeri dei paesi che formano l'Unione Europea, 
dopo di che calcolo i 10 paesi che hanno il più altro numero di 
persone colpite. Qui di seguito indico l'andamento temporale 
dei totali giornalieri per questi dieci paesi, a partire dal 14 gennaio 2020.


.. image:: /media/images/210/covid19-worldwide-${UPDATED}_1-10.png
   :height: 700 px
   :width:  900 px
   :scale: 85 %
   :align: center
   :alt:   COVID-19, Mondo
   :name:  COVID-19, Mondo
  
| 
| 
  
Invece, il seguente grafico mostra l'andamento dei casi complessivi,
partendo dal 20 Febbraio 2020, eliminando i dati dei due paesi più colpiti. In tal modo
è possibile osservare meglio l'andamento in quest'ultimo periodo per i paesi dal terzo al decimo
posto tra quelli più colpiti dal virus.

.. image:: /media/images/210/covid19-worldwide-${UPDATED}_3-10.png
   :height: 700 px
   :width:  900 px
   :scale: 85 %
   :align: center
   :alt:   COVID-19, Mondo, senza le due nazioni più colpite
   :name:  COVID-19, Mondo, senza le due nazioni più colpite

| 
| 
  
Infine, qui di seguito, la situazione per i 10 paesi membri dell'Unione Europea più colpiti.
Anche in questo caso partendo dal 20 Febbraio 2020.

.. image:: /media/images/210/covid19-worldwide-${UPDATED}_eu_1-10.png
   :height: 700 px
   :width:  900 px
   :scale: 85 %
   :align: center
   :alt:   COVID-19, Unione Europea
   :name:  COVID-19, Unione Europea

I dati da cui sono derivati i grafici sono consultabili 
a `questo indirizzo </media/data/210/covid19-worldwide-${UPDATED}.csv>`_.

Sintesi della situazione al $UPDATED
------------------------------------------------------------------------

Qui di seguito una sintesi della situazione per i venti paesi più colpiti
alla data di aggiornamento di questo documento. Le colonne indicano:

* *date*, la data del giorno;
* *cases*, il totale dei casi alla data indicata: positivi+guariti+deceduti;
* *death*, il totale dei deceduti alla data indicata;
* *death/cases*, il rapporto tra decessi e totale dei casi;
* *cases/population*, il rapporto tra numero totale di casi e la popolazione;
* *death/population*, il rapporto tra numero di decessi e la popolazione;
* *country*, il nome della nazione.

Nella prima tabella i paesi dell'Unione Europea sono aggregati.

.. csv-table:: situazione dei venti paesi più colpiti al $UPDATED, EU aggregata

$DATA_TABLE

|
|

Invece in questa tabella i paesi dell'Unione Europea sono disaggregati.

.. csv-table:: situazione dei venti paesi più colpiti al $UPDATED, EU disaggregata

$DATA_TABLE_EU


Osservazioni
---------------------

Le osservazioni più recenti precedono quelle temporalmente più datate.

*[23 Giugno 2020]* Con sgomento e con dolore osservo gli andamenti di contagi negli 
Stati Uniti e in Brasile. Nei fatti questi paesi stanno applicando politiche di 
contenimento del contagio molto blande. E il risultato si osserva guardando 
come sale la relativa curva dei casi totali.

Ormai gli Stati Uniti hanno superato i due milioni e trecentomila casi totali, 
con oltre 120000 decessi. Mentre il Brasile in poco più di due mesi ha 
superato il milione di casi totali, con oltre 50000 decessi.

Riguardo il dolorosissimo aspetto dei decessi. Mentre posso pensare,
fino ad un certo punto, che negli
US il servizio sanitario possa essere più avanzato di quello dell'Unione Europea
(che con meno casi totali: un milione e duecentomila, ha avuto più decessi:
oltre centotrentamila), faccio fatica ad accettare la stessa considerazione 
per il sistema sanitario brasiliano. In questo caso temo che molti decessi
avvengano al di fuori degli ospedali e/o che in ogni caso non vengano 
diagnosticati come dovuti all'infezione di COVID-19.

Dato l'attuale comportamento di questi paesi, che per diminuire gli impatti sull'economia
non seguono politiche sanitarie di lockdown, temo che vedremo quale sarà
l'efficacia del concetto di immunità di gregge. Spero solo che la medicina
faccia rapidi progressi nel mettere a punto cure adeguate. Perché se
l'immunità di gregge si raggiungerà con un 60% della popolazione infettata
(questa era l'ipotesi ventilata in Gran Bretagna), considerando la popolazione
di circa 330 milioni di persone in US, si raggiungeranno ben 198 milioni di 
casi totali prima che l'immunità di gregge sia efficace. E se la mortalità 
dovesse rimanere quella attuale (il 5.2% dei 
casi totali), gli US sperimenterebbero la spaventosa cifra di circa 10 milioni di decessi.

E in questo momento mi preoccupa anche la situazione dell'India, la cui curva
dei casi totali ha assunto un andamento polinomiale con concavità verso l'alto.
Segno che la politica di lockdown si sta dimostrando poco efficace. 
Anche in questo caso la percentuale di decessi attribuita al COVID-19 è 
molto inferiore a quella misurata in Unione Europea. E anche in questo caso non credo
il servizio sanitario sia all'altezza di quello della UE.
Inoltre qui stiamo parlando di un miliardo e trecento milioni di persone. L'impatto 
globale come perdita di vite umane sarebbe tremendo.

*[23 Giugno 2020 - fine]*

*[15 Aprile 2020]* Finalmente, in Europa si osserva che le curve dei casi totali
della Spagna e dell'Italia cominciano ad appiattirsi. Ciò è indicativo del fatto
che in queste due nazioni l'epidemia comincia a rallentare. Anche la Germania
mostra lo stesso andamento, mentre sembrano esservi incertezze per l'efficacia
delle misure di contenimento in Francia. Infatti in questo paese si era osservato
un netto miglioramento qualche giorno fa; miglioramento ora vanificato da un deciso 
aumento della pendenza della relativa curva.

Complessivamente l'Unione Europea mostra un lieve rallentamento della diffusione
del virus. Invece non vedo ancora chiari segni di rallentamento negli Stati Uniti.

Più che mai trovo schizofrenica la politica di Trump.
Da un lato accusa OMS di non avere avvertito con efficacia dell'estensione
dell'epidemia in arrivo, e gli revoca i fondi americani. Dall'altro
preme per riprendere le attività lavorative, quando l'epidemia è ancora 
pienamente in corso. Che cosa ci avrebbe fatto con gli avvertimenti
dell'OMS (che sono stati emessi a paccate), se comunque li ignora?

*[15 Aprile 2020 - fine]*

*[31 Marzo 2020]* Sbalorditiva la velocità con cui si è impennata
la curva dei casi totali degli USA. Evidentemente la trascuratezza con cui
gli USA (non) hanno affrontato il problema ha lasciato covare l'epidemia
senza che ne venisse rilevata la presenza per un lungo periodo 
di tempo. Ora purtroppo ne pagano le conseguenze. Fortunatamente, almeno per ora, con un 
numero di decessi percentualmente basso.

Il numero totale dei casi della Francia ha superato quello dell'IRAN. Quest'ultimo
sta vedendo un certo incremento dei contagi, anche se non al ritmo dei principali
paesi europei: Italia, Spagna, Germania, e Francia.

Purtroppo tutti i rapporti decessi/casi totali, sono in peggioramento. L'Italia
ha superato l'11%, la Spagna è oltre l'8%. Anche IRAN e Francia hanno superato il 6%.
Solo la Germania continua ad avere una percentuale inferiore all'1%: spero 
riescano a mantenerla costante.

*[31 Marzo 2020 - fine]*

*[26 Marzo 2020]* Ho aggiunto una tabella riassuntiva dei dati relativi
alla data di aggiornamento. In questa tabella ho inserito una colonna che riporta il rapporto tra 
decessi e numero totale di casi positivi.

I numeri di questa colonna sono contrastanti. A fronte di una mortalità
del 9.8% dell'Italia, si osserva un 4% della Cina e un 1.4% degli USA. Per
non parlare del 0.3% dell'Australia o della Germania o della Norvegia.

Questi divari sono eccessivi per 
sistemi sanitari che sono qualitativamente comparabili. Anche volendo
mettere in conto per l'Italia un eccesso di popolazione in età avanzata.
Sono convinto che siamo di fronte a diversi criteri di censimento dei dati. Sia per 
definire la positività alla malattia, che per la causa del decesso. 

E sono convinto che la prima cosa da fare consiste nell'imporre un standard
di comportamento tra tutte le nazioni, altrimenti il monitoraggio non ha senso.
E quanto fatto in un paese, non è analizzabile e confrontabile con quanto 
fatto in un'altra nazione. Ad esempio, insisto, si osservi la curva 
dei casi totali dell'Iran; che per me è un grosso punto interrogativo.

*[26 Marzo 2020 - fine]*


*[20 marzo 2020]* Alla data di stesura di questo articolo osserviamo:

* come indicato dall'andamento costante della curva della Cina,
  questo paese è in una fase di gestione post epidemica; i nuovi 
  casi sono molto contenuti, e in gran parte, o totalmente, dovuti 
  a contagi di persone provenienti dall'estero;
* in Italia l'infezione è ancora in pieno sviluppo, come si 
  nota osservando la pendenza accentuata della relativa curva;
* così come sono in piena fase di diffusione la Spagna e gli 
  USA; questi addirittura sembrano avere tassi di espansione dell'epidemia
  superiori all'Italia;
* sorprendente la Corea, che è riuscita a contenere rapidamente 
  l'espansione del virus; da questo paese avremmo (tutti) da imparare;
  non sarebbe male chiedere loro consiglio;
* strano l'Iran; la sua curva, dopo il primo andamento (come al solito)
  polinomiale, ora si è appiattito in modo simile ad una retta; segno
  che le attività di contrasto in corso sono piuttosto efficaci
  anche se non riescono a bloccare completamente la diffusione del virus;
  anche questo sarebbe un caso da cui apprendere qualcosa.

*[20 marzo 2020 - fine]*


Ed alcune considerazioni
---------------------------

Questa pandemia ha reso evidente più che mai il fatto che "*tutto il mondo
è paese*". Un vecchio proverbio che voleva mettere in evidenza come certi
comportamenti siano osservabili in tutte le persone. Ma che ora si 
può intendere alla lettera: i viaggi per piacere o per lavoro tessono
una ragnatela che avvolge tutta l'umanità nel mondo.

A mio avviso non è un caso che in Italia la diffusione sia avvenuta proprio
nelle regioni più attive industrialmente: Lombardia, Emilia Romagna e Veneto.
Sono le regioni che hanno avuto più contatti con le industrie in Cina, dove 
è avvenuta la prima diffusione.

**Attenzione**, non sto dicendo che sia colpa
della Cina, o che non si deve commerciare con essa. Sono convinto che una
nuova epidemia si sarebbe potuta sviluppare in un qualunque altro paese 
nel mondo. E se questo paese fosse stato attivo industrialmente 
(esempi: Germania, Francia, USA, Brasile, UK, Italia, ...) sarebbe
accaduto esattamente ciò che stiamo vivendo ora: dal paese in questione
(la nazione zero :-) si sarebbe diffuso ad un suo partner industriale
(la nazione uno ...) per poi diffondersi nel resto del mondo.

Quindi, che facciamo? Fermiamo  i viaggi, e riportiamo il mondo ad un 
medioevo fatto di feudi i cui confini potevano essere attraversati
solo per gravissimi motivi? (ricordate il film *Non ci resta che piangere*
di Benigni e Troisi? Il gabelliere
che chiedeva: "chi siete? cosa portate? quanti siete? un fiorino!").

Qualunque cosa dica Trump, io non credo sia una buona idea. Anche perché sono 
convinto che se in quel periodo carestia e malattie mietevano vittime, era
proprio a causa della miseria di risorse fisiche e di conoscenza
imposte da questa parcellizzazione che impediva aiuto e conoscenza
reciproche.

In un corso di comunicazione che ho frequentato tempo fa, l'insegnante
esordì dicendo: "Quando parlate con qualcuno ricordate a voi stessi:
la sua differenza è la vostra ricchezza".

Questo concetto è cardine. Attraverso le differenze tra persone si scoprono
nuovi modi di vedere le cose. E ogni volta si scopre qualcosa, gli orizzonti
si allargano, migliorando noi stessi e chi ci circonda. Ampliando le nostre 
capacità e quelle del nostro vicino.

Quindi io penso: ben vengano i viaggi, un mondo sempre più connesso, 
scambi commerciali con tutti. Ma ... **attrezziamoci**!

Nel 2015 un persona, tal Bill Gates, in una sua 
`esposizione a TED <https://www.youtube.com/watch?v=6Af6b_wyiwI>`_ si disse 
convinto che il maggior rischio per l'umanità è la possibilità di una pandemia.
In quell'occasione Bill Gates propose di organizzarsi con un modello
sanitario in grado di reagire rapidamente in tutto il mondo per contrastare
con efficacia una epidemia. E concluse il suo intervento dicendo: "se iniziamo
(a prepararci) adesso, potremo essere pronti per la prossima epidemia".

Non ci siamo preparati. E ora ne paghiamo le conseguenze, in termini economici
e, sopratutto, di vite perse.

Da tutto ciò, saremo in grado di imparare?

Per finire: come ne usciamo? Più che mai con uno sforzo comune. E necessario
mettere a fattor comune le risorse dei diversi paesi per farle confluire dove servono
maggiormente. Sento di persone che si alterano perchè pensano che tamponi
prodotti in Italia non dovevano essere forniti agli USA. Ma noi italiani, a nostra volta,
non ci siamo fatti scrupolo di acquistare i sistemi sanitari di ventilazione 
dalla Germania. Quindi? Insisto, non è chiudendoci nel nostro feudo che ne 
verremo fuori senza acciacchi. Bene l'Unione Europea se veramente organizzarà
una riserva di materiali sanitari da impiegare nei paesi con maggiori necessità.

