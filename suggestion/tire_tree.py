#!/usr/bin/env python
# coding=utf-8
import time
import pypinyin
import jieba
from pinyindict import *

#jieba_config = {'cache_file':'/home/chunliang/python_utils/suggestion/jieba.cache'}
#jieba_config = {'cache_file':'jieba.cache','tmp_dir':"/home/chunliang/"}
#jieba.Tokenizer(jieba_config)
#jieba.load_userdict("userdict.txt")
#jieba.initialize("/home/chunliang/t")


'''
node|[0]    |[1]   |[2]  |[3]   |[4] |[5]  |[6]    |[7]
----|-------|------|-----|------|----|-----|-------|-------
    |keyword|weight|mtime|parent|type|level|weight2|children
note: only leaf node has weight and mtime, other node's is 0 and 0
'''
KEYWORD = 0
WEIGHT = 1
MTIME = 2
PARENT = 3
TYPE =4
LEVEL=5
WEIGHT2 = 6
CHILDREN = 7

NORMAL_NODE = 0
PINYIN_NODE = 1
INDEX_FLOOR = 4
tree_nodes = [['root', 0, 0, -1, NORMAL_NODE, 0, 0, []]]
node_index = {}


'''
update weight upword till root
'''
def add_weight(node_id, weight):
    node = tree_nodes[node_id]
    diff = node[WEIGHT2]
    node[WEIGHT2] = max(weight, diff)
    diff = node[WEIGHT2] - diff
    if diff == 0:
        return
    
    node[WEIGHT] += diff
    node[MTIME] = time.time()

    while node[PARENT] != 0:
        node = tree_nodes[node[PARENT]]
        node[WEIGHT] += diff


'''
new node from tire tree
@keyword: tire keyword
@parent: parent node id
'''
def new_node(keyword, parent=0, ntype=NORMAL_NODE):
    level = tree_nodes[parent][LEVEL] + 1
    node = [keyword, 0, 0, parent, ntype, level, 0, []]
    node_id = len(tree_nodes)
    tree_nodes.append(node)

    #update parent node, add into node index if nessory
    parent_node = tree_nodes[parent]
    if parent > 0:#first level has no children list
        if ntype == PINYIN_NODE:
            parent_node[CHILDREN].append(node_id)
        else:
            parent_node[CHILDREN].insert(0, node_id)
        
    if len(parent_node[CHILDREN]) == INDEX_FLOOR:
        #too much children, need node index
        for nid in parent_node[CHILDREN]:
            if tree_nodes[nid][TYPE] == NORMAL_NODE:
                node_index[str(parent)+'-'+tree_nodes[nid][KEYWORD]] = nid
            else:
                node_index[str(parent)+'_'+tree_nodes[nid][KEYWORD]] = nid
    elif parent == 0 or len(parent_node[CHILDREN]) > INDEX_FLOOR:
        if ntype == NORMAL_NODE:
            node_index[str(parent)+'-'+keyword] = node_id
        else:
            node_index[str(parent)+'_'+keyword] = node_id
        
    return node_id

'''
match 'word' from children
@node_id: parent id
@word: keyword to be matched
从node_id 向下匹配字符word，
一直到返回最深的孩子节点
'''
def child_match(node_id, word, node_type):
    child_id = 0
    node = tree_nodes[node_id]
    if node_id == 0 or len(node[CHILDREN]) >= INDEX_FLOOR:
        if node_type == NORMAL_NODE:
            key = str(node_id)+'-'+word
        else:
            key = str(node_id)+'_'+word
        
        if key in node_index:
            child_id = node_index[key]
    else:
        for nid in node[CHILDREN]:
            if tree_nodes[nid][TYPE] != node_type:
                continue
            if tree_nodes[nid][KEYWORD] == word:
                child_id = nid
                break
    return child_id

'''
max prefix match, if pinyin node match, stop and return
@words: word list
@parent: begin from this node to match
从parent=0 根节点开始依次匹配每个字符
每成功一个节点向下一级，字符向后一个
'''
def max_prefix_match(words, types, parent=0):
    node_id = parent
    level = 0

    while True:
        nid = child_match(node_id, words[level], types[level])
        if nid == 0:
            break

        level += 1
        node_id = nid
        if tree_nodes[nid][TYPE] == PINYIN_NODE:
            break
        if level == len(words):
            break

    return level, node_id

