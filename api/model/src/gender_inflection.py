"""Usage:
    gender_inflection.py --word=WORD [--debug]
"""
# External imports
import logging
from docopt import docopt
import ast
import csv
from pathlib import Path

# Local imports
from generate_neutral import make_neutral
from spacy_utils import get_nlp_pt, get_word_pos_and_morph

def get_gender_inflections(word):
    gender_inflections = {}
    text_raw, pos, morph = get_word_pos_and_morph(word)
    text = text_raw.lower()
    original_text = text
    gender = str(morph.get("Gender")).lower()
    number = str(morph.get("Number"))

    should_get_plural = 'Plur' in number

    if should_get_plural:
        text = text.rstrip("s")

    matches = get_matches(text, pos)
    if matches is None:
        return "No matches"

    gender_inflections['word'] = original_text
    gender_inflections['pos'] = pos
    forms = matches['forms']
    forms_obj = ast.literal_eval(forms)
    forms_matched = []

    for form in forms_obj:
        if any(gender not in string for string in form['tags']) and form['form'] != original_text:
            if should_get_plural and 'plural' in form['tags']:
                forms_matched.append(form)
            elif not should_get_plural and 'plural' not in form['tags']:
                forms_matched.append(form)

    if "fem" in gender and len(forms_matched) == 0 and text != matches['word']:
        form_obj = {'form': matches['word']}
        forms_matched.append(form_obj)

    if len(forms_matched) > 0:
        neutral = make_neutral(gender_inflections['word'])
        new_obj = {}
        new_obj['form'] = neutral.strip()
        new_obj['tags'] = ['neutral']
        forms_matched.append(new_obj)

    gender_inflections['forms'] = forms_matched
    return gender_inflections

def get_matches(text, pos):
    text_lower = text.lower()
    my_file = Path("model/src/pt-inflections-ordered.csv")
    if my_file.is_file():
        path = 'model/src/pt-inflections-ordered.csv'
    else:
        path = 'pt-inflections-ordered.csv'    

    with open(path, newline='') as users_csv:
        user_reader = csv.DictReader(users_csv)
        for row in user_reader:
            if row['word'] == text_lower and pos in row['pos'].upper():
                return row
            elif text_lower in row['forms'] and pos in row['pos'].upper():
                forms = row['forms']
                forms_obj = ast.literal_eval(forms)
                for form in forms_obj:
                    if text_lower == form['form']:
                        return row


def format_sentence_inflections(possible_words):
    combined = [j for i in zip(*possible_words) for j in i]
    last_word = possible_words[-1][-1]
    joined = " ".join(combined)
    joined_replace_comma = joined.replace(" ,", ",")
    joined_replace_dot = joined_replace_comma.replace(" .", ".")
    joined_replace_question_marks = joined_replace_dot.replace(" \"", "\"").replace("\" ", "\"")
    splitted_by_dot = joined_replace_question_marks.split(last_word)
    
    first_option = splitted_by_dot[0].strip()
    first_word = first_option[0].capitalize() + " " if len(first_option) == 1 else first_option[0].capitalize() 
    first_sentence = first_word + first_option[1:] + last_word
    
    second_option = splitted_by_dot[1].strip()
    first_word = second_option[0].capitalize() + " " if len(second_option) == 1 else second_option[0].capitalize() 
    second_sentence = first_word + second_option[1:] + last_word
    
    neutral = splitted_by_dot[2].strip()
    first_word = neutral[0].capitalize() + " " if len(neutral) == 1 else neutral[0].capitalize() 
    neutral_sentence = first_word + neutral[1:] + last_word
    
    return first_sentence, second_sentence, neutral_sentence


def get_just_possible_words(translation):
    forms_list = []
    for word in translation:
        if word.pos_ == "CCONJ" or word.pos_ == "PUNCT":
            forms_list.append([word.text, word.text, word.text])
        else:
            inflections = get_gender_inflections(word)
            forms = []
            if inflections == "No matches":   
                forms.append(word.text)
                forms.append(word.text)
                forms.append(word.text)
            else:    
                forms.append(inflections['word'])

                for inflection in inflections['forms']:
                    forms.append(inflection['form'])
                
                if len(inflections['forms']) == 0: 
                    forms.append(inflections['word'])
                    forms.append(inflections['word'])

            forms_list.append(forms)
    
    return forms_list

def get_just_possible_words_sentence(translation):
    forms_list = []
    for word in translation:
        if word.pos_ == "CCONJ" or word.pos_ == "PUNCT" or word.head.dep_ == 'obj':
            forms_list.append([word.text, word.text, word.text])
        else:
            inflections = get_gender_inflections(word)
            forms = []
            if inflections == "No matches":   
                forms.append(word.text)
                forms.append(word.text)
                forms.append(word.text)
            else:    
                forms.append(inflections['word'])

                for inflection in inflections['forms']:
                    forms.append(inflection['form'])
                
                if len(inflections['forms']) == 0: 
                    forms.append(inflections['word'])
                    forms.append(inflections['word'])

            forms_list.append(forms)
    
    return forms_list


if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    word_fn = args["--word"]
    debug = args["--debug"]

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    word = get_nlp_pt(word_fn)
    inflections = get_just_possible_words(word_fn)
    print(inflections)

    logging.info("DONE")
