#!/usr/bin/env python3

# Copyright (c) 2018 Marco Zollinger <marco@freelabs.space>


def ca_code_gen(sv):
    """GPS coarse acquisition (C/A) code generator (gold code)
    
    Arguments:
    sv -- space vehicle PRN number
    Returns:
    infinite symmetric C/A code sequence as generator for a single int (-1/1)
    """
    # Initialization constants for LFSR-2 (init code implementation)
    init_codes = {1:  [1, 1, 1, 1, 1, 0, 1, 1, 0, 0],  # SV:1
                  2:  [1, 1, 1, 1, 0, 1, 1, 0, 0, 0],  # SV:2
                  3:  [1, 1, 1, 0, 1, 1, 0, 0, 0, 0],  # SV:3
                  4:  [1, 1, 0, 1, 1, 0, 0, 0, 0, 0],  # SV:4
                  5:  [0, 0, 1, 0, 0, 1, 0, 1, 1, 0],  # SV:5
                  6:  [0, 1, 0, 0, 1, 0, 1, 1, 0, 0],  # SV:6
                  7:  [0, 1, 1, 0, 0, 1, 0, 1, 1, 0],  # SV:7
                  8:  [1, 1, 0, 0, 1, 0, 1, 1, 0, 0],  # SV:8
                  9:  [1, 0, 0, 1, 0, 1, 1, 0, 0, 0],  # SV:9
                  10: [1, 1, 0, 1, 1, 1, 0, 1, 0, 0],  # SV:10
                  11: [1, 0, 1, 1, 1, 0, 1, 0, 0, 0],  # SV:11
                  12: [1, 1, 1, 0, 1, 0, 0, 0, 0, 0],  # SV:12
                  13: [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],  # SV:13
                  14: [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # SV:14
                  15: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # SV:15
                  16: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # SV:16
                  17: [1, 0, 0, 0, 1, 0, 0, 1, 1, 0],  # SV:17
                  18: [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],  # SV:18
                  19: [0, 0, 1, 0, 0, 1, 1, 0, 0, 0],  # SV:19
                  20: [0, 1, 0, 0, 1, 1, 0, 0, 0, 0],  # SV:20
                  21: [1, 0, 0, 1, 1, 0, 0, 0, 0, 0],  # SV:21
                  22: [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # SV:22
                  23: [0, 0, 1, 1, 0, 0, 1, 1, 1, 0],  # SV:23
                  24: [1, 0, 0, 1, 1, 1, 0, 0, 0, 0],  # SV:24
                  25: [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # SV:25
                  26: [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # SV:26
                  27: [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # SV:27
                  28: [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # SV:28
                  29: [0, 0, 0, 1, 0, 1, 0, 1, 1, 0],  # SV:29
                  30: [0, 0, 1, 0, 1, 0, 1, 1, 0, 0],  # SV:30
                  31: [0, 1, 0, 1, 0, 1, 1, 0, 0, 0],  # SV:31
                  32: [1, 0, 1, 0, 1, 1, 0, 0, 0, 0]}  # SV:32

    # LFSR-1: init with all 1, feedback taps @3, 10
    lfsr1 = lfsr([1] * 10, [0, 0, 1, 0, 0, 0, 0, 0, 0, 1])

    # LFSR-2: init with init code, feedback taps @2, 3, 6, 8, 9, 10
    lfsr2 = lfsr(init_codes[sv], [0, 1, 1, 0, 0, 1, 0, 1, 1, 1])

    while True:
        asymmetric = next(lfsr1) ^ next(lfsr2)
        yield {0: -1, 1: 1}[asymmetric]


def lfsr(seed, taps):
    """Linear feedback shift register with arbitrary length for PRN sequence
    
    Arguments:
    seed -- initialisation seed as list of int (0/1)
    taps -- position of feedback taps as list of int (0/1)
    Returns:
    infinite LFSR output as generator for a single int (0/1)
    """
    state = seed
    while True:
        feedback = 0
        for bit, tap in zip(state, taps):
            if tap == 1:
                feedback ^= bit
        state.insert(0, feedback)
        yield state.pop()


# Output the first 10 C/A chips for each of the 32 SVs
if __name__ == "__main__":
    for sv_no in range(1, 33):
        gen = ca_code_gen(sv_no)
        chips = []
        for i in range(10):
            chips.append(next(gen))
        print("SV PRN: {:>2}, first 10 chips: {}".format(sv_no, chips))
