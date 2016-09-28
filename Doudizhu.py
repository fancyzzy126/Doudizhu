#!/usr/bin/python
#author:tarzonz
import random
import itertools
import sys
import copy





# debug == for parts of traces:

# 1-5:Basci finding types
# 5:find length error
# 2:rockets,quadruplets,tirplets,pairs,singles
# 1: check all details

# 15: find_more_better check
# 9: rough check and show results repectively of every findings set
# 6: find a play check

# 12: only permutations finding(find_all,find_more) is barred
# 10: no trace output
debug = 10

ori_pack = []            #original cards pack
lef_pack = []            #left cards after filtering
arr = [[],[],[],[]]      #For easy search cards type

#basic types group:
#card types saved as below,[[]]actually:
seq = []       #straight/sequence
roc = []       #rocket: a pair of jokers
qua = []       #quadruplet/bomb
tri = []       #triplet
pai = []       #pair 
sin = []       #single
seq_tri = []   #max straight Sequences e.g.333444,888999101010
seq_pai = []   #seq pairs 33 44 55 66 77

report = []    #find more to check if there is a such result
factor = 7     #for random findings

#enhancement 2 find_more find more and better
#These two value means hands not card num if 33 then 1 not 2
n_need = 0 #e.g 333444 n_need = 2 or 333444,8888 n_need = 4
n_give = 0 #e.g A,J,K n_give = 3  or AA,JJ,K n_give = 3
f_better = False

#advanced groups not used as global
#plane = []     #seq_tri plus same numbers of pairs or singles
#qua_two = []   #quadruplet with 2 cards
#tri_one = []   #triplet plus one card or pair

def clear():
    '''
    clear found card types global storage
    '''
    global seq
    global roc
    global qua
    global tri
    global pai
    global sin
    global seq_tri
    global seq_pai
    global arr
    arr = [[],[],[],[]]
    seq = []
    roc = []
    qua = []
    tri = []
    pai = []
    sin = []
    seq_tri = []
    seq_pai = []
###############end clear######################


def init_globals():
    '''
    clear all the types of globals for a new runnnig case
    '''
    global seq
    global roc
    global qua
    global tri
    global pai
    global sin
    global seq_tri
    global seq_pai
    global ori_pack
    global lef_pack
    global arr

    global result
    global report
    #en12
    global f_better
    f_better = False
    
    #Bug 18
    report = []
    ori_pack = []            #original cards pack
    lef_pack = []            #left cards after folding
    arr = [[],[],[],[]]      #For easy search cards type
    seq = []
    roc = []
    qua = []
    tri = []
    pai = []
    sin = []
    seq_tri =[]
    seq_pai =[]
    
    result = []

    #en 2
    n_need = 0
    n_give = 0

    return
 ########end init###########


def str_to_num(ss):
    '''
    translate from string to number list
    '''
    p = []
    for i in ss:
        if i == "S" or i == "s":
            p.append(10)
        elif i == "J" or i == "j":
            p.append(11)
        elif i == "Q" or i == "q":
            p.append(12)
        elif i == "K" or i == "k":
            p.append(13)
        elif i == "A" or i == "a":
            p.append(14)
        elif i == "W" or i == "w":
            p.append(99)
        elif i == "2":
            p.append(20)
        else:
            if i.isdigit() and int(i)<=9\
            and int(i)>=2:
                p.append(int(i))
            else:
                print "%s is not a card!"%(i)
    
    return p;


def num_to_str(num):
    '''
    translate number to string list
    '''
    p = []
    for i in num:
        if i == 10:
            p.append("S")
        elif i == 11:
            p.append("J")
        elif i == 12:
            p.append("Q")
        elif i == 13:
            p.append("K")
        elif i == 14:
            p.append("A")
        elif i == 99:
            p.append("W")
        elif i == 20:
            p.append("2")
        else:
            p.append(str(i))

    return p;


def put_to_arr(l):

    '''
    put the cards into 4 arrays for easy search card pack
    The purpose is to easy find pairs from arr[1], triplets
    from arr[2] and quadruplets from arr[3]

    example: 3 4 5 5 5 6 6 7 
    after put_to_arr:
    arr[0] = [3,4,5,6,7]
    arr[1] = [5,6]
    arr[2] = [5]
    arr[3] = []
    '''

    global arr
    i = 0
    temp = 0
    #notice to refresh the arr
    for i in range(4):
        arr[i] = []

    i = 0
    for item in l:

        if temp == item:
            i = (i+1)%4
        else:
            i = 0

        arr[i].append(item)
        temp = item

    return;
#######end put_to_arr#################

def remove_pack(ori,l):
    
    for item in l:
        ori.remove(item)

    return;
#####end remove_pack############

#bug 10 add flag for only grab one item
#flag = true means only one grabbed is OK!
# num means grab number, default = 99 means as many as possible
def ext_seq(seq_to,l_from,num = 99):
    '''
    Try to find every item in the l_from to extend the sequence seq_to
    Delete those item in l_from when finishing
    ''' 
    i = 0 
    # Care for remove the index will be changed too
    p = []
    #en12
    n = num
    #BUG5
    if len(seq_to) == 0:
        return False
    if debug <= 1:
        print "Start extend the seq_to",seq_to
        print "from the list:l_from",l_from

    for i in range(len(l_from)):
        if seq_to[0] - 1 == l_from[i]:
            seq_to.insert(0,l_from[i])
            p.append(l_from[i])
            #BUG 10 only once for give back case
            n = n - 1
            if n <= 0:
                break
        elif seq_to[-1] + 1 == l_from[i]:
            seq_to.append(l_from[i])
            p.append(l_from[i])
            #BUG 10 only once for give back case
            n = n - 1
            if n == 0:
                break
        else:
            continue


    if len(p) > 0:
        remove_pack(l_from,p)
        
        if debug <=1:
            print "finish extend, the seq_to now is",seq_to
            print "the left item in l_from is",l_from
        return True;
    else:
        if debug <=1:
            print "nothing extended"
        return False;

def find_roc(lpa):
    '''
    Find rocket from the left pack
    '''
    global roc
    global arr
    global lef_pack
    
    if debug <= 2:
        print "find_roc() from lpa:",lpa
    
    put_to_arr(lpa)

    len_lpa = len(lpa)

    if len(arr[1]) == 0:
        return True

    for item in arr[1]:
        if item == 99:
            roc.append([99,99])
            lpa.remove(99)
            lpa.remove(99)
    
    if debug <= 2:
        print "find roc:",roc

    if len_lpa - len(roc)*2 != len(lef_pack):
        return False

    return True;

#en 12 num = 99 means try to find qua as possible as 99
#step means from arr[3][step] to find a qua
def find_qua(lpa,num = 99,step = 0):
    '''
    find quadruplets from the lpa
    '''
    global qua
    global arr
    global lef_pack

    put_to_arr(lpa)
    
    len_lpa = len(lpa)
    len_qua = sum(map(len,qua))
    
    #en 12
    s = 0
    n = num
    if len(arr[3])!= 0:
        s = step%len(arr[3]) #not overflow

    if debug <= 2:
        print "find_qua() from lpa",lpa

    if len(arr[3]) == 0:
        if debug <= 2:
            print "no find qua",qua
        return True
    #en 12 from the arr3[s] to find n number qua(s)
    for i in range(s,len(arr[3])):
        if arr[3][i] != 99:
            temp = [arr[3][i]]*4
            qua.append(temp)
            for k in range(4):
                lpa.remove(arr[3][i])
            #en 12 find n number qua
            n = n - 1 
            if n == 0:
                break

    if debug <= 2:
        print "find qua:",qua
        if len_lpa + len_qua != len(lef_pack) + sum(map(len,qua)):
            return False

    return True
##############end find_qua####################

#en12 num means how many tris is expected to build
def find_tri(lpa, num = 99, step = 0):
    '''
    Find the triplets from the lpa except those quadruplets
    '''
    global tri
    global arr
    global lef_pack

    put_to_arr(lpa)
    len_lpa = len(lpa)
    len_tri = sum(map(len,tri))

    if debug <= 2:
        print "find_tri from lpa",lpa

    if len(arr[2]) == 0:
        return True

    temp = []
    #i from len(arr[3]) to ignore those cards can be quadruplet
    # en12
    n = num
    if n != 99:
        s = step%len(arr[2])
    else:
        s = len(arr[3])
    #for i in range(len(arr[3]), len(arr[2])):
    for i in range(s, len(arr[2])):
        temp = [arr[2][i]]*3
        tri.append(temp)
        
        for k in range(3):
            lpa.remove(arr[2][i])
        #en12
        n = n - 1
        if n == 0:
            break

    if debug <= 2:
        print "Triplets finded:",tri


    if debug <= 2:
        if len_lpa + len_tri != len(lef_pack) + sum(map(len,tri)):
            print "len_lpa:%d + len_tri:%d != len(lef_pack):%d + newlen Tri:%d"\
            %(len_lpa,len_tri,len(lef_pack),sum(map(len,tri)))
            return False

    return True;
 #############################end find_tri   