'''
convert term to words, split ascii string into
pinyin list completely if possible, if not, ascii
string as one word
'''
def term2words(term, py_split=False):
    term = unicode(term).lower()
    words = []
    types = []
    estr = ''
    
    for word in term:
        if ord(word)>=19904 and ord(word)<=40895:
            if estr != '':
                pylist = None
                if py_split:
                    pylist = estr2pinyin(estr)
                    if pylist != None:
                        words += pylist
                        for _ in pylist:
                            types.append(PINYIN_NODE)
                    else:
                        return [], []
                else:
                    for c in estr:
                        words.append(c)
                        types.append(NORMAL_NODE)
                estr = ''
            words.append(word)
            types.append(NORMAL_NODE)
        elif ord(word)>=ord('a') and ord(word)<=ord('z'):
            estr += word
        elif ord(word)>=ord('0') and ord(word)<=ord('9'):
            estr += word

    if estr != '':
        pylist = None
        if py_split:
            pylist = estr2pinyin(estr)
            if pylist != None:
                words += pylist
                for _ in pylist:
                    types.append(PINYIN_NODE)
            else:
                return [], []
        else:
            for c in estr:
                words.append(c)
                types.append(NORMAL_NODE)

    return words, types

def push_pinyin_node(parent, child, py):
    py_node = child_match(parent, py, PINYIN_NODE)
    if py_node == 0:
        py_node = new_node(py, parent, PINYIN_NODE)
        tree_nodes[py_node][CHILDREN].append(child)
    else:
        conflict = False
        for cid in tree_nodes[py_node][CHILDREN]:
            if cid == child:
                conflict = True
                break
        if conflict == False:
            tree_nodes[py_node][CHILDREN].append(child)
        
'''
add one term into tire tree
@term: words list, UNICODE
'''
def add_term(term, weight):
    words, types = term2words(term)
    if len(words) == 0: #avoid '......'
        return
    #max prefix match
    level, node_id = max_prefix_match(words, types)
    
    # 如果全部存在这个字符序列，则更新 node_id
    if level == len(words):#exist already
        add_weight(node_id, weight)#may lead to parent weight bigger than weight sum of all children
    else:
        for word in words[level:]:
            #insert normal node
            parent = node_id
            node_id = new_node(word, parent)
            if len(word)==1 and ord(word)>=19904 and ord(word)<=40895:
                #insert pinyin node
                pys = pypinyin.pinyin(word, style=pypinyin.NORMAL, heteronym=True)
                for py in pys[0]:
                    #complete pinyin
                    push_pinyin_node(parent, node_id, py)
                    push_pinyin_node(parent, node_id, py[0])
                    if py[0]=='c' or py[0]=='s' or py[0]=='z':
                        if py[1] == 'h':
                            push_pinyin_node(parent, node_id, py[:2])
                
        add_weight(node_id, weight)

'''
match max prefix and return suggestion list
'''
def match_words(words, types, parent=0):
    last_match_list = [parent] #can be return as max prefix match result because some prefix matched
    max_match_list = [parent] #try match more prefix
    isbottom = False
    
    while len(max_match_list) > 0:
        last_match_list = max_match_list
        
        if isbottom:
            break
        
        max_match_list = []
        for nid in last_match_list:
            idx = tree_nodes[nid][LEVEL] - tree_nodes[parent][LEVEL]
            level, max_node_id = max_prefix_match(words[idx:], types[idx:], nid)
            
            if tree_nodes[max_node_id][LEVEL] == len(words):#match the whole words
                isbottom = True
                
            if level == 0: #match fail
                continue
            elif tree_nodes[max_node_id][TYPE] == PINYIN_NODE: #match pinyin node
                for child in tree_nodes[max_node_id][CHILDREN]:
                    max_match_list.append(child)
            else: #match normal node
                max_match_list.append(max_node_id)

    return last_match_list

def suggest(parent, suggestion_num):
    if len(tree_nodes[parent][CHILDREN]) == 0:
        return [parent]
    
    result = []
    tot_weight = float(int(tree_nodes[parent][WEIGHT]*10000))/10000
    sum_weight = tree_nodes[parent][WEIGHT2]
    have_suggestion_num = 0
    
    for child in tree_nodes[parent][CHILDREN]:
        node = tree_nodes[child]
        if node[TYPE] == PINYIN_NODE:
            break
        sum_weight += node[WEIGHT]
        num = int(sum_weight*suggestion_num/tot_weight)
        this_suggestion_num = num - have_suggestion_num
        have_suggestion_num = num
        if this_suggestion_num > 0:
            result += suggest(child, this_suggestion_num)

    return result

