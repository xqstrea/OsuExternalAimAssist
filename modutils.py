def arToMS(AR):
    ms: int
    if AR < 5: 
        ms = 1200 + (5 - AR) * 120

    elif AR == 5:
        ms = 1200

    else:
        ms = 1200 - (AR - 5) * 150
    return ms

def csRadiusToPX(CS):
    return (109 - (9 * CS)) / 2



def ARHR(AR):
    AR = min(AR * 1.4 , 10)
    return AR

def hrPos(hits):
    for hit in hits:
        y_HR = 384 - round((hit["y"] - 126) /2.25)
        hit["y"] = round(y_HR * 2.25 + 126)
    return hits

def csToHR(CS):
    return min(CS * 1.3, 10)



def AREZ(AR):
    return AR/2

def csToEZ(CS):
    return CS/2



def ARDT(AR):
    if AR > 5:
       AR = (2/3 * AR + 13/3) * 100
       AR = round(AR)
    else:
        AR = (5 + (8/15)*AR) * 100
        AR = round(AR)

    if AR / 100 < 11:
        return AR / 100
    else:
        return 11



def ARHT(AR):
    if AR > 5:
        AR = ((4/3 * AR) - 13/3) * 100
        AR = round(AR)
    else:
        AR = ((4/3 * AR) - 5) * 100
        AR = round(AR)
        
    return AR / 100