#en12 num means how long the seq pai is 2 means 5 pair long
def find_seq_pai(lpa,num = 99,step = 0):
    '''
    Find every max seq_pai from lpa
    '''
    global seq_pai
    global lef_pack
    global arr
    
    put_to_arr(lpa)
    len_lpa = len(lpa)
    len_seq_pai = sum(map(len,seq_pai))


    if debug <= 4:
        print "find_seq_pai form lpa:",lpa
        print "previous seq_pai:",seq_pai

    if len(arr[1]) < 3:
        if debug <= 4:
            print "seq_pai",seq_pai
        return True

    #en12
    n = num
    if len(arr[1]) ==  3:
        s = 0
    else:
        s = step%(len(arr[1]) - 3)

    i = s
    count = 0
    while i < (len(arr[1]) - 1):
    
        while arr[1][i] + 1 == arr[1][i+1]:
            count = count + 1
            i = i + 1
            #en 12
            
            if count == n or i == len(arr[1]) - 1:
                break
            
        if count > 1: #Find 2 pairs to combine seq_pai since 3 at least
            temp = arr[1][i-count:i+1]
            seq_pai.append(sorted(temp*2))
            remove_pack(lpa,temp*2)
            count = 0
            #Bug23 also same with find_seq_tri
            i = i + 1
        else:
            count = 0 #restart count
            i = i + 1
    
    
    if debug <= 4:
        print "find seq_pai",seq_pai

    #en12 old + old = new + new
    if debug <= 5:
        if len_lpa + len_seq_pai != len(lpa) +  sum(map(len,seq_pai)):
            print "len_lpa%d + len_seq_pai:%d == len(lpa)%d + sum(map(len(seq_pai))%d"\
            %(len_lpa,len_seq_pai,len(lpa),sum(map(len,seq_pai)) )
            return False

    return True
####################end find_seq_pai###################### 

#en 12 num means how long the seq_tri is
def find_seq_tri(lpa,num = 99, step = 0):
    '''
    Find every max seq_tri from lpa
    BUG 11 33334444 -> 333444 34 Pass this case!
    '''
    global seq_tri
    global lef_pack
    global arr
    

    put_to_arr(lpa)
    len_lpa = len(lpa)
    
    #12 old = new intotal
    len_seq_tri = sum(map(len,seq_tri))

    if debug <= 3:
        print "find_seq_tri from lpa",lpa

    if len(arr[2]) < 1:
         return True
    
    #12
    n = num
    if len(arr[2]) - 1 != 0:
        s = step%(len(arr[2]) - 1)
    else:
        s = 0
    i = s
    count = 0
    while i < (len(arr[2]) - 1):
        while arr[2][i] + 1 == arr[2][i+1]:
            #bug 11 consider if there are seq_qua:
        #    if i < (len(arr[3]) - 1):
         #       if arr[3][i] + 1 == arr[3][i+1]:
          #          break
            #end bug 11

            count = count + 1
            i = i + 1
            if i == len(arr[2]) - 1:
                break
            if count == num:
                break
        if count > 0: #Find seq_tri
            temp = arr[2][i-count:i+1]
            seq_tri.append(sorted(temp*3))
            remove_pack(lpa,temp*3)
            
            count = 0
            #Bug23 deleted more
            i = i + 1 #When 333444 decide to build the i should move to
                      #next item 555 but now i still stay at 444 and 444555
                      #will be deleted to trigger 4 not exsited error
        else:
            i = i + 1

    if len(seq_tri) == 0:
        if debug <= 3:
            print "no Finded seq_tri",seq_tri
        return True

    if debug <= 3:
        print "finded seq_tri:",seq_tri

    #end 12 old+old = new + new
    if len_lpa + len_seq_tri != len(lef_pack) + sum(map(len,seq_tri)):
        if debug <= 5 or debug >=15:
            print "len_lpa:%d + len_seq_tri:%d == len(lef_pack):%d + len(seq_tri):%d"\
            %(len_lpa,len_seq_tri,len(lef_pack),sum(map(len,seq_tri)))
        return False

    return True;
###########end find_seq_tri########################


def find_pai(lpa, num = 99, step = 0):
    '''
    find every pairs from the left cards lpa
    '''
    global pai
    global arr
    
    put_to_arr(lpa)
    len_pai = sum(map(len,pai))
    len_lpa = len(lpa)

    if debug <=2 :
        print "find pairs from lpa",lpa

    if len(arr[1]) == 0:
        return True
    #en2
    s = step%len(arr[1])
    n = num
    for i in range(s,len(arr[1])):
        pai.append([arr[1][i]]*2)
        lpa.remove(arr[1][i])
        lpa.remove(arr[1][i])
        #en2
        n = n - 1
        if n == 0:
            break
    
    pai = sorted(pai)
    new_pai = sum(map(len,pai))
    new_lpa = len(lpa)

    if debug <=1 :
        if len_lpa + len_pai != new_lpa + new_pai:
            print "len_lpa:%d + len_pai:%d != new_lpa:%d + new_pai:%d"%\
            (len_lpa,len_pai,new_lpa,new_pai)
            return False
    
    if debug <= 2:
        print "pairs have been found:",pai

    #bug 12 find seq_pai or qua

    return True;
#############end find_pai###########

def find_sin(lpa):
    '''
    After a series of findings,
    ALl the left cards in the lpa should be singles
    '''
    global sin
    
    if debug <= 2:
        print "find singles form lpa",lpa

    len_lpa = len(lpa)
    len_sin = sum(map(len,sin))
   
    temp = []
    for ite in lpa:
        sin.append([ite])
        temp.append(ite)

    remove_pack(lpa,temp)

    if debug <= 5:
        if len(lpa)!= 0 or sum(map(len,sin)) != len_lpa:
            print "find sin error"
            return False

    if debug <= 2:
        print "sin have been found",sin

    return True;
##########end find_sin############

def find_seq(lpa,num = 99, step =0):
    global seq
    global arr
    global lef_pack
    global seq_pai
    global seq_tri
    global f_better

    put_to_arr(lpa)
    temp = []
    
    #en12
    if len(arr[0]) - 4 > 0:
        s = step%(len(arr[0])-4)
    else:
        #bug 25
        return True

    if debug <= 2:
        print "find_seq begin from  lpa=",lpa
    #steps: 1.find minimum Sequences
    #       high priority for qua and tri finding
    #       2.extend those Sequences to longest ones
    #BUG30 del no need to find the other types,since this will be block 
    #in find_more_better to find new types
    #       3.combine the same Sequences to pair or triplet sequence
    # 4. is deleted since find_more_better will take care other types in priority
    #       4.two special cases

    #1 First find every minimum Sequence
    #en12
    i = s
    while i < (len(arr[0])-4):
        if len(arr[0]) < 5 :
            break
        else:
            while i < (len(arr[0])-4):
                if arr[0][i+4] == arr[0][i] + 4:
                    for k in range(5):
                        temp.append(arr[0][i+k])
                    #find and allocate a minimum Sequence
                    seq.append(temp) 
                    remove_pack(lpa,temp)
                    put_to_arr(lpa)
                    i = 0 #Bug23 This way is OK refresh arr and
                          #refind from the beginning
                    temp = []
                    break
                else:
                    #bug 1
                    #i = i + 4
                    i = i + 1

    if debug <= 2:
        print "Finded every minimum Sequence in Seq:",seq
      

    #2.contitue to extend every minimus seq from the left lpa
    
    len_lpa = len(lpa)    #record the previous length for debug
    len_seq = sum(map(len,seq))
    len_seq_pai = sum(map(len,seq_pai))
    
    #en12
    if num == 99 and f_better:
        if debug >= 15:
            print "Here by default return"
        return True
    n = num
    for i in range(len(seq)):
        if len(lpa) == 0:
            break
    #bug 10 False means grab as many as possible
        #en12
        ext_seq(seq[i],lpa,n)


    #3. combine the possible seqs 
    #3.1 comibne those longest sequences if possible
    temp = []
    for i in range(len(seq) - 1):
        #only consider the bigger one to be combined
        #Since the sequence is in order
        if seq[i][-1] + 1 == seq[i+1][0]:
            seq[i] = seq[i] + seq[i+1]
            temp.append(seq[i+1])

    if len(temp) != 0:
        remove_pack(seq,temp)

    #3.2 Find overlapped seq to seq_pai
    seq = sorted(seq)
    t_seq = []
    for i in range(len(seq) -1):
        if seq[i] == seq[i+1]:
            seq_pai.append(sorted(seq[i]*2))
            t_seq.append(seq[i])
            t_seq.append(seq[i])

    remove_pack(seq,t_seq)
    seq_pai = sorted(seq_pai)


    if debug <= 2:
        print "Finded every maximum sequence in Seq:", seq


    return True;
##############end find_seq#################

