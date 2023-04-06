import unittest
from cards import Stapel, AblageStapel, Farbe, Karte, KartenTyp, AnlageStapel


class TestKarte(unittest.TestCase):
    def test_sorting_ops(self):
        karten = [Karte(farbe=f, typ=t) for f in list(Farbe)
                  for t in list(KartenTyp)]
        for idx, k in enumerate(karten):
            with self.subTest(idx=idx, karte=k):
                for n, cmp_karte in enumerate(karten):
                    if n < idx:
                        self.assertTrue(expr=cmp_karte < k,
                                        msg=f"{cmp_karte} < {k}")
                        self.assertTrue(expr=k >= cmp_karte,
                                        msg=f"{k} >= {cmp_karte}")
                    elif n > idx:
                        self.assertTrue(expr=cmp_karte > k,
                                        msg=f"{cmp_karte} > {k}")
                        self.assertTrue(expr=k <= cmp_karte,
                                        msg=f"{k} <= {cmp_karte}")
                    else:
                        self.assertEqual(
                            k, cmp_karte, msg=f"{cmp_karte} == {k}")
                        self.assertEqual(
                            cmp_karte, k, msg=f"{k} == {cmp_karte}")

    def test_non_equality(self):
        karten = [Karte(farbe=f, typ=t) for f in list(Farbe)
                  for t in list(KartenTyp)]
        for i1, k1 in enumerate(karten):
            for i2, k2 in enumerate(karten):
                if i1 != i2:
                    self.assertTrue(k1 != k2)
                    self.assertTrue(k2 != k1)

    def test_turn_card(self):
        k = Karte(farbe=Farbe.HERZ, typ=KartenTyp.ACHT)
        k.aufdecken()
        self.assertTrue(k.aufgedeckt())
        k.aufdecken()
        self.assertTrue(k.aufgedeckt())


class TestAblageStapel(unittest.TestCase):
    def test_nicht_anlegbar(self):
        ablage = AblageStapel(farbe=Farbe.HERZ)
        k = Karte(farbe=Farbe.KARO, typ=KartenTyp.AS, visible=True)
        self.assertFalse(ablage.anlegbar(k))
        self.assertRaises(ValueError, lambda: ablage.anlegen(k))

    def test_anlegen(self):
        for f in list(Farbe):
            karten = [Karte(farbe=f, typ=t) for t in list(KartenTyp)]
            for idx, k in enumerate(karten):
                stapel = AblageStapel(f, karten[0:idx])
                with self.subTest(stapel=stapel, karte=k):
                    stapel.anlegen(k)

    def test_anlegbar(self):
        for f in list(Farbe):
            stapel = AblageStapel(f)
            karten = [Karte(farbe=f, typ=t) for t in list(KartenTyp)]
            for idx, k in enumerate(karten):
                with self.subTest(k=k):
                    stapel.karten = karten[0:idx].copy()
                    self.assertTrue(stapel.anlegbar(k))

    def test_komplett(self):
        komplett = [Karte(farbe=Farbe.HERZ, typ=t) for t in list(KartenTyp)]
        k = komplett.pop()
        s = AblageStapel(farbe=Farbe.HERZ, karten=komplett)
        self.assertFalse(s.komplett())
        s.anlegen(k)
        self.assertTrue(s.komplett())

    def test_eq_empty(self):
        s1 = AblageStapel(farbe=Farbe.HERZ)
        s2 = AblageStapel(farbe=Farbe.HERZ)
        self.assertEqual(s1, s2)
        self.assertEqual(s2, s1)

    def test_eq_nonempty(self):
        karten = [Karte(farbe=Farbe.HERZ, typ=t) for t in list(KartenTyp)]
        s1 = AblageStapel(Farbe.PIK, karten)
        s2 = AblageStapel(Farbe.PIK, karten)
        self.assertEqual(s1, s2)
        self.assertEqual(s2, s1)

    def test_ne(self):
        karten = [Karte(farbe=Farbe.KREUZ, typ=t) for t in list(KartenTyp)]
        s1 = AblageStapel(farbe=Farbe.KREUZ, karten=karten)
        s2 = AblageStapel(farbe=Farbe.KREUZ, karten=karten)
        s4 = AblageStapel(farbe=Farbe.HERZ, karten=karten)
        s3 = AblageStapel(farbe=Farbe.KREUZ)
        s4 = AblageStapel(farbe=Farbe.HERZ, karten=karten)
        self.assertEqual(s1, s2)
        s2.ziehen()
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s3, s1)
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s2, s1)
        self.assertNotEqual(s4, s1)
        self.assertNotEqual(s1, s4)


