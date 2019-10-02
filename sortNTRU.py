'''
wrapper to assist a future change of sorting method
'''


def sortIrisLinesForClient(iris_lines):
    """ we need to shift the iris code before sorting/rearranging it """
    """ optimised for iris codes composed of 10*512 bits """
    __sorted_list = []
    # sectors right and left (0347)
    # lines 647523
    __sorted_list += iris_lines[6][0:64]
    __sorted_list += iris_lines[6][192:320]
    __sorted_list += iris_lines[6][448:512]
    __sorted_list += iris_lines[4][0:64]
    __sorted_list += iris_lines[4][192:320]
    __sorted_list += iris_lines[4][448:512]
    __sorted_list += iris_lines[7][0:64]
    __sorted_list += iris_lines[7][192:320]
    __sorted_list += iris_lines[7][448:512]
    __sorted_list += iris_lines[5][0:64]
    __sorted_list += iris_lines[5][192:320]
    __sorted_list += iris_lines[5][448:512]
    __sorted_list += iris_lines[2][0:64]
    __sorted_list += iris_lines[2][192:320]
    __sorted_list += iris_lines[2][448:512]
    __sorted_list += iris_lines[3][0:64]
    __sorted_list += iris_lines[3][192:320]
    __sorted_list += iris_lines[3][448:512]
    # sectors top and bot (1256)
    # lines 564273
    __sorted_list += iris_lines[5][64:192]
    __sorted_list += iris_lines[5][320:448]
    __sorted_list += iris_lines[6][64:192]
    __sorted_list += iris_lines[6][320:448]
    __sorted_list += iris_lines[4][64:192]
    __sorted_list += iris_lines[4][320:448]
    __sorted_list += iris_lines[2][64:192]
    __sorted_list += iris_lines[2][320:448]
    __sorted_list += iris_lines[7][64:192]
    __sorted_list += iris_lines[7][320:448]
    __sorted_list += iris_lines[3][64:192]
    __sorted_list += iris_lines[3][320:448]
    # lines 8 and 9
    # first sectors right and left, then top and bot
    __sorted_list += iris_lines[8][0:64]
    __sorted_list += iris_lines[8][192:320]
    __sorted_list += iris_lines[8][448:512]
    __sorted_list += iris_lines[9][0:64]
    __sorted_list += iris_lines[9][192:320]
    __sorted_list += iris_lines[9][448:512]
    __sorted_list += iris_lines[8][64:192]
    __sorted_list += iris_lines[8][320:448]
    __sorted_list += iris_lines[9][64:192]
    __sorted_list += iris_lines[9][320:448]
    # lines 1 and 0 complete
    __sorted_list += iris_lines[1]
    __sorted_list += iris_lines[0]

    return __sorted_list


def sortIrisBitsForServer(iris_bits):
    """ sorts bits, and returns a list with all sorted bits """
    """ optimised for iris codes composed of 10*512 bits """
    __sorted_list = []  # sorted list
    
    """sectors left and right 0347"""
    # row 6 sectors 0347
    __sorted_list += iris_bits[3072:3136]
    __sorted_list += iris_bits[3264:3392]
    __sorted_list += iris_bits[3520:3584]
    # row 4 sectors 0347
    __sorted_list += iris_bits[2048:2112]
    __sorted_list += iris_bits[2240:2368]
    __sorted_list += iris_bits[2496:2560]
    # row 7 sectors 0347
    __sorted_list += iris_bits[3584:3648]
    __sorted_list += iris_bits[3776:3904]
    __sorted_list += iris_bits[4032:4096]
    # row 5 sectors 0347
    __sorted_list += iris_bits[2560:2624]
    __sorted_list += iris_bits[2752:2880]
    __sorted_list += iris_bits[3008:3072]
    # rows 2-3 sectors 0347
    __sorted_list += iris_bits[1024:1088]
    __sorted_list += iris_bits[1216:1344]
    __sorted_list += iris_bits[1472:1600]
    __sorted_list += iris_bits[1728:1856]
    __sorted_list += iris_bits[1984:2048]
    """sectors top and bot 1256"""
    # row 5 sectors 1256
    __sorted_list += iris_bits[2624:2752]
    __sorted_list += iris_bits[2880:3008]
    # row 6 sectors 1256
    __sorted_list += iris_bits[3136:3264]
    __sorted_list += iris_bits[3392:3520]
    # row 4 sectors 1256
    __sorted_list += iris_bits[2112:2240]
    __sorted_list += iris_bits[2368:2496]
    # row 2 sectors 1256
    __sorted_list += iris_bits[1088:1216]
    __sorted_list += iris_bits[1344:1472]
    # row 7 sectors 1256
    __sorted_list += iris_bits[3648:3776]
    __sorted_list += iris_bits[3904:4032]
    # row 3 sectors 1256
    __sorted_list += iris_bits[1600:1728]
    __sorted_list += iris_bits[1856:1984]
    """most outer rows at the end"""
    # rows 8-9 sectors 0347
    __sorted_list += iris_bits[4096:4160]
    __sorted_list += iris_bits[4288:4416]
    __sorted_list += iris_bits[4544:4672]
    __sorted_list += iris_bits[4800:4928]
    __sorted_list += iris_bits[5056:5120]
    # row 8 sectors 1256
    __sorted_list += iris_bits[4160:4288]
    __sorted_list += iris_bits[4416:4544]
    # row 9 sectors 1256
    __sorted_list += iris_bits[4672:4800]
    __sorted_list += iris_bits[4928:5056]
    # row 1 complete
    __sorted_list += iris_bits[512:1024]
    # row 0 complete
    __sorted_list += iris_bits[:512]
    
    return __sorted_list
