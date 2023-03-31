# Solitair
This project developes a game of Solitair. It is meant as the srouce for a coure developed for the hackerschool (https://hacker-school.de) to introduce Object Oriented Programming using Python. 
The game is solely based on a terminal and only requires a python 3.9 or higher installation to run. No additional external dependencies are necessary.

To run the game simply run 
```shell
python solitair.py
```


## Gameplay
Solitair is a single player game where user needs to move all cards from deck A5 to the decks A1-4. Where each deck A1-4 must contain a complete suite diamonds, hearts, spades and clubs. Each complete suite consists of the cards in order Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen and King.  

To move the cards form A5 to A1-4 the player has to go through the stacks S0-S6. At the beginning of the game each stack contains a set of cards (as shown) with the top card being displayed. 

<pre>
┌──┐ ┌──┐ ┌──┐ ┌──┐      ┌──┐ ┌──┐
│A1│ │A2│ │A3│ │A4│      │A5│ │  │
└──┘ └──┘ └──┘ └──┘      └──┘ └──┘
 
┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
│S0│ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
└──┘ │S1│ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
     └──┘ │S2│ ┌──┐ ┌──┐ ┌──┐ ┌──┐
          └──┘ │S3│ ┌──┐ ┌──┐ ┌──┐
               └──┘ │S4│ ┌──┐ ┌──┐
                    └──┘ │S5│ ┌──┐
                         └──┘ |S6│
                              └──┘
                             
────────────────────────────────── 
Menü
</pre>
The player has the option to either move a card form A5 or S0-6 to the decks A1-4 as long as they are of the correct suite can be applied according to order. The order of the decks A1-A4 is ascending. 

Or he can add a card to the stack S0-6 as long as the card has an alternate color to the top most card and its value is the next lower value in the order of the suite.

Example:
<pre>
 Before    After      
┌──┐┌──┐   ┌──┐                                  
│♥8│|♠7|   │♥8│   
└──┘└──┘   ┌──┐ 
           |♠7|
           └──┘
</pre>
The player can also move cards from one of the stacks S0-6 to another stack as long as the upper most card of the moved cards can be applied to the tagert stack. This is the case if it has an alternate color and its value is the next lower value in the order of a suite. 

Example: Moving from S3 to S0
<pre>
 Before      After

 S0  S3      S0  S3 
┌──┐┌──┐    ┌──┐┌──┐                 
┌──┐┌──┐    ┌──┐┌──┐      
┌──┐┌──┐    ┌──┐┌──┐      
┌──┐┌──┐    ┌──┐|  |                                 
│♥8│|♠7|    |♥8│└──┘                                  
└──┘┌──┐    ┌──┐                                 
    │♦6|    │♦7|                                 
    ┌──┐    ┌──┐                                 
    │♣5|    │♦6|                                 
    └──┘    ┌──┐
            |♣5|
            └──┘                           
</pre>
The game is one if all cards are on the decks A1-4


