import time
from ttpNTRU import TTP
from clientNTRU import CLIENT
from serverNTRU import SERVER

ENROLLED = 1  # which sample is in database; nr from 1 to 5

if __name__ == '__main__':
    security_in_bits = 256  # {112, 128, 192, 256}
    factor_keep = 0.25
    
    ttp = TTP(security_in_bits, factor_keep)
    # ttp.FACTOR_KEEP = 0.125  # it is possible to adjust this factor during runtime
    
    id_probe = (174, 5)
    
    print('factor keep:', ttp.FACTOR_KEEP)
    
    print('ID probe:', id_probe)
    
    client1 = CLIENT(ttp.ring, ttp.pk)
    
    t0 = time.time()
    server1 = SERVER(ttp.ring, ttp.pk, ENROLLED)
    t1 = time.time()
    
    probe = client1.CLIENTencryptProbe(id_probe)
    t2 = time.time()
    print('verification:', server1.SERVERverification(ttp, probe, id_probe))
    t3 = time.time()
    print('baseline_verification:', server1.SERVERverificationAll(ttp, probe, id_probe))
    t4 = time.time()
    print('identification with factor keep:', ttp.FACTOR_KEEP, ', ID found:', server1.SERVERidentification(ttp, probe))
    t5 = time.time()
    
    print('server_init:          ', t1 - t0)
    print('probe_encryption:     ', t2 - t1)
    print('verification:         ', t3 - t2)
    print('baseline_verification:', t4 - t3)
    print('identification:       ', t5 - t4)
