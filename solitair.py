from cards import Karte, Stapel, AnlageStapel, AblageStapel, Farbe, KartenTyp
from ascii import AsciiScreen, AsciiKarte, AsciiStapel
from copy import deepcopy
from collections import deque
import logging
from logging.config import dictConfig
from json import load as jload
import sys

LOG = logging.getLogger("solitair")


class Spielstand(object):
    """
    Speichert den aktuellen Spielstand eines Solitairspiels
    """
    ID_GEN = 0

    @classmethod
    def _gen_id(self) -> int:
        Spielstand.ID_GEN += 1
        return Spielstand.ID_GEN

    def __init__(self, anlageStapel: list[AnlageStapel], ziehStapel: Stapel, ablageStapel: Stapel, ablagen: list[AblageStapel], punkte: int) -> None:
        self.ablagen = deepcopy(ablagen)
        self.anlageStapel = deepcopy(anlageStapel)
        self.ablageStapel = deepcopy(ablageStapel)
        self.ziehStapel = deepcopy(ziehStapel)
        self.punkte = punkte
        self.id = Spielstand._gen_id()

    def __eq__(self, other: object) -> bool:
        if type(other) == Spielstand:
            return (self.ablagen == other.ablagen and
                    self.anlageStapel == other.anlageStapel and
                    self.ablageStapel == other.ablageStapel and
                    self.ziehStapel == other.ziehStapel and
                    self.punkte == other.punkte)
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"Sp:{self.id}({','.join([str(a) for a in self.ablagen])},{','.join([str(a) for a in self.anlageStapel])},{str(self.ablageStapel)},{str(self.ziehStapel)},{str(self.punkte)})"

    def __repr__(self) -> str:
        return f"Spielstand({repr(self.ablagen)},{repr(self.anlageStapel)},{repr(self.ablageStapel)},{repr(self.ziehStapel)},{repr(self.punkte)})"