class TestStapel(unittest.TestCase):
    def test_ziehen_von_leerem_stapel(self):
        deck = Stapel()
        deck.karten = []
        self.assertEqual(None, deck.ziehen())

    def test_ziehen(self):
        karten = [Karte(farbe=f, typ=t) for f in list(Farbe)
                  for t in list(KartenTyp)]
        deck = Stapel()
        deck.karten = karten.copy()
        karten.reverse()
        for k in karten:
            self.assertEqual(k, deck.ziehen())

    def test_ablegen_auf_stapel(self):
        s = Stapel()
        k = Karte(farbe=Farbe.HERZ, typ=KartenTyp.ACHT)
        s.anlegen(k)
        self.assertEqual(1, len(s.karten))
        self.assertEqual(k, s.karten[-1])
        s.anlegen(Karte(farbe=Farbe.KARO, typ=KartenTyp.DAME))
        self.assertEqual(2, len(s.karten))

    def test_top(self):
        s = Stapel()
        k1 = Karte(farbe=Farbe.HERZ, typ=KartenTyp.ACHT)
        k2 = Karte(farbe=Farbe.KARO, typ=KartenTyp.ZWEI)
        self.assertEqual(None, s.top())
        s.anlegen(k1)
        self.assertEqual(k1, s.top())
        s.anlegen(k2)
        self.assertEqual(k2, s.top())

    def test_aufdecken_on_empty_stapel(self):
        s = Stapel()
        s.aufdecken()

    def test_aufdecken(self):
        s = Stapel(karten=[Karte(farbe=Farbe.HERZ, typ=KartenTyp.ACHT)])
        self.assertFalse(s.top().aufgedeckt())
        s.aufdecken()
        self.assertTrue(s.top().aufgedeckt())

    def test_eq_empty(self):
        s1 = Stapel()
        s2 = Stapel()
        self.assertEqual(s1, s2)
        self.assertEqual(s2, s1)

    def test_eq_nonempty(self):
        karten = [Karte(farbe=f, typ=t) for f in list(Farbe)
                  for t in list(KartenTyp)]
        s1 = Stapel(karten)
        s2 = Stapel(karten)
        self.assertEqual(s1, s2)
        self.assertEqual(s2, s1)

    def test_ne(self):
        karten = [Karte(farbe=f, typ=t) for f in list(Farbe)
                  for t in list(KartenTyp)]
        s1 = Stapel(karten)
        s2 = Stapel(karten)
        s3 = Stapel()
        self.assertEqual(s1, s2)
        s2.ziehen()
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s3, s1)
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s2, s1)


