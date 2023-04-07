from __future__ import annotations
from cards import Farbe, Karte, KartenTyp, AblageStapel, AnlageStapel, Stapel
from ascii import AsciiStapel
from copy import deepcopy
from json import dump, load


class SpielstandDeSerializer(object):

    kartentyp_lookup = {t.blatt: t for t in list(KartenTyp)}
    farbstr_lookup = {Farbe.HERZ: "h", Farbe.KARO: "ka",
                      Farbe.KREUZ: "kr", Farbe.PIK: "p"}
    farb_lookup = {"h": Farbe.HERZ, "p": Farbe.PIK,
                   "ka": Farbe.KARO, "kr": Farbe.KREUZ}

    def serialize(self, spielstand: Spielstand) -> dict[str:str]:
        res = {}
        res["anlagen"] = self._anlagen_schreiben(spielstand.anlageStapel)
        res["ablagen"] = self._ablagen_schreiben(spielstand.ablagen)
        res["ablage"] = self._karten_schreiben(spielstand.ablageStapel.karten)
        res["punkte"] = spielstand.punkte
        return res

    def deserialize(self, data: dict[str:str]) -> Spielstand:
        s = Spielstand(
            ablagen=self._ablagen_lesen(data["ablagen"]),
            anlageStapel=self._anlagen_lesen(data["anlagen"]),
            ablageStapel=Stapel(self._karten_lesen(data["ablage"])),
            ziehStapel=Stapel(karten=[Karte(col, type) for col in list(Farbe)
                                      for type in list(KartenTyp)]),
            punkte=int(data["punkte"]))
        for a in s.anlageStapel:
            self._karten_vom_ziehstapel_entfernen(
                a.karten, s.ziehStapel)
        for a in s.ablagen:
            self._karten_vom_ziehstapel_entfernen(a.karten, s.ziehStapel)
        self._karten_vom_ziehstapel_entfernen(
            s.ablageStapel.karten, s.ziehStapel)
        return s

    def _karten_vom_ziehstapel_entfernen(self, karten: list[Karte], zieh: Stapel):
        for k in karten:
            try:
                zieh.karten.remove(k)
            except:
                raise ValueError(
                    f"Karte {k} ist nicht mehr im Ziehstapel wahrscheinlich doppelt vergeben!")

    def _karten_schreiben(self, karten: list[Karte]) -> str:
        return ",".join(
            [f"{'' if k.visible else '-'}{SpielstandDeSerializer.farbstr_lookup[k.farbe]}:{k.typ.blatt.lower()}" for k in karten]
        )

    def _kartentyp_lesen(self, data: str) -> KartenTyp:
        try:
            return SpielstandDeSerializer.kartentyp_lookup[data.upper()]
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
                    if farbStr in SpielstandDeSerializer.farb_lookup:
                        farbe = SpielstandDeSerializer.farb_lookup[farbStr]
                    else:
                        raise ValueError(
                            f"Unbekannte Farbe {farbStr}! Erlaubt kr,p,h,ka.")

                    typ = self._kartentyp_lesen(typStr)

                    ret.append(Karte(farbe, typ, aufgedeckt))
        return ret

    def _anlagen_schreiben(self, anlagen: list[AnlageStapel]) -> dict[str, str]:
        return {str(idx): self._karten_schreiben(s.karten) for idx, s in enumerate(anlagen)}

    def _anlagen_lesen(self, anlagen: dict[str, str]) -> list[AnlageStapel]:
        res = []
        for k, v in anlagen.items():
            if int(k) < 0 or int(k) > 6:
                raise ValueError(
                    "Anlagestapel index muss im Interval [0,6] liegen!")
            res.insert(int(k), AnlageStapel(self._karten_lesen(v)))
        return res

    def _ablagen_schreiben(self, ablagen: list[AblageStapel]) -> dict[str:str]:
        return {SpielstandDeSerializer.farbstr_lookup[a.farbe]: ",".join([k.typ.blatt.lower() for k in a.karten]) for a in ablagen}

    def _ablagen_lesen(self, ablage: dict[str:str]) -> list[AblageStapel]:
        res = []
        for k, v in ablage.items():
            if k in SpielstandDeSerializer.farb_lookup:
                farbe = SpielstandDeSerializer.farb_lookup[k]
                res.append(AblageStapel(farbe, [
                    Karte(farbe, self._kartentyp_lesen(s)) for s in v.split(",") if len(v) > 0]))
            else:
                raise ValueError(f"Illegale ablage definition {k}!")
        return res


class Spielstand(object):
    """
    Speichert den aktuellen Spielstand eines Solitairspiels
    """
    ID_GEN = 0
    SD = SpielstandDeSerializer()

    @classmethod
    def _gen_id(self) -> int:
        Spielstand.ID_GEN += 1
        return Spielstand.ID_GEN

    def __init__(self, anlageStapel: list[AnlageStapel], ziehStapel: Stapel, ablageStapel: Stapel, ablagen: list[AblageStapel], punkte: int) -> None:
        self.ablagen = deepcopy(ablagen)
        self.anlageStapel = deepcopy(anlageStapel)
        self.ablageStapel = deepcopy(ablageStapel)
        self.ziehStapel = deepcopy(ziehStapel)
        self.punkte = punkte
        self.id = Spielstand._gen_id()

    def __eq__(self, other: object) -> bool:
        if type(other) == Spielstand:
            return (self.ablagen == other.ablagen and
                    self.anlageStapel == other.anlageStapel and
                    self.ablageStapel == other.ablageStapel and
                    self.ziehStapel == other.ziehStapel and
                    self.punkte == other.punkte)
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"Sp:{self.id}({','.join([str(a) for a in self.ablagen])},{','.join([str(a) for a in self.anlageStapel])},{str(self.ablageStapel)},{str(self.ziehStapel)},{str(self.punkte)})"

    def __repr__(self) -> str:
        return f"Spielstand({repr(self.ablagen)},{repr(self.anlageStapel)},{repr(self.ablageStapel)},{repr(self.ziehStapel)},{repr(self.punkte)})"

    def speichern(self, dateiName: str):
        with open(file=dateiName, mode="w", encoding="utf-8") as f:
            dump(Spielstand.SD.serialize(self), f,
                 sort_keys=True, ensure_ascii=True)

    def laden(self, dateiName: str) -> None:
        with open(file=dateiName, mode="r", encoding="utf-8") as f:
            sp: Spielstand = Spielstand.SD.deserialize(load(f))
            self.ablagen = sp.ablagen
            self.anlageStapel = sp.anlageStapel
            self.ablageStapel = sp.ablageStapel
            self.ziehStapel = sp.ziehStapel
            self.punkte = sp.punkte


if __name__ == "__main__":
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
    spielstand = Spielstand(anlageStapel=[
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

    dateiName = "spielstand.save.json"
    spielstand.speichern(dateiName)
    spielstand.laden(dateiName)
