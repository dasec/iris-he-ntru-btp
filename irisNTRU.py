from biometricNTRU import NTRUEncrypt


class IRIS(object):
    """docstring for IRIS"""
    """ helper functions and constant values for iris recognition with NTRU """
    # set path to iris codes, e.g.: PATH="../../IITD_IrisCodes/lg_%03d%02d.png.txt"
    PATH = "../../../dasec/databases/IITD_IrisCodes/lg_%03d%02d.png.txt"
    
    """ since this was written for LG/QSW feature extraction[1], we assume filenames with 5 digits """
    """ in format XXXYY with 3 digits (XXX) for subject nr and 2 digits (YY) sample nr with sample nr in the range """
    """ from 1 to 2*NREYES since samples from both eyes of one subject are successive """
    """ [1] http://wavelab.at/sources/USIT/ """
    
    NRTRAINING = 24  # nr of subjects in training set
    NRENROLMENT = 150  # nr of enrolled subjects
    NRIMPOSTER = 50  # nr of imposters
    NREYES = 5  # nr of samples / eye
    
    NRSHIFTS = 17  # nr of shifts (from -8 via 0 to +8) !! must be odd and mininum 1 !!
    SIZE_IRISCODE = 5120  # nr of total bits in iris code
    ROWS_IRISCODE = 10  # nr of rows in iris code
    BITSPERROW_IRISCODE = 512  # bits per row in iris code
    
    def __init__(self):
        super(IRIS, self).__init__()
    
    def encryptBlocks(self, pk, ring, m):
        c = []
        b = 0
        for block in range(0, self.SIZE_IRISCODE - ring.N, ring.N):
            c.append(NTRUEncrypt(ring, pk, m[block:block + ring.N]))
            b += 1
        c.append(NTRUEncrypt(ring, pk, m[b * ring.N:]))  # the last block is not padded
        return c
        
    # ------------- HELPER FUNCTIONS -------------------------------------------------------
    
    def shiftIrisCode(self, original, n):
        """ shifts each line of the original iris code by n bits and saves in shifted """
        """ positive shifts are to the right or counter clockwise in the iris """
        """ negative shifts are to the left or clockwise in the iris """
        if n < 0: n += self.BITSPERROW_IRISCODE
        shifted = [0] * self.ROWS_IRISCODE
        for i in range(self.ROWS_IRISCODE):
            shifted[i] = original[i][self.BITSPERROW_IRISCODE - n:] + original[i][:self.BITSPERROW_IRISCODE - n]
        return shifted
    
    def readIrisBitsFromFile(self, subject, sample):
        """ opens the file, reads iris code, and writes each bit to iris_code """
        iris_code = []
        f = open(self.PATH % (subject, sample), "rb")
        for i in range(self.ROWS_IRISCODE - 1):
            for bit in range(self.BITSPERROW_IRISCODE):
                iris_code.append(int(f.read(1)))
            f.seek(+(self.BITSPERROW_IRISCODE + 2), 1)
        for bit in range(self.BITSPERROW_IRISCODE):
            iris_code.append(int(f.read(1)))
        f.close()
        return iris_code
    
    def readIrisLinesFromFile(self, subject, sample):
        """ opens the file, reads iris code, and writes each line i to iris_rows[i] """
        iris_rows = [0] * self.ROWS_IRISCODE
        f = open(self.PATH % (subject, sample), "rb")
        for i in range(self.ROWS_IRISCODE - 1):
            one_row = []
            for bit in range(self.BITSPERROW_IRISCODE):
                one_row.append(int(f.read(1)))
            f.seek(+(self.BITSPERROW_IRISCODE + 2), 1)
            iris_rows[i] = one_row
        one_row = []
        for bit in range(self.BITSPERROW_IRISCODE):
            one_row.append(int(f.read(1)))
        iris_rows[self.ROWS_IRISCODE - 1] = one_row
        f.close()
        return iris_rows
