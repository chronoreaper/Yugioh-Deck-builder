import os
import glob
import errno
import sys
import random
#import Image

def findCard(index):
    for i in card_to_index:
        if card_to_index[i]==index:
            return i
    return -1

def card_card_index(card,find):
    for i in range(len(card_to_card[card])):
        if card_to_card[card][i]==find:
            return i
    return -1
def card_percent(card,index):
    total = 0
    val = 0
    for i in range(len(card_to_card[card])):
        total +=card_to_deck[card][i]
        if i == index:
            val =card_to_deck[card][i]
    return val/total

#Image.open('pathToFile').show()
deck_path = os.path.dirname(__file__)+'/deck/*.ydk'
fllist = os.path.dirname(__file__)+'/expansions/live2017links/lflist.conf'
files = glob.glob(deck_path)
pic_path = os.path.dirname(__file__)+'/pics'

count=0
lines=[]
card_to_index= {}
index_to_place= []
cards_checked= [] #first time going through
cards_checked2= [] #when checking for card relation ships

card_in_decks= []#how many decks it appears in
card_ratio = []#the ratio in decks, it is the average

card_to_card = [] # a 2d array, [card,index]=card relation
card_to_ratio = [] #2d array, = ratio in decks
card_to_deck = [] # 2d array = how many decks it is in

for file in files:
    try:
        with open(file) as f:             
            if ('1Most Used' not in file and '1New Deck' not in file
                and '1test' not in file):
                cards_checked.clear()
                cards_checked2.clear()
                
                name = file[ file.find('\\')+1:len(file)-4]
                count+=1
                
                place = 0 #0 = main, 1 = extra, 2 = side, 3 = main+side 
                #4 = extra+side
                
                lines = [line.rstrip('\n') for line in f]
                for line in lines: #loop through all lines
                    
                    if line == '#extra':
                        place = 1
                    elif line == '!side':
                        place = 2
                    
                    if '#'not in line and '!' not in line: # check for card line
                        #add the card to the index list if not in it already
                        if line not in card_to_index:
                            card_to_index[line] = len(card_to_index)
                        
                        #data with cards
                        index = card_to_index[line]
                        if index not in cards_checked:#only tiggers once
                            cards_checked.append(index)
                            ratio=lines.count(line)
    
                            #adds to cards in deck
                            if len(card_in_decks)<=index:
                                card_in_decks.append(1)
                                card_to_card.append([])
                                card_to_ratio.append([])
                                card_to_deck.append([])                                  
                            else:
                                card_in_decks[index] +=1   
                                    
                            #show card ratio
                            if len(card_ratio)<=index:
                                card_ratio.append(ratio)
                            else:
                                card_ratio[index]=((card_ratio[index]
                                                *(card_in_decks[index]-1)+ratio) 
                                                /card_in_decks[index])                         
                            #tell if the card is in main side or extra usually
                            if len(index_to_place)<=index:
                                index_to_place.append(place)
                            elif index_to_place[index]==2 and place<2:
                                index_to_place[index]+=place+1
                            elif place==2 and index_to_place[index]<2:
                                index_to_place[index]+=3  
                
                cards_checked.clear()             
                for line in lines:#loop through all the cards again
                    if '#'not in line and '!' not in line: 
                        index = card_to_index[line]
                        if index not in cards_checked:#only tiggers once
                            cards_checked.append(index)    
                        
                            cards_checked2.clear()
                            
                            for line2 in lines:#create links
                                if '#'not in line2 and '!' not in line2: 
                                    index2 = card_to_index[line2]
                                    if index2 not in cards_checked2:#tiggers 1
                                        
                                        cards_checked2.append(index2) 
                                        if index2 not in card_to_card[index]:
                                            card_to_card[index].extend([index2])
                                            card_to_deck[index].extend([0])
                                            card_to_ratio[index].extend([0])
                                        
                                        pos = card_card_index(index,index2)
                                        
                                        ratio=lines.count(line2)
                                        
                                        card_to_deck[index][pos]+=1  
                                        card_to_ratio[index][pos] = (
                                            (card_to_ratio[index][pos]
                                            *(card_to_deck[index][pos]-1)+ratio) 
                                            /card_to_deck[index][pos])                                           
                            
                
            pass # do what you want
    
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
        
#
print('decks:'+str(count))
print('cards:'+str(len(card_to_index)))
main = 0
extra = 0
side = 0
for i in index_to_place:
    if i == 0 or i ==3:
        main+=1
    elif i==1 or i ==4:
        extra+=1
    else:
        side +=1



most=[]
mostCard= []
mostCardt= []
mostRatio=[]#card ratio
loop=1

