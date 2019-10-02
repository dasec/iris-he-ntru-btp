from irisNTRU import IRIS
from sortNTRU import sortIrisBitsForServer
import random
import time


class SERVER(object):
    """docstring for server"""
    
    def __init__(self, public_ring, public_key, enrol_sample_nr):
        super(SERVER, self).__init__()
        # self.ring = public_ring # not need except that someone wants to verify whether the pk of client and server
        # are the same
        # self.pk = public_key
        self.enrolled = enrol_sample_nr
        # for loading database
        self.__allref = []
        self.__idall = []
        
        # init Database
        for ref in range(IRIS.NRTRAINING + 1, IRIS.NRENROLMENT + IRIS.NRTRAINING + 1):
            # encrypt ref
            self.__allref += (IRIS.encryptBlocks(IRIS, public_key, public_ring, sortIrisBitsForServer(IRIS.readIrisBitsFromFile(IRIS, ref, self.enrolled))))  # left eye
            self.__allref += (IRIS.encryptBlocks(IRIS, public_key, public_ring, sortIrisBitsForServer(IRIS.readIrisBitsFromFile(IRIS, ref, self.enrolled + IRIS.NREYES))))  # right eye
            
            self.__idall.append((ref, self.enrolled))
            self.__idall.append((ref, self.enrolled + IRIS.NREYES))
    
    @staticmethod
    def __sum1blockforallshifts(probe, ref_block, block, nr_of_blocks):
        sum_all_shifts = []
        for shift in range(IRIS.NRSHIFTS):
            sum_all_shifts.append(([probe[shift * nr_of_blocks + block][0][0] + ref_block[0][0]], ref_block[1]))
        return sum_all_shifts

    @staticmethod
    def __sum2ciphertexts(c1, c2):
        c_sum = []
        for block in range(len(c1)):
            c_sum.append(([c1[block][0][0] + c2[block][0][0]], c1[block][1]))
        return c_sum
    
    def SERVERverification(self, ttp, probe, id):
        """ verifies whether the probe belongs to the enrolled id """
        if not (id[0] in range(IRIS.NRTRAINING + 1, IRIS.NRTRAINING + IRIS.NRENROLMENT + 1) and id[1] in range(1, 11)):
            return False
        if id[1] > IRIS.NREYES:
            ref = self.__allref[
                  self.__idall.index((id[0], self.enrolled + IRIS.NREYES)) * ttp.blocks:self.__idall.index((id[0], self.enrolled + IRIS.NREYES)) * ttp.blocks + ttp.blocks]
        else:
            ref = self.__allref[self.__idall.index((id[0], self.enrolled)) * ttp.blocks:self.__idall.index((id[0], self.enrolled)) * ttp.blocks + ttp.blocks]
        
        sum_all_shifts = []
        for shift in range(0, IRIS.NRSHIFTS * ttp.blocks, ttp.blocks):
            sum_all_shifts += (self.__sum2ciphertexts(probe[shift:shift + ttp.blocks], ref))
        
        return ttp.TTPverify(sum_all_shifts)
    
    def SERVERverificationAll(self, ttp, probe, id):
        """ gets the hd of all blocks but accepts after first matching shift for benchmark purposes """
        if not (id[0] in range(IRIS.NRTRAINING + 1, IRIS.NRTRAINING + IRIS.NRENROLMENT + 1) and id[1] in range(1, 11)):
            return False
        if id[1] > IRIS.NREYES:
            ref = self.__allref[
                  self.__idall.index((id[0], self.enrolled + IRIS.NREYES)) * ttp.blocks:self.__idall.index((id[0], self.enrolled + IRIS.NREYES)) * ttp.blocks + ttp.blocks]
        else:
            ref = self.__allref[self.__idall.index((id[0], self.enrolled)) * ttp.blocks:self.__idall.index((id[0], self.enrolled)) * ttp.blocks + ttp.blocks]
        
        sum_all_shifts = []
        for shift in range(0, IRIS.NRSHIFTS * ttp.blocks, ttp.blocks):
            sum_all_shifts += (self.__sum2ciphertexts(probe[shift:shift + ttp.blocks], ref))
        
        return ttp.TTPverifyAll(sum_all_shifts)
    
    def SERVERidentification(self, ttp, probe):
        """ sends first block of all sums to ttp, gets indexes back for lowest hds and sends next block """
        """ in the end only 1 index remains and this is the subject with the lowest hd """
        sum_all = []
        index = list(range(IRIS.NRENROLMENT << 1))
        block = 0
        
        for i in range(0, len(self.__allref), ttp.blocks):
            sum_all.append(self.__sum1blockforallshifts(probe, self.__allref[i], block, ttp.blocks))
        
        timeseed = time.time()
        random.seed(timeseed)
        random.shuffle(index)
        random.seed(timeseed)
        random.shuffle(sum_all)
        del timeseed
        
        keep = ttp.TTPidentify(sum_all, block)
        if keep is None: return None
        while len(keep) > 1 and block < ttp.blocks - 1:
            block += 1
            sum_all.clear()
            # sum next block
            for i in range(len(keep)):
                sum_all.append(
                    self.__sum1blockforallshifts(probe, self.__allref[index[keep[i]] * ttp.blocks + block], block, ttp.blocks))
            
            keep = ttp.TTPidentify(sum_all, block)
            if keep is None: return None
        
        sum_all.clear()
        """ possible to check whether the lowest HD verifies the reference """
        # if self.SERVERverification(ttp, probe, self.__idall[index[keep[0]]]): return self.__idall[index[keep[0]]]
        """ else return ID of lowest HD (or adjust to support returning multiple IDs, however this may need adjusting ttp, too) """
        return self.__idall[index[keep[0]]]


'''
    def BASELINEverification(self, ttp, probe, id):
        """ gets the hd of all blocks and shifts for benchmark purposes """
        if not (id[0] in range(IRIS.NRTRAINING+1, IRIS.NRTRAINING+IRIS.NRENROLMENT+1) and id[1] in range(1, 11)):
            return False
        if id[1] > IRIS.NREYES: ref = self.__allref[self.__idall.index((id[0],self.enrolled+IRIS.NREYES))*ttp.blocks:self.__idall.index((id[0],self.enrolled+IRIS.NREYES))*ttp.blocks+ttp.blocks]
        else: ref = self.__allref[self.__idall.index((id[0],self.enrolled))*ttp.blocks:self.__idall.index((id[0],self.enrolled))*ttp.blocks+ttp.blocks]

        sum_all_shifts=[]
        for shift in range(0,IRIS.NRSHIFTS*ttp.blocks,ttp.blocks):
            sum_all_shifts += (self.__sum2ciphertexts(probe[shift:shift+ttp.blocks], ref))

        return ttp.BASELINEverify(sum_all_shifts
)

    
'''
