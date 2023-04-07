import unittest
from solitair import Solitair
from cards import AblageStapel, Karte, Farbe, KartenTyp
from copy import deepcopy

class SolitairTest(unittest.TestCase):

    def test_gewonnen(self):
        s = Solitair()
        self.assertFalse(s._gewonnen())
        s.ablagen = [
            AblageStapel(farbe=Farbe.HERZ, karten=[Karte(
                farbe=Farbe.HERZ, typ=t) for t in list(KartenTyp)]),
            AblageStapel(farbe=Farbe.KARO, karten=[Karte(
                farbe=Farbe.KARO, typ=t) for t in list(KartenTyp)]),
            AblageStapel(farbe=Farbe.PIK, karten=[Karte(
                farbe=Farbe.PIK, typ=t) for t in list(KartenTyp)]),
            AblageStapel(farbe=Farbe.KREUZ, karten=[Karte(
                farbe=Farbe.KREUZ, typ=t) for t in list(KartenTyp)])]
        self.assertTrue(s._gewonnen())

    def test_undo_after_last_returns_none(self):
        s1 = Solitair()
        s1._spielstand_sichern(s1._spielstand_erzeugen())
        self.assertEqual(1, len(s1.speicher))
        s1._spielzug_zurueck_nehmen()
        self.assertEqual(0, len(s1.speicher))
        self.assertIsNone(s1._spielzug_zurueck_nehmen())

    def test_undo_on_empty_return_none(self):
        s1 = Solitair()
        self.assertEqual(0, len(s1.speicher))
        self.assertIsNone(s1._letzter_gesicherter_spielstand())
        self.assertIsNone(s1._spielzug_zurueck_nehmen())

    def test_undo_over_max_replaces_first(self):
        s1 = Solitair()
        start = s1.ziehStapel.karten_anzahl()
        for i in range(0, 10):
            s1._spielstand_sichern(s1._spielstand_erzeugen())
            s1.ziehStapel.ziehen()
        self.assertEqual(Solitair.MAX_UNDOS, len(s1.speicher))
        self.assertEqual(start, s1.speicher[0].ziehStapel.karten_anzahl())
        s1.ziehStapel.ziehen()
        s1._spielstand_sichern(s1._spielstand_erzeugen())
        self.assertEqual(Solitair.MAX_UNDOS, len(s1.speicher))
        self.assertEqual(start-1, s1.speicher[0].ziehStapel.karten_anzahl())
        self.assertEqual(start-11, s1.speicher[-1].ziehStapel.karten_anzahl())

    def test_spielstand_wiederherstellen(self):
        def spielzug1():
            for i in range(0, 6):
                k = s1.ziehStapel.ziehen()
                s1.anlageStapel[i].stapel.karten.pop()
                s1.ablageStapel.anlegen(k)
            for i in range(0, 4):
                s1.ablagen[i].karten = [
                    Karte(farbe=s1.ablagen[i].farbe, typ=KartenTyp.AS)]

        def spielzug2():
            for i in range(0, 4):
                s1.ablagen[i].karten.append(
                    Karte(farbe=s1.ablagen[i].farbe, typ=KartenTyp.ZWEI))

        s1 = Solitair()
        anlagen = [deepcopy(s.stapel) for s in s1.anlageStapel]
        ablagen = [deepcopy(a) for a in s1.ablagen]
        ablage = deepcopy(s1.ablageStapel)
        punkte = s1.punkte
        ziehen = deepcopy(s1.ziehStapel)

        sp1 = s1._spielstand_erzeugen()
        s1._spielstand_sichern(sp1)
        spielzug1()
        sp2 = s1._spielstand_erzeugen()
        self.assertNotEqual(sp1, sp2)
        self.assertEqual(1, len(s1.speicher))
        sp3 = s1._spielzug_zurueck_nehmen()
        self.assertEqual(sp1, sp3)
        s1._spielstand_herstellen(sp3)
        self.assertEqual(0, len(s1.speicher))

        self.assertEqual(anlagen, [s.stapel for s in s1.anlageStapel])
        self.assertEqual(ablagen, s1.ablagen)
        self.assertEqual(ablage, s1.ablageStapel)
        self.assertEqual(punkte, s1.punkte)
        self.assertEqual(ziehen, s1.ziehStapel)

        s1._spielstand_sichern(s1._spielstand_erzeugen())
        spielzug1()
        s1._spielstand_sichern(s1._spielstand_erzeugen())
        spielzug2()
        s1._spielzug_zurueck_nehmen()
        sp4 = s1._spielzug_zurueck_nehmen()
        s1._spielstand_herstellen(sp4)

        self.assertEqual(anlagen, [s.stapel for s in s1.anlageStapel])
        self.assertEqual(ablagen, s1.ablagen)
        self.assertEqual(ablage, s1.ablageStapel)
        self.assertEqual(punkte, s1.punkte)
        self.assertEqual(ziehen, s1.ziehStapel)


if __name__ == "__main__":
    unittest.main()
