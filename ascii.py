from cards import Karte, Farbe, KartenTyp, Stapel


class AsciiScreen(object):
    def __init__(self, width=90, height=35):
        self.width = width
        self.height = height
        self.screen = [" " for x in range(0, width) for y in range(0, height)]
        self.buffer = ""

    def _update_buffer(self) -> str:
        result = ""
        for y in range(self.height):
            for x in range(self.width):
                result += self.screen[self.width*y+x]
            result += "\n"
        self.buffer = result

    def write_to_screen(self, text: str, x: int = 0, y: int = 0):
        # TODO check that x y are within limits
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
        print(self.buffer)


class AsciiStapel(object):
    def __init__(self, stapel: Stapel):
        self.stapel = stapel

    def width(self) -> int:
        return AsciiKarte.width()

    def height(self) -> int:
        return len(self.stapel.karten)-1 * 2 + AsciiKarte.height()

    def print(self) -> str:
        return AsciiKarte.print(self.stapel.top())

    def printFanned(self) -> str:
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
    @classmethod
    def width(self) -> int:
        return 10

    @classmethod
    def height(self) -> int:
        return 5

    @classmethod
    def print(self, karte: Karte) -> str:
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
        typ = karte.typ.blatt
        farbe = karte.farbe.blatt
        return """┌────────┐
│ {0}    {1} │
│        │
│        │
│ {1}    {0} │
└────────┘""".format(typ, farbe)

    @classmethod
    def back(self) -> str:
        return """┌────────┐
│\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588│
│\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588│
│\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588│
│\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588│
└────────┘
"""

    @classmethod
    def empty(self) -> str:
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
        Karte(farbe=Farbe.KREUZ, typ=KartenTyp.FUENF),
        Karte(farbe=Farbe.KARO, typ=KartenTyp.DAME),
        Karte(farbe=Farbe.PIK, typ=KartenTyp.FUENF, visible=True),
        Karte(farbe=Farbe.KARO, typ=KartenTyp.VIER, visible=True),
        Karte(farbe=Farbe.KREUZ, typ=KartenTyp.DREI, visible=True),
        Karte(farbe=Farbe.HERZ, typ=KartenTyp.ZWEI, visible=True)
    ]))
    screen.write_to_screen(stapel.printFanned(), 0, 0)
    # with open(file="spielfeld.txt", mode="r") as f:
    #     txt="".join(f.readlines())
    #     screen.write_to_screen(txt)
    # screen.write_to_screen("Hello what do you want to do? ", 0,28)
    screen.print()