def find_types(lpa):
    '''
    search cards types from the left cards
    Notice! the lpa should be in ascending order
    '''
    global seq
    global pai
    global tri
    global qua

    #Bug 13 seq_pai -> seq_tri
    global seq_pai
    global seq_tri
    #end Bug 13

    if not find_roc(lpa):
        if debug <= 1:
            print "find_roc failed"
            return False

    #qua,tri finding were inserted to find_seq
    #if not find_qua(lpa):
    #    print "find_qua failed"
    #    return False
       
    #if not find_tri(lpa):
    #   print "find_tri failed"
    #    return False
    
    if not find_seq_tri(lpa):
        if debug <= 1:
            print "find seq_tri failed"
            return False

    if not find_seq_pai(lpa):
        if debug <=1:
            print "find seq_pai failed"
            return False

    if not find_seq(lpa):
        if debug <=1:
            print "find_seq failed"
            return False

    #Bug 25 recover the finding of tri and qua
    #Since find_more_better cover all the
    #types finding priority and cases
    if not find_qua(lpa):
        if debug <=1:
            print "find_qua failed"
            return False

    if not find_tri(lpa):
        if debug <=1:
            print "find_tri failed"
            return False
    #end qua,tri priority finding
    
    #bug 12 There may be seq_pai or qua in lpa
    find_seq_pai(lpa)
    find_qua(lpa)
    #end bug 12

    if not find_pai(lpa):
        if debug <= 1: 
            print "find_pai failed"
            return False

    if not find_sin(lpa):
        if debug <= 1:
            print "find_sin failed"
            return False

    if len(lef_pack) != 0:
        if debug <= 1:
            print "should no cards left,error"
            print "lef_pack:",lef_pack
            return False
    return True;
#################end find_types########################


def show_status():
    '''
    Show all the kinds of packs filtered right now
    '''

    global result
    global report
           
    if debug <= 5 or debug >= 15:
        print
        print "*"*10,"Basic types are as below","*"*10
        print "original pack".ljust(25)," <%d>:"%(len(ori_pack)),ori_pack
        print "left pack after filtered".ljust(25)," <%d>:"%(len(lef_pack)),lef_pack
        if len(seq_tri) != 0:
            print "sequence triplets".ljust(25)," <%d>:"%(sum(map(len,seq_tri))),seq_tri

        if len(seq_pai) != 0:
            print "sequence pairs".ljust(25)," <%d>:"%(sum(map(len,seq_pai))),seq_pai

        if len(seq) != 0:
            print "sequences".ljust(25)," <%d>:"%(sum(map(len,seq))),seq

        if len(roc) != 0:
            print "rockets".ljust(25)," <%d>:"%(sum(map(len,roc))),roc

        if len(qua) != 0:
            print "quardruplets".ljust(25)," <%d>:"%(sum(map(len,qua))),qua

        if len(tri) != 0:
            print "triplets".ljust(25)," <%d>:"%(sum(map(len,tri))),tri

        if len(pai) != 0:
            print "pairs".ljust(25)," <%d>:"%(sum(map(len,pai))),pai

        if len(sin) != 0:
            print "singles".ljust(25)," <%d>:"%(sum(map(len,sin))),sin 
        
        print "*" * 25
        print
    #------final results as requested are here-------#
    if debug <= 9 or debug >= 15:
        print
        print "Possibly,all the result are summarised as follow:"
        print len(result)
        for item in report:
            show(item)
            print
        print 
    else:
        print len(result)
        for item in report:
            show(item)
            print
        print 

    return;
#########################end show_status###################################


def combine (set,l,pack):
    '''
    output set [[]]
    input: l,pack
    set = l + pack
    [[]] = [] + [[],[]] [3,3,3,4,4,4] + [[7,7],[8,8]] = [[3,3,3,4,4,4,7,7,8,8]
    '''
    ll = l[:]
    
    for ite in pack:
        ll  = ll + ite

    set.append(ll)

    return
###########end combine ###########

def is_pai(l):
    '''
    check if l is a pai 
    '''
    if len(l) == 0:
        return False

    #Bug17 2,W
    if len(l) == 2 and l[0] == l[1]:
        return True

#######end is_pai##########################

def is_sin(l):
    '''
    check if i l a sin except 2 or joker
    '''
    if len(l) == 0:
        return False

    #Bug17 2,W
    if len(l) == 1:
        return True

#########end is_sin#########################


def step4_big_seq_discard(t_seq,pool,flag):
    '''
    This special function is to let a card
    discarded from a big seq to pool
    the choice to discard which side card
    is according to the flag
    Thus, in the find_all_plays this flag 
    should be different from the previous 
    '''
    if len(pool) == 0:
        if debug <= 6:
            print "Error in step4_big_seq_discard"
        return False
    
    len_pool = sum(map(len,pool))
    len_seq = sum(map(len,seq))


    if is_sin(pool[0]):
        for i in range(len(t_seq)):
            if len(t_seq[i]) > 5: #find a 5+ seq
                #BUG 15
                if pool[0][0]!=t_seq[i][0] and pool[0][0]!=t_seq[i][-1]:
                    continue #find the next one
                if flag: #become a pari 5  5678910-> 55 678910
                    pool[0].append(pool[0][0])  #[[5]] -> [[5,5]]
                    t_seq[i].remove(pool[0][0]) #5 removed from t_seq[i]
                    break #only once
                else:

                    if t_seq[i][0] != pool[0][0]:
                        t_seq[i].remove(t_seq[i][0])
                        pool[0].append(t_seq[i][0]) #[[5]] -> [[10,5]]
                    else:
                        pool.append([t_seq[i][-1]])#pool append another sin Bug 24 
                        t_seq[i].remove(t_seq[i][-1])
                        break #only one card case

    else:
        if debug <= 6:
            print "Error in step4_big_seq_discard"
        return False
    
    new_len_pool = sum(map(len,pool))
    new_len_seq = sum(map(len,t_seq))

    if new_len_pool != 1: #There is a change
        if debug <= 6:
            if len_pool + len_seq != new_len_pool + new_len_seq:
                print "Step 4.5 seq give back one failed"
                return False

    if debug <= 6:
        print "Step 4.5 special case success"
        print "seq",t_seq
        print "pool",pool

    return True
################end step4_big_seq_discard#################################

    


def step6_tri_sin_pai(tri_one,t_tri,pool):
    '''
    output:tri_one,t_tri,pool
    from pool,
    triplets get one single or pair,randomly
    '''
    
    if debug <= 6:
        print "******step 6 ****** small tri get ONE begin"
        print "tri_one:",tri_one
        print "t_tri:",tri
        print "pool:",pool
     
    if len(t_tri) == 0 or len(pool) == 0:
        if debug <= 6:
            print "no tri or sin or pai"
            print "tri_one:",tri_one
            return True

    d_tri = []  #to be deleted from tri which find a sin or a pair
    d_ite = []   #item may be a sin or pair
    r_stri = t_tri[:] #no necessary for a reversed order by length of t_tri

    #r_stri = sorted(stri, key=lambda s:len(s), reverse=1)
    if debug <= 6:
        print "r_stri:",r_stri
    
    len_tri = sum(map(len,t_tri))
    len_pool = sum(map(len,pool))
    len_tri_one = sum(map(len,tri_one))
   

    for i in range(len(r_stri)):
        if len(pool) < 1: 
            if debug <= 6:
                print "no items in pool:",pool
            break   
        for k in range(len(pool)):
            d_ite.append(pool[k])
            if debug <= 6:
                print "find a d_ite",d_ite
            combine(tri_one,r_stri[i],d_ite)
            remove_pack(pool,d_ite)
            d_ite = []
            d_tri.append(r_stri[i])
            break 

    new_len_pool = sum(map(len,pool))
    new_len_tri_one = sum(map(len,tri_one))

    #some tri has got a ONE
    if new_len_pool != len_pool:
        remove_pack(t_tri,d_tri)

        new_len_tri = sum(map(len,t_tri))
        if debug <= 6:
            if len_tri + len_pool + len_tri_one != new_len_tri + new_len_pool\
            + new_len_tri_one:
                print "numbers inconsistence"
                print "step 6 failed combine tri_one",tri_one
                return False
    
    if debug <= 6:
        print "step6 finished, tri_one <%d>:"%(sum(map(len,tri_one))),tri_one
        print "t_tri:",t_tri
        print "pool:",pool
    return True
#############end step6_tri_sin_pai######################################


