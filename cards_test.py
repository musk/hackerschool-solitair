import unittest
from cards import Stapel, AblageStapel, Farbe, Karte, KartenTyp


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


class TestAblageStapel(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
