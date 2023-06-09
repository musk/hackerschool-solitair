from enum import Enum
from random import shuffle


class Constants(Enum):
    """
    Definiert Konstanten die im Programm genutzt werden
    """
    ROT = 0
    SCHWARZ = 1


class Farbe(Enum):
    """
    Enum um die Spielkartenfarben zu beschreiben. 
    Jeder Enum beinhaltet ob die Karte ROT oder SCHWARZ
    und das Unicodesymbol für die Darstellung.
    """
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
    """
    Enum für die Kartenwerte in Anlagereihenfolge.
    Jeder Enum beinhaltet das Symbol für die Darstellung.
    """
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, blatt: str):
        self.blatt = blatt

    AS = "A"
    ZWEI = "2"
    DREI = "3"
    VIER = "4"
    FUENF = "5"
    SECHS = "6"
    SIEBEN = "7"
    ACHT = "8"
    NEUN = "9"
    ZEHN = "10"
    BUBE = "B"
    DAME = "D"
    KOENIG = "K"


class Karte(object):
    def __init__(self, farbe: Farbe, typ: KartenTyp, visible: bool = False) -> None:
        """
        Erstellt eine Spielkarte mit der angegebenen Frabe und dem angegebenen Kartentyp 
        und ob sie offen oder zugedeckt ist

        farbe - `Farbe` die Farbe der Karte 
        typ - `KartenTyp` der Wert der Karte
        visible - `bool` Ob die Karte offen oder zugedeckt ist
        """
        self.farbe = farbe
        self.typ = typ
        self.visible = visible

    def __repr__(self) -> str:
        """
        strukturelle Darstellung der Klasse
        """
        return f"Karte({self.farbe},{self.typ},{self.visible})"

    def __str__(self) -> str:
        """
        textuelle Darstellung der Karte 
        """
        return f"{'' if self.visible else '-'}{self.farbe.blatt}{self.typ.blatt}"

    def __eq__(self, other: object) -> bool:
        """
        Gibt `True` zurück wenn diese Karte gleich ist wie 
        die Karte `other` ansonsten `False.` 
        Zwei Karten gelten als gleich wenn sie beide vom Type Karte sind 
        und die gleiche Farbe wie auch den gleichen Wert haben.

        other - `object` das Objekt mit dem verglichen wird 
        """
        if type(other) == Karte:
            return self.farbe == other.farbe and self.typ == other.typ
        return False

    def __lt__(self, other: object) -> bool:
        """
        Gibt `True` zurück wenn der Farbwert und Wert dieser Karte Kleiner ist als 
        die der Karte `other` ansonsten `False.`

        other - `object` das Objekt mit dem verglichen wird
        """
        if self.farbe == other.farbe:
            return self.typ.value < other.typ.value
        return self.farbe.value < other.farbe.value

    def __le__(self, other: object) -> bool:
        """
        Gibt `True` zurück wenn der Farbwert und Wert dieser Karte kleiner oder gleich 
        ist als die der Karte `other` ansonsten `False.`

        other - `object` das Objekt mit dem verglichen wird
        """
        if self.farbe == other.farbe:
            return self.typ.value <= other.typ.value
        return self.farbe.value <= other.farbe.value

    def __gt__(self, other: object) -> bool:
        """
        Gibt `True` zurück wenn der Farbwert und Wert dieser Karte größer ist als 
        die der Karte `other` ansonsten `False.`

        other - `object` das Objekt mit dem verglichen wird
        """
        if self.farbe == other.farbe:
            return self.typ.value > other.typ.value
        return self.farbe.value > other.farbe.value

    def __ge__(self, other: object) -> bool:
        """
        Gibt `True` zurück wenn der Farbwert und Wert dieser Karte größer oder gleich 
        ist als die der Karte `other` ansonsten `False.`

        other - `object` das Objekt mit dem verglichen wird
        """
        if self.farbe == other.farbe:
            return self.typ.value >= other.typ.value
        return self.farbe.value >= other.farbe.value

    def __ne__(self, other: object) -> bool:
        """
        Gibt an ob diese Karte ungleich Karte `other` ist.
        Diese Methode ist equivalent mit not self.__eq__(other)

        other - `object` das Objekt mit dem verglichen wird
        """
        return not self.__eq__(other)

    def aufgedeckt(self) -> bool:
        """
        Gibt `True` zurück wenn diese Karte sichtbar, offen gelegt ist,
        ansonsten `False`
        """
        return self.visible

    def aufdecken(self):
        """
        Deckt diese Karte auf
        """
        self.visible = True
        return self

    def zudecken(self):
        """
        Deckt diese Karte zu
        """
        self.visible = False
        return self