def step5_small_plane_pair(plane,stri,pool):
    '''
    output:plane,stri,pool
    from pool,
    small planes get one pair
    notice this step only consider small planes
    '''
    
    if debug <= 6:
        print "******step 5 ****** small plane plus one pair begin"
        print "plane:",plane
        print "stri:",stri
        print "pool:",pool
     
    if len(stri) == 0 or len(pool) == 0:
        if debug <= 6:
            print "no seq_tri or pai"
            print "plane:",plane
            return True

    d_stri = []  #to be deleted from stri which find a pair
    d_pai = []   #pairs to be deleted from pool
    r_stri = stri[:] #no necessary for a reversed order by length of seq_tri

    #r_stri = sorted(stri, key=lambda s:len(s), reverse=1)
    if debug <= 6:
        print "r_stri:",r_stri
    
    len_stri = sum(map(len,stri))
    len_pool = sum(map(len,pool))
    len_plane = sum(map(len,plane))
    #First let's count the number of pair in pool:
    pai_num = 0;
    for item in pool:
        if is_pai(item):
            pai_num = pai_num + 1

    if pai_num < 1 :
        if debug <= 6:
            print "no pai in pool",pool
            print "plane:",plane
            return True

    need_num = 0  
    pai_num = 0
    if debug <= 6:
        print "r_stri",r_stri
        print "pool:",pool
        print "start search"

    for i in range(len(r_stri)):
        pai_num = 0
        for item in pool:
            if is_pai(item):
                pai_num = pai_num + 1

        if pai_num < 1:   # this step only take care small planes, so at least 1 pair
            if debug <= 6:
                print "no pai in pool:",pool
            break   
        if len(r_stri[i]) == 6: #only consider small plane
            need_num = 1   #only need one pai
            if need_num <= pai_num:
                for k in range(len(pool)):
                    if is_pai(pool[k]):
                        d_pai.append(pool[k])
                        need_num = need_num - 1
                        
                        if need_num == 0:  #enough sins find
                            if debug <= 6:
                                print "find enough a pai for plane,d_pai",d_pai
                            combine(plane,r_stri[i],d_pai)
                            #del pai from pool
                            remove_pack(pool,d_pai)
                            d_pai = []
                            #record this seq_str ,to delete outside of the circle
                            d_stri.append(r_stri[i])
                            pai_num = 0 #restart count the total pai number
                            break 
            else:
                continue #loop the next less stri


    new_len_pool = sum(map(len,pool))
    new_len_plane = sum(map(len,plane))

    if new_len_pool != len_pool:
    #some seqtri has got a pair
        remove_pack(stri,d_stri)

        new_len_stri = sum(map(len,stri))
        if debug <= 6:
            if len_stri + len_pool + len_plane != new_len_stri + new_len_pool\
            + new_len_plane:
                print "numbers inconsistence"
                print "step 5 failed combine plane",plane
                return False
    
    if debug <= 6:
        print "step5 finished, plane <%d>:"%(sum(map(len,plane))),plane
        print "stri:",stri
        print "pool:",pool
    return True
################end step5_small_plane_pair################################

# rule updated qua only get 2 hands cards
# like 33334455 or 3333810, two different sins or two different pairs
def step3_qua_two(qua_two,t_qua,pool):
    '''
    output:qua_two,t_qua,pool
    from pool,
    qua get two hands cards 
    '''

    if debug <= 6:
        print "\n"
        print "******step 3.****** qua get TWO begin"
        print "t_qua:",t_qua
        print "pool:",pool
     
    if len(t_qua)==0 or len(pool)<2:
        if debug <= 6:
            print "no qua or 2 more hands item in pool"
            return True

    d_qua = []  #to be deleted from t_qua which find two sins
    d_ite = []   #to be deleted from pool
    
    r_qua = t_qua[:] #for notcie this is a temp of t_qua
    if debug <= 6:
        print "r_qua:",r_qua
    
    len_qua = sum(map(len,t_qua))
    len_pool = sum(map(len,pool))
    len_qua_two = sum(map(len,qua_two))
    for i in range(len(r_qua)):
        
        need_num = 2 #qua need 2 hands item
        pai_num = 0
        sin_num = 0
        for item in pool:
            if is_pai(item):
                pai_num = pai_num + 1
            else:
                sin_num = sin_num + 1
        f_find_pai = False
        f_two_pai_same = False
        need_num = 2
        #Bug22 continue to find the same type as the first if enough
        #according to number and first intem to decide grab two what        
        temp = []
        if sin_num == 2:
            for j in range(len(pool)):
                if is_sin(pool[j]):
                    temp.append(pool[j])
            if len(temp) == 2 and temp[0] == temp[1]:
                f_find_pai = True

        if pai_num == 2:
            temp = []
            for j in range(len(pool)):
                if is_pai(pool[j]):
                    temp.append(pool[j])

            if len(temp)==2 and temp[0] == temp[1]:
                f_two_pai_same = True
                if f_find_pai:
                    break


        if pai_num < 2 and sin_num < 2:
            break
        
        elif pai_num >= 2 and sin_num >= 2:
            if is_pai(pool[0]) and not f_two_pai_same:
                f_find_pai = True
            elif is_pai(pool[0]) and f_two_pai_same:
                if f_find_pai:
                    break
                else:
                    f_find_pai == False
        elif sin_num >= 2 and pai_num < 2:
            if f_find_pai:
                break
            f_find_pai = False
        elif sin_num < 2 and pai_num >=2:
            if f_two_pai_same:
                break
            f_find_pai = True
        else:
            f_find_pai = True
        #Bug22 continue to find the same type as the first if enough
        for j in range(len(pool)):
            if f_find_pai:
                if is_sin(pool[j]):
                    continue
                else:
                #bug28 same item in quaTwo
                    if len(d_ite) == 1 and need_num == 1:
                        if d_ite[0] == pool[j]:
                            if pai_num - 2 <= 0: #no others
                                d_ite = []
                                need_num = 2
                                break

                    d_ite.append(pool[j])
                    need_num = need_num - 1
                    pai_num = pai_num - 1
                    if need_num == 0:
                        combine(qua_two,r_qua[i],d_ite)
                        remove_pack(pool,d_ite)
                        d_ite = []
                        d_qua.append(r_qua[i])
                        break
            else:
                if is_pai(pool[j]):
                    continue
                else:
                    if len(d_ite) == 1 and n_need == 1:
                        if d_ite[0] == pool[j]:
                            if sin_num - 2 <= 0:
                                d_ite = []
                                need_num = 2
                                break
                    d_ite.append(pool[j])
                    need_num = need_num - 1
                    sin_num = sin_num - 1
                    if need_num == 0:
                        combine(qua_two,r_qua[i],d_ite)
                        remove_pack(pool,d_ite)
                        d_ite = []
                        d_qua.append(r_qua[i])
                        break

    new_len_pool = sum(map(len,pool))
    new_len_qua_two = sum(map(len,qua_two))

    if new_len_pool != len_pool:
    #some qua has got a TWO
        remove_pack(t_qua,d_qua)


        new_len_qua = sum(map(len,t_qua))
        if debug <= 6:
            if len_qua + len_pool + len_qua_two != new_len_qua + new_len_pool\
            + new_len_qua_two:
                print "len_qua:%d + len_pool:%d + len_qua_two:%d != new_len_qua:%d\
+ new_len_pool:%d + new_len_qua_two:%d"%(len_qua,len_pool,len_qua_two\
                ,new_len_qua,new_len_pool,new_len_qua_two)
                print "numbers inconsistence"
                print "step 4 failed combine qua_two",qua_two
                return False
    

    if debug <= 6:
        print "step 3 finished, qua_two <%d>:"%(sum(map(len,qua_two))),qua_two
        print "t_qua:",t_qua
        print "pool:",pool
    return True
####################end step3_qua_two############################################


def step2_small_plane_sins(plane,stri,pool):
    '''
    output:plane,stri,pool
    from pool,
    small planes get two sins
    notice this step only consider small planes
    '''
    
    if debug <= 6:
        print "******step 2.5 ****** small plane plus two sins begin"
        print "plane:",plane
        print "stri:",stri
        print "pool:",pool
     
    if len(stri) == 0 or len(pool) == 0:
        if debug <= 6:
            print "no seq_tri or sin"
            print "plane:",plane
            return True

    d_stri = []  #to be deleted from stri which find sins or pairs
    d_sin = []   #sinor to be deleted from pool
    r_stri = stri[:] #no necessary for a reversed order by length of seq_tri

    #r_stri = sorted(stri, key=lambda s:len(s), reverse=1)
    if debug <= 6:
        print "r_stri:",r_stri
    
    len_stri = sum(map(len,stri))
    len_pool = sum(map(len,pool))
    len_plane = sum(map(len,plane))
    #First let's count the number of sins in pool:
    sin_num = 0;
    for item in pool:
        if is_sin(item):
            sin_num = sin_num + 1

    if sin_num < 2 :
        if debug <= 6:
            print "no sin in pool",pool
            print "plane:",plane
            return True

    need_num = 0  
    sin_num = 0
    if debug <= 6:
        print "r_stri",r_stri
        print "pool:",pool
        print "start search"

    for i in range(len(r_stri)):
        sin_num = 0
        for item in pool:
            if is_sin(item):
                sin_num = sin_num + 1


        if sin_num < 2:   # this step only take care small planes, so at least 2 length
            if debug <= 6:
                print "no  sin in pool:",pool
            break   
        if len(r_stri[i]) == 6: #only consider small plane
            need_num = len(r_stri[i])/3   #don't forget /3
            if need_num <= sin_num:
                for k in range(len(pool)):
                    if is_sin(pool[k]):
                        d_sin.append(pool[k])#d_item:[[3],[5,5]]
                        need_num = need_num - 1
                        
                        if need_num == 0:  #enough sins find
                            if debug <= 6:
                                print "find enough sins for plane,d_sin",d_sin
                            combine(plane,r_stri[i],d_sin)
                            #del sin from pool
                            remove_pack(pool,d_sin)
                            d_sin = []
                            #record this seq_str ,to delete outside of the circle
                            d_stri.append(r_stri[i])
                            sin_num = 0 #restart count the total sin number
                            break # finish this stri combination and break
            else:
                continue #loop the next less stri


    new_len_pool = sum(map(len,pool))
    new_len_plane = sum(map(len,plane))

    if new_len_pool != len_pool:
    #some seqtri has got sins
        remove_pack(stri,d_stri)

        new_len_stri = sum(map(len,stri))
        if debug <= 6:
            if len_stri + len_pool + len_plane != new_len_stri + new_len_pool\
            + new_len_plane:
                print "numbers inconsistence"
                print "step 2.5 failed combine plane",plane
                return False
    
    if debug <= 6:
        print "step2 finished, plane <%d>:"%(sum(map(len,plane))),plane
        print "stri:",stri
        print "pool:",pool
    return True
