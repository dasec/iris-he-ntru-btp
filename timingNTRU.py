import time
from clientNTRU import CLIENT
from serverNTRU import SERVER
from ttpNTRU import TTP


''' this may take some time, maybe you want to manually split the timing function '''

def printList(llist):
    for elem in llist:
        print(elem)
    print('\n')

def timing():
    print('timing benchmark\n')
    #warming up
    ttp_warmup=TTP(256, 0.5)
    server_warmup = SERVER(ttp_warmup.ring, ttp_warmup.pk, 1)

    time112=['timing for 112']
    time128=['timing for 128']
    time192=['timing for 192']
    time256=['timing for 256']
    tmp = []
    tmp112 = []
    tmp128 = []
    tmp192 = []
    tmp256 = []

    factors = [1, 0.5, 0.25, 0.125, 0.0625]

    # use odd value to get median in order to exclude peak values biased by other processes
    slowloop = 25
    fastloop = 25 #multiple of 5 for all possible enrolled samples

    #start timing

    # TTP
    print('TTP')

    #ttp112
    tmp.clear()
    for i in range(fastloop):
        t_start = time.time()
        ttp112=TTP(112, 0.5)
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time112.append('ttp_init: %.6f' % tmp[len(tmp)//2])
    #ttp128
    tmp.clear()
    for i in range(fastloop):
        t_start = time.time()
        ttp128=TTP(128, 0.5)
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time128.append('ttp_init: %.6f' % tmp[len(tmp)//2])
    #ttp192
    tmp.clear()
    for i in range(fastloop):
        t_start = time.time()
        ttp192=TTP(192, 0.5)
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time192.append('ttp_init: %.6f' % tmp[len(tmp)//2])
    #ttp256
    tmp.clear()
    for i in range(fastloop):
        t_start = time.time()
        ttp256=TTP(256, 0.5)
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time256.append('ttp_init: %.6f' % tmp[len(tmp)//2])

    # CLIENT
    print('Client')

    client112 = CLIENT(ttp112.ring, ttp112.pk)
    client128 = CLIENT(ttp128.ring, ttp128.pk)
    client192 = CLIENT(ttp192.ring, ttp192.pk)
    client256 = CLIENT(ttp256.ring, ttp256.pk)

    # SERVER
    print('Server')

    #server112
    print('Server_112')
    tmp.clear()
    for i in range(fastloop//5):
        t_start = time.time()
        server112_1 = SERVER(ttp112.ring, ttp112.pk, 1)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server112_2 = SERVER(ttp112.ring, ttp112.pk, 2)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server112_3 = SERVER(ttp112.ring, ttp112.pk, 3)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server112_4 = SERVER(ttp112.ring, ttp112.pk, 4)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server112_5 = SERVER(ttp112.ring, ttp112.pk, 5)
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time112.append('server_init: %.3f' % tmp[len(tmp)//2])

    #server128
    print('Server_128')
    tmp.clear()
    for i in range(fastloop//5):
        t_start = time.time()
        server128_1 = SERVER(ttp128.ring, ttp128.pk, 1)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server128_2 = SERVER(ttp128.ring, ttp128.pk, 2)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server128_3 = SERVER(ttp128.ring, ttp128.pk, 3)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server128_4 = SERVER(ttp128.ring, ttp128.pk, 4)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server128_5 = SERVER(ttp128.ring, ttp128.pk, 5)
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time128.append('server_init: %.3f' % tmp[len(tmp)//2])

    #server192
    print('Server_192')
    tmp.clear()
    for i in range(fastloop//5):
        t_start = time.time()
        server192_1 = SERVER(ttp192.ring, ttp192.pk, 1)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server192_2 = SERVER(ttp192.ring, ttp192.pk, 2)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server192_3 = SERVER(ttp192.ring, ttp192.pk, 3)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server192_4 = SERVER(ttp192.ring, ttp192.pk, 4)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server192_5 = SERVER(ttp192.ring, ttp192.pk, 5)
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time192.append('server_init: %.3f' % tmp[len(tmp)//2])

    #server256
    print('Server_256')
    tmp.clear()
    for i in range(fastloop//5):
        t_start = time.time()
        server256_1 = SERVER(ttp256.ring, ttp256.pk, 1)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server256_2 = SERVER(ttp256.ring, ttp256.pk, 2)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server256_3 = SERVER(ttp256.ring, ttp256.pk, 3)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server256_4 = SERVER(ttp256.ring, ttp256.pk, 4)
        t_end = time.time()
        tmp.append(t_end-t_start)
        t_start = time.time()
        server256_5 = SERVER(ttp256.ring, ttp256.pk, 5)
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time256.append('server_init: %.3f' % tmp[len(tmp)//2])

    # PROBE
    print('Probe')

    #probe112
    tmp.clear()
    for i in range(fastloop):
        t_start = time.time()
        probe112=client112.CLIENTencryptProbe((25,1))
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time112.append('probe_enc: %.6f' % tmp[len(tmp)//2])

    #probe128
    tmp.clear()
    for i in range(fastloop):
        t_start = time.time()
        probe128=client128.CLIENTencryptProbe((25,1))
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time128.append('probe_enc: %.6f' % tmp[len(tmp)//2])

    #probe192
    tmp.clear()
    for i in range(fastloop):
        t_start = time.time()
        probe192=client192.CLIENTencryptProbe((25,1))
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time192.append('probe_enc: %.6f' % tmp[len(tmp)//2])

    #probe256
    tmp.clear()
    for i in range(fastloop):
        t_start = time.time()
        probe256=client256.CLIENTencryptProbe((25,1))
        t_end = time.time()
        tmp.append(t_end-t_start)
    tmp.sort()
    time256.append('probe_enc: %.6f' % tmp[len(tmp)//2])

    tmp.clear()
    tmp112.clear()
    tmp128.clear()
    tmp192.clear()
    tmp256.clear()

    # VERIFICATION
    print('Verification')

    for subj in range(25,176):
        for sample in range(1,11):
            #print('veri', subj, sample)
            probe112 = client112.CLIENTencryptProbe((subj, sample))
            probe128 = client128.CLIENTencryptProbe((subj, sample))
            probe192 = client192.CLIENTencryptProbe((subj, sample))
            probe256 = client256.CLIENTencryptProbe((subj, sample))


            if sample % 5 != 1:
                t_start = time.time()
                server112_1.SERVERverification(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                t_start = time.time()
                server128_1.SERVERverification(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_1.SERVERverification(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_1.SERVERverification(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)
            if sample % 5 != 2:
                t_start = time.time()
                server112_2.SERVERverification(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                server128_2.SERVERverification(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_2.SERVERverification(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_2.SERVERverification(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)
            if sample % 5 != 3:
                t_start = time.time()
                server112_3.SERVERverification(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                server128_3.SERVERverification(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_3.SERVERverification(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_3.SERVERverification(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)
            if sample % 5 != 4:
                t_start = time.time()
                server112_4.SERVERverification(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                server128_4.SERVERverification(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_4.SERVERverification(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_4.SERVERverification(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)
            if sample % 5 != 0:
                t_start = time.time()
                server112_5.SERVERverification(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                server128_5.SERVERverification(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_5.SERVERverification(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_5.SERVERverification(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)


    tmp112.sort()
    time112.append('veri: %.6f' % tmp112[len(tmp112)//2])
    tmp128.sort()
    time128.append('veri: %.6f' % tmp128[len(tmp128)//2])
    tmp192.sort()
    time192.append('veri: %.6f' % tmp192[len(tmp192)//2])
    tmp256.sort()
    time256.append('veri: %.6f' % tmp256[len(tmp256)//2])

    tmp112.clear()
    tmp128.clear()
    tmp192.clear()
    tmp256.clear()
    
    # BASELINE VERIFICATION ALL BLOCKS
    print('Baseline Verification')

    for subj in range(25,176):
        for sample in range(1,11):
            #print('veri', subj, sample)
            probe112 = client112.CLIENTencryptProbe((subj, sample))
            probe128 = client128.CLIENTencryptProbe((subj, sample))
            probe192 = client192.CLIENTencryptProbe((subj, sample))
            probe256 = client256.CLIENTencryptProbe((subj, sample))


            if sample % 5 != 1:
                t_start = time.time()
                server112_1.SERVERverificationAll(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                t_start = time.time()
                server128_1.SERVERverificationAll(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_1.SERVERverificationAll(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_1.SERVERverificationAll(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)
            if sample % 5 != 2:
                t_start = time.time()
                server112_2.SERVERverificationAll(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                server128_2.SERVERverificationAll(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_2.SERVERverificationAll(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_2.SERVERverificationAll(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)
            if sample % 5 != 3:
                t_start = time.time()
                server112_3.SERVERverificationAll(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                server128_3.SERVERverificationAll(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_3.SERVERverificationAll(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_3.SERVERverificationAll(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)
            if sample % 5 != 4:
                t_start = time.time()
                server112_4.SERVERverificationAll(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                server128_4.SERVERverificationAll(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_4.SERVERverificationAll(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_4.SERVERverificationAll(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)
            if sample % 5 != 0:
                t_start = time.time()
                server112_5.SERVERverificationAll(ttp112, probe112, (subj, sample))
                t_end = time.time()
                tmp112.append(t_end-t_start)
                server128_5.SERVERverificationAll(ttp128, probe128, (subj, sample))
                t_end = time.time()
                tmp128.append(t_end-t_start)
                t_start = time.time()
                server192_5.SERVERverificationAll(ttp192, probe192, (subj, sample))
                t_end = time.time()
                tmp192.append(t_end-t_start)
                t_start = time.time()
                server256_5.SERVERverificationAll(ttp256, probe256, (subj, sample))
                t_end = time.time()
                tmp256.append(t_end-t_start)


    tmp112.sort()
    time112.append('veri_baseline: %.6f' % tmp112[len(tmp112)//2])
    tmp128.sort()
    time128.append('veri_baseline: %.6f' % tmp128[len(tmp128)//2])
    tmp192.sort()
    time192.append('veri_baseline: %.6f' % tmp192[len(tmp192)//2])
    tmp256.sort()
    time256.append('veri_baseline: %.6f' % tmp256[len(tmp256)//2])

    tmp112.clear()
    tmp128.clear()
    tmp192.clear()
    tmp256.clear()

    # IDENTIFICATION
    print('Identification')

    
    for keep in factors:
        ttp112.FACTOR_KEEP = keep
        ttp128.FACTOR_KEEP = keep
        ttp192.FACTOR_KEEP = keep
        ttp256.FACTOR_KEEP = keep
        #id112
        print('id_factor_keep', keep, '112')
        tmp.clear()
        for i in range(slowloop):
            t_start = time.time()
            server112_1.SERVERidentification(ttp112, probe112)
            t_end = time.time()
            tmp.append(t_end-t_start)
        tmp.sort()
        time112.append('id_factor_keep %.3f: %0.3f' % (keep, tmp[len(tmp)//2]))
        #id128
        print('id_factor_keep', keep, '128')
        tmp.clear()
        for i in range(slowloop):
            t_start = time.time()
            server128_1.SERVERidentification(ttp128, probe128)
            t_end = time.time()
            tmp.append(t_end-t_start)
        tmp.sort()
        time128.append('id_factor_keep %.3f: %0.3f' % (keep, tmp[len(tmp)//2]))
        #id192
        print('id_factor_keep', keep, '192')
        tmp.clear()
        for i in range(slowloop):
            t_start = time.time()
            server192_1.SERVERidentification(ttp192, probe192)
            t_end = time.time()
            tmp.append(t_end-t_start)
        tmp.sort()
        time192.append('id_factor_keep %.3f: %0.3f' % (keep, tmp[len(tmp)//2]))
        #id256
        print('id_factor_keep', keep, '256')
        tmp.clear()
        for i in range(slowloop):
            t_start = time.time()
            server256_1.SERVERidentification(ttp256, probe256)
            t_end = time.time()
            tmp.append(t_end-t_start)
        tmp.sort()
        time256.append('id_factor_keep %.3f: %0.3f' % (keep, tmp[len(tmp)//2]))


        
    tmp.clear()
    print('done\n')


    # print all results
    printList(time112)
    printList(time128)
    printList(time192)
    printList(time256)

    return 1


if __name__ == '__main__':
    timing()