class Solitair(object):
    """
    Basis Klasse für Solitär

    Die Klasse initialsiert alle wichtigen elemente und startet das spiel mit `starten()`
    """

    SOLITAIR = """
        ███████╗ ██████╗ ██╗     ██╗████████╗ █████╗ ██╗██████╗
        ██╔════╝██╔═══██╗██║     ██║╚══██╔══╝██╔══██╗██║██╔══██╗
        ███████╗██║   ██║██║     ██║   ██║   ███████║██║██████╔╝
        ╚════██║██║   ██║██║     ██║   ██║   ██╔══██║██║██╔══██╗
        ███████║╚██████╔╝███████╗██║   ██║   ██║  ██║██║██║  ██║
        ╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
                        (c) 2023 Stefan Langer"""

    COMMANDS = {"z": {"text": "[z]iehen", "method": f"self._ziehen()"},
                "a": {"text": "[a]nlegen", "method": f"self._anlegen()"},
                "l": {"text": "ab[l]egen", "method": f"self._ablegen()"},
                "m": {"text": "neu [m]ischen", "method": f"self._neu_mischen()"},
                "v": {"text": "[v]erschieben", "method": f"self._verschieben()"},
                "u": {"text": "[u]ndo", "method": f"self._undo()"},
                "g": {"text": "neu [g]eben", "method": f"self._umdrehen()"},
                "b": {"text": "[b]eenden", "method": f"self._ende()"}, }

    MAX_UNDOS = 10

    def __init__(self) -> None:
        '''
        Der Konstruktor für die Klasse Solitair. Im Konstruktor werden die verschiedenen Spielelemente
        erzeugt.
        1. Der Stapel von dem Karten gezogen werden
        2. Die Ablagestapel wo die Karten final abgelegt werden
        3. Die 7 Anlagestapel wo die Karten während des Spiels sortiert werden
        4. Der AsciiScreen auf den das Spielfeld dargestellt wird
        5. Das Menü und die Navigationshilfen um das Spiel zu bedienen
        '''
        self.ziehStapel = Stapel(karten=[Karte(col, type) for col in list(Farbe)
                                         for type in list(KartenTyp)])
        self.ziehStapel.shuffle()
        self.ablageStapel = Stapel()
        self.ablagen = [AblageStapel(farbe=Farbe.HERZ),
                        AblageStapel(farbe=Farbe.KARO),
                        AblageStapel(farbe=Farbe.KREUZ),
                        AblageStapel(farbe=Farbe.PIK)]
        self.screen = AsciiScreen(width=74, height=AsciiKarte.height()*2 + 33)
        self.navigation = False
        self.navigation_anlage = False
        self.navigation_ablage = False
        self.status_msg = ""
        self.punkte = 0
        self.anlageStapel = [AsciiStapel(AnlageStapel(karten=self._initAnlage(i+1)))
                             for i in range(7)]
        self.speicher = deque(maxlen=Solitair.MAX_UNDOS)

    def _initAnlage(self, kartenZiehen: int) -> list[Karte]:
        """
        Hilfs methode um die Anlagestapel zu initialisieren.
        Die methode zieht die angegebenen Anzahl von Karten vom Stapel und gibt sie als list[Karte] zurück.

        kartenZiehen - `int` die Anzahl der verdeckten Karten die zurückgegeben werden
        """
        karten = []
        for i in range(kartenZiehen):
            karten.append(self.ziehStapel.ziehen())
            if i == kartenZiehen-1:
                karten[i].aufdecken()
        return karten

    def _undo_speicher_str(self) -> str:
        return f"[{','.join([str(s.id) for s in self.speicher])}]"
    
    def _spielstand_erzeugen(self) -> Spielstand:
        return Spielstand(self.anlageStapel, self.ziehStapel,
                             self.ablageStapel, self.ablagen, self.punkte)
        
    def _spielstand_sichern(self, spielstand: Spielstand):
        LOG.debug("Spielstand %s sichern!", spielstand.id)
        LOG.debug("%s", spielstand)
        self.speicher.append(spielstand)
        LOG.debug("Undo Speicher %s", self._undo_speicher_str())

    def _spielstand_herstellen(self, spielstand: Spielstand):
        LOG.info("Herstellen von Spielstand %s!", spielstand.id)
        LOG.debug("Herzustellender Spielstand %s", spielstand)
        self.ablagen = spielstand.ablagen
        self.ablageStapel = spielstand.ablageStapel
        self.anlageStapel = spielstand.anlageStapel
        self.ziehStapel = spielstand.ziehStapel
        self.punkte = spielstand.punkte
        
    def _spielzug_zurueck_nehmen(self) -> Spielstand:
        if len(self.speicher) > 0:
            sp = self.speicher.pop()
            LOG.info("Zug zurueck genommen! Spielstand %s", sp.id)
            LOG.debug("Undo Speicher %s", self._undo_speicher_str())
            return sp
        return None

    def _letzter_gesicherter_spielstand(self) -> Spielstand:
        return self.speicher[-1] if len(self.speicher) > 0 else None

    def _punkte_hinzufügen(self, punkte: int) -> int:
        self.punkte += punkte
        return self.punkte

    def _zeichnen(self) -> None:
        """
        Malt das Spielfeld in dem es die notwendigen Ascii zeichen auf den AsciiScreen schreibt und anschliessend
        print aufruft.

        Siehe auch self.write_to_screen()
        """
        score_txt = f"Punkte: {self.punkte:>4}"
        self.screen.write_to_screen(
            score_txt, self.screen.width - len(score_txt) - 3)
        for idx, a in enumerate(self.ablagen):
            self.screen.write_to_screen(AsciiKarte.print(a.top()),
                                        AsciiKarte.width()*idx+2, 1)

        self.screen.write_to_screen(AsciiKarte.print(self.ablageStapel.top()),
                                    self.screen.width - AsciiKarte.width()*2-2, 1)
        if self.navigation_ablage:
            self.screen.write_to_screen(
                f"[{len(self.anlageStapel)}]", self.screen.width - AsciiKarte.width()*2-1, AsciiKarte.height()+2)
        self.screen.write_to_screen(AsciiKarte.print(self.ziehStapel.top()),
                                    self.screen.width - AsciiKarte.width()-2, 1)

        for idx, a in enumerate(self.anlageStapel):
            self.screen.write_to_screen(
                a.printFanned(), AsciiKarte.width()*idx+2, AsciiKarte.height()+5)
            if self.navigation_anlage:
                self.screen.write_to_screen(
                    f"[{idx}]", AsciiKarte.width()*idx+3, AsciiKarte.height()+4)

        self.screen.write_to_screen(
            self._menue(), 0, AsciiKarte.height()*2 + 30)
        self.screen.write_to_screen(
            self.status_msg, 2, AsciiKarte.height()*2 + 28)
        self.screen.print()

    def _menue(self) -> str:
        """
        Generiert das Menü, dass in `Solitair.COMMANDS` definiert ist.
        """
        menu = "".join(["─" for i in range(self.screen.width)]) + "\n"
        idx = 1
        for cmd in [v["text"] for k, v in Solitair.COMMANDS.items()]:
            menu += f"{cmd:<15}"
            if idx % 4 == 0:
                menu += "\n"
            idx += 1
        return menu

    def _eingabe(self):
        """
        Verarbeitet die Menüeingaben. Die Eingabe wird gegen self.COMMANDOS geprüft. Wird das Kommando
        gefunden wird die hinterlegte methode ausgeführt. Ansonsten wird eine Fehlermeldung ausgegeben.
        """
        eingabe: str = input("Option: ").lower().strip()
        if eingabe in Solitair.COMMANDS:
            
            exec(Solitair.COMMANDS[eingabe]["method"])    
        else:
            self._schreibe_status(
                f"Ungültige eingabe: {eingabe}! Bitte wählen sie eine gültige Option.")

    def _schreibe_status(self, text: str):
        """
        Speichert die angegebene Status message in den internen Puffer. Beim nächste aufruf von print wird die
        Statusnachricht angzeigt.

        text - `str` die Statusnachricht
        """
        self.status_msg = text

    def _lese_nummer(self, msg: str, range: range) -> int:
        """
        Fragt den user nach einer nummerischen Eingabe.
        Die Frage wird so lange wiederholt bis die Eingabe valide ist.

            msg - `str`  die Frage für die Eingabe
          range - `range` das Intervall in dem sich die Eingabe befinden muss. Das obere Ende der Range is exklusive
        """
        num = ""
        while True:
            num = input(msg).strip()
            if num.isdigit() and int(num) in range:
                return int(num)
            else:
                self._schreibe_status("Bitte geben sie eine gültige Zahl an!")
                self._zeichnen()

    def _zeige_navihilfe(self, withAblage=False):
        """
        Setzt navigation flag auf True so dass die Eingabehilfe beim nächsten screen.print() mit angezeigt wird

        withAblage - `bool` sagt ob die Navigationshilfe für den Ablagestapel ebenfalls angezeigt werden soll
        """
        self.navigation_anlage = True
        if withAblage:
            self.navigation_ablage = True
        self._zeichnen()

    def _verstecke_navihilfe(self):
        """
        Setzt das Navigationsflag auf False so dass die Eingabehilfe beim naächen screen.print() nicht mehr angezeigt wird.
        """
        self.navigation_anlage = False
        self.navigation_ablage = False

    def _ende(self):
        """
        Method wird aufgerufen wenn der beenden Menüpunkt gewählt wird.
        Die Methode gibt den Endscreen aus und beendet dann das Programm mit exit(0)
        """
        self.screen.clear_screen()
        self.screen.write_to_screen(Solitair.SOLITAIR + """
                Danke das sie Solitair gespielt haben!
                    Drücke Enter um fortzufahren
""", 0, 10)
        self.screen.print()
        input()
        exit(0)

    def _umdrehen(self):
        """
        Die Methode wird aufgerufen wenn der umdrehen Menüpunkt ausgewählt wird.
        Zunächst wird gepräft ob der Ziehstapel leer ist und falls ja werden die Karten
        auf dem Ablagestapel neugemischt und verdeckt auf den Ziehstapel abgelegt.
        """
        if self.ziehStapel.leer():
            k = self.ablageStapel.ziehen()
            while k:
                self.ziehStapel.anlegen(k.zudecken())
                k = self.ablageStapel.ziehen()
            self.ziehStapel.shuffle()
            self._punkte_hinzufügen(-20)
        else:
            self._schreibe_status(
                "Umdrehen nicht möglich, es sind noch Karten auf dem Stapel!")

    def _undo(self):
        if self._ja_nein_frage("Wollen sie den Zug wirklich zurücknehmen?"):
            if self._spielzug_zurueck_nehmen():
                self._spielstand_herstellen()
            else:
                self._schreibe_status("Sie können nicht weiter zurück gehen!")

    def _ziehen(self):
        """
        Die Methode wird aufgerufen wenn der ziehen Menüpunkt ausgewählt wird.
        Es wird eine Karte vom Stapel gezogen und auf den Ablagestapel gelegt.
        """
        LOG.info("Karte ziehen")
        k = self.ziehStapel.ziehen()
        if k:
            LOG.debug("Karte %s gezogen und abgelegt", k)
            self.ablageStapel.anlegen(k.aufdecken())
            self._spielstand_sichern()

    def _ablegen(self):
        """
        Die Methode wird aufgerufen wenn der ablegen Menüpunkt ausgewählt wird.
        Die Method
        * zeigt zunächst das Navigationshilemenü
        * dann fragt es nach dem Stapel von dem die Karte genommen werden soll
        * dann wird überprüft ob die Karte tatsächlich abgelegt werden kann
            * wenn nein dann wird eine Fehlernachricht angezeigt und der Vorgan abgebrochen
            * wenn ja dann wird die Karte auf dem entsprechenden Ablagestapel abgelegt
        """
        self._zeige_navihilfe(withAblage=True)
        idx = self._lese_nummer(
            "Welchen Stapel möchten sie ablegen? ", range(0, len(self.anlageStapel)+1))
        self._verstecke_navihilfe()
        if idx < len(self.anlageStapel):
            stapel = self.anlageStapel[idx].stapel
        elif idx == len(self.anlageStapel):
            stapel = self.ablageStapel

        k = stapel.top()
        msg = ""
        if k:
            for s in self.ablagen:
                if k.farbe == s.farbe:
                    if s.anlegbar(k):
                        s.anlegen(stapel.ziehen())
                        stapel.aufdecken()
                        self._punkte_hinzufügen(10)
                        break
                    else:
                        msg = f"Karte {str(k)} kann nicht abgelegt werden!"
            self._schreibe_status(msg)

    def _anlegen(self):
        """
        Die Method wird aufgerufen wenn der anlege Menüpunkt ausgwählt wird.
        Die Method
        * zeigt das Navigationshilfemenü an
        * Fragt dann nach dem Anlagestapel an den angelegt werden soll
        * Überprüft dann ob die Karte angelegt werden kann
            * wenn ja dann wir die Karte vom Ablagestapel genommen und angelegt
            * wenn nein wird eine Fehlermeldung angezeigt und der Vorgang abgebrochen
        """
        k = self.ablageStapel.top()
        if k:
            self._zeige_navihilfe(withAblage=False)
            idx = self._lese_nummer(f"Wo möchten sie die Karte {k.farbe.blatt} {k.typ.blatt} anlegen? ",
                                    range(0, len(self.anlageStapel)))
            self._verstecke_navihilfe()
            stapel = self.anlageStapel[idx].stapel

            if stapel.anlegbar(k):
                stapel.anlegen(self.ablageStapel.ziehen())
                self._punkte_hinzufügen(2)
            else:
                self._schreibe_status(
                    f"Karte {k.farbe.blatt} {k.typ.blatt} kann nicht an Stapel [{idx}] angelegt werden!")

    def _verschieben(self):
        """
        Die Method wird aufgerufen wenn der verschieben Menüpunkt ausgwählt wird.
        Die Method
        * zeigt das Navigationshilfemenü an
        * Fragt nach von welchem Stapel Karten verschoben werden sollen
        * Fragt nach zu welchen Stapel die Karten verschoben werden sollen
        * Versucht dann die Karten mit Stapel.verschieben_nach(zielStapel) zu verschieben
            * wenn das klappt werden die Karten verschoben
            * wenn nicht dann wird eine Fehlermeldung angezeigt und der Vorgang wird abgebrochen
        """
        self._zeige_navihilfe(withAblage=False)
        von = self._lese_nummer(f"Von welchem Stapel wollen sie Karten verschieben? ",
                                range(0, len(self.anlageStapel)))
        vonStapel = self.anlageStapel[von].stapel
        self._schreibe_status(f"Verschieben von Stapel {von}")
        self._zeichnen()
        zu = self._lese_nummer(f"Zu welchem Stapel wollen sie die Karten verschieben? ",
                               range(0, len(self.anlageStapel)))
        zuStapel = self.anlageStapel[zu].stapel
        self._verstecke_navihilfe()
        if vonStapel.verschieben_nach(zuStapel):
            self._schreibe_status("")
        else:
            self._schreibe_status(
                f"Verschieben von Stapel {von} auf Stapel {zu} nicht möglich!")
        
    def _gewonnen(self):
        """
        Überprüft ob das Spiel gewonnen ist.
        Wenn alle Ablagestapel komplett sind wird True zurückgegeben ansonsten False.
        """
        return all([a.komplett() for a in self.ablagen])

    def _ja_nein_frage(self, frage: str) -> bool:
        """
        Stellt die Ja-Nein-Frage `frage` und gibt `True` zurück wenn der User mit Ja antwortet ansonsten `False`.

        frage - `str` Die Ja-Nein-Frage die gestellt werden soll.
        """
        while True:
            eingabe = input(f"{frage} (j/n)")
            if eingabe.lower() == "j":
                return True
            elif eingabe.lower() == "n":
                return False
            else:
                self._schreibe_status(
                    "Bitte geben sie j für Ja oder n für Nein ein!")
                self._zeichnen()

    def _neu_mischen(self):
        """
        Mischt alle Karten auf dem Spielfeld neu durch.
        """
        if self._ja_nein_frage("Wollen sie die Karten wirklich neu mischen?"):
            auswahl = [a.stapel for a in self.anlageStapel] + [self.ablageStapel]
            for a in auswahl:
                while not a.leer():
                    k = a.ziehen()
                    k.zudecken()
                    self.ziehStapel.anlegen(k)

            self.ziehStapel.shuffle()
            self.anlageStapel = [AsciiStapel(AnlageStapel(karten=self._initAnlage(i+1)))
                                 for i in range(7) if self.ziehStapel.karten_anzahl() > i]
            self._punkte_hinzufügen(-100)

    def _willkommen(self):
        """
        Zeigt den Welcome Screen für das Spiel an.
        """
        self.screen.clear_screen()
        self.screen.write_to_screen(Solitair.SOLITAIR + """
                     Drücke Enter um fortzufahren
""", 0, 10)
        self.screen.print()

    def _gewonnen_zeichnen(self):
        """
        Zeigt den Sieger Screen für das Spiel an.
        """
        self.screen.clear_screen()
        self.screen.write_to_screen(f"""
        ███████╗ ██████╗ ██╗     ██╗████████╗ █████╗ ██╗██████╗
        ██╔════╝██╔═══██╗██║     ██║╚══██╔══╝██╔══██╗██║██╔══██╗
        ███████╗██║   ██║██║     ██║   ██║   ███████║██║██████╔╝
        ╚════██║██║   ██║██║     ██║   ██║   ██╔══██║██║██╔══██╗
        ███████║╚██████╔╝███████╗██║   ██║   ██║  ██║██║██║  ██║
        ╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝

 ██████╗ ███████╗██╗    ██╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗███╗   ██╗
██╔════╝ ██╔════╝██║    ██║██╔═══██╗████╗  ██║████╗  ██║██╔════╝████╗  ██║
██║  ███╗█████╗  ██║ █╗ ██║██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██╔██╗ ██║
██║   ██║██╔══╝  ██║███╗██║██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║╚██╗██║
╚██████╔╝███████╗╚███╔███╔╝╚██████╔╝██║ ╚████║██║ ╚████║███████╗██║ ╚████║
 ╚═════╝ ╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝

                      (c) 2023 Stefan Langer
                      Sie haben {self.punkte:>4} Punkte
""", 0, 10)
        self.screen.print()

    def _init_logging(self):
        pass

    def starten(self):
        """
        Methode führt das Spiel aus.
        * zuerst wird der Willkommens Screen angezeigt
        * dann wird das Spielfeld angezeigt
        * als nächstes wird die Spielschleife gestartet die solange läuft bis das Spiel
          gewonnen wurde oder der Benutzer das Spiel beendet
        * Die Spielschleife führt folgende Kommandos der Reiche nach aus:
            * Zunächst wird der Statusnachrichtenpuffer gelöscht
            * Dann wird die Eingabe des Spielers verarbeitet
            * Anschliessend wird der Bildschirm gelöscht
            * um dann den neuen Zustand des Spiels anzuzeigen
        * wenn die Schleife durch einen Sieg beendet wird wird der Siegerbildschirm angezeigt
        * und das Spiel beendet
        """
        self._willkommen()
        input()
        self.screen.clear_screen()
        self._zeichnen()
        # the game loop
        while not self._gewonnen():
            self.status_msg = ""
            self._eingabe()
            self.screen.clear_screen()
            self._zeichnen()
        self._gewonnen_zeichnen()
        input()


if __name__ == "__main__":
    with open(file="logging.json", mode="r", encoding="utf-8") as logconfig:
        configDict = jload(logconfig)
        dictConfig(configDict)

    s = Solitair()
    s.starten()
