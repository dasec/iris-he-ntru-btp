"""client for efficient NTRU iris recognition"""
from irisNTRU import IRIS
from sortNTRU import sortIrisLinesForClient


class CLIENT(object):
    """docstring for client"""
    def __init__(self, public_ring, public_key):
        super(CLIENT, self).__init__()
        self.ring = public_ring
        self.pk = public_key
        
    def CLIENTencryptProbe(self, id):
        # open file
        probe_shifted = []
        icode = IRIS.readIrisLinesFromFile(IRIS, id[0], id[1])
        tmp = sortIrisLinesForClient(icode)
        probe_shifted += (IRIS.encryptBlocks(IRIS, self.pk, self.ring, tmp))

        # shift & encrypt
        if IRIS.NRSHIFTS > 1:
            for i in range(1, IRIS.NRSHIFTS >> 1 | 1):
                tmp = sortIrisLinesForClient(IRIS.shiftIrisCode(IRIS, icode, -i))  # shift -i
                probe_shifted += (IRIS.encryptBlocks(IRIS, self.pk, self.ring, tmp))
                tmp = sortIrisLinesForClient(IRIS.shiftIrisCode(IRIS, icode, i))  # shift  i
                probe_shifted += (IRIS.encryptBlocks(IRIS, self.pk, self.ring, tmp))

        # return 17 encrypted probes
        icode.clear()
        tmp.clear()
        return probe_shifted

