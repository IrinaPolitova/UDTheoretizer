import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import spacy

def graph_viz(deps):
    # visualizes the dependencies deps as a graph using the networkx library
    
    edges = [(dep['head'], dep['id']) for dep in deps if dep['head'] != dep['id']]
    node_labels = {dep['id']: dep['text'] for dep in deps}

    node_colors = {}
    for dep in deps:
        if dep['id'] != dep['head']:
            node_colors[dep['id']] = 'black'
        else:
            node_colors[dep['id']] = 'red'

    G = nx.DiGraph()
    G.add_edges_from(edges)
    
    if len(edges) > 0:
        layout = {dep['id']: [dep['id'], 0] for dep in deps}
        left = [edge for edge in edges if edge[0] > edge[1]]
        right = [edge for edge in edges if edge[0] < edge[1]]
        left_labels = {edge: deps[edge[1]]['dep'] for edge in left}
        right_labels = {edge: deps[edge[1]]['dep'] for edge in right}
        max_len = max([np.abs(edge[1] - edge[0]) for edge in edges])
        word_len = max([len(dep['text']) for dep in deps])
        
        plt.figure(figsize=(len(deps)*2+word_len, max_len+word_len/4))
        nx.draw_networkx_edges(G, pos=layout, alpha=0.5, edgelist=left, connectionstyle='arc3, rad=0.5')
        nx.draw_networkx_edges(G, pos=layout, alpha=0.5, edgelist=right, connectionstyle='arc3, rad=-0.5')
        nx.draw_networkx_labels(G, pos=layout, font_color=node_colors, labels=node_labels)
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=left_labels, connectionstyle='arc3, rad=0.5')
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=right_labels, connectionstyle='arc3, rad=-0.5')
        plt.axis('off')
        plt.show()

    else:
        if len(deps) == 1:
            word_len = len(deps[0]['text'])
        else:
            word_len = 1
        layout = {0: [0.5, 0.5]}
        plt.figure(figsize=(word_len, 1))
        nx.draw_networkx_labels(G, pos=layout, font_color=node_colors, labels=node_labels)
        plt.axis('off')
        plt.show()

def doc_viz(deps, nlp, parser):
    # turns the dependencies deps into a standard spacy doc object

    if parser == 'stanza':
        return 'This format not available for stanza!'
        
    elif parser in ['spacy-udpipe', 'spacy']:
    
        mydeps = deps.copy()
        words, lemmas, morphs, pos, heads, deps = [], [], [], [], [], []
        
        for d in mydeps:
            words.append(d['text'])
            lemmas.append(d['lemma'])
            morphs.append(str(d['gram']))
            pos.append(d['pos'])
            heads.append(d['head'])
            deps.append(d['dep'])
            
        spaces = [True] * len(words)
    
        result = spacy.tokens.doc.Doc(vocab=nlp.vocab,
                                      words=words,
                                      spaces=spaces,
                                      lemmas=lemmas,
                                      morphs=morphs,
                                      pos=pos,
                                      heads=heads,
                                      deps=deps)
    
        return result

def visualizer(deps, out, nlp, parser):
    # final function that takes dependencies deps and visualizes them in a necessary format
    # the argument 'out' determines the format in which it should be given
    
    if out == 'dict':
        return deps
    elif out == 'graph':
        return graph_viz(deps)
    elif out == 'doc':
        return doc_viz(deps, nlp, parser)
    else:
        return 'Format unknown, the "out" argument must be "dict", "graph", or "doc".'
