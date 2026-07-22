def parse_hitobjects(map_content):
    circles = []

    parsing = False
    for line in map_content.splitlines():
        if line.strip() == "[HitObjects]":
            parsing = True
            continue

        if parsing and line.strip():
            parts = line.split(",")
            
            x = round(int(parts[0]) * 2.25 + 384)
            y = round(int(parts[1]) * 2.25 + 126)
            time = int(parts[2])
            obj_type = int(parts[3])

            if obj_type & 1:
                circles.append({
                    "x": x,
                    "y": y,
                    "time": time,
                    "obj_type" : obj_type,
                })


            elif obj_type & 2:
                slider_data = parts[5].split("|")
                repeats = int(parts[6])
                pixel_length = float(parts[7])

                circles.append({
                    "x": x,
                    "y": y,
                    "time": time,
                    "obj_type" : obj_type,
                    "slider_data" : slider_data,
                    "repeats" : repeats,
                    "pixel_length" : pixel_length
                })

            elif obj_type & 8:
                spinner_end = int(parts[5])

                circles.append({
                    "x": x,
                    "y": y,
                    "time": time,
                    "obj_type" : obj_type,
                    "spinner_end": spinner_end
                })


    return circles

def parse_timingPoints(map_content):
    timing_points = []
    parsing = False

    for line in map_content.splitlines():
        if line.strip() == "[TimingPoints]":
            parsing = True
            continue

        if line.strip() == "[Colours]":
            break

        if parsing and line.strip():
            parts = line.split(",")

            offset = int(float(parts[0]))          
            beat_length = float(parts[1])          
            meter = int(parts[2])
            is_bpm = int(parts[6])      

            timing_points.append({
                "offset": offset,
                "beat_length": beat_length,
                "meter": meter,
                "is_bpm": is_bpm,
            })

    return timing_points

def parse_stats(map_content):
    stats = {}
    parsing = False

    for line in map_content.splitlines():
        if  line.strip() == "[Difficulty]":
            parsing = True
            continue

        if parsing and ":" in line:
            key, value = line.split(":", 1)
            stats[key] = value

    return stats

    


