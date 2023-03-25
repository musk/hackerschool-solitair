from enum import Enum
from random import shuffle


class Farbe(Enum):
    PIK = 1
    KREUZ = 2
    HERZ = 3
    KARO = 4


class KartenTyp(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, wert):
        self.wert = wert

    ZWEI = 2
    DREI = 3
    VIER = 4
    FUENF = 5
    SECHS = 6
    SIEBEN = 7
    ACHT = 8
    NEUN = 9
    BUBE = 10
    DAME = 10
    KOENIG = 10
    AS = 11


class Karte(object):
    def __init__(self, farbe: Farbe, typ: KartenTyp) -> None:
        self.farbe = farbe
        self.typ = typ

    def __repr__(self) -> str:
        return f"Karte({self.farbe},{self.typ})"

    def __str__(self) -> str:
        return f"{self.farbe.name} {self.typ.name} ({self.typ.wert})"

    def __eq__(self, other: object) -> bool:
        if type(other) == Karte:
            return self.farbe == other.farbe and self.typ == other.typ
        return False


class Deck(object):
    def __init__(self) -> None:
        self.karten = [Karte(col, type) for col in list(Farbe)
                       for type in list(KartenTyp)]

    def __str__(self) -> str:
        return ", ".join([str(k) for k in self.karten])

    def shuffle(self):
        shuffle(self.karten)
        return self


class AblageStapel(object):
    def __init__(self, farbe: Farbe, karten: list[Karte] = []):
        self.farbe = farbe
        self.karten = karten

    def __repr__(self) -> str:
        return f"Stapel({repr(self.farbe)}, {repr(self.karten)})"

    def __str__(self) -> str:
        return f"Stapel({self.farbe.name}, {self.karten[-1] if len(self.karten) > 0 else []})"

    def ablegen(self, karte: Karte) -> None:
        if karte.farbe != self.farbe:
            raise ValueError(
                f"Karte {karte} kann nicht auf dem Stapel {self.farbe} abgelegt werden!")
        elif not self.ablegbar(karte):
            raise ValueError(
                f"Die Karte {karte} kann nicht als nächstes auf dem Stapel {self} abgelegt werden!")
        self.karten.append(karte)

    def ablegbar(self, karte) -> bool:
        """
        :karte Karte: prüft ob karte auf dem Stapel abgelegt werden kann
        """
        if len(self.karten) <= 0:
            nextKarte = Karte(farbe=self.farbe, typ=KartenTyp.ZWEI)
        elif self.karten[-1].typ.value >= len(list(KartenTyp)):
            return False
        else:
            next_idx = self.karten[-1].typ.value
            nextKarte = Karte(farbe=self.farbe, typ=list(KartenTyp)[next_idx])
        return karte == nextKarte
