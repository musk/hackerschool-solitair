from cards import Karte, Farbe, KartenTyp

class AsciiScreen(object):
    def __init__(self, width=90, height=35):
        self.width = width
        self.height = height
        self.screen = [ " " for x in range(0,width) for y in range(0,height)]
        self.buffer = ""

    def _update_buffer(self)-> str:
        result = ""
        for y in range(self.height):
            for x in range(self.width):
                result += self.screen[self.width*y+x]
            result += "\n"
        self.buffer = result
    
    def write_to_screen(self, text: str, x: int=0, y: int=0):
        # TODO check that x y are within limits
        # initialize start coordinates
        _x = x
        _y = y
        # split text into lines
        lines = text.splitlines()
        for line in lines:
            # go character by character
            for ch in line:
                if self.width*_y+_x < len(self.screen):
                    self.screen[self.width*_y+_x] = ch
                _x+=1                
            _x = x
            _y +=1
            if _y >= self.height:
                # stop if we have reached bottom of screen
                break
            
        self._update_buffer()

    def print(self):
        print(self.buffer)

class AsciiKarte(object):
    @classmethod
    def width(self)->int:
        return 10
    
    @classmethod
    def height(self) -> int:
        return 5
    
    @classmethod
    def front(self, karte: Karte) -> str:
        typ = karte.typ.blatt
        farbe = karte.farbe.blatt
        return """┌────────┐
│ {0}    {1} │
│        │
│        │
│ {1}    {0} │
└────────┘""".format(typ, farbe)
    
    @classmethod
    def back(self) -> str:
        return """┌────────┐
│▒▒▒▒▒▒▒▒│
│▒▒▒▒▒▒▒▒│
│▒▒▒▒▒▒▒▒│
│▒▒▒▒▒▒▒▒│
└────────┘
"""


if __name__ == "__main__":
    screen = AsciiScreen(height=7, width=22)
    herz5 =AsciiKarte.front(Karte(typ=KartenTyp.FUENF, farbe=Farbe.HERZ))
    screen.write_to_screen(herz5, 0, 0)
    karo5 = AsciiKarte.front(Karte(typ=KartenTyp.FUENF, farbe=Farbe.KARO))
    screen.write_to_screen(karo5, 10, 0)
    # with open(file="spielfeld.txt", mode="r") as f:
    #     txt="".join(f.readlines())
    #     screen.write_to_screen(txt)
    # screen.write_to_screen("Hello what do you want to do? ", 0,28)
    screen.print()
