import unittest
from cards import AblageStapel, Farbe, Karte, KartenTyp


class TestKarte(unittest.TestCase):
    def test_equality(self):
        left = [Karte(farbe=f, typ=t) for f in list(Farbe)
                for t in list(KartenTyp)]
        right = [Karte(farbe=f, typ=t) for f in list(Farbe)
                 for t in list(KartenTyp)]
        for (l, r) in zip(left, right):
            with self.subTest(l=l, r=r):
                self.assertEqual(l, r)
                self.assertEqual(r, l)


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


if __name__ == "__main__":
    unittest.main()
