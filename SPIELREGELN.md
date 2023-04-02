
## Spielregeln
Solitair ist ein Einzelspielerspiel bei dem alle Karten vom Ziehstapel auf 4 Ablagestapel (A1-4) verschoben werden müssen. 

Ziel ist es die Karten in der Reihenfolge AS, 2, 3, 4, 5, 6, 7, 8, 9, 10, BUBE, DAME und KÖNIG nach Farben HERZ, KARO, PIK, KREUZ auf die Ablagestapel zu bringen.

Am Anfang sind auf den Anlegestapeln S1-6 jeweils 1 bis 7 Karten verteilt wobei auf jedem Stape eine Karte mehr als auf dem vorherigen liegt und alle Karten bis auf die oberste verdeckt sind. 

### Spielfeld
<pre>
┌──┐ ┌──┐ ┌──┐ ┌──┐      ┌──┐ ┌──┐
│A1│ │A2│ │A3│ │A4│      │A5│ │  │
└──┘ └──┘ └──┘ └──┘      └──┘ └──┘
 
┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
│S0│ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
└──┘ │S1│ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
     └──┘ │S2│ ┌──┐ ┌──┐ ┌──┐ ┌──┐
          └──┘ │S3│ ┌──┐ ┌──┐ ┌──┐
               └──┘ │S4│ ┌──┐ ┌──┐
                    └──┘ │S5│ ┌──┐
                         └──┘ |S6│
                              └──┘
                             
──────────────────────────────────                                                                                   
Menü
</pre>

### Karten Verschieben
Karten dürfen nur von den Anlagestapeln (S1-6) und vom Ablagestapel (A5) auf die Ablagestapel (A1-4) abgelegt werden.

Bei jedem Zug hat der Spieler die Möglichkeit:

* Karten auf die Ablagestapel (A1-4) abzulegen.
* Karten vom Ablagestapel A5 an die Anlagestapel S1-6 anzulegen. Wobei gilt die Karten müssen immer abwechselnd rot oder schwarz sein und der Wert der Karte muss in der Reihenfolge 1 Wert niedriger sein als die oberste Karte.
* Karten können von einem Anlagestapel S1-6 auf einen anderen Anlagestapel verschoben werden wobei die Anlageregel das der Wert der obersten zu verschiebenden Karten in der Reihenfolge eins niedriger sein muss als die Karte an die angelegt wird und die Farbe muss immer zwischen rot und schwarz wechseln.

### Beispiel Anlage von ♠7
<pre>
 Before    After      
┌──┐┌──┐   ┌──┐                                  
│♥8│|♠7|   │♥8│   
└──┘└──┘   ┌──┐ 
           |♠7|
           └──┘
</pre>

Beispiel Verschieben von S3 zu S0
<pre>
 Before      After

 S0  S3      S0  S3 
┌──┐┌──┐    ┌──┐┌──┐                 
┌──┐┌──┐    ┌──┐┌──┐      
┌──┐┌──┐    ┌──┐┌──┐      
┌──┐┌──┐    ┌──┐|  |                                 
│♥8│|♠7|    |♥8│└──┘                                  
└──┘┌──┐    ┌──┐                                 
    │♦6|    │♦7|                                 
    ┌──┐    ┌──┐                                 
    │♣5|    │♦6|                                 
    └──┘    ┌──┐
            |♣5|
            └──┘                           
</pre>


