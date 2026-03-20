from inverters import inverter
from visualizers import visualizer

class UDTheoretizer:

    def __init__(self, parser='spacy-udpipe', model='ru'):
        # initializes the original parser

        self.parser = parser

        if self.parser == 'spacy':
            import spacy
            self.nlp = spacy.load(model)
        
        elif self.parser == 'stanza':
            import stanza
            self.nlp = stanza.Pipeline(model)
        
        else:
            if self.parser != 'spacy-udpipe':
                print('Parser unknown! Spacy-udpipe will be used instead')
                self.parser = 'spacy-udpipe'
            import spacy_udpipe
            self.nlp = spacy_udpipe.load(model)

    def get_original_analysis(self, sentence, out='dict'):
        # returns the original analysis produced by spacy-udpipe or another parser
        # the argument 'out' determines the format in which it must be returned
        
        doc = self.nlp(sentence)
        deps = []
        
        if self.parser in ['spacy-udpipe', 'spacy']:
            for token in doc:
                deps.append({'id': token.i,
                             'text': token.text,
                             'lemma': token.lemma_,
                             'pos': token.pos_,
                             'gram': str(token.morph),
                             'head': token.head.i,
                             'dep': token.dep_})
        
        elif self.parser == 'stanza':
            for sentence in doc.sentences:
                for token in sentence.words:
                    if token.head == 0:
                        head = token.id-1
                    else:
                        head = token.head-1
                    deps.append({'id': token.id-1,
                                 'text': token.text,
                                 'lemma': token.lemma,
                                 'pos': token.upos,
                                 'gram': str(token.feats),
                                 'head': head,
                                 'dep': token.deprel})
        
        return visualizer(deps, out, nlp=self.nlp, parser=self.parser)

    def get_theoretical_analysis(self, sentence, out='dict'):
        # returns a more theoretical version of the analysis
        # the argument 'out' determines the format in which it must be returned
        
        deps = self.get_original_analysis(sentence, out='dict')
        deps = inverter(deps)
        return visualizer(deps, out, nlp=self.nlp, parser=self.parser)
