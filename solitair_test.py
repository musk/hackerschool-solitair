import unittest
from solitair import Solitair
from cards import AblageStapel, Karte, Farbe, KartenTyp


class SolitairTest(unittest.TestCase):
    def test_gewonnen(self):
        s = Solitair()
        self.assertFalse(s._gewonnen())
        s.ablageHerz = AblageStapel(farbe=Farbe.HERZ, karten=[Karte(
            farbe=Farbe.HERZ, typ=t) for t in list(KartenTyp)])
        s.ablageKaro = AblageStapel(farbe=Farbe.KARO, karten=[Karte(
            farbe=Farbe.KARO, typ=t) for t in list(KartenTyp)])
        s.ablagePik = AblageStapel(farbe=Farbe.PIK, karten=[Karte(
            farbe=Farbe.PIK, typ=t) for t in list(KartenTyp)])
        s.ablageKreuz = AblageStapel(farbe=Farbe.KREUZ, karten=[Karte(
            farbe=Farbe.KREUZ, typ=t) for t in list(KartenTyp)])
        self.assertTrue(s._gewonnen())

    def test_neu_mischen(self):
        s = Solitair()
          


if __name__ == "__main__":
    unittest.main()
