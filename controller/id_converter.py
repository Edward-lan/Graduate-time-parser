def NCTU(number):
    # get the length of number
    length = len(number)
    if length == 9:
        number = number[1:3]
        number = "1" + number
    if length == 7:
        number = number[0:2]
        if(number[0]=="0"):
            number = "1" + number        
    return number

def NCU(number):
    if(number[0]=="1"):
        number = number[0:3]
    else:
        number = number[0:2]
    return number

def NTHU(number):
    if(number[0]=="1"):
        number = number[0:3]
    else:
        number = number[0:2]
    return number

def NYMU(number):
    number = number[1:3]
    if(number[0]=="0"):
        number = "1" + number
    return number


if __name__ == "__main__":
    # test nycu id 
    print(NCTU("310510176"))
    # test nctu id 
    print(NCTU("0560438"))
    # test nthu id
    print(NTHU("109064507"))
    
