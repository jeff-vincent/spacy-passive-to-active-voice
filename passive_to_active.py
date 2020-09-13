import spacy

pronouns = {'her ':'she ', 'him ':'he ', 'whom ':'who ', 'me ': 'I ', 'us ':'we ', 'them ':'they '}

nlp = spacy.load('en_core_web_sm')

with open('passive.txt', 'r') as text:
    doc = nlp(text.read())

for sent in doc.sents:
    try:
        sent_list = []
        for token in sent:
            sent_list.append(token)

        main_verb_index = None
        agent_index = None
        recipient_index = None
        agent = ''
        append = False
        inflection = ''
        agent_article = ''
        start_word = ''
        sentence_remainder = []
    
        index_counter = 0

        for token in sent_list:
            if token.dep_ in ['nsubjpass', 'nsubj']:
                recipient_index = index_counter
                recipient = token.lower_
                article_list = [t.text for t in token.lefts]
                try:
                    compound_article = ' '.join(article_list).lower()
                except:
                    compound_article = ''
            if token.dep_ == 'ROOT':
                main_verb_index == index_counter
                main_verb = token.text
                base_form_of_main_verb = token.lemma_
                # TODO: convert VBN to VBD
                # if token.tag_ == 'VBN':
            
            if token.dep_ == 'agent':
                agent_index = index_counter
                agent_children_list = [t.text for t in token.rights]
                agent_children_right = ' '.join(agent_children_list)
                agent = token.text + ' ' + agent_children_right
                agent_children_left = [t.text for t in token.lefts]
                append = True
            if agent and not token.is_punct:
                sentence_remainder.append(token)
            if token.is_punct:
                punct = token.text
            if token.dep_ == 'pobj':
               append = False
               if not agent:
                   agent = token.text
            if token.text in ['may', 'must', 'might', 'could', 'will']:
                inflection = ' ' + token.text + ' '

            index_counter += 1
        if punct in ['?']:
            for token in sent:
                if token.text in ['Can', 'May']:
                    start_word = token.text
                    break

        for key, value in pronouns.items():
            if key in agent.lower() + ' ':
                agent = value.strip()
        index = 0 
        for t in sentence_remainder:
            if t.pos_ in ['DET'] and index >= 2:
                agent_article = t.text
                index += 1

        if recipient_index < agent_index:
            print('-'*50+'\n {}'.format(
                sent)+'\n Active voice skeleton:{} {} {} {}{} {} {}{}'.format(
                    start_word, agent_article, agent, inflection, main_verb, compound_article, recipient, punct).replace(
                        'by ', ''))
            print('Base form of main verb: {}'.format(base_form_of_main_verb))
    except:
        print(sent)
        for token in sent:
            print('Text: ' + token.text + ' |   Dep: ' + token.dep_ + ' |   Tag: ' + token.tag_)