################end step2_small_plane_sins################################

def step2_plane_singles(plane,stri,pool):
    '''
    output:plane,stri,pool
    from pool,
    planes get singles in a reversed order of planes' length
    notice this step only for big planes
    '''
    
    if debug <= 6:
        print "\n"
        print "******step 2.****** plane with singles begin"
        print "plane:",plane
        print "stri:",stri
        print "pool:",pool
     
    if len(stri) == 0 or len(pool) == 0:
        if debug <= 6:
            print "no seq_tri or pai"
            print "plane:",plane
            return True

    d_stri = []  #to be deleted from stri which find pairs
    d_sin = []   #to be deleted from pool
    r_stri = stri[:] #reversed order by length of seq_tri

    r_stri = sorted(stri, key=lambda s:len(s), reverse=1)
    if debug <= 6:
        print "r_stri:",r_stri
    
    len_stri = sum(map(len,stri))
    len_pool = sum(map(len,pool))
    len_plane = sum(map(len,plane))
    #First let's count the number of pairs in pool:
    sin_num = 0
    for i in range(len(pool)):
        if is_sin(pool[i]):
            sin_num = sin_num + 1

    if sin_num < 3:#big plane at least need 3 singles
        if debug <= 6:
            print "not enough sins in pool",pool
            print "plane:",plane
            return True

    need_num = 0
    sin_num = 0
    if debug <= 6:
        print "r_stri",r_stri
        print "pool:",pool
        print "start search"
    #in a reversed ord to get pairs
    for i in range(len(r_stri)):
        if len(r_stri[i]) >= 9: #big plane
            sin_num = 0 #recount the sin number
            for j in range(len(pool)):
                if is_sin(pool[j]):
                    sin_num = sin_num + 1
            if sin_num < 3:   # this step only take care big planes, so at least 3 sins
                if debug <= 6:
                    print "no enough sins now,sin_num:",sin_num
                break    #no enough sins to find
            need_num = len(r_stri[i])/3   #don't forget /3
            if need_num <= sin_num:
                for k in range(len(pool)):
                    if is_sin(pool[k]):
                        d_sin.append(pool[k])#d_sin:[[3],[4],[5]]
                        need_num = need_num - 1
                        if need_num == 0:  #enough sins find
                            if debug <= 6:
                                print "find enough sins for plane,d_sin",d_sin
                            #Add to plane like [[6,6,6,7,7,7,8,8,8,3,4,5]]
                            combine(plane,r_stri[i],d_sin)
                            #del sin from pool
                            remove_pack(pool,d_sin)
                            d_sin = []
                            #record this seq_str ,to delete outside of the circle
                            d_stri.append(r_stri[i])
                            sin_num = 0 #restart count the total sin number
                            break # finish this stri combination and break
            else:
                continue #loop the next less stri


    new_len_pool = sum(map(len,pool))
    new_len_plane = sum(map(len,plane))

    if new_len_pool != len_pool:
    #some seqtri has got sins
        remove_pack(stri,d_stri)

        new_len_stri = sum(map(len,stri))
        if debug <= 6:
            if len_stri + len_pool + len_plane != new_len_stri + new_len_pool\
            + new_len_plane:
                print "numbers inconsistence"
                print "step 2 failed combine plane",plane
                return False
    
    if debug <= 6:
        print "step2 finished, plane <%d>:"%(sum(map(len,plane))),plane
        print "stri:",stri
        print "pool:",pool
    return True

###################end step2_plane_singles#####################3


def step1_plane_pairs(plane,stri,pool):
    '''
    output:plane,stri,pool
    from pool,
    planes get pairs in a reversed order of planes' length
    '''

    if debug <= 6:
        print "\n"
        print "******step 1.****** plane with pairs begin"
        print "stri:",stri
        print "pool:",pool
     
    if len(stri) == 0 or len(pool) == 0:
        if debug <= 6:
            print "no seq_tri or pai"
            print "plane:",plane
            return True

    d_stri = []  #to be deleted from stri which find pairs
    d_pai = []   #to be deleted from pool
    r_stri = stri[:] #reversed order by length of seq_tri

    r_stri = sorted(stri, key=lambda s:len(s), reverse=1)
    if debug <= 6:
        print "r_stri:",r_stri
    
    len_stri = sum(map(len,stri))
    len_pool = sum(map(len,pool))
    len_plane = sum(map(len,plane))
    #First let's count the number of pairs in pool:
    pai_num = 0
    for i in range(len(pool)):
        if is_pai(pool[i]):
            pai_num = pai_num + 1

    if pai_num < 2:#333444 need two pairs
        if debug <= 6:
            print "not enough pairs in pool",pool
            print "plane:",plane
            return True

    need_num = 0
    pai_num = 0
    if debug <= 6:
        print "r_stri",r_stri
        print "pool:",pool

    #in a reversed ord to get pairs
    for i in range(len(r_stri)):
        pai_num = 0 #recount the total number
        for j in range(len(pool)):
            if is_pai(pool[j]):
                pai_num = pai_num + 1
        if pai_num < 2:
            if debug <= 6:
                print "no enough pairs now,pai_num:",pai_num
            break    #no enough pairs to find
        need_num = len(r_stri[i])/3   #don't forget /3
        if need_num <= pai_num:
            for k in range(len(pool)):
                if is_pai(pool[k]):
                    d_pai.append(pool[k])#d_pai:[[3,3],[4,4],[5,5]]
                    need_num = need_num - 1
                    if need_num == 0:  #enough pairs find
                        if debug <= 6:
                            print "find enough pairs for plane,d_pai",d_pai
                        #Add to plane like [[6,6,6,7,7,7,8,8,8,3,3,4,4,5,5,]]
                        combine(plane,r_stri[i],d_pai)
                        #del pai from pool
                        remove_pack(pool,d_pai)
                        d_pai = []
                        #record this seq_str ,to delete outside of the circle
                        d_stri.append(r_stri[i])
                        pai_number = 0
                        break
        else:
            continue


    new_len_pool = sum(map(len,pool))
    new_len_plane = sum(map(len,plane))

    if new_len_pool != len_pool:
    #some seqtri has got pairs
        remove_pack(stri,d_stri)

        new_len_stri = sum(map(len,stri))
        if debug <= 6:
            if len_stri + len_pool + len_plane != new_len_stri + new_len_pool\
            + new_len_plane:
                print "numbers inconsistence"
                print "step 1 failed combine plane",plane
                return False
    
    if debug <= 6:
        print "step1 finished, plane <%d>:"%(sum(map(len,plane))),plane
        print "stri:",stri
        print "pool:",pool
    return True

################end step1_plane_pairs##################

def show(l):
    '''
    show the result of l
    '''
    ss = ""
    temp =""
    l = sorted(l)  #asceding order to show
    l = sorted(l,key=lambda x:len(x),reverse=1) #descending order of length to show

    #translation:
    for i in range(len(l)):
        ss = ""
        for j in range(len(l[i])):
            if l[i][j] == 20:
                temp = "2"
            elif l[i][j] == 99:
                temp = "W"
            elif l[i][j] == 10:
                temp = "S"
            elif l[i][j] == 11:
                temp = "J"
            elif l[i][j] == 12:
                temp = "Q"
            elif l[i][j] == 13:
                temp = "K"
            elif l[i][j] == 14:
                temp = "A"
            else:
                temp = str(l[i][j])
            
            ss = ss + temp
        if i != len(l)-1:
            ss = ss + " "
        print ss,

########end show#######################################

