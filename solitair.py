from cards import Stapel, Karte

def main():
    '''
    The enty program for the solitair program
    '''
    deck = Stapel()
    print(deck)
    print()
    deck.shuffle()
    print(deck)

if __name__=="__main__":
    main()
        
        
 
