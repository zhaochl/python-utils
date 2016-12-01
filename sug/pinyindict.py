#!/usr/bin/env python
smdict={'b':0, 'c':1, 'ch':2, 'd':3,
        'f':4, 'g':5, 'h':6, 'j':7,
        'k':8, 'l':9, 'm':10, 'n':11,
        'p':12, 'q':13, 'r':14, 's':15,
        'sh':16, 't':17, 'x':18, 'z':19, 'zh':20, "'":21, 'w':22, 'y':23}
ymdict={'a':0, 'ai':1, 'an':2, 'ang':3, 'ao':4,
        'e':5, 'ei':6, 'en':7, 'eng':8, 'er':9,
        'i':10, 'ia':11, 'ian':12, 'iang':13, 'iao':14, 'ie':15, 'in':16, 'ing':17, 'io':-1, 'ion':-1, 'iong':18, 'iu':19,
        'o':20, 'on':-1, 'ong':21, 'ou':22,
        'u':23, 'ua':24, 'uai':25, 'uan':26, 'uang':27, 'ue':28, 'ui':29, 'un':30, 'uo':31,
        'v':32}


pinyin_table=[
#b, c, ch, d, f, g, h, j, k, l, m, n, p, q, r, s, sh, t, x, z, zh, ', w, y
#------------------------------------------------------------------------------
[1, 1, 1,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1,  1, 0, 1, 1,  1, 1, 1],#'a':0,
[1, 1, 1,  1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1,  1, 0, 1, 1,  1, 1, 0],#'ai':1,
[1, 1, 1,  1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1,  1, 0, 1, 1,  1, 1, 1],#'an':2,
[1, 1, 1,  1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1,  1, 0, 1, 1,  1, 1, 1],#'ang':3,
[1, 1, 1,  1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,  1, 0, 1, 1,  1, 0, 1],#'ao':4,
[0, 1, 1,  1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1,  1, 0, 1, 1,  1, 0, 1],#'e':5,
[1, 0, 0,  1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1,  1, 0, 1, 1,  1, 1, 0],#'ei':6,
[1, 1, 1,  1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1,  0, 0, 1, 1,  1, 1, 0],#'en':7,
[1, 1, 1,  1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1,  1, 0, 1, 1,  1, 1, 0],#'eng':8,
[0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  1, 0, 0],#'er':9,
[1, 1, 1,  1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,  1, 1, 1, 1,  0, 0, 1],#'i':10,
[0, 0, 0,  1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 0],#'ia':11,
[1, 0, 0,  1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0,  1, 1, 0, 0,  0, 0, 0],#'ian':12,
[0, 0, 0,  0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 0],#'iang':13,
[1, 0, 0,  1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0,  1, 1, 0, 0,  0, 0, 0],#'iao':14,
[1, 0, 0,  1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0,  1, 1, 0, 0,  0, 0, 0],#'ie':15,
[1, 0, 0,  0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 1],#'in':16,
[1, 0, 0,  1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0,  1, 1, 0, 0,  0, 0, 1],#'ing':17,
[0, 0, 0,  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 0],#'iong'18,
[1, 0, 0,  1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 0],#'iu':19,
[0, 0, 0,  0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0,  0, 0, 0, 0,  1, 1, 0],#'o':20,
[0, 1, 1,  1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0,  1, 0, 1, 1,  0, 0, 1],#'ong':21,
[0, 1, 1,  1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1,  1, 0, 1, 1,  0, 0, 1],#'ou':22,
[1, 1, 1,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  1, 1, 1, 1,  0, 1, 1],#'u':23,
[0, 0, 0,  0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,  0, 0, 0, 1,  0, 0, 0],#'ua':24,
[0, 0, 1,  0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,  0, 0, 0, 1,  0, 0, 0],#'uai':25,
[0, 1, 1,  1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1,  1, 1, 1, 1,  0, 0, 1],#'uan':26,
[0, 0, 1,  0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,  0, 0, 0, 1,  0, 0, 0],#'uang':27,
[0, 0, 0,  0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 1],#'ue':28,
[0, 1, 1,  1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1,  1, 0, 1, 1,  0, 0, 0],#'ui':29,
[0, 1, 1,  1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1,  1, 1, 1, 1,  0, 0, 1],#'un':30,
[0, 1, 1,  1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1,  1, 0, 1, 1,  0, 0, 0],#'uo':31,
[0, 0, 0,  0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0],#'v':32
]

'''
split english str into pinyin list
'''
def estr2pinyin(estr):
    if len(estr) == 0:
        return None
    pylist = []
    smidx = smdict["'"]

    i = 0
    while i < len(estr):
        if estr[i] > 'z' or estr[i] < 'a':
            return None
        #match sm
        begin = end = i
        n = 0
        smidx = smdict["'"]
        if estr[i] in smdict:
            n = 1
            smidx = smdict[estr[i]]
            if estr[i]=='z' or estr[i]=='c' or estr[i]=='s':
                if i+1 < len(estr) and estr[i+1] == 'h':
                    n = 2
                    smidx = smdict[estr[i]+estr[i+1]]

        #match ym
        i += n
        end = i
        n = 0
        ym = ''
        for c in estr[i:]:
            n += 1
            ym += c
            if ym in ymdict:
                ymidx = ymdict[ym]
                if ymidx == -1:#prefix of yunmu
                    continue
                else:
                    if pinyin_table[ymidx][smidx] == 1:#is a valid pinyin
                        end = i + n
            else:
                break

        if begin < end: #matched
            pylist.append(estr[begin:end])
            i = end
        else: #error
            if len(pylist) == 0:
                return None
            #go backwords to first sm
            j = 0
            while len(pylist) > 0:
                k = 0
                last = pylist.pop()
                for c in last[::-1]:
                    j += 1
                    k += 1
                    if c in smdict:
                        j = -j
                        k = -k
                        break
                if j < 0:
                    break

            if j < 0:
                li = estr2pinyin(last[:k])
                if li == None:
                    return None
                else:
                    pylist += li
                    i += j#go backwords to first sm
            else:
                return None

    return pylist


if __name__ == '__main__':
    estr2pinyin('p2p')
    estr2pinyin('wode')
    estr2pinyin('lengou')
    estr2pinyin('ing')
    estr2pinyin('ziang')
    estr2pinyin('zhiang')
