def head_inverter(dep, b, old_d, new_d):
    # takes a dependency dep and a new head for this dependency b
    # takes the lists of old and new dependenies - old_d and new_d
    # adds dependency d to old_d
    # changes the head in it to b and adds the new dependency to new_d
    
    old_d1 = dep
    old_d.append(old_d1)
    new_d1 = {'id': old_d1['id'],
              'text': old_d1['text'],
              'lemma': old_d1['lemma'],
              'pos': old_d1['pos'],
              'gram': old_d1['gram'],
              'head': b,
              'dep': old_d1['dep']}
    new_d.append(new_d1)
    return old_d, new_d

def remover(deps, old_d, new_d):
    # takes the list of dependencies deps and the lists of dependenies to delete and to add
    # removes the dependencies from old_d and adds the dependencies from new_d
    
    for d in old_d:
        deps.remove(d)
    for d in new_d:
        deps.append(d)
    deps = sorted(deps, key=lambda d: d['id'])
    return deps

def one_inverter(dep, deps, copula):
    # takes a dependency dep and a list of all dependencies deps
    # takes an argument copula indicating whether additional changes associated with copula are necessary
    # inverts the dependency dep and, if necessary, some other dependencies associated with it
    # e.g., in case of copula inversion, after the AUX becomes head, the subject of the sentence should also become its subject
    
    mydeps = deps.copy()
    old_d, new_d = [], []
    
    for d1 in mydeps:
        if d1 == dep:
            a = d1['head']
            b = d1['id']
            old_d1 = d1
            old_d.append(old_d1)
            for d2 in deps:
                if d2['id'] == a:
                    if d2['head'] != d2['id']:
                        c = d2['head']
                    else:
                        c = d1['id']
                    old_d2 = d2
                    old_d.append(old_d2)
            new_d1 = {'id': a,
                      'text': old_d2['text'],
                      'lemma': old_d2['lemma'],
                      'pos': old_d2['pos'],
                      'gram': old_d2['gram'],
                      'head': b,
                      'dep': old_d1['dep']}
            new_d2 = {'id': b,
                      'text': old_d1['text'],
                      'lemma': old_d1['lemma'],
                      'pos': old_d1['pos'],
                      'gram': old_d1['gram'],
                      'head': c,
                      'dep': old_d2['dep']}
            new_d.append(new_d1)
            new_d.append(new_d2)
            
    mydeps = remover(mydeps, old_d, new_d)
    old_d, new_d = [], []
    
    for d3 in mydeps:
        if d3['head'] == a:
            if (d3['dep'] in ['cc', 'punct']) or ((d3['dep'] == 'advmod') and (d3['id'] < b)):
                old_d, new_d = head_inverter(d3, b, old_d, new_d)
            elif d3['dep'] == 'conj':
                for d4 in mydeps:
                    if d4['id'] == d3['head']:
                        mypos = d4['pos']
                    elif d4['id'] == b:
                        mygram = d4['gram']
                if (d3['pos'] != mypos) or (d3['gram'] == mygram):
                    old_d, new_d = head_inverter(d3, b, old_d, new_d)
            else:
                if copula == True:
                    if (d3['dep'].startswith('nsubj')):
                        old_d, new_d = head_inverter(d3, b, old_d, new_d)
                
    mydeps = remover(mydeps, old_d, new_d)
    return mydeps

def many_inverter(deps, deps_to_invert, poses_to_invert, copula=False):
    # takes the list of deps, the values of deps to remove, the values of poses to remove
    # identifies all dependencies that will be removed
    # then applies one_inverter so that the dependencies be removed one by one
    
    mydeps = deps.copy()
    deps_for_inverting = []
    for d1 in deps:
        if (d1['dep'] in deps_to_invert) and (d1['pos'] in poses_to_invert):
            deps_for_inverting.append(d1)
    if len(deps_for_inverting) > 0:
        deps_for_inverting.reverse()
        for d in deps_for_inverting:
            mydeps = one_inverter(d, mydeps, copula)
    sorted_deps = sorted(mydeps, key=lambda d: d['id'])
    return sorted_deps

def invert_case(deps):
    # case - the adposition must be a head, the nominal a dependent
    return many_inverter(deps, ['case'], ['ADP'])

def invert_num(deps):
    # num - the numeral must be a head, the nominal a dependent
    return many_inverter(deps, ['nummod:gov'], ['NUM'])

def invert_mark(deps):
    # mark - the complementizer must be a head, the verb of the second clause a dependent
    return many_inverter(deps, ['mark'], ['SCONJ'])
   
def invert_aux(deps):
    # aux - the auxiliary verb must be a head, the lexical verb a dependent
    return many_inverter(deps, ['aux', 'aux:pass'], ['AUX'], copula = True)
    
def invert_cop(deps):
    # cop - the auxiliary verb must be a head, anything else (e.g. a nominal) a dependent
    return many_inverter(deps, ['cop'], ['AUX'], copula = True)

def invert_cc(deps):
    # cс - the conjunction must be a head, the second conjunct a dependent
    return many_inverter(deps, ['cc'], ['CCONJ'])

def inverter(deps):
    # final inverter that combines the existing inverters in a certain order
    # the order is dictated syntactically, so that the most 'inner' things are changed in the end
    
    return invert_cc(invert_num(invert_case(invert_aux(invert_cop(invert_mark(deps))))))