class TestAnlageStapel(unittest.TestCase):
    def test_koenige_koennen_an_leeren_stapel_angelegt_werden(self):
        erlaubt = [Karte(farbe=f, typ=KartenTyp.KOENIG) for f in list(Farbe)]
        for k in erlaubt:
            stapel = AnlageStapel()
            stapel.anlegen(k)

    def test_nicht_koenige_resultieren_in_value_error_wenn_stapel_leer(self):
        nicht_erlaubt = [Karte(farbe=f, typ=t) for f in list(
            Farbe) for t in list(KartenTyp) if t != KartenTyp.KOENIG]
        for k in nicht_erlaubt:
            stapel = AnlageStapel()
            self.assertRaises(ValueError, lambda: stapel.anlegen(k))

    def test_nicht_aufeinander_folgende_values(self):
        stapel = AnlageStapel()
        stapel.karten = [Karte(farbe=Farbe.HERZ, typ=KartenTyp.FUENF)]
        for k in [Karte(farbe=Farbe.KREUZ, typ=KartenTyp.SECHS), Karte(farbe=Farbe.KREUZ, typ=KartenTyp.DREI)]:
            with self.subTest(karte=k):
                self.assertRaises(ValueError, lambda: stapel.anlegen(k))

    def test_falsche_farbe_anlegen(self):
        stapel = AnlageStapel()
        stapel.anlegen(Karte(farbe=Farbe.KARO, typ=KartenTyp.KOENIG))
        self.assertRaises(ValueError, lambda: stapel.anlegen(
            Karte(farbe=Farbe.HERZ, typ=KartenTyp.DAME)))

    def test_anlegen(self):
        kreuz = self._karten(Farbe.KREUZ)
        pik = self._karten(Farbe.PIK)
        herz = self._karten(Farbe.HERZ)
        karo = self._karten(Farbe.KARO)

        anlageStapel = [AnlageStapel(), AnlageStapel(),
                        AnlageStapel(), AnlageStapel()]
        zum_ablegen = [(kreuz[i], herz[i], pik[i], karo[i])
                       for i in range(0, len(kreuz))]
        idx = 0
        for (kr, he, pi, ka) in zum_ablegen:
            i1 = idx % 4
            anlageStapel[i1].anlegen(kr)
            self._assertOrder(anlageStapel[i1])
            i2 = (idx+1) % 4
            anlageStapel[i2].anlegen(he)
            self._assertOrder(anlageStapel[i2])
            i3 = (idx+2) % 4
            anlageStapel[i3].anlegen(pi)
            self._assertOrder(anlageStapel[i3])
            i4 = (idx+3) % 4
            anlageStapel[i4].anlegen(ka)
            self._assertOrder(anlageStapel[i4])
            idx += 1

    def test_verschieben_auf_leeren_stapel(self):
        behalten = [Karte(farbe=Farbe.HERZ, typ=KartenTyp.VIER),
                    Karte(farbe=Farbe.KARO, typ=KartenTyp.DREI),]
        verschoben = [Karte(farbe=Farbe.PIK, typ=KartenTyp.KOENIG, visible=True),
                      Karte(farbe=Farbe.HERZ, typ=KartenTyp.DAME, visible=True),
                      Karte(farbe=Farbe.KREUZ, typ=KartenTyp.BUBE, visible=True),
                      Karte(farbe=Farbe.KARO, typ=KartenTyp.ZEHN, visible=True),]
        von = AnlageStapel(karten=behalten+verschoben)
        zu = AnlageStapel(karten=[])
        self.assertTrue(von.verschieben_nach(zu))
        self.assertEqual(behalten, von.karten)
        self.assertEqual(verschoben, zu.karten)
        self.assertTrue(von.top().aufgedeckt())

    def test_verschieben_auf_bestehenden_stapel(self):
        behalten = [Karte(farbe=Farbe.HERZ, typ=KartenTyp.VIER),
                    Karte(farbe=Farbe.KARO, typ=KartenTyp.DREI),]
        verschoben = [Karte(farbe=Farbe.PIK, typ=KartenTyp.ACHT, visible=True),
                      Karte(farbe=Farbe.HERZ, typ=KartenTyp.SIEBEN, visible=True),
                      Karte(farbe=Farbe.KREUZ, typ=KartenTyp.SECHS, visible=True),
                      Karte(farbe=Farbe.KARO, typ=KartenTyp.FUENF, visible=True),]
        exist = [Karte(farbe=Farbe.KREUZ, typ=KartenTyp.BUBE, visible=False),
                 Karte(farbe=Farbe.PIK,
                       typ=KartenTyp.AS, visible=False),
                 Karte(farbe=Farbe.PIK, typ=KartenTyp.ZEHN),
                 Karte(farbe=Farbe.HERZ, typ=KartenTyp.NEUN)]
        von = AnlageStapel(karten=behalten+verschoben)
        zu = AnlageStapel(karten=exist)
        self.assertTrue(von.verschieben_nach(zu))
        self.assertEqual(behalten, von.karten)
        self.assertEqual(exist+verschoben, zu.karten)
        self.assertTrue(von.top().aufgedeckt())

    def test_verschieben_partiell_auf_bestehenden_stapel(self):
        behalten = [Karte(farbe=Farbe.HERZ, typ=KartenTyp.VIER),
                    Karte(farbe=Farbe.KARO, typ=KartenTyp.DREI),
                    Karte(farbe=Farbe.PIK, typ=KartenTyp.ACHT, visible=True),
                    Karte(farbe=Farbe.HERZ, typ=KartenTyp.SIEBEN, visible=True)]
        verschoben = [Karte(farbe=Farbe.KREUZ, typ=KartenTyp.SECHS, visible=True),
                      Karte(farbe=Farbe.KARO, typ=KartenTyp.FUENF, visible=True),]
        exist = [Karte(farbe=Farbe.KREUZ, typ=KartenTyp.BUBE, visible=False),
                 Karte(farbe=Farbe.PIK,
                       typ=KartenTyp.AS, visible=False),
                 Karte(farbe=Farbe.PIK, typ=KartenTyp.ZEHN),
                 Karte(farbe=Farbe.HERZ, typ=KartenTyp.NEUN),
                 Karte(farbe=Farbe.KREUZ, typ=KartenTyp.ACHT),
                 Karte(farbe=Farbe.KARO, typ=KartenTyp.SIEBEN)]
        von = AnlageStapel(karten=behalten+verschoben)
        zu = AnlageStapel(karten=exist)
        self.assertTrue(von.verschieben_nach(zu))
        self.assertEqual(behalten, von.karten)
        self.assertEqual(exist+verschoben, zu.karten)
        self.assertTrue(von.top().aufgedeckt())

    def test_verschieben_hinterlaest_leeren_stapel(self):
        behalten = []
        verschoben = [Karte(farbe=Farbe.PIK, typ=KartenTyp.ACHT, visible=True),
                      Karte(farbe=Farbe.HERZ, typ=KartenTyp.SIEBEN, visible=True),
                      Karte(farbe=Farbe.KREUZ, typ=KartenTyp.SECHS, visible=True),
                      Karte(farbe=Farbe.KARO, typ=KartenTyp.FUENF, visible=True),]
        exist = [Karte(farbe=Farbe.KREUZ, typ=KartenTyp.BUBE, visible=False),
                 Karte(farbe=Farbe.PIK,
                       typ=KartenTyp.AS, visible=False),
                 Karte(farbe=Farbe.PIK, typ=KartenTyp.ZEHN),
                 Karte(farbe=Farbe.HERZ, typ=KartenTyp.NEUN)]
        von = AnlageStapel(karten=behalten+verschoben)
        zu = AnlageStapel(karten=exist)
        self.assertTrue(von.verschieben_nach(zu))
        self.assertEqual(behalten, von.karten)
        self.assertEqual(exist+verschoben, zu.karten)
        self.assertTrue(von.leer())

    def test_eq_empty(self):
        s1 = AnlageStapel()
        s2 = AnlageStapel()
        self.assertEqual(s1, s2)
        self.assertEqual(s2, s1)

    def test_eq_nonempty(self):
        karten = [Karte(farbe=f, typ=t) for f in list(Farbe)
                  for t in list(KartenTyp)]
        s1 = AnlageStapel(karten)
        s2 = AnlageStapel(karten)
        self.assertEqual(s1, s2)
        self.assertEqual(s2, s1)

    def test_ne(self):
        karten = [Karte(farbe=f, typ=t) for f in list(Farbe)
                  for t in list(KartenTyp)]
        s1 = AnlageStapel(karten)
        s2 = AnlageStapel(karten)
        s3 = AnlageStapel()
        self.assertEqual(s1, s2)
        s2.ziehen()
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s3, s1)
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s2, s1)

    def _assertOrder(self, stapel: AnlageStapel) -> None:
        prev_farbe = None
        prev_value = -1
        for k in stapel.karten:
            if prev_farbe == None:
                continue
            if prev_farbe == k.farbe.farbe:
                raise AssertionError(
                    f"Vorherige Farbe {prev_farbe} == aktuelle Farbe {k.farbe.farbe}")
            if prev_value >= k.typ.value:
                raise AssertionError(
                    f"Vorherige wert {prev_value} >= aktuellem wert {k.typ.value}")

    def _karten(self, farbe: Farbe) -> list[Karte]:
        return [Karte(farbe=farbe, typ=t) for t in reversed(list(KartenTyp))]


if __name__ == "__main__":
    unittest.main()
