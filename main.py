from Game import Game

def main():
    rawData = [3142, 1528,  560, 1026,  556, 1028,  556, 176,  642, 176,  638, 180,  640, 1026,  560, 176,  640, 176,  642, 1026,  556, 1032,  556, 172,  648, 1028,  556, 172,  646, 174,  644, 1028,  554, 1030,  554, 174,  644, 1026,  560, 1028, 
 552, 176,  644, 168,  650, 1024,  556, 178,  640, 178,  640, 174,  644, 1028,  558, 174,  644, 174,  642, 178,  642, 172,  642, 178,  644, 174,  642, 172,  644, 176,  640, 178,  640, 176,  642, 176,  640, 172,  646, 176,  640, 176,  642, 174,  644, 180,  
638, 176,  642, 180,  636, 178,  640, 176,  642, 1028,  554, 180,  636, 244,  576, 172,  644, 176,  642, 180,  638, 180,  638, 176,  642, 176,  638, 182,  638, 176,  642, 176,  642, 182,  634, 182,  638, 172,  646, 176,  642, 178,  638, 184,  634, 180,  636, 246,  572, 184,  610, 236,  608, 176,  614, 238,  578, 242,  602, 184,  610, 234,  586, 230,  584, 238,  602, 186,  610, 232,  584, 238,  578, 238,  604, 244,  574, 186,  606, 242,  580, 234,  580, 240,  582, 228,  586, 238,  578, 298,  522, 296,  526, 
230,  582, 246,  594, 244,  574, 244,  572, 246,  574, 246,  544, 304,  540, 250,  572, 242,  548, 300,  542, 244,  548, 300,  542, 244,  572, 250,  570, 242,  546, 302,  542, 1054,  530, 242,  546, 1082,  502, 302,  542, 242,  546, 1082,  502, 1084,  500, 302,  512]


    # Thresholds for short/long pulses (adjust as needed)
    SHORT_PULSE =   5200  # µs
    LONG_PULSE = 1000  # µs

    # Skip the header (first two values)
    rawData = rawData[2:]

    # Decode to binary
    binary_data = []
    for i in range(0, len(rawData) - 1, 2):  # Step through ON/OFF pairs
        on_time = rawData[i]
        off_time = rawData[i + 1]
        
        if off_time > LONG_PULSE:
            binary_data.append('1')  # Long OFF → Binary 1
        elif off_time < SHORT_PULSE:
            binary_data.append('0')  # Short OFF → Binary 0

    # Combine binary data
    binary_string = ''.join(binary_data)

    print("Decoded Binary Data:", binary_string)

    hex_code = hex(int(binary_string, 2))
    print("Hex Code:", hex_code)







if __name__ == "__main__":
    main()