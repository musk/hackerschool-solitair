import enum

class Color(enum.Enum):
    PIK=0
    KREUZ=1
    HERZ=2
    KARO=3

class CardType(enum.Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj
      
    def __init__(self, wert):
        self.wert = wert

    SIEBEN = 7
    ACHT = 8
    NEUN = 9
    BUBE = 10
    DAME = 10
    KOENIG = 10
    AS = 11
    
class Karte(object):
    def __init__(self, color: Color, type: CardType) -> None:
        self.color= color
        self.type = type

    def __str__(self) -> str:
        return f"{self.color.name} {self.type.name} ({self.type.wert})"

class Deck(object):
    def __init__(self) -> None:
        self.karten = [Karte(col, type) for col in list(Color) for type in list(CardType)]
        self._str = ", ".join([str(k) for k in self.karten])

    def __str__(self) -> str:
        return self._str