def find_a_play():
    '''
    Give a optimal solution in the asceding order of the basic types
    '''
    global seq
    global roc
    global qua
    global tri
    global pai
    global sin
    global seq_tri
    global seq_pai

    global result #to record this optimal play for finding others
    global report #add this optimal play to the report

    #Here goes a serises of plays by priority as below:
    #1. planes in length reversed order get pairs
    #2. big planes(len>6) in length reversed order get singles
    #2.5 small planes get 2 singles
    #3. quadruplets get 2 hands cards

    #4.5 special case: qua get another single from seq:
    #   e.g.,333355 678910 -> 3333510,56789
    #4.6 special case: small planes get another single from seq
    #   e.g.,33344455 678910 -> 333444510,56789

    #5. small planes get one pair
    #6. triplets get one pair
    #7. triplets get one single
    #8. All types played out
    
    #A sample for the purpose of keep all the types in globals
    #for find_all_plays to use

    plane = []     #seq_tri plus same numbers of pairs or singles
    qua_two = []   #quadruplet with 2 cards
    tri_one = []   #triplet plus one card or pair

    #Bug 23 copy the value not the address for all the item
    t_seq_tri = copy.deepcopy(seq_tri)
    t_seq_pai = copy.deepcopy(seq_pai)
    t_roc = copy.deepcopy(roc)
    t_qua = copy.deepcopy(qua)
    t_tri = copy.deepcopy(tri)
    t_seq = copy.deepcopy(seq)
    t_pai = copy.deepcopy(pai)
    t_sin = copy.deepcopy(sin)

    #Bug17 2,W
    pool = []    #contain all the sins and pairs
    for ite in roc:
        t_pai.append(ite[:])

    for ite in t_pai:
        pool.append(ite[:])
    for ite in t_sin:
        pool.append(ite[:])

    if debug <= 6:
        print "########Find_a_play begin#######"
    #1
    if not step1_plane_pairs(plane,t_seq_tri,pool):
        if debug <= 6:
            print "step1_plane_pairs failed"
            return False

    #2
    if not step2_plane_singles(plane,t_seq_tri,pool):
        if debug <= 6:
            print "step2_plane_singles failed"
            return False

    #2.5
    if not step2_small_plane_sins(plane,t_seq_tri,pool):
        if debug <= 6:
            print "step 2.5 failed"
            return False

    #3
    if not step3_qua_two(qua_two,t_qua,pool):
        if debug <= 6:
            print "step 3 failed"
            return False

    #4 rule changed: 3,4 - > qua two

    #############2 special cases as the question example!#########
    #4.5 special case: qua get another single from seq:
    #   e.g.,333355 678910 -> 3333510,56789
    #4.6 special case: small planes get another single from seq
    #   e.g.,33344455 678910 -> 333444510,56789
    
    #to conclude the above 2 special cases
    #Method is to let a 5+ seq return its first card or the last
    #card to the pool and start step2.5,step3,step4 and step5

    #have qua, small seq_tri and just have one
    #as: 333444 5 5678910 only one sin 5 in pool
    #True means discard the paired able card
    
    if len(t_qua) != 0 or (6 in map(len,t_seq_tri)):
        
        #bug 14 W and 2 not considerere
        if sum(map(len,pool)) == 1 and pool[0][0] != 20 and \
        pool[0][0] != 99:
            if not step4_big_seq_discard(t_seq,pool,True):
                if debug <= 6:
                    print "step 4.5 failed"
                    return False
            step2_small_plane_sins(plane,t_seq_tri,pool)
            step3_qua_two(qua_two,t_qua,pool)
    ##########end 4.5 4.6 Special cases#########################

    #5
    if not step5_small_plane_pair(plane,t_seq_tri,pool):
        if debug <= 6:
            print "Step 5 failed"
            return False

    #6 #7
    if not step6_tri_sin_pai(tri_one,t_tri,pool):
        if debug <= 6:
            print "Step 6,7 failed"
            return False


    #8 give this play!
    final = []

    final = final + plane + t_seq_tri + t_seq_pai + qua_two + tri_one\
    + t_qua + t_tri + t_seq + pool

    result = sorted(final)
    report.append(result)

    #Give the result combination
    if debug <= 9:
        print "######find_a_play finished:######"
        print len(final)
        show(final)
        print
    
    
    return True
##############end find_a_play###################


def find_all_plays():
    '''
    Offer all possible optimal plays!
    '''
    #Here goes a serises of plays by priority as below:
    #as find a play
    #The distinguish is the permutations for all the possibel 
    #case that every sin and pair can be selected to combine.

    global seq
    global roc
    global qua
    global tri
    global pai
    global sin
    global seq_tri
    global seq_pai
    
    global report
    global result

    min= len(result)
    bad_count = 0 # to record how many bad result drieved
    bad_result = []
    final_set = [] # to record every different final plays with minimum turns

    if debug <= 7:
        print "\n"
        print "#####find_all_plays begin######"

    pp = []
    pool= []
    pool_per_set = []
    #enhancement 1
    d_pool = []
    #Bug 23
    for ite in pai:
        pp.append(ite[:])
    for ite in sin:
        pp.append(ite[:])
    #Bug17 2,W
    for ite in roc:
        pp.append(ite[:])

    cp_pp = copy.deepcopy(pp) #record the original pp
    #enhancement 1 decrease permutations
    necessary_num = len(qua)*2 + len(tri) + sum(map(len,seq_tri))
    
    per_num = len(pp)
    if per_num >= necessary_num:
        per_num = necessary_num
    #logically the per_num <= 5 in 17 cards

    #enhancement 1
    if per_num != 0:
        pool_per_set = list(itertools.permutations(pp,per_num))
        for i in range(len(pool_per_set)):
            pool_per_set[i] = list(pool_per_set[i])
    else:
        pool_per_set = [pp]  #no need to do permutations since no tri,seq_tri or qua
      
    #Permutations Circle to find every possible optimal plays:
    for i in range(len(pool_per_set)):
        pool = pool_per_set[i]
        #enhancement 1
        d_pool = copy.deepcopy(pool) #BUG 19 
         
        cp_pp = copy.deepcopy(pp) 
        #Bug23 bad results due to partial pool
        remove_pack(cp_pp,d_pool)
        for item in cp_pp:
            pool.append(item[:])

        if len(pool) != len(pp) and debug <=6:
            print "pool length error"
            return False


        plane = []     #seq_tri plus same numbers of pairs or singles
        qua_two = []   #quadruplet with 2 cards
        tri_one = []   #triplet plus one card or pair
        #Bug 23
        t_seq_tri = copy.deepcopy(seq_tri)
        t_seq_pai = copy.deepcopy(seq_pai)
        t_roc = copy.deepcopy(roc)
        t_qua = copy.deepcopy(qua)
        t_tri = copy.deepcopy(tri)
        t_seq = copy.deepcopy(seq)
        t_pai = copy.deepcopy(pai)
        t_sin = copy.deepcopy(sin)

        #1
        if not step1_plane_pairs(plane,t_seq_tri,pool):
            if debug <= 6:
                print "step1_plane_pairs failed"
                return False

        #2
        if not step2_plane_singles(plane,t_seq_tri,pool):
            if debug <= 6:
                print "step2_plane_singles failed"
                return False

        #2.5
        if not step2_small_plane_sins(plane,t_seq_tri,pool):
            if debug <= 6:
                print "step 2.5 failed"
                return False

        #3
        if not step3_qua_two(qua_two,t_qua,pool):
            if debug <= 6:
                print "step 3 failed"
                return False
        
        ##  find_all
        #############2 special cases as the question example!#########
        #4.5 special case: qua get another single from seq:
        #   e.g.,333355 678910 -> 3333510,56789
        #4.6 special case: small planes get another single from seq
        #   e.g.,33344455 678910 -> 333444510,56789

        #have qua, small seq_tri and just have one
        #as: 333444 5 5678910 only one sin 5 in pool
        #True means discard the paired able card
        if len(t_qua) != 0 or (6 in map(len,t_seq_tri)):
            #bug 14 W and 2 not considerere
            if sum(map(len,pool)) == 1 and pool[0][0] != 20 and \
            pool[0][0] != 99:
                
                if not step4_big_seq_discard(t_seq,pool,False):
                    if debug <= 6:
                        print "step 4.5 failed"
                        return False
                step2_small_plane_sins(plane,t_seq_tri,pool)
                step3_qua_two(qua_two,t_qua,pool)
        ##########end 4.5 4.6 Special cases#########################

        #5
        if not step5_small_plane_pair(plane,t_seq_tri,pool):
            if debug <= 6:
                print "Step 5 failed"
                return False

        #6 #7
        if not step6_tri_sin_pai(tri_one,t_tri,pool):
            if debug <= 6:
                print "Step 6,7 failed"
                return False
                       
        #8 give this play!
        final = []
        final = final + plane + t_seq_tri + t_seq_pai + qua_two + tri_one\
        + t_qua + t_tri + t_seq + pool
        
        f_same = False

        if len(final) > min:
            if debug <= 8:
                print "This is not a optimized final"
                show(final)
                return False

        elif len(final) == min:
            #sort every item and compare Bug 16
            s_final = sorted(map(sorted,final))
            #Bug21 repeated result
            for item in report:
                if s_final == sorted(map(sorted,item)):
                    f_same = True
                    break
            if not f_same:
                final_set.append(final)
                report.append(final)
        else: 
            if debug <= 8:
                print "here find a better solution?!IMPOSSIBLE!"
                print "len(final)",len(final)
                show(final)
                print
                print "The preious result is"
                print len(result)
                show(result)
                print
                print "find_all ERROR"
                return False
    #end circle of permutations of sins and pairs
    

    if debug <= 9:
        print "########find_all finished##########"
        print "find_all found  %d other possible plays"%(len(final_set))

        for i in range(len(final_set)):
            show(final_set[i])
            print 

    final_set = []


    return True
