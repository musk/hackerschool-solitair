from cards import Deck, Karte

def main():
    '''
    The enty program for the solitair program
    '''
    deck = Deck()
    print(deck)
    print()
    deck.shuffle()
    print(deck)

if __name__=="__main__":
    main()
        
        
 
