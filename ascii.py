from cards import Karte, Farbe, KartenTyp, Stapel
from time import sleep


class AsciiScreen(object):
    """
    Die Klasse definiert einen zeichenbaren Bildschirm im Terminal. 
    Der Bildschirm kann dann vorbereitet werden und mittels `print()` 
    im Terminal ausgegeben werden. 
    """

    def __init__(self, width: int = 90, height: int = 35):
        """
        Erstellt einen AsciiScreen mit der Breite `width` und der Höhe `height`

        width   - `int` die Breite des Bildschirms
                  Default: 90
        height  - `int` die Höhe des Bildschirms
                  Default: 35
        """
        self.width = width
        self.height = height
        self.screen = [" " for t in range(0, width*height)]
        self.buffer = ""

    def _update_buffer(self) -> str:
        """
        Beschreibt den internen Puffer mit dem aktuellen Inhalt des Bildschirms
        Gibt den internen Puffer als `str` zurück. 
        """
        result = ""
        for y in range(self.height):
            for x in range(self.width):
                result += self.screen[self.width*y+x]
            result += "\n"
        self.buffer = result
        return result

    def clear_screen(self):
        """
        Löscht den Inhalt des Bildschirms in dem alle Zeichen mit ' ' ersetzt werden.
        """
        self.screen = [" " for t in range(0, self.width*self.height)]

    def write_to_screen(self, text: str, x: int = 0, y: int = 0):
        """
        Schreibt den Text `text` an die Stelle x,y in den internen Puffer. 
        Zum anzeigen des textes muss `self.print()` aufgerufen werden. 
        Die Zeichen werden mittels `for ch in text` in den internen Puffer übertragen 
        und daher werden nur einzeln kodierte Zeichen unterstützt. 

         text - `str` Der auszugebende Text 
            x - `int` x-Koordinate wo der Text dargestellt wird
            y - `int` y-Koordinate wo der Text dargestellt wird
        """
        if x not in range(0, self.width):
            raise ValueError(f"x ist nicht im Bereich [{0},{self.width}[")
        if y not in range(0, self.height):
            raise ValueError(f"y ist nicht im Bereich [{0},{self.height}[")
        # initialize start coordinates
        _x = x
        _y = y
        # split text into lines
        lines = text.splitlines()
        for line in lines:
            # go character by character
            for ch in line:
                if self.width*_y+_x < len(self.screen):
                    self.screen[self.width*_y+_x] = ch
                _x += 1
            _x = x
            _y += 1
            if _y >= self.height:
                # stop if we have reached bottom of screen
                break

        self._update_buffer()

    def print(self):
        """
        Zeichnet den Bildschirm auf Terminal mittels print()
        """
        print(self.buffer)


class AsciiStapel(object):
    """
    Die Klasse definiert Methoden mit denen ein Stapel auf einem 
    Terminal gezeichnet werden können.
    """
    def __init__(self, stapel: Stapel):
        """
        Erstellt einen AsciiStapel mit den angegebenen Karten `karten`.

        stapel - `Stapel` der Stapel der dekoriert werden soll
        """
        self.stapel = stapel

    def width(self) -> int:
        """
        Gibt die Breite des Stapels als `int` zurück.
        """
        return AsciiKarte.width()

    def height(self, fanned: bool = True) -> int:
        """
        Gibt die Höhe des Stapels als `int` zurück.
        Wenn `fanned` `True` ist dann wird die Höhe in gefächerter 
        Form dargegeben ansonsten entspricht die Höhe einer einzelnen Karte.

        fanned - `bool` `True` wenn der Stapel gefächert dargestellt werden soll 
                 `False` wenn nicht.
        """
        if fanned:
            return len(self.stapel.karten)-1 * 2 + AsciiKarte.height()
        else:
            return AsciiKarte.height()

    def print(self) -> str:
        """
        Gibt den Stapel als str zurück in Form einer einzelne Karte. Die Methode zeichnet 
        die oberste Karte mittels `AsciiKarte.print(karte)`.
        """
        return AsciiKarte.print(self.stapel.top())

    def printFanned(self) -> str:
        """
        Gibt den Stapel als str in gefächerter Darstellung zurück. 
        Der Stapel wird in die aufgedeckten und verdeckten Karten gesplitet. 
        Für jede Karte bis auf die oberste werden die oberen 2 Zeilen der Karten Darstellung gezeichnet
        Die oberste Karte wird komplett dargestellt. 
        Ist die Karte verdeckt wird `AsciiKarte.back()` aufgerufen für aufgedeckte Karten wird `AsciiKarte.front()` 
        aufgerufen.
        """
        card_top = AsciiKarte.back().splitlines(keepends=True)[0]
        result = ""
        hidden = [k for k in self.stapel.karten if not k.aufgedeckt()]
        shown = [k for k in self.stapel.karten if k.aufgedeckt()]

        if len(hidden) == 0 and len(shown) == 0:
            return AsciiKarte.empty()

        for k in enumerate(hidden):
            result += card_top

        for idx, k in enumerate(shown):
            if idx < len(shown)-1:
                result += "".join(AsciiKarte.front(
                    k).splitlines(keepends=True)[:2])
            else:
                result += AsciiKarte.front(k)
        return result


