import unittest
from solitair import Solitair, Spielstand
from cards import AblageStapel, Karte, Farbe, KartenTyp, AnlageStapel, Stapel
from ascii import AsciiStapel
from random import shuffle
from copy import deepcopy


class SpielfeldParser(object):

    kartentyp_lookup = {t.blatt: t for t in list(KartenTyp)}

    def setup_spielstand(self, data) -> Solitair:
        s = Solitair()
        s.ablagen = self._ablagen_lesen(data["ablagen"])
        s.anlageStapel = self._anlagen_lesen(data["anlagen"])
        s.ablageStapel = self._ablage_lesen(data["ablage"])
        ziehStapel = Stapel(karten=[Karte(col, type) for col in list(Farbe)
                                    for type in list(KartenTyp)])
        for a in s.anlageStapel:
            self._karten_vom_ziehstapel_entfernen(a.stapel.karten, ziehStapel)
        for a in s.ablagen:
            self._karten_vom_ziehstapel_entfernen(a.karten, ziehStapel)
        self._karten_vom_ziehstapel_entfernen(
            s.ablageStapel.karten, ziehStapel)
        s.ziehStapel = ziehStapel
        return s

    def _karten_vom_ziehstapel_entfernen(self, karten: list[Karte], zieh: Stapel):
        for k in karten:
            try:
                zieh.karten.remove(k)
            except:
                raise ValueError(
                    f"Karte {k} ist nicht mehr im Ziehstapel wahrscheinlich doppelt vergeben!")

    def _kartentyp_lesen(self, data: str) -> KartenTyp:
        try:
            return self.kartentyp_lookup[data.upper()]
        except:
            raise ValueError(
                f"Unbekannter KartenType '{data}'! Erlaubt a,2,3,4,5,6,7,8,9,10,b,d,k.")

    def _karten_lesen(self, anlage: str) -> list[Karte]:
        ret = []
        if len(anlage) > 0:
            karten = anlage.lower().split(",")
            if len(karten) > 0:
                for el in karten:
                    aufgedeckt = True
                    (farbStr, typStr) = el.split(":")
                    if farbStr.startswith("-"):
                        farbStr = farbStr[1:]
                        aufgedeckt = False

                    farbe = None
                    if farbStr == "kr":
                        farbe = Farbe.KREUZ
                    elif farbStr == "ka":
                        farbe = Farbe.KARO
                    elif farbStr == "h":
                        farbe = Farbe.HERZ
                    elif farbStr == "p":
                        farbe = Farbe.PIK
                    else:
                        raise ValueError(
                            f"Unbekannte Farbe {farbStr}! Erlaubt kr,p,h,ka.")

                    typ = self._kartentyp_lesen(typStr)

                    ret.append(Karte(farbe, typ, aufgedeckt))
        return ret

    def _anlagen_lesen(self, anlagen: dict[int, str]) -> list[AsciiStapel]:
        res = []
        for k, v in anlagen.items():
            if k < 0 or k > 6:
                raise ValueError(
                    "Anlagestapel index muss im Interval [0,6] liegen!")
            res.insert(k, AsciiStapel(AnlageStapel(self._karten_lesen(v))))
        return res

    def _ablage_lesen(self, ablage: str) -> AblageStapel:
        return Stapel(self._karten_lesen(ablage))

    def _ablagen_lesen(self, ablage: dict[str:str]) -> list[AblageStapel]:
        res = []
        for k, v in ablage.items():
            if k == "herz":
                res.append(AblageStapel(Farbe.HERZ, [
                           Karte(Farbe.HERZ, self._kartentyp_lesen(s)) for s in v.split(",") if len(v) > 0]))
            elif k == "karo":
                res.append(AblageStapel(Farbe.KARO, [
                           Karte(Farbe.KARO, self._kartentyp_lesen(s)) for s in v.split(",") if len(v) > 0]))
            elif k == "pik":
                res.append(AblageStapel(
                    Farbe.PIK, [Karte(Farbe.PIK, self._kartentyp_lesen(s)) for s in v.split(",") if len(v) > 0]))
            elif k == "kreuz":
                res.append(AblageStapel(Farbe.KREUZ, [
                           Karte(Farbe.KREUZ, self._kartentyp_lesen(s)) for s in v.split(",") if len(v) > 0]))
            else:
                raise ValueError(f"Illegale ablage definition f{k}!")
        return res


