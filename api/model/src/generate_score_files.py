"""Usage:
    generate_score_files.py [--debug]
"""

# External imports
import logging
from docopt import docopt
import json
import random

# Local imports
from generate_translations import generate_translations
from spacy_utils import get_sentence_with_punctuation, get_translation_with_punctuation
from split_sentence import split_on_punctuation

def generate_translations_test_wino():
    """
    Creates a file with 10 translations of random sentences from WinoMT challenge set
    """
    english_sentences = get_english_sentences()
    google_translation = get_google_translations()
    
    random_index = random.sample(range(0, 3888), 10)

    for index in random_index:
        source_sentence = get_sentence_with_punctuation(english_sentences[index])
        translation_google = get_translation_with_punctuation(google_translation[index])
        translation = generate_translations(source_sentence, translation_google)
        
        name_file = './data_score/wino/model-teste-1.txt'
        with open(name_file, 'a') as gen_file:
            gen_file.write("==> index    "+str(index)+"  ====>\n")
            gen_file.write(json.dumps(translation))
            gen_file.write("\n") 
            
def generate_translations_test_bleu():
    """
    Creates a file with 10 translations of random sentences from TED Talks to check BLEU score
    """
    english_sentences = get_english_sentences_bleu()
    google_translation = get_google_translations_bleu()
    
    random_index = random.sample(range(0, 1200), 20)

    for index in random_index:
        source_sentence = get_sentence_with_punctuation(english_sentences[index])
        translation_google = get_translation_with_punctuation(google_translation[index])
        translation = generate_translations(source_sentence, translation_google)
        
        name_file = './data_score/model-teste-bleu-1.txt'
        with open(name_file, 'a') as gen_file:
            gen_file.write("==> index    "+str(index)+"  ====>\n")
            gen_file.write(json.dumps(translation))
            gen_file.write("\n")             

def generate_translations_wino():
    """
    Creates a file with 3888 translations of WinoMT challenge set
    """
    english_sentences = get_english_sentences()
    google_translation = get_google_translations()
    translations = []
    
    start = 0
    end = 3888

    for index in range(start, end):
        source_sentence = get_sentence_with_punctuation(english_sentences[index])
        translation_google = get_translation_with_punctuation(google_translation[index])
        translation = generate_translations(source_sentence, translation_google)
        translations.append(translation)
        
        name_file = './data_score/wino/model-teste.txt'
        with open(name_file, 'a') as gen_file:
            gen_file.write(translation)
            gen_file.write("\n") 


def generate_translations_bleu(): 
    """
    Creates a file with 1200 translations of TED Talk for BLEU score
    """   
    english_sentences = get_english_sentences_bleu()
    google_translation = get_google_translations()
    translations = []
    start = 0
    end = 1200
    
    for index in range(start, end):
        sent_english = split_on_punctuation(english_sentences[index])
        sent_trans = split_on_punctuation(google_translation[index])
        translations = ""
        for ind, sentence in enumerate(sent_english):
            source_sentence = get_sentence_with_punctuation(sentence)
            translation_google = get_translation_with_punctuation(sent_trans[ind])
            
            translation = generate_translations(source_sentence, translation_google)
            translations += translation + " "

        name_file = './data_score/model-en-pt-ted.txt'
        with open(name_file, 'a') as gen_file:
            gen_file.write(translations.strip())
            gen_file.write("\n") 
       

def get_google_translations():
    portuguese_sentences = []

    with open('./data_score/wino/en-pt.txt') as sentences: 
        for line in sentences:
            portuguese_sentences.append(line.strip())

    return portuguese_sentences

def get_english_sentences():
    english_sentences = []

    with open('./data_score/wino/en.txt') as sentences: 
        for line in sentences:
            sp = line.split("\t")
            english_sentences.append(sp[2])

    return english_sentences

def get_google_translations_bleu():
    english_sentences = []

    with open('./data_score/pt-ted-google.txt') as sentences: 
        for line in sentences:
            english_sentences.append(line.strip())

    return english_sentences

def get_english_sentences_pro():
    english_sentences = []

    with open('./data_score/wino/en_pro.txt') as sentences: 
        for line in sentences:
            sp = line.split("\t")
            english_sentences.append(sp[2])

    return english_sentences

def get_english_sentences_anti():
    english_sentences = []

    with open('./data_score/wino/en_anti.txt') as sentences: 
        for line in sentences:
            sp = line.split("\t")
            english_sentences.append(sp[2])

    return english_sentences

def get_english_sentences_bleu():
    english_sentences = []

    with open('./data_score/en-ted.txt') as sentences: 
        for line in sentences:
            english_sentences.append(line.strip())

    return english_sentences

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    debug = args["--debug"]

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    translation = generate_translations_test_wino()
    print(translation)

    logging.info("DONE")