class AsciiKarte(object):
    """
    Die Klasse definiert statische Methoden für die Darstellung von einzelnen Karten 
    auf einem Terminal.
    """
    @classmethod
    def width(self) -> int:
        """
        Gibt die Breite einer Karte als int zurück
        """
        return 10

    @classmethod
    def height(self) -> int:
        """
        Gibt die Höhe einer Karte als int zurück
        """
        return 5

    @classmethod
    def print(self, karte: Karte) -> str:
        """
        Gibt die Karte `karte` als `str` zurück. Wenn die Karte
        aufgedeckt ist wird `self.front(karte)` aufgerufen ansonsten 
        wird `self.back()` aufgerufen.
        
        karte - Karte die darzustellende Karte
        """
        blatt = ""
        if karte is None:
            blatt = self.empty()
        elif karte.aufgedeckt():
            blatt = self.front(karte)
        else:
            blatt = self.back()
        return blatt

    @classmethod
    def front(self, karte: Karte) -> str:
        """
        Gibt Vorderseite der Karte `karte` als `str` zurück.
        
        karte - Karte die darzustellende Karte
        """
        typ = karte.typ.blatt
        farbe = karte.farbe.blatt
        return """┌────────┐
│ {0:<2s}   {1} │
│        │
│        │
│ {1}   {0:>2s} │
└────────┘""".format(typ, farbe)

    @classmethod
    def back(self) -> str:
        """
        Gibt die Rückseite einer Karte als `str` zurück.
        """
        return """┌────────┐
│\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588│
│\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588│
│\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588│
│\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588│
└────────┘
"""

    @classmethod
    def empty(self) -> str:
        """
        Gibt die Darstellung eines leeren Stapels zurück.
        """
        return """┌────────┐
│        │
│   \/   │
│   /\   │
│        │
└────────┘
"""


if __name__ == "__main__":
    screen = AsciiScreen(height=20, width=22)
    stapel = AsciiStapel(Stapel(karten=[
        Karte(farbe=Farbe.HERZ, typ=KartenTyp.FUENF),
        Karte(farbe=Farbe.PIK, typ=KartenTyp.ZWEI),
        Karte(farbe=Farbe.KREUZ, typ=KartenTyp.AS),
        Karte(farbe=Farbe.HERZ, typ=KartenTyp.DAME),
        Karte(farbe=Farbe.KREUZ, typ=KartenTyp.ZEHN),
        Karte(farbe=Farbe.KARO, typ=KartenTyp.DAME),
        Karte(farbe=Farbe.PIK, typ=KartenTyp.FUENF, visible=True),
        Karte(farbe=Farbe.KARO, typ=KartenTyp.VIER, visible=True),
        Karte(farbe=Farbe.KREUZ, typ=KartenTyp.DREI, visible=True),
        Karte(farbe=Farbe.HERZ, typ=KartenTyp.ZWEI, visible=True)
    ]))
    for i in range(0, 11):
        screen.write_to_screen(stapel.printFanned(), 0, 0)
        screen.print()
        stapel.stapel.ziehen()
        stapel.stapel.aufdecken()
        sleep(1)
        screen.clear_screen()