TERM_TYPE_HANZI=1
TERM_TYPE_ESTR=2
TERM_TYPE_MIX=3
def get_suggestion(term, suggestion_num=8):
    candidate_list = []
    term = unicode(term)
    term_type = TERM_TYPE_HANZI
    if len(term) == len(str(term)):
        term_type = TERM_TYPE_ESTR
    elif len(term)*3 == len(str(term)):
        term_type = TERM_TYPE_HANZI
    else:
        term_type = TERM_TYPE_MIX

    #direct match
    direct_level = 0
    direct_words, direct_types = term2words(term)
    if len(direct_words) == 0: #avoid '......'
        return []
    direct_list = match_words(direct_words, direct_types)
    direct_level = tree_nodes[direct_list[0]][LEVEL]
    if direct_level == len(direct_words):
        candidate_list += direct_list

    #pinyin match
    pinyin_level = 0
    pinyin_words, pinyin_types = term2words(term, True)
    if term_type != TERM_TYPE_HANZI and len(pinyin_words) > 0: #have valid pinyin in words
        pinyin_list = match_words(pinyin_words, pinyin_types)
        pinyin_level = tree_nodes[pinyin_list[0]][LEVEL]
        if pinyin_level == len(pinyin_words):
            candidate_list += pinyin_list

    if len(candidate_list) == 0:
        #direct-pinyin
        if direct_level > 0:#have matched some prefix
            dpy_words, dpy_types = term2words(term[direct_level:], True)
            if len(dpy_words) > 0 and dpy_types[0] == 1:
                for nid in direct_list:
                    dpy_list = match_words(dpy_words, dpy_types, nid)
                    dpy_level = tree_nodes[dpy_list[0]][LEVEL]
                    if dpy_level == direct_level + len(dpy_words):
                        candidate_list += dpy_list

        #pinyin-direct match
        if pinyin_level > 0 and pinyin_types[0] == 1:#start with pinyin and have matched some pinyin
            pyd_level = 0
            for i in range(pinyin_level):
                pyd_level += len(pinyin_words[i])
            pyd_words, pyd_types = term2words(term[pyd_level:])
            for nid in pinyin_list:
                pyd_list = match_words(pyd_words, pyd_types, nid)
                pyd_level = tree_nodes[pyd_list[0]][LEVEL]
                if pyd_level == pinyin_level + len(pyd_words):
                    candidate_list += pyd_list
                    
    result = []
    tot_weight = 0
    sum_weight = 0
    have_suggestion_num = 0
    for node_id in candidate_list:
        tot_weight += tree_nodes[node_id][WEIGHT]
    tot_weight = float(int(tot_weight*10000))/10000
        
    for node_id in candidate_list:
        sum_weight += tree_nodes[node_id][WEIGHT]
        num = int(sum_weight*suggestion_num/tot_weight)
        this_suggestion_num = num - have_suggestion_num
        have_suggestion_num = num
        if this_suggestion_num > 0:
            result += suggest(node_id, this_suggestion_num)

    #if len(result) < suggestion_num: #relation term suggestion
    suggestion = []
    for leaf in result:
        node_id = leaf
        sug = ''
        while node_id != 0:
            sug = tree_nodes[node_id][KEYWORD] + sug
            node_id = tree_nodes[node_id][PARENT]
        suggestion.append(sug)
        
    return suggestion

if __name__ == '__main__':
    add_term('我的祖国', 1)
    add_term('我的世界', 2)
    add_term('我的shi姐', 3)
    a = get_suggestion('我的')
    for s in a:
        print s,
    print ''
    a = get_suggestion('wd')
    for s in a:
        print s,
    print ''
    a = get_suggestion('wod')
    for s in a:
        print s,
    print ''
    a = get_suggestion('wde')
    for s in a:
        print s,
    print ''
    a = get_suggestion('wds')
    for s in a:
        print s,
    print ''
    a = get_suggestion('wdsh')
    for s in a:
        print s,
    print ''
    a = get_suggestion('wdj')
    for s in a:
        print s,
    print ''
    a = get_suggestion('w')
    for s in a:
        print s,
    print ''

