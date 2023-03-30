from enum import Enum
from random import shuffle


class Constants(Enum):
    ROT = 0
    SCHWARZ = 1


class Farbe(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, farbe: Constants, blatt: str):
        self.farbe = farbe
        self.blatt = blatt

    KARO = Constants.ROT, "\u2666"
    HERZ = Constants.ROT, "\u2665"
    PIK = Constants.SCHWARZ, "\u2660"
    KREUZ = Constants.SCHWARZ, "\u2663"


class KartenTyp(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, wert: int, blatt: str):
        self.wert = wert
        self.blatt = blatt

    AS = 11, "A"
    ZWEI = 2, "2"
    DREI = 3, "3"
    VIER = 4, "4"
    FUENF = 5, "5"
    SECHS = 6, "6"
    SIEBEN = 7, "7"
    ACHT = 8, "8"
    NEUN = 9, "9"
    ZEHN = 10, "10"
    BUBE = 10, "B"
    DAME = 10, "D"
    KOENIG = 10, "K"


class Karte(object):
    def __init__(self, farbe: Farbe, typ: KartenTyp, visible: bool = False) -> None:
        self.farbe = farbe
        self.typ = typ
        self.visible = visible

    def __repr__(self) -> str:
        return f"Karte({self.farbe},{self.typ},{self.visible})"

    def __str__(self) -> str:
        return f"{self.farbe.blatt} {self.typ.name} ({self.typ.wert})"

    def __eq__(self, other: object) -> bool:
        if type(other) == Karte:
            return self.farbe == other.farbe and self.typ == other.typ
        return False

    def __lt__(self, other) -> bool:
        if self.farbe == other.farbe:
            return self.typ.value < other.typ.value
        return self.farbe.value < other.farbe.value

    def __le__(self, other) -> bool:
        if self.farbe == other.farbe:
            return self.typ.value <= other.typ.value
        return self.farbe.value <= other.farbe.value

    def __gt__(self, other) -> bool:
        if self.farbe == other.farbe:
            return self.typ.value > other.typ.value
        return self.farbe.value > other.farbe.value

    def __ge__(self, other) -> bool:
        if self.farbe == other.farbe:
            return self.typ.value >= other.typ.value
        return self.farbe.value >= other.farbe.value

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def aufgedeckt(self) -> bool:
        return self.visible

    def aufdecken(self):
        self.visible = True
        return self

    def zudecken(self):
        self.visible = False
        return self


class Stapel(object):
    def __init__(self, karten: list[Karte] = [], ablage: bool = True) -> None:
        self.ablage = ablage
        self.karten = karten.copy()

    def __str__(self) -> str:
        return ", ".join([str(k) for k in self.karten])

    def top(self) -> Karte:
        return self.karten[-1] if len(self.karten) > 0 else None

    def aufdecken(self):
        k = self.top()
        if k:
            k.aufdecken()

    def ziehen(self) -> Karte:
        if len(self.karten) > 0:
            k = self.karten.pop()
            return k
        return None

    def anlegen(self, karte: Karte) -> None:
        if not self.anlegbar(karte):
            raise ValueError(
                f"Karte {karte} kann nicht auf dem Stapel {self} abgelegt werden!")
        self.karten.append(karte)

    def anlegbar(self, karte) -> bool:
        return self.ablage

    def shuffle(self):
        shuffle(self.karten)
        return self

    def leer(self) -> bool:
        return len(self.karten) == 0

class AblageStapel(Stapel):
    def __init__(self, farbe: Farbe, karten: list[Karte] = []):
        Stapel.__init__(self, karten)
        self.farbe = farbe

    def __repr__(self) -> str:
        return f"AblageStapel({repr(self.farbe)}, {repr(self.karten)})"

    def __str__(self) -> str:
        return f"AblageStapel({self.farbe.name}, {self.karten[-1] if len(self.karten) > 0 else []})"

    def anlegbar(self, karte) -> bool:
        """
        :karte Karte: prüft ob karte auf dem Stapel abgelegt werden kann
        """
        if karte.farbe != self.farbe:
            return False
        if len(self.karten) <= 0:
            nextKarte = Karte(farbe=self.farbe, typ=KartenTyp.AS)
        elif self.karten[-1].typ.value >= len(list(KartenTyp)):
            return False
        else:
            next_idx = self.karten[-1].typ.value
            nextKarte = Karte(farbe=self.farbe, typ=list(KartenTyp)[next_idx])
        return karte == nextKarte


class AnlageStapel(Stapel):
    def __init__(self, karten: list[Karte] = []):
        Stapel.__init__(self, karten)

    def anlegbar(self, karte) -> bool:
        if len(self.karten) <= 0:
            if karte.typ != KartenTyp.KOENIG:
                return False
        else:
            oberste_karte = self.karten[-1]
            if oberste_karte.farbe.farbe == karte.farbe.farbe:
                return False
            elif karte.typ.value >= oberste_karte.typ.value or karte.typ.value < oberste_karte.typ.value-1:
                return False
        return True


if __name__ == "__main__":
    for k in [Karte(farbe=Farbe.HERZ, typ=KartenTyp.AS), Karte(farbe=Farbe.KREUZ, typ=KartenTyp.AS), Karte(farbe=Farbe.PIK, typ=KartenTyp.AS), Karte(farbe=Farbe.KARO, typ=KartenTyp.AS)]:
        print(k)
