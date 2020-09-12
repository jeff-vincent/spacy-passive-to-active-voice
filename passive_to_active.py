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
                # TODO: convert VBN to VBD
                # if token.tag_ == 'VBN':
            
            if token.dep_ == 'agent':
                agent_index = index_counter
                agent = token.text
                append = True
            if agent and token.text != agent and not token.is_punct:
                agent = agent + ' ' + token.text + ' '
            if token.is_punct:
                punct = token.text
            if token.dep_ == 'pobj':
               append = False
               if not agent:
                   agent = token.text
            if token.text in ['may', 'must', 'might', 'could', 'will']:
                inflection = ' ' + token.text + ' '

            index_counter += 1

        for key, value in pronouns.items():
            if key in agent.lower() + ' ':
                agent = value

        if recipient_index < agent_index:
            print('-'*50+'\n {}'.format(
                sent)+'\n Active voice skeleton: {}{}{} {} {}{}'.format(
                    agent, inflection, main_verb, compound_article, recipient, punct).replace('by the', 'The').replace(' by ', ' '))
    except:
        print(sent)
        for token in sent:
            print('Text: ' + token.text + ' |   Dep: ' + token.dep_ + ' |   Tag: ' + token.tag_)