class Stapel(object):
    def __init__(self, karten: list[Karte] = []):
        """
        Erzeugt einen Kartenstapel bestehend aus den angegebenen Karten `karten`. 

        karten - `list[Karte]` die Karten auf dem Stapel. 
                 Default: []
        """
        self.karten = karten.copy()
    def _karten_str(self) -> str:
        return f"[{','.join([str(k) for k in self.karten])}]"
    
    def __str__(self) -> str:
        """
        textuelle Darstellung dieses Stapels
        """
        return f"Stapel({self._karten_str()})"

    def __repr__(self) -> str:
        return f"Stapel({repr(self.karten)})"

    def __eq__(self, other: object) -> bool:
        if type(other) == Stapel:
            return other.karten == self.karten
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def top(self) -> Karte:
        """
        Gibt die oberste Karte oder `None` zurück sollte der Stapel leer sein.
        """
        return self.karten[-1] if len(self.karten) > 0 else None

    def aufdecken(self):
        """
        Deckt die oberste Karte des Stapels auf, falls der Stapel nicht leer ist. 
        """
        k = self.top()
        if k:
            k.aufdecken()

    def ziehen(self) -> Karte:
        """
        Entfernt die oberste Karte vom Stapel und gibt sie zurück. Wenn der Stapel 
        leer ist wird `None` zurück gegeben. 
        """
        if len(self.karten) > 0:
            k = self.karten.pop()
            return k
        return None

    def anlegen(self, karte: Karte) -> None:
        """
        Legt Karte `karte` an diesen Stapel an wenn `self.anlegbar(karte)` `True` zurück gibt
        ansonsten wird ein `ValueError` geschmissen. 

        karte - `Karte` die Karte die angelegt wird 
        """
        if not self.anlegbar(karte):
            raise ValueError(
                f"Karte {karte} kann nicht auf dem Stapel {self} abgelegt werden!")
        self.karten.append(karte)

    def anlegbar(self, karte: Karte) -> bool:
        """
        Gibt `True` zurück wenn Karte `karte` an diesen Stapel angelegt werden kann 
        ansonsten `False`.

        karte - `Karte` die zu prüfende Karte
        """
        return True

    def shuffle(self):
        """
        Mischt diesen Stapel.
        Gibt den Stapel selbst zurück.
        """
        shuffle(self.karten)
        return self

    def leer(self) -> bool:
        """
        Gibt `True` zurück wenn der Stapel leer ist ansonsten `False`
        """
        return len(self.karten) == 0

    def karten_anzahl(self) -> int:
        """
        Gibt die Anzahl der Karten auf dem Stapel als `int` zurück.
        """
        return len(self.karten)


class AblageStapel(Stapel):
    def __init__(self, farbe: Farbe, karten: list[Karte] = []):
        super().__init__(karten)
        self.farbe = farbe

    def __repr__(self) -> str:
        return f"AblageStapel({repr(self.farbe)},{repr(self.karten)})"

    def __str__(self) -> str:
        return f"AblageStapel({self.farbe.blatt},{self._karten_str()})"

    def __eq__(self, other: object) -> bool:
        if type(other) == AblageStapel:
            return self.farbe == other.farbe and self.karten == other.karten
        return False

    def anlegbar(self, karte) -> bool:
        """
        Prüft ob die Karte `karte` auf diesem AblageStapel abgelegt werden kann. 
        Gibt `True` zurück wenn
        * die Karte hat die selbe Farbe wie der AblageStapel
        * der Wert der Karte passt nach der Reihenfolge As,2,3,4,5,6,7,8,9,10,Bube,Dame und König als nächstes auf den Stapel. 
          Das As kann auf einen leeren Stapel abgelegt werden.
        ansonsten `False`

        karte - `Karte` die Karte die geprüft wird.
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

    def komplett(self) -> bool:
        """
        Gibt `True` zurück wenn der AblageStapel komplett ist ansonsten `False`
        """
        return len(self.karten) == len(list(KartenTyp))


class AnlageStapel(Stapel):
    def __init__(self, karten: list[Karte] = []):
        super().__init__(karten)

    def __eq__(self, other: object) -> bool:
        if type(other) == AnlageStapel:
            return self.karten == other.karten
        return False

    def __str__(self) -> str:
        return f"AnlageStapel({self._karten_str()})"

    def __repr__(self) -> str:
        return f"AnlageStapel({repr(self.karten)})"

    def anlegbar(self, karte) -> bool:
        """
        Gibt `True` zurück wenn Karte `karte` die Bedinungen erfüllt:
        * `karte` ist ein KOENIG und der Stapel ist leer
        * `karte` hat eine andere Farbe (schwarz, rot) als die oberste 
                  Karte und der Wert der Karte ist um eins niedriger als 
                  der Wert der obersten Karte
        ansonsten `False`.

        karte - `Karte` die zuprüfende Karte
        """
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

    def verschieben_nach(self, zu) -> bool:
        """
        Verschiebt die aufgedeckten Karten von diesem Stapel zum Stapel `zu` wenn die Karten anlegbar sind. 
        Zum ermitteln der zu verschiebenden Karten wird folgender Algorithmus verwendet:
            Der Stapel wird von unten nach oben Karte um Karte durchlaufen wenn die Karte aufgedeckt 
            und anlegbar ist werden die Karte und alle folgenden Karten auf den `zu` Stapel verschoben.
            Wird keine Karte gefunden die anlegbar ist werden keine Karten verschoben.
        Gibt `True` zurück wenn Karten verschoben wurden ansonsten `False`.

        zu - `AnlageStapel` auf den die Karten verschoben werden sollen 
        """
        for idx, s in enumerate(self.karten):
            if s.aufgedeckt() and zu.anlegbar(s):
                zuverschieben = self.karten[idx:]
                behalten = self.karten[0:idx].copy()
                zu.karten += zuverschieben
                self.karten = behalten
                self.aufdecken()
                return True
        return False


if __name__ == "__main__":
    """
    Code für Debuggingzwecke
    """
    for k in [Karte(farbe=Farbe.HERZ, typ=KartenTyp.AS), Karte(farbe=Farbe.KREUZ, typ=KartenTyp.AS), Karte(farbe=Farbe.PIK, typ=KartenTyp.AS), Karte(farbe=Farbe.KARO, typ=KartenTyp.AS)]:
        print(k)
