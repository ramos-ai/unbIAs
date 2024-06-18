# Local imports
from gender_inflection import get_just_possible_words
from spacy_utils import get_nlp_en

def format_question(source_sentence):
    token = source_sentence.split()[0]
    if token.lower() == "did":
        return source_sentence[1:]
    
    return source_sentence

def format_sentence(sentence):
    new_sentence = ""
    for token in sentence:
        if "CONJ" in token.pos_ or "PUNCT" in token.pos_:          
            new_sentence = new_sentence.strip() + "###" + token.text_with_ws
        else:
            new_sentence += token.text_with_ws

    splitted = new_sentence.split("###")
    return splitted  
   
def should_remove_first_word(sentence):
    sent = get_nlp_en(sentence)
    for token in sent:
        return (token.pos_ == "CCONJ" or token.is_punct) and token.i == 0

def should_remove_last_word(sentence):
    sent = get_nlp_en(sentence)
    for token in sent:
        return (token.pos_ == "CCONJ" or token.is_punct) and token.is_sent_end

def format_translations_subjs(index_to_replace, sentence, inflections):
    translations = []
    for id in range(3):
        new_sentence = ""
        cont = 0
        for index, word in enumerate(sentence):
            if index not in index_to_replace:
                new_sentence += word.text_with_ws
            else:
                new_sentence += inflections[cont][id] + " "
                cont = cont + 1
        sentence_formatted = new_sentence[0].capitalize() + new_sentence[1:]
        translation = format_translation(sentence_formatted)
        translations.append(translation)

    return translations

def get_formatted_translations_nsubj_and_pobj_with_pronoun(translation_nlp, people_to_neutral, people_control_model):
    words_to_neutral = []
    index_to_replace = []
    for index, token in enumerate(translation_nlp):
            if token.head.text in people_to_neutral or token.head.text[:-1] in people_to_neutral or token.head.lemma_ in people_to_neutral or token.text in people_to_neutral or token.text[:-1] in people_to_neutral or token.lemma_ in people_to_neutral :
                words_to_neutral.append(token)
                index_to_replace.append(index)

    inflections = get_just_possible_words(words_to_neutral)
    first_sentence, second_sentence, neutral  = format_translations_subjs(index_to_replace, translation_nlp, inflections)
    translation = format_translations_subjs(index_to_replace, translation_nlp, inflections)
    
    sentence_more_likely = [sentence for sentence in translation if people_control_model in sentence]        
    if second_sentence == sentence_more_likely:
        more_likely = second_sentence
        less_likely = first_sentence
    else:
        more_likely = first_sentence
        less_likely = second_sentence
        
    return more_likely, less_likely, neutral

def format_translation(translation):
    sentence = translation.replace(" ,", ",").replace(" .", ".").replace(" ;", ";").replace(" ?", "?")
    
    return sentence

def join_translations(translations):
    obj = {'first_sentence': '', 'second_sentence': '', 'neutral': ''}

    if len(translations) == 1:
        return translations[0]
    
    for sentence in translations:
        if len(sentence) == 2:
            obj['first_sentence'] = obj['first_sentence'] + ' ' + sentence['translation']
            obj['second_sentence'] = obj['second_sentence'] + ' ' + sentence['translation']
            obj['neutral'] = obj['neutral'] + ' ' + sentence['neutral']
        else:
            obj['first_sentence'] = obj['first_sentence'] + ' ' + sentence['first_option']
            obj['second_sentence'] = obj['second_sentence'] + ' ' + sentence['second_option']
            obj['neutral'] = obj['neutral'] + ' ' + sentence['neutral']    
    
    return obj