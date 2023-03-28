from enum import Enum
from random import shuffle


class Farbe(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, farbe, blatt: str):
        self.farbe = farbe
        self.blatt = blatt

    KARO = "rot", "\u2666"
    HERZ = "rot", "\u2665"
    PIK = "schwarz", "\u2660"
    KREUZ = "schwarz", "\u2663"


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
    BUBE = 10, "B"
    DAME = 10, "D"
    KOENIG = 10, "K"


class Karte(object):
    def __init__(self, farbe: Farbe, typ: KartenTyp, visible: bool = False) -> None:
        self.farbe = farbe
        self.typ = typ
        self.visible = visible

    def __repr__(self) -> str:
        return f"Karte({self.farbe},{self.typ})"

    def __str__(self) -> str:
        return f"{self.farbe.name} {self.typ.name} ({self.typ.wert})"

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

    def print(self) -> str:
        return self.typ.front(self.farbe) if self.visible else self.typ.back()


class Stapel(object):
    def __init__(self, karten: list[Karte] = []) -> None:
        self.karten = karten.copy()

    def __str__(self) -> str:
        return ", ".join([str(k) for k in self.karten])

    def top(self) -> Karte:
        return self.karten[-1] if len(self.karten) > 0 else None

    def shuffle(self):
        shuffle(self.karten)
        return self

    def ziehen(self) -> Karte:
        if len(self.karten) > 0:
            k = self.karten.pop()
            k.aufdecken()
            return k
        return None

    def ablegen(self, karte: Karte) -> None:
        karte.aufdecken()
        self.karten.append(karte)


class AblageStapel(object):
    def __init__(self, farbe: Farbe, karten: list[Karte] = []):
        self.farbe = farbe
        self.karten = karten.copy()

    def __repr__(self) -> str:
        return f"Stapel({repr(self.farbe)}, {repr(self.karten)})"

    def __str__(self) -> str:
        return f"Stapel({self.farbe.name}, {self.karten[-1] if len(self.karten) > 0 else []})"

    def top(self) -> Karte:
        return self.karten[-1] if len(self.karten) > 0 else None

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
            nextKarte = Karte(farbe=self.farbe, typ=KartenTyp.AS)
        elif self.karten[-1].typ.value >= len(list(KartenTyp)):
            return False
        else:
            next_idx = self.karten[-1].typ.value
            nextKarte = Karte(farbe=self.farbe, typ=list(KartenTyp)[next_idx])
        return karte == nextKarte


class AnlageStapel(object):
    def __init__(self, karten: list[Karte] = []):
        self.karten = karten.copy()

    def top(self) -> Karte:
        return self.karten[-1] if len(self.karten) > 0 else None

    def anlegen(self, karte: Karte) -> None:
        if len(self.karten) <= 0:
            if karte.typ != KartenTyp.KOENIG:
                raise ValueError(
                    f"Die Karte {karte} kann nicht an einen leeren Stapel angelegt werden!")
        else:
            oberste_karte = self.karten[-1]
            if oberste_karte.farbe.farbe == karte.farbe.farbe:
                raise ValueError(
                    f"Gleichfarbige Karte {karte} kann nicht angelegt werden! Sie hat die selbe farbe wie die oberste {oberste_karte}!")
            if karte.typ.value >= oberste_karte.typ.value or karte.typ.value < oberste_karte.typ.value-1:
                raise ValueError(
                    f"Karte {karte} kann nicht abgelegt werden! Sie folgt nicht auf die oberste Karte {oberste_karte} auf dem Stapel!")
        self.karten.append(karte)


if __name__ == "__main__":
    for k in [Karte(farbe=Farbe.HERZ, typ=KartenTyp.AS), Karte(farbe=Farbe.KREUZ, typ=KartenTyp.AS), Karte(farbe=Farbe.PIK, typ=KartenTyp.AS), Karte(farbe=Farbe.KARO, typ=KartenTyp.AS)]:
        print(k)
