from spielstand import Spielstand, SpielstandDeSerializer
from cards import AblageStapel, AnlageStapel, Stapel, Karte, KartenTyp, Farbe
from copy import deepcopy
from random import shuffle
import unittest


class SpielstandDeSerializerTest(unittest.TestCase):

    def setUp(self) -> None:
        gezogeneKarten = [Karte(Farbe.KREUZ, KartenTyp.BUBE),
                          Karte(Farbe.KARO, KartenTyp.DAME),
                          Karte(Farbe.PIK, KartenTyp.BUBE),
                          Karte(Farbe.HERZ, KartenTyp.ZEHN),
                          Karte(Farbe.KREUZ, KartenTyp.ZWEI),
                          Karte(Farbe.HERZ, KartenTyp.SECHS),
                          Karte(Farbe.KARO, KartenTyp.KOENIG),
                          Karte(Farbe.PIK, KartenTyp.DAME),
                          Karte(Farbe.HERZ, KartenTyp.BUBE),
                          Karte(Farbe.PIK, KartenTyp.ZEHN),
                          Karte(Farbe.HERZ, KartenTyp.FUENF),
                          Karte(Farbe.KREUZ, KartenTyp.DREI),
                          Karte(Farbe.HERZ, KartenTyp.AS),
                          Karte(Farbe.HERZ, KartenTyp.ZWEI),
                          Karte(Farbe.HERZ, KartenTyp.DREI),
                          Karte(Farbe.HERZ, KartenTyp.VIER),
                          Karte(Farbe.KARO, KartenTyp.AS),
                          Karte(Farbe.KARO, KartenTyp.ZWEI),
                          Karte(Farbe.PIK, KartenTyp.AS)]
        alleKarten = [Karte(f, t) for f in list(Farbe)
                      for t in list(KartenTyp)]
        ziehKarten = [k for k in alleKarten if k not in gezogeneKarten]
        self.spielstand = Spielstand(anlageStapel=[
            AnlageStapel(karten=[
                Karte(Farbe.KREUZ,
                      KartenTyp.BUBE, visible=True)
            ]),
            AnlageStapel(),
            AnlageStapel(karten=[
                Karte(Farbe.KARO, KartenTyp.DAME,
                      visible=True),
                Karte(Farbe.PIK, KartenTyp.BUBE,
                      visible=True),
                Karte(Farbe.HERZ, KartenTyp.ZEHN,
                      visible=True)
            ]),
            AnlageStapel(karten=[
                Karte(Farbe.KREUZ, KartenTyp.ZWEI),
                Karte(Farbe.HERZ, KartenTyp.SECHS, visible=True)
            ]),
            AnlageStapel(karten=[
                Karte(Farbe.KARO,
                      KartenTyp.KOENIG, visible=True),
                Karte(Farbe.PIK, KartenTyp.DAME,
                      visible=True),
                Karte(Farbe.HERZ, KartenTyp.BUBE,
                      visible=True),
                Karte(Farbe.PIK, KartenTyp.ZEHN,
                      visible=True),
            ]),
            AnlageStapel(),
            AnlageStapel()],
            ziehStapel=Stapel(karten=ziehKarten),
            ablageStapel=Stapel(karten=[
                Karte(Farbe.HERZ, KartenTyp.FUENF,
                      visible=True),
                Karte(Farbe.KREUZ, KartenTyp.DREI,
                      visible=True),
            ]),
            ablagen=[
            AblageStapel(Farbe.HERZ, karten=[
                Karte(Farbe.HERZ, KartenTyp.AS,
                      visible=True),
                Karte(Farbe.HERZ, KartenTyp.ZWEI,
                      visible=True),
                Karte(Farbe.HERZ, KartenTyp.DREI,
                      visible=True),
                Karte(Farbe.HERZ, KartenTyp.VIER,
                      visible=True)
            ]),
            AblageStapel(Farbe.KARO, karten=[
                Karte(Farbe.KARO, KartenTyp.AS,
                      visible=True),
                Karte(Farbe.KARO, KartenTyp.ZWEI,
                      visible=True)
            ]),
            AblageStapel(Farbe.PIK, karten=[
                Karte(Farbe.PIK, KartenTyp.AS,
                      visible=True)
            ]),
            AblageStapel(Farbe.KREUZ, karten=[])],
            punkte=66)
        self.spielstandDict = {
            "ablagen": {
                "h": "a,2,3,4",
                "ka": "a,2",
                "p": "a",
                "kr": "",
            },
            "anlagen": {
                "0": "kr:B",
                "1": "",
                "2": "ka:d,p:b,h:10",
                "3": "-kr:2,h:6",
                "4": "ka:k,p:d,h:b,p:10",
                "5": "",
                "6": ""
            },
            "ablage": "h:5,kr:3",
            "punkte": 66
        }

    def test_serialize_deserialize(self):
        sd = SpielstandDeSerializer()
        sp2 = sd.deserialize(sd.serialize(self.spielstand))
        self.assertEqual(self.spielstand, sp2)

    def test_deserialize_serialize(self):
        sd = SpielstandDeSerializer()
        sd.serialize(sd.deserialize(self.spielstandDict))

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

    @unittest.skip
    def test_save(self):
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
        s2 = Spielstand(anlageStapel=anlagen,
                        ziehStapel=zieh,
                        ablageStapel=ablage,
                        ablagen=ablagen,
                        punkte=10)
        test = s2.speichern()

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