##############end find_all_plays##################


def find_more():
    '''
    Offer all possible optimal plays!
    By analysis..
    '''
    global roc
    global qua
    global tri
    global pai
    global sin
    global seq_tri
    global seq_pai
    
    global result
    global report
    global factor
    min = len(result)
    find_more_set = []

    if debug <= 7:
        print "\n"
        print "********find_more begin******"
        print "report now is ",report
        print "min play turn is",min
    pp = []   #the previous sins and pais
    pool= []  #After permutations(pp,per_num),the per_num sins and pais
    #enhancement 1
    d_pool = [] #The different need to del from pp
    pool_per_set = []  #All the permutations result put in here [(),(),()...]
    

    for ite in pai:
        pp.append(ite[:])
    for ite in sin:
        pp.append(ite[:])
    #Bug17 2,W
    for ite in roc:
        pp.append(ite[:])
    
    cp_pp = copy.deepcopy(pp)
    #enhancement 1 decrease permutations
    necessary_num = len(qua)*2 + len(tri) + sum(map(len,seq_tri))
    
    per_num = len(pp)
    if per_num >= necessary_num:
        per_num = necessary_num
    #logically the per_num <= 5 in 17 cards

    #enhancement 1
    if per_num != 0:
        pool_per_set = list(itertools.permutations(pp,per_num))
        for i in range(len(pool_per_set)):
            pool_per_set[i] = list(pool_per_set[i])#[(),(),...] --->[[],[],...]
    else:
        pool_per_set = [pp]  #no need to do permutations since no tri,seq_tri or qua
        
    if debug <= 6:
        print "Find more start!"
        print "all the set of sins and pairs are:"
        print pool_per_set

    #Permutations Circle to find every possible optimal plays:
    for i in range(len(pool_per_set)):
        pool = pool_per_set[i]
        #enhancement 1
        d_pool = pool[:] #record to del from the pp

        #Bug23
        cp_pp = copy.deepcopy(pp)
        remove_pack(cp_pp,d_pool)
        for item in cp_pp:
            pool.append(item[:])

        if len(pool) != len(pp) and debug <=6:
            print "find more permutation error"
            return False

        plane = []     #seq_tri plus same numbers of pairs or singles
        qua_two = []   #quadruplet with 2 cards
        tri_one = []   #triplet plus one card or pair
        #Bug 23
        t_seq_tri = copy.deepcopy(seq_tri)
        t_seq_pai = copy.deepcopy(seq_pai)
        t_roc = copy.deepcopy(roc)
        t_qua = copy.deepcopy(qua)
        t_tri = copy.deepcopy(tri)
        t_seq = copy.deepcopy(seq)
        t_pai = copy.deepcopy(pai)
        t_sin = copy.deepcopy(sin)

        #1
        if not step1_plane_pairs(plane,t_seq_tri,pool):
            if debug <= 6:
                print "step1_plane_pairs failed"
                return False

        #2
        if not step2_plane_singles(plane,t_seq_tri,pool):
            if debug <= 6:
                print "step2_plane_singles failed"
                return False

        #2.5
        random.shuffle(t_seq_tri)
        if not step2_small_plane_sins(plane,t_seq_tri,pool):
            if debug <= 6:
                print "step 2.5 failed"
                return False

        #3
        random.shuffle(t_qua)
        if  not step3_qua_two(qua_two,t_qua,pool):
            if debug <= 6:
                print "step 3 failed"
                return False
        

        #4.5
        #True means discard the paired able card
        if len(t_qua) != 0 or (6 in map(len,t_seq_tri)):
            
            #bug 14 W and 2 not considerere
            if sum(map(len,pool)) == 1 and pool[0][0] != 20 and \
            pool[0][0] != 99:
                if not step4_big_seq_discard(t_seq,pool,False):
                    if debug <= 6:
                        print "step 4.5 failed"
                        return False
                step3_qua_two(qua_two,t_qua,pool)
                #notice
                #here the order is different form the find_a_play
                step2_small_plane_sins(plane,t_seq_tri,pool)
        ##########end 4.5 4.6 Special cases#########################

        #5
        random.shuffle(t_seq_tri)
        if not step5_small_plane_pair(plane,t_seq_tri,pool):
            if debug <= 6:
                print "Step 5 failed"
            return False

        #6 #7
        #for more anwsers
        random.shuffle(t_tri)
        if not step6_tri_sin_pai(tri_one,t_tri,pool):
            if debug <= 6:
                print "Step 6,7 failed"
            return False

        #8 give this play!
        final = []
        f_same = False

        final = final + plane + t_seq_tri + t_seq_pai + qua_two + tri_one\
        + t_qua + t_tri + t_seq + pool

        if len(final) == min:
            s_final = sorted(map(sorted,final)) #for sorted purpose
            for item in report:
                if s_final == sorted(map(sorted,item)):
                    f_same = True
                    break
            if not f_same:
                report.append(final)
                find_more_set.append(final)
        elif len(final) < min: # A better solution finded
            if debug <=9:
                print "find_more find a better solution?!IMPOSSIBLE!"
                print "len(final)",len(final)
                show(final)
                print
                print "compare to the result"
                print len(result)
                show(result)
                print
            #return False
            #break
            result = copy.deepcopy(final)
            find_more_set = []
            report = []
            report.append(final)
            find_more_set.append(final)
            min = len(final)
        else:
            continue

    #end circle of random of tri seq_tri..
    

    if len(find_more_set) != 0 and debug <= 9:

        print "****find_more finished*******"
        print "find_more ended with %d more solution:" \
        %(len(find_more_set))
        for i in range(len(find_more_set)):
            show(find_more_set[i])
            print 
        print "end\n"

    return True

#################end find_more##################################

#analysis to find if has different types not played:

def save_all_possible(all_cards):
    '''
    find out differnet types
    '''
    global qua
    global seq_tri
    global seq_pai
    global seq
    global tri
    global pai

    cp_all_cards = all_cards[:]
    
    find_qua(all_cards)
    all_cards = cp_all_cards[:]

    find_seq_tri(all_cards)
    all_cards = cp_all_cards[:]

    find_seq(all_cards)
    all_cards = cp_all_cards[:]

    find_seq_pai(all_cards)
    all_cards = cp_all_cards[:]

    find_tri(all_cards)
    all_cards = cp_all_cards[:]
    
    find_pai(all_cards)
    all_cards = cp_all_cards[:]

