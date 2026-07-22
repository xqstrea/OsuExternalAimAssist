def offsets(hits, speed, arMS):
    offsets = []
    spinner_offset = 400
    delay: int

    if hits[0]["obj_type"] & 8: 
        if speed == "DT":
            delay = (spinner_offset * 2) / 3
        elif speed == "NM":
            delay = spinner_offset
        elif speed == "HT": 
            delay = delay = (spinner_offset * 4) / 3
    else:
        delay = arMS

    if speed == "NM":
        for hit in hits:
            off = (hit["time"] - (hits[0]["time"] )) #+ delay
            offsets.append(off)

    elif speed == "DT":
        for hit in hits:
            off = (((hit["time"] * 2 ) / 3) - ((hits[0]["time"] * 2 ) / 3)) + delay
            offsets.append(off)

    elif speed == "HT":
        for hit in hits:
            off = (((hit["time"] * 4 ) / 3) - ((hits[0]["time"] * 4 ) / 3)) + delay
            offsets.append(off)

    return offsets