while loop==1:
    selection=-1
    most.clear()
    mostRatio.clear()
    mostCard.clear()
    mostCardt.clear()
    
    while selection==-1:
        print("Type a command")
        print("list: list the 100 most used cards")
        print("deck: builds a deck")
        print("quit: quits application")
        inpt= input()
        if inpt == "list":
            selection=0
        elif inpt=="deck":
            selection=1
        elif inpt=="quit":
            loop=0
        else:
            print("please choose a choice")
            selection=-1
    
    
    if loop==1:
        if selection==0:
            print('main '+str(main))
            print('extra '+str(extra))
            print('side '+str(side))          
            for i in range(100):
                most.append(-1)
                mostCard.append(-1)
                mostRatio.append(-1)
            for i in range(len(card_in_decks)):
                before=count+1#reset
                added =0
                for k in range(len(most)):
                    if added==0:
                        #if card_in_decks[i]<=before:
                            if card_in_decks[i]>=most[k]:
                                for j in range(len(most)-1,k,-1):
                                    most[j]=most[j-1]
                                    mostCard[j]=mostCard[j-1]
                                 
                                most[k]=card_in_decks[i]
                                mostCard[k]=i

                                added=1
                    before=most[k]
                    
                    
            for i in range(len(most)):
                print('most used '+str(findCard(mostCard[i]))+' ratio '
                      +str('%.1f' %card_ratio[mostCard[i]])
                      +' ' +str(most[i])+'/'+str(count))
            #make new deck
            f= open(os.path.dirname(__file__)+'/deck/1Most Used.ydk',"w")    
        
        elif selection==1:
            sel = '-1'
            while sel =='-1':
                inpt = input("Finish Deck (f),Start from scratch(s),or random(r)?")
                if inpt=='s':
                    sel=0
                elif inpt == 'f':
                    sel=1
                elif inpt =='r':
                    sel=2
            card_listing=[]
            main = 0
            extra = 0
            side = 0   
            if sel==0:
                print("enter cards to base the deck off of."
                            + "enter stop to stop")            
                inpt = input()
                while inpt!= "stop":
                    if inpt in card_to_index:
                        card_listing.append(inpt)
                    else:
                        print("enter a valid card")
                    inpt = input()
            elif sel==1:
                inpt = input("enter deck name: ")
                for file in files:
                    with open(file) as f:             
                        name = file[ file.find('\\')+1:len(file)-4] 
                        if name==inpt:
                            lines = [line.rstrip('\n') for line in f]
                            for line in lines: #loop through all lines
                                if '#'not in line and '!' not in line: 
                                    card_listing.append(line)
            elif sel==2:
                inpt=input("enter number of random cards ")
                cnt = int(inpt)
                while cnt >0:
                    card_listing.append(findCard(random.randint(0,len(card_to_index))))
                    cnt-=1
                                        
            max_main=int(input("enter the upper deck limit. 40-60: "))
            max_main=max(40,max_main)
            for i in range(50):
                most.append(-1)
                mostRatio.append(-1)
                mostCardt.append(-1)  
            c = 0
            l=1 #loops or layers in card checking
            while l>=0:
                for m in range(len(card_listing)):
                    
                    print("checking card "+str(card_listing[m])+" "+str(m+1)
                          +"/"+str(len(card_listing)))
                    card_index=card_to_index[card_listing[m]]    
                    before=count+1#reset
                    added =0   
                    for i in range(len(card_to_card[card_index])):
                        before=count+1#reset       
                        for k in range(len(most)):
                            if card_to_card[card_index][i] not in mostCardt:
                                
                                #determines how often it is paired with other cards
                                percent = card_percent(card_index,i) 
                                #percent = percent*random.random()
                                #r = card_card_index(card_index,i)
                                #percent=percent*(card_to_ratio[card_index][r] /3)                           
                                
                                if percent<=before or before==-1:
                                    if (percent>most[k] 
                                        or percent==most[k] and random.randint(0,1)==0
                                        and l==1):
                                        for j in range(len(most)-1,k,-1):
                                            most[j]=most[j-1]
                                            mostCardt[j]=mostCardt[j-1]
                                            mostRatio[j]=mostRatio[j-1]
                                        most[k]=percent
                                        mostCardt[k]=card_to_card[card_index][i]
                                        r = card_card_index(
                                            card_index,card_to_card[card_index][i])
                                        mostRatio[k]=card_to_ratio[card_index][r]
                            before=most[k] 
                l-=1;
                if l==0:
                    card_listing.clear()
                    for i in mostCardt:
                        if findCard(i)!=-1:
                            card_listing.append(findCard(i))
                            
            for i in range(len(mostCardt)):#add into deck
                # i is the card index in the master list
                if i!=-1:
                    for k in range(round(mostRatio[i])):
                        if c<90:
                            if (index_to_place[mostCardt[i]]==0 
                                or index_to_place[mostCardt[i]]==3):
                                if main<max_main:
                                    main+=1
                                    mostCard.append(mostCardt[i])
                                    c+=1
                            elif (index_to_place[mostCardt[i]]==1 or
                                index_to_place[mostCardt[i]]==4):
                                if extra<15:
                                    extra+=1
                                    mostCard.append(mostCardt[i])
                                    c+=1
                            elif side<15:
                                side+=1
                                mostCard.append(mostCardt[i])
                                c+=1
            print('main '+str(main))
            print('extra '+str(extra))
            print('side '+str(side))    
                        
            f= open(os.path.dirname(__file__)+'/deck/1New Deck.ydk',"w")
        
        else:
            f= open(os.path.dirname(__file__)+'/deck/1Most Used.ydk',"w")
        
        
        f.write("#created by deck_maker_ai\n")
        f.write("#main\n")
        cardcount=0
        for i in range(len(mostCard)):
            cardid = str(findCard(mostCard[i]))
            if index_to_place[mostCard[i]]==0 or index_to_place[mostCard[i]]==3:
                if cardcount<60:
                    f.write(cardid+'\n')
                    cardcount+=1
                
        f.write("#extra\n")
        cardcount=0
        for i in range(len(mostCard)):
            cardid = str(findCard(mostCard[i]))
            if index_to_place[mostCard[i]]==1 or index_to_place[mostCard[i]]==4:
                if cardcount<15:
                    f.write(cardid+'\n')
                    cardcount+=1
                
        f.write("!side\n")
        cardcount=0
        for i in range(len(mostCard)):
            cardid = str(findCard(mostCard[i]))
            if (index_to_place[mostCard[i]]==2 ):
                #or index_to_place[mostCard[i]]==3 
                #or index_to_place[mostCard[i]]==4):
                if cardcount<15:
                    f.write(cardid+'\n')
                    cardcount+=1
        f.close()