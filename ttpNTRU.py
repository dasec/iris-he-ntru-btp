""" version for optimised ntru """
""" trusted third party with full access to NTRU key """
from biometricNTRU import *
from irisNTRU import IRIS


class TTP(object):
    """docstring for TTP"""
    
    def __init__(self, k, factor_keep):
        super(TTP, self).__init__()
        # private
        self.__key = NTRUKey(NTRUParams(k))
        # public
        self.pk = self.__key.h
        self.ring = self.__key.ring

        self.FACTOR_KEEP = factor_keep

        self.__hd_all_identify = []
        self.__min_hd_all_identify = []

        """ thresholds for different block sizes """
        if self.ring.N == 401:
            self.__accept = [110, 239, 405, 609, 801,  974, 1155, 1323, 1507, 1672, 1847, 2024, 2197]
            self.__reject = [172, 346, 541, 720, 893, 1069, 1233, 1402, 1567, 1755, 1911, 2139, 2274]
            self.blocks = 13
        elif self.ring.N == 439:
            self.__accept = [122, 273, 462, 687, 863, 1083, 1273, 1451, 1652, 1845, 2034, 2197]
            self.__reject = [187, 384, 593, 795, 989, 1148, 1328, 1545, 1730, 1896, 2147, 2274]
            self.blocks = 12
        elif self.ring.N == 593:
            self.__accept = [183, 396, 693,  962, 1232, 1471, 1738, 1999, 2197]
            self.__reject = [238, 530, 810, 1057, 1278, 1558, 1817, 2119, 2274]
            self.blocks = 9
        elif self.ring.N == 743:
            self.__accept = [214, 539,  888, 1239, 1548, 1854, 2197]
            self.__reject = [322, 669, 1001, 1279, 1604, 1937, 2274]
            self.blocks = 7

    """ both possible - self.pk(/ring) or the function getPublicKey()/ring """
    def getPublicKey(self):
        return self.__key.h
    def getPublicRing(self):
        return self.__key.ring
    
    def TTPverify(self, enc_sum):
        """ receives all encrypted msg blocks and compares against thresholds to return a fast accept/reject """

        tmp_hd = [0] * IRIS.NRSHIFTS
        ntmp = [0, 0, 0, 0]
        for block in range(self.blocks): 
            for shift in range(IRIS.NRSHIFTS):
                mtmp = NTRUDecrypt(self.__key, *enc_sum[shift * self.blocks + block])
                tmp_hd[shift] += mtmp.count(1)
                if tmp_hd[shift] < self.__accept[block]:
                    return True
            if min(tmp_hd) > self.__reject[block]:
                return False
        
        tmp_hd.clear()
        return False

    def TTPverifyAll(self, enc_sum):
        """ gets hd of all blocks but accept for first matching shift """
        """ since verification is quiet fast, we can keep the baseline accuracy by comparing all blocks"""
        
        tmp_hd = [0] * IRIS.NRSHIFTS
        ntmp = [0, 0, 0, 0]
        for shift in range(IRIS.NRSHIFTS):
            for block in range(self.blocks):
                mtmp = NTRUDecrypt(self.__key, *enc_sum[shift * self.blocks + block])
                tmp_hd[shift] += mtmp.count(1)
            if tmp_hd[shift] < self.__accept[self.blocks - 1]:
                return True
    
        tmp_hd.clear()
        return False

    def TTPidentify(self, sums_of_1_block, block_nr):
        """ receives a shuffled list of sums of 1 block and the block number """
        """ decrypts the sums to get the hamming weight, safes the #FACTOR_KEEP lowest hws and returns the indexes of those """
        index_min_hds = []
        ntmp = [0, 0, 0, 0]

        if block_nr == 0:
            self.__hd_all_identify.clear()
            self.__min_hd_all_identify.clear()
            for i in range(len(sums_of_1_block)):
                for shift in range(IRIS.NRSHIFTS):
                    mtmp = NTRUDecrypt(self.__key, *sums_of_1_block[i][shift])
                    self.__hd_all_identify.append(mtmp.count(1))
                self.__min_hd_all_identify.append((min(self.__hd_all_identify[i*IRIS.NRSHIFTS:i*IRIS.NRSHIFTS+IRIS.NRSHIFTS]), i))

        else:
            assert(len(sums_of_1_block) == len(self.__min_hd_all_identify))
            for i in range(len(sums_of_1_block)):
                old_index = self.__min_hd_all_identify[i][1]*IRIS.NRSHIFTS
                for shift in range(IRIS.NRSHIFTS):
                    mtmp = NTRUDecrypt(self.__key, *sums_of_1_block[i][shift])
                    self.__hd_all_identify[old_index+shift] += (mtmp.count(1))
                self.__min_hd_all_identify[i] = (min(self.__hd_all_identify[old_index:old_index+IRIS.NRSHIFTS]), self.__min_hd_all_identify[i][1])

        # every time
        self.__min_hd_all_identify.sort()
        if int(len(self.__min_hd_all_identify)*self.FACTOR_KEEP) == 0: self.__min_hd_all_identify = self.__min_hd_all_identify[:1]
        else: self.__min_hd_all_identify = self.__min_hd_all_identify[:int(len(self.__min_hd_all_identify)*self.FACTOR_KEEP)]
        for i in range(len(self.__min_hd_all_identify)):
            index_min_hds.append(self.__min_hd_all_identify[i][1])

        return index_min_hds


'''
""" this was used to be able to benchmark a constant verification time """
    def BASELINEverify(self, encSum):
        """ gets hd of all blocks and shifts, to benchmark a constant time as baseline """
        verify = False
        tmp_hd = [0] * IRIS.NRSHIFTS
        ntmp = [0,0,0,0]
        for block in range(self.blocks):
            for shift in range(IRIS.NRSHIFTS):
                mtmp = NTRUDecrypt(self.__key, *encSum[shift*self.blocks+block])
                ntmp[0] = mtmp.count(2)
                ntmp[1] = mtmp.count(-2)
                ntmp[2] = mtmp.count(1)
                ntmp[3] = mtmp.count(-1)
                tmp_hd[shift] += (ntmp[0] + ntmp[1])
        if min(tmp_hd) < self.__accept[self.blocks-1]:
            verify = True

        tmp_hd.clear()
        return verify

'''