class SpielstandTest(unittest.TestCase):
    def _gen_ablage(self, farbe: Farbe, zahl: int = len(list(KartenTyp))) -> AblageStapel:
        karten = [Karte(farbe=farbe, typ=t)
                  for idx, t in enumerate(list(KartenTyp)) if idx < zahl]
        return AblageStapel(farbe, karten)

    def _gen_karten(self, zahl: int) -> list[Karte]:
        ziehen = [Karte(farbe=f, typ=t) for t in list(KartenTyp)
                  for f in list(Farbe)]
        shuffle(ziehen)
        karten = []
        for i in range(0, zahl):
            karten.append(ziehen.pop())
        return karten

    def _gen_anlage(self, zahl: int) -> AnlageStapel:
        return AnlageStapel(karten=self._gen_karten(zahl))

    def _gen_stapel(self, zahl: int) -> Stapel:
        return Stapel(karten=self._gen_karten(zahl))

    def test_eq_empty_spielstand(self):
        s1 = Spielstand(anlageStapel=[], ziehStapel=None,
                        ablageStapel=None, ablagen=[], punkte=0)
        s2 = Spielstand(anlageStapel=[], ziehStapel=None,
                        ablageStapel=None, ablagen=[], punkte=0)
        self.assertEqual(s1, s2)
        self.assertEqual(s2, s1)

    def test_eq_spielstand(self):
        anlagen = [self._gen_anlage(4),
                   self._gen_anlage(5),
                   self._gen_anlage(3),
                   self._gen_anlage(7)]
        zieh = self._gen_stapel(30)
        ablage = self._gen_stapel(5)
        ablagen = [self._gen_ablage(Farbe.HERZ, 4),
                   self._gen_ablage(Farbe.KARO, 7),
                   self._gen_ablage(Farbe.PIK, 2),
                   self._gen_ablage(Farbe.KREUZ, 6)]
        s1 = Spielstand(anlageStapel=deepcopy(anlagen),
                        ziehStapel=deepcopy(zieh),
                        ablageStapel=deepcopy(ablage),
                        ablagen=deepcopy(ablagen),
                        punkte=10)
        s2 = Spielstand(anlageStapel=anlagen,
                        ziehStapel=zieh,
                        ablageStapel=ablage,
                        ablagen=ablagen,
                        punkte=10)

        self.assertEqual(s1, s2)
        self.assertEqual(s2, s1)


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

    def test_undo(self):
        spielstand1 = {
            "ablagen": {
                "herz": "a,2,3,4",
                "karo": "a,2",
                "pik": "a",
                "kreuz": "",
            },
            "anlagen": {
                0: "kr:B",
                1: "",
                2: "ka:d,p:b,h:10",
                3: "-kr:2,-h:6,ka:k,p:d,h:b,p:10",
                4: "",
                5: "",
                6: ""
            },
            "ablage": "h:5,kr:3"
        }
        spielstand2 = {
            "ablagen": {
                "herz": "a,2,3,4",
                "karo": "a,2",
                "pik": "a",
                "kreuz": "",
            },
            "anlagen": {
                0: "kr:B",
                1: "",
                2: "ka:d,p:b,h:10",
                3: "-kr:2,h:6",
                4: "ka:k,p:d,h:b,p:10",
                5: "",
                6: ""
            },
            "ablage": "h:5,kr:3"
        }
        s1: Solitair = SpielfeldParser().setup_spielstand(spielstand1)
        s1._spielstand_sichern(s1._spielstand_erzeugen())
        first = s1._letzter_gesicherter_spielstand()
        self.assertEqual(1, len(s1.speicher))
        von: AnlageStapel = s1.anlageStapel[3].stapel
        zu: AnlageStapel = s1.anlageStapel[4].stapel
        von.verschieben_nach(zu)
        s1._spielstand_sichern(s1._spielstand_erzeugen())
        stand1 = s1._letzter_gesicherter_spielstand()
        self.assertEqual(2, len(s1.speicher))
        stand2 = s1._spielzug_zurueck_nehmen()
        self.assertEqual(1, len(s1.speicher))
        self.assertEqual(stand1, stand2)
        stand3 = s1._spielzug_zurueck_nehmen()
        self.assertEqual(stand3, first)
        self.assertEqual(0, len(s1.speicher))

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