#######end save_all_possible##########
#en 2 
def find_more_better():
    '''
    After analyze of previous result and all possible types
    to detect better solutions 
    '''

    global roc
    global tri
    global pai
    global sin
    global seq
    global seq_tri
    global seq_pai
    global qua

    global ori_pack
    global lef_pack
    global arr
    global report
    global result #the best result

    global n_need
    global n_give
    global factor
    global f_better

    f_better = True
    if debug >= 15:
        print "#########find_more_better,begin"

    lef_pack = sorted(ori_pack[:])
    find_better_set = []
    pre_report = report
    min = len(result)

    #analysis previous reslut
    n_need = sum(map(len,seq_tri))/3 + len(qua)*2 + len(tri)
    n_give = sum(map(len,pai)) + sum(map(len,roc)) + len(sin)

    #compare to all possible pack types
    #to call for the types that were not played
    pre_qua = qua[:]
    pre_seq_tri = seq_tri[:]
    pre_seq_pai = seq_pai[:]
    pre_tri = tri[:]
    pre_pai = pai[:]
    pre_seq = seq[:]
    pre_sin = sin[:]

    save_all_possible(lef_pack[:])

    try_qua = False
    try_tri = False
    try_pai = False
    try_seq = False
    try_seq_tri = False
    try_seq_pai = False

    if len(qua) != 0 and len(pre_qua) == 0:
        try_qua = True
        n_need = n_need + len(qua)*2
    if len(tri) != 0 and len(pre_tri) == 0:
        try_tri = True
        n_need = n_need + len(tri)
    if len(pai) != 0 and len(pre_pai) == 0:
        try_pai = True
    if len(seq) != 0 and len(pre_seq) == 0:
        try_seq_ = True
    if len(seq_tri) != 0 and len(pre_seq_tri) == 0:
        try_seq_tri = True
        n_need = n_need + sum(map(len,seq_tri))/3
    if len(seq_pai) != 0 and len(pre_seq_pai) == 0:
        try_seq_pai = True

    if n_need > n_give or try_qua or try_seq_tri\
    or try_seq_pai or try_tri or try_pai:
        pass
    else:
        if debug >=15:
            print "no needed find_more_better"
        return True

    max_tri = len(tri)
    max_seq_tri = len(seq_tri)
    max_seq = len(seq)
    max_qua = len(qua)
    max_pai = len(pai)

    if len(seq) != 0:
        max_seq_length = max(map(len,seq))
    else:
        max_seq_length = 0

    if len(seq_pai)!= 0:
        max_seq_pai_len = max(map(len,seq_pai))
    else:
        max_seq_pai_len = 0
    if len(seq_tri)!= 0:
        max_seq_tri_len = max(map(len,seq_tri))
    else:
        max_seq_pai_len = 0
    #e.g 4444 8888 AA ->444488AA,88 j circle find->888844AA,44
    #*pai_factor  means double loop if pai is exsited
    
    pai_factor = 1
    if max_pai != 0:
        pai_factor = 2

    max_num = max(max_tri,max_seq,max_seq_tri,max_qua,max_pai)
    if max_num == 0:
        max_num = 1

    loop_factor = 2
    if n_need != 0:
        loop_factor = n_need

    loop_n = loop_factor * max_num * pai_factor
    if debug >= 15:
        print "find_more_better will loop %d times"%(loop_n)

    #--------loop j started-------------------------------
    for j in range(loop_n): 
        if debug >= 16:
            print "j=%d"%(j)

        clear()        #clear all the basic types global storage
        qua_two = []
        plane = []
        tri_one = []
        lef_pack = ori_pack[:] #[3,4,5,5,6,7]
        put_to_arr(sorted(lef_pack))
        
        len_pack = len(lef_pack)   
        
        if debug >= 15:
            print "find_more_better %d times,started with"%(j)
            print lef_pack

        #the X factor!
        for i in range(loop_factor):
            x = random.randint(1,6)

            if try_pai:
                find_pai(lef_pack,i%max_pai,j)

            if try_tri:
                find_tri(lef_pack,i%max_tri,j)

            if x <= 2 or try_qua: # True mean need to find this type
                if max_qua != 0:
                    find_qua(lef_pack,j%max_qua,j)
            elif max_qua > 3:
                find_pai(lef_pack,j%max_qua,j)
                    
            if (x >= 2 and x <= 4) or try_seq:
                if max_seq_length - n_need > 0:
                    find_seq(lef_pack,j%(max_seq_length - n_need),j)

            if x == 1 or x == 6 or try_seq_tri:
                if max_seq_tri != 0:
                    find_seq_tri(lef_pack,j%(max_seq_tri_len),j)

            if x < 2 or x == 6 or try_seq_pai or try_tri:
                if max_seq_pai_len != 0 and x<2 and max_pai/2 - n_need>0:
                    find_seq_pai(lef_pack,j%(max_pai/2-n_need),j)

            if x >= 3 or try_tri:
                if max_tri != 0:
                    find_tri(lef_pack,j%max_tri,j)
                else:
                    find_tri(lef_pack,j,j)

            if j%2 == 0 and (x > 3 or try_pai):#half loop a pai is called for
                find_pai(lef_pack,(j + 1)%(max_pai),j)

            if j%3 == 0 and try_tri:
                find_tri(lef_pack,(j+1)%(max_tri),j)

        if debug >= 15:
            if len(lef_pack) + sum(map(len,seq_tri)) + sum(map(len,seq_pai))\
            + sum(map(len,qua)) + sum(map(len,tri)) + sum(map(len,pai)) +\
            sum(map(len,sin)) + sum(map(len,seq))!= len_pack:
                print "ERROR of numbers of lec_pack,in find_more_better"
                print "len(lef_pack):%d + seq_tri:%d + seq_pai:%d +,qua):%d\
                + tri:%d +pai:%d + sin:%d + seq:%d != len_pack:%d"\
               %(len(lef_pack), sum(map(len,seq_tri)),sum(map(len,seq_pai))\
               , sum(map(len,qua)), sum(map(len,tri)), sum(map(len,pai)),\
               sum(map(len,sin)),sum(map(len,seq)),len_pack)

                print "len_pack",len_pack
                return False

     #---find types as before--------       
        find_types(lef_pack)

     #-----play those cards----------------
        t_seq_tri = copy.deepcopy(seq_tri)
        t_seq_pai = copy.deepcopy(seq_pai)
        t_roc = copy.deepcopy(roc)
        t_qua = copy.deepcopy(qua)
        t_tri = copy.deepcopy(tri)
        t_seq = copy.deepcopy(seq)
        t_pai = copy.deepcopy(pai)
        t_sin = copy.deepcopy(sin)

        pool = []    #contain all the sins and pairs
        for ite in roc:
            t_pai.append(ite[:])
        for ite in t_pai:
            pool.append(ite[:])
        for ite in t_sin:
            pool.append(ite[:])

        #en12
        random.shuffle(pool)
        #here may have en13 for disorder below steps:
        #anyway,result is enough good by now..
        #1
        if not step1_plane_pairs(plane,t_seq_tri,pool):
            if debug >= 15 or debug <= 6:
                print "step1_plane_pairs failed in find_more_better"
                return False

        #2
        if not step2_plane_singles(plane,t_seq_tri,pool):
            if debug >= 15 or debug <= 6:
                print "step2_plane_singles failed in find_more_better"
                return False

        #2.5
        if not step2_small_plane_sins(plane,t_seq_tri,pool):
            if debug >= 15 or debug <= 6:
                print "step 2.5 failed in find_more_better"
                return False

        #3
        if  not step3_qua_two(qua_two,t_qua,pool):
            if debug >= 15 or debug <= 6:
                print "step 3 failed in find_more_better"
                return False
        
        #5
        if not step5_small_plane_pair(plane,t_seq_tri,pool):
            if debug >= 15 or debug <= 6:
                print "Step 5 failed in find_more_better"
                return False

        #6 #7
        if not step6_tri_sin_pai(tri_one,t_tri,pool):
            if debug >= 15 or debug <= 6:
                print "Step 6,7 failed in find_more_better"
                return False


        #8 Will a better final find in find_more_better?
        #let's see
        final = []
        s_final = []
        f_same = False

        final = final + plane + t_seq_tri + t_seq_pai + qua_two + tri_one\
        + t_qua + t_tri + t_seq + pool
        
        if sum(map(len,final)) != len(ori_pack):
            if debug <= 1 or debug >=15:
                print "ERROR"
                print "cards lost"
                print "final",final
                print "ori_pack",ori_pack
                #return False
                continue #This result is discarded

        if len(final) == min:
            s_final = sorted(map(sorted,final)) 
            for item in report:
                if s_final == sorted(map(sorted,item)):
                    f_same = True
                    break
            if not f_same:
                report.append(final)
        elif len(final) < min: # A better solution finded
            min = len(final)
            if debug >= 15:
                print "Better one find!"
                print "len(final)",len(final)
                show(final)
                print
                print "compare to the result"
                print len(result)
                show(result)
                print
            #refresh new results
            result = copy.deepcopy(final)
            find_better_set = []
            report = []
            report.append(final)
            find_better_set.append(final)
    
    #--------loop j ended-------------------------------------
    if debug >= 15:
        print "find_more_better ended"


    if len(find_better_set) != 0 and debug >= 15:
        print "find_more found %d more plays!:" \
        %(len(find_better_set))
        for i in range(len(find_better_set)):
            show(find_better_set[i])
            print 

        print "end\n"
        print "compared to previous result:"
        for i in range(len(pre_report)):
            show(pre_report[i])
            print 
        print "Good Luck!"
        

    return True
##############end find_more_better########################

def PlayCard(cards,debugLv = 10,factor = 7):
    '''
    input  formated cards like ['W','Q','J','2','3']
    output the possible every plays of minimum turns
    '''

    global ori_pack
    global lef_pack
    global debug 
    global report
    global seq
    global pai
    global sin
    global qua
    global tri
    global seq_tri

    init_globals()

    debug = debugLv
    ori_pack = sorted(str_to_num(cards))
    lef_pack = ori_pack[:]
    put_to_arr(lef_pack)
    
    if not find_types(lef_pack):
        if debug <=1:
            print "Error during find_types"
            return False

    if not find_a_play():
        if debug <=1:
            print "Error to find a solution"
            return False


    if debug != 12:
        if not find_all_plays():
            if debug <=1:
                print "Error to find more solution"
                return False

    if debug != 12:
        for i in range(factor):
            if not find_more():
                if debug <=1:
                    print "Error to find MORE!"
                    return False


    #en 2 find_more_better
    for i in range(factor):
        if not find_more_better():
            if debug <=1:
                print "Error to find_more_better"
                return False

        
    show_status()

    if debug <= 9:
        print "factor = %d"%(factor)
    return True
#################end PlayCard##########


if __name__ == "__main__":

        
    s = raw_input(" ").strip()

    ori_pack = sorted(str_to_num(s.split(" ")))
    lef_pack = ori_pack[:] 
    deck = s.split(" ")
        
    if len(sys.argv) > 1:
        debug = int(sys.argv[1])
    else:
        debug = 10 #trace turn off by default
    if len(sys.argv) > 2:
        factor = int(sys.argv[2])
    else:
        factor = 7 

        
    PlayCard(deck,debug,factor)

