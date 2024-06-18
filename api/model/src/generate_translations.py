#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Usage:
    generate_translations.py --sentence=SENTENCE [--translation=TRANS] [--debug]
"""

# External imports
import logging
from docopt import docopt
import more_itertools

# Local imports
from spacy_utils import get_morph, get_people_source, get_pronoun_on_sentence, get_pronoun_on_sentence_with_it, get_sentence_with_punctuation, get_sentence_with_punctuation_text, get_translation_with_punctuation, is_plural, \
    get_only_subject_sentence, get_people, get_nlp_en, get_sentence_gender, get_nsubj_sentence, get_nlp_pt, get_noun_chunks
from generate_model_translation import generate_translation_with_constraints, generate_translation
from gender_inflection import get_just_possible_words, format_sentence_inflections, get_just_possible_words_sentence
from constrained_beam_search import get_constrained_subject_and_neutral, get_constraints_one_subj, get_constrained_translation, get_constraints_without_people, \
    get_translation_constrained_and_aligned_different_gender, get_translation_constrained_and_aligned_same_gender, get_translations_aligned, get_word_to_add
from roberta import get_disambiguate_pronoun, get_roberta_subject
from split_sentence import split_on_punctuation, split_sentences_by_nsubj
from format_translations import format_question, format_sentence, get_formatted_translations_nsubj_and_pobj_with_pronoun, join_translations, should_remove_first_word, should_remove_last_word
from translation_google import get_google_translation
from word_alignment import get_align_people, get_people_google_people_to_neutral, get_people_model_people_control_model, get_translations_aligned_model_google
from generate_neutral import make_neutral


def translate(source_sentence):
    """
    Main method, receives source sentence, splits it on punctuation, generates it translations and 
    returns to the APP
    """
    
    sent_english = split_on_punctuation(source_sentence)
    translations = []
    
    for sentence in sent_english:
        source_sentence = get_sentence_with_punctuation(sentence)
        translation = get_google_translation(source_sentence.text)
        
        translation_google = get_translation_with_punctuation(translation)
            
        translation = generate_translations(source_sentence, translation_google)
        translations.append(translation)
    
    return join_translations(translations)


def generate_translations(source_sentence, google_translation):
    """
    Performs linguistic analysis and directs to the correct method to generate the translation
    """
    try:
        if ' ' not in source_sentence.text.strip():
            return get_translation_for_one_word(source_sentence.text,
                    google_translation.text)

        subjects = get_nsubj_sentence(source_sentence)
        pronoun_list = get_pronoun_on_sentence(source_sentence)
        pronoun_list_it = \
            get_pronoun_on_sentence_with_it(source_sentence)
        gender = get_sentence_gender(source_sentence)
        people_source = get_people_source(source_sentence)

        is_all_same_pronoun = is_all_equal(pronoun_list)
        is_all_same_subject = is_all_equal(subjects)

        if is_all_same_pronoun and is_all_same_subject and len(pronoun_list_it) > 0 and len(subjects) > 0 and len(people_source) <= len(pronoun_list_it) and len(people_source) > 0:
            if is_neutral(pronoun_list, gender):
                return generate_translation_for_one_subj_neutral(source_sentence, google_translation)
            return generate_translation_for_one_subj(source_sentence, google_translation)
        
        elif len(pronoun_list) == 1 and len(people_source) == 0:
             return generate_translation_for_one_subj(source_sentence, google_translation)
        
        elif len(gender) == 0 and len(set(pronoun_list)) == 0 and len(subjects) == 0:
            return generate_translation_with_subject_and_neutral(source_sentence, google_translation)
        
        elif len(gender) == 0 and len(set(pronoun_list)) == 0 and len(subjects) > 0 or len(gender) == 1 and len(pronoun_list) == 1 and len(people_source) == 0:
            return generate_translation_with_subject_and_neutral(source_sentence, google_translation)
        
        elif len(set(pronoun_list)) == 1 and all('it' == elem.text for elem in pronoun_list_it):
            return generate_translation_it(source_sentence, google_translation)
        
        elif len(pronoun_list) > 0 and (len(people_source) > len(pronoun_list) or len(people_source) > len(gender) or len(gender) > 1 and 'Neut' in gender):
            return generate_translation_for_nsubj_and_pobj_with_pronoun(source_sentence, google_translation)
        
        elif len(subjects) == len(pronoun_list) and len(subjects) > 0 and len(gender) > 1:
            return generate_translation_more_subjects(source_sentence, subjects, google_translation, people_source)
        
        elif len(subjects) > len(pronoun_list) and (len(people_source) == 0 or len(pronoun_list_it) == 0):
            return generate_translation_without_people(source_sentence, google_translation)
        
        else:
            return generate_translation_for_nsubj_and_pobj_with_pronoun(source_sentence, google_translation)
    
    except:
        model_translation = generate_translation(source_sentence.text_with_ws)
        model_nlp = get_nlp_pt(model_translation)
        (first_option, second_option, neutral) = generate_neutral_translation(model_nlp)
        
        return {'first_option': first_option, 'second_option': second_option, 'neutral': neutral}


def is_all_equal(list):
    return all(i.text == list[0].text for i in list)


def is_neutral(pronoun_list, gender):
    return ['Neut'] == gender or len(gender) == 0 or len(pronoun_list) == 0 or all('I' == elem.text for elem in pronoun_list) or all('they' == elem.text.lower() for elem in pronoun_list) or all('we' == elem.text.lower() for elem in pronoun_list)


def get_translation_for_one_word(source_sentence, google_translation):
    """
    Generate translation for one word and returns it inflections, ex Cat 
    Returns: {possible_words}: [masculine, feminine, neutral]
    """
    translation = generate_translation(source_sentence)
    formatted = translation.rstrip('.')
    formatted_translation = get_nlp_pt(formatted)
    source = get_nlp_en(source_sentence)
    is_source_plural = is_plural(source)
    is_translation_plural = is_plural(formatted_translation)

    if is_source_plural != is_translation_plural:
        formatted_translation = google_translation

    possible_words = get_just_possible_words(formatted_translation)[0]
    first_sentence, second_sentence, neutral = [word.capitalize() for word in
                                possible_words]

    return {'first_option': first_sentence, 'second_option': second_sentence, 'neutral': neutral}


def generate_translation_for_one_subj_neutral(source_sentence, google_translation):
    """
    Generate translation for sentence with entity and neutral in source, ex I like to read a lot
    Returns: {'first_option': first_sentence, 'second_option': second_sentence, 'neutral': neutral}
    """
    translation_nlp = google_translation

    people = get_people(translation_nlp)
    constrained_splitted = get_constrained_translation(translation_nlp,
            people)
    
    if len(constrained_splitted) == 0:
        return generate_neutral_translation(translation_nlp)

    translations = []
    for constraints in constrained_splitted:
        constrained_translation = generate_translation_with_constraints(source_sentence.text_with_ws, constraints)
        translations.append(constrained_translation)

    translation = get_translations_aligned(translations,
            constrained_splitted, source_sentence)

    
    translation_formatted = get_translation_with_punctuation(translation_formatted.text)
    possible_words = get_just_possible_words(translation)
    first_sentence, second_sentence, neutral = format_sentence_inflections(possible_words)

    return {'first_option': first_sentence, 'second_option': second_sentence, 'neutral': neutral}


def generate_translation_for_one_subj(source_sentence, google_translation):
    """
    Generate translation for sentence one entity and gender in source, ex The doctor finished her work
    Returns: {'translation': first_sentence, 'neutral': neutral}
    """
    translation_google = google_translation
    subject = get_only_subject_sentence(translation_google)
    pronoun_list = get_pronoun_on_sentence(source_sentence)
    gender = get_sentence_gender(source_sentence)
    
    if is_neutral(pronoun_list, gender):
            return generate_translation_for_one_subj_neutral(source_sentence, google_translation)

    constrained_splitted = get_constraints_one_subj(translation_google, [subject])
    if len(constrained_splitted) == 0:
        constrained_splitted = get_constraints_without_people(google_translation)
    
    translations = []
    for constraints in constrained_splitted:
        constrained_translation = generate_translation_with_constraints(source_sentence.text_with_ws, constraints)
        translations.append(constrained_translation)

    translation = get_translations_aligned(translations, constrained_splitted, source_sentence)
    
    possible_words = get_just_possible_words(translation)
    first_sentence, second_sentence, neutral = format_sentence_inflections(possible_words)


    return {'translation': first_sentence, 'neutral': neutral}


def generate_translation_for_sentence_without_pronoun_and_gender(source_sentence, google_translation):
    """
    Generate translation for sentence without gender and entity, ex The dog
    Returns: {'first_option': first_sentence, 'second_option': second_sentence, 'neutral': neutral}
    """
    translation = generate_translation(source_sentence.text_with_ws)
    translation_nlp = get_translation_with_punctuation(translation)

    possible_words = get_just_possible_words_sentence(translation_nlp)
    (first_option, second_option, neutral) = format_sentence_inflections(possible_words)

    return {'first_option': first_option,'second_option': second_option, 'neutral': neutral}

def generate_translation_with_subject_and_neutral(source_sentence, google_translation):
    """
    Generate translation for sentence without gender or gender neutral and subject, ex Mari is a great kisser
    Returns: {'first_option': first_sentence, 'second_option': second_sentence, 'neutral': neutral}
    """
    source = format_question(source_sentence.text) ################
    translation_model = generate_translation(source)
    constraints = get_constrained_subject_and_neutral(google_translation)

    translation = get_translations_aligned_model_google(google_translation, translation_model, constraints)
    possible_words = get_just_possible_words_sentence(translation)
    (first_option, second_option, neutral) = format_sentence_inflections(possible_words)

    return {'first_option': first_option, 'second_option': second_option, 'neutral': neutral}


def generate_translation_it(source_sentence, google_translation):
    """
    Generate translation for sentence with 'it' as only pronoun, ex The trophy would not fit in the brown suitcase because it was too big.
    Returns: {'translation_it': first_option}
    """
    google_trans = google_translation
    it_token = get_nlp_pt('it')
    subj_roberta = get_disambiguate_pronoun(source_sentence, it_token)

    google_trans = get_nlp_pt(google_trans)

    sentence_splitted_source = format_sentence(source_sentence)

    index_it = 0
    index_without_it = 0
    for (index, sentence) in enumerate(sentence_splitted_source):
        if ' it ' in sentence:
            index_it = index
        else:
            index_without_it = index

    sentence_splitted_trans = format_sentence(google_trans)
    sentence_pt_with_it = sentence_splitted_trans[index_it]

    noun_chunks_source = get_noun_chunks(source_sentence)
    noun_chunks_pt = get_noun_chunks(google_trans)

    index_subj = 0
    for (index, chunk) in enumerate(noun_chunks_source):
        if subj_roberta in chunk.text_with_ws:
            index_subj = index

    sub = noun_chunks_pt[index_subj]
    gender_sub = get_sentence_gender(sub)
    sentence_pt = get_nlp_pt(sentence_pt_with_it)
    gender_chunk = get_sentence_gender(sentence_pt)

    if all(i == gender_sub[0] for i in gender_chunk):
        translation = get_sentence_with_punctuation_text(google_trans)
        return {'translation_it': translation}
    
    else:
        possible_words = get_just_possible_words(sentence_pt)
        sentences = format_sentence_inflections(possible_words)
        sentence = sentence_splitted_trans[index_without_it]
        first_option = sentence + ' ' + sentences['first_option'].lower().replace('.', '').strip() + '.'

        return {'translation_it': first_option}


def generate_translation_for_nsubj_and_pobj_with_pronoun(source_sentence, google_translation):
    """
    Generate translation for sentence with more entities than gender indications, ex The chief gave the housekeeper a tip because she was satisfied.
    Returns: {'first_option': more_likely, 'second_option': less_likely, 'neutral': neutral}
    """
    translation_nlp = google_translation
    people = get_align_people(source_sentence, translation_nlp)
    translation_model = generate_translation(source_sentence)

    source_nlp = get_nlp_en(source_sentence)
    translation_model_nlp = get_nlp_pt(translation_model)
    people_model = get_align_people(source_nlp, translation_model_nlp)

    subjects = get_roberta_subject(source_sentence)
    sub_split = subjects[0].split()[-1]

    source_people = get_people_source(source_sentence)
    people_to_neutral_source = [person.text for person in source_people if person.text != sub_split]

    (people_model, people_control_model) = get_people_model_people_control_model(source_sentence, translation_model_nlp, people_to_neutral_source, sub_split)
    (people_google, people_to_neutral) = get_people_google_people_to_neutral(source_sentence, translation_nlp, people_to_neutral_source, sub_split)

    people_model_nlp = get_nlp_pt(people_model)
    people_google_nlp = get_nlp_pt(people_google)
    model_morph = get_morph(people_model_nlp)
    model_google = get_morph(people_google_nlp)

    gender_people_model = get_sentence_gender(people_model_nlp)

    if (people_google == None or len(people_google) == 0) and len(people_model_nlp) > 0:
        translation_nlp = translation_model_nlp
    
    elif len(gender_people_model) > 0 and model_morph != model_google:
        translation_nlp = get_translation_constrained_and_aligned_different_gender(translation_nlp, people, source_sentence, subjects)
    
    elif people_model == people_google:
        translation_nlp = get_translation_constrained_and_aligned_same_gender(people_google, translation_model_nlp, people_model, translation_nlp)

    (more_likely, less_likely, neutral) = get_formatted_translations_nsubj_and_pobj_with_pronoun(translation_nlp, people_to_neutral, people_control_model)

    return {'first_option': more_likely, 'second_option': less_likely, 'neutral': neutral}


def generate_translation_without_people(source_sentence, google_translation):
    """
    Generate translation for sentence without entity, ex It is difficult to walk in the sand.
    Returns: {'first_option': first_sentence, 'second_option': second_sentence, 'neutral': neutral}
    """
    constrained_splitted = get_constraints_without_people(google_translation)

    translations = []
    for constraints in constrained_splitted:
        constrained_translation = generate_translation_with_constraints(source_sentence.text_with_ws, constraints)
        translations.append(constrained_translation)

    translations_aligned_model = get_translations_aligned(translations,
            constrained_splitted, source_sentence)

    translation_nlp = get_translation_with_punctuation(translations_aligned_model.text)

    possible_words = get_just_possible_words_sentence(translation_nlp)
    first_sentence, second_sentence, neutral = format_sentence_inflections(possible_words)

    return {'first_option': first_sentence, 'second_option': second_sentence, 'neutral': neutral}


def generate_translation_more_subjects(source_sentence, subjects, google_translation, people):
    """
    Generate translation for sentence with several entities and pronouns, ex The doctor finished her work but the nurse was still eating his lunch.
    Returns: {'first_option': first_sentence, 'second_option': second_sentence, 'neutral': neutral}
    """
    sentence = format_sentence(source_sentence)
    
    if len(people) == 0:
        translation = generate_translation(source_sentence)
        translation_nlp = get_nlp_pt(translation)
        possible_words = get_just_possible_words(translation_nlp)
        first_sentence, second_sentence, neutral = format_sentence_inflections(possible_words)

        return {'first_option': first_sentence, 'second_option': second_sentence, 'neutral': neutral}

    splitted_list = []
    for sent in sentence:
        sent = get_nlp_en(sent)
        splitted_list.append(split_sentences_by_nsubj(sent, subjects))

    collapsed = list(more_itertools.collapse(splitted_list))
    translations_more_likely = []
    translations_neutral = []

    for sentence in collapsed:
        should_remove_first = should_remove_first_word(sentence)
        should_remove_last = should_remove_last_word(sentence[-1])
        sentence_to_translate = ''
        word_to_add = ''
        word_to_add_last = ''
        if should_remove_first:
            sentence_to_translate = sentence.strip().split(' ', 1)[1]
            first_word = sentence.strip().split(' ', 1)[0]
            
            first_split = get_word_to_add(first_word) + ' '
            word_to_add = first_split.split(', ', 1)[0] + ' '
            
        elif should_remove_last:
            sentence_to_translate = sentence.strip()[:-1]
            last_word = sentence.strip().split(' ', 1)[-1]
            word_to_add_last = get_word_to_add(last_word)
        else:
            sentence_to_translate = sentence

        sent = get_nlp_en(sentence_to_translate)
        translations = generate_translation_for_one_subj(sent, google_translation)
        more_likely = word_to_add + translations['translation'] + word_to_add_last
        neutral = make_neutral(more_likely)
        translations_more_likely.append(more_likely)
        translations_neutral.append(neutral)

    sentence_more_likely = ' '.join(translations_more_likely).replace('.', '').lower().capitalize() + '.'
    sentence_neutral = ' '.join(translations_neutral).replace('.', '').lower().capitalize() + '.'

    return {'translation': sentence_more_likely,'neutral': sentence_neutral}


def generate_neutral_translation(translation):
    possible_words = get_just_possible_words(translation)
    (first_option, second_option, neutral) = format_sentence_inflections(possible_words)

    return {'first_option': first_option, 'second_option': second_option, 'neutral': neutral}


if __name__ == '__main__':
    # Parse command line arguments
    args = docopt(__doc__)
    sentence_fn = args['--sentence']
    translation_fn = args['--translation']
    debug = args['--debug']

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    sent = get_nlp_en(sentence_fn)
    trans = get_nlp_pt(translation_fn)
    translation = generate_translations(sent, trans)
    print('###########################')
    print('TRANSLATIONS: ', translation)
    print('###########################')

    logging.info('DONE')