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
    def test_nicht_ablegbar(self):
        ablage = AblageStapel(farbe=Farbe.HERZ)
        k = Karte(farbe=Farbe.KARO, typ=KartenTyp.AS, visible=True)
        self.assertFalse(ablage.ablegbar(k))
        self.assertRaises(ValueError, lambda: ablage.ablegen(k))

    def test_ablegen(self):
        for f in list(Farbe):
            karten = [Karte(farbe=f, typ=t) for t in list(KartenTyp)]
            for idx, k in enumerate(karten):
                stapel = AblageStapel(f, karten[0:idx])
                with self.subTest(stapel=stapel, karte=k):
                    stapel.ablegen(k)

    def test_ablegbar(self):
        for f in list(Farbe):
            stapel = AblageStapel(f)
            karten = [Karte(farbe=f, typ=t) for t in list(KartenTyp)]
            for idx, k in enumerate(karten):
                with self.subTest(k=k):
                    stapel.karten = karten[0:idx].copy()
                    self.assertTrue(stapel.ablegbar(k))


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
