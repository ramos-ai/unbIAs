# External imports
import re

# Local imports
from spacy_utils import get_nlp_en

def split_on_punctuation(sentence):
    splitted_sentence = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', sentence)
    return splitted_sentence

def split_on_subj_and_bsubj(sentence, people):
    sentence_splitted = []
    new_sent = ""   
    
    for token in sentence:
        if token not in people and token.pos_ != "DET":
            new_sent += token.text_with_ws
        elif token.pos_ == "DET" and token.head not in people:
            new_sent += token.text_with_ws
             
        if token.is_sent_end or token in people:
            if len(new_sent.strip()) > 0 and new_sent != ".":
                sentence_splitted.append(new_sent.strip())

            new_sent = ""
                       
    return sentence_splitted      


def get_new_sentence_without_subj(sentence_complete, sentence_to_remove):
    if len(sentence_to_remove) > 0:
        new_sentence = sentence_complete.text.split(sentence_to_remove)[-1]

    else:
        new_sentence = sentence_complete.text

    return get_nlp_en(new_sentence)

def get_subj_subtree(source_sentence, index):
    sentence = ""
  
    for subtree in source_sentence[index].head.subtree:
        sentence += subtree.text_with_ws

    return sentence  


def split_sentences_by_nsubj(source_sentence, subj_list):
    splitted = []
    sentence_complete = source_sentence
    sentence_to_remove = ""

    for sub in subj_list:
        sentence = get_new_sentence_without_subj(sentence_complete, sentence_to_remove)
        for token in sentence:
            if token.text == str(sub):
                sentence_to_remove = get_subj_subtree(sentence, token.i)
                splitted.append(sentence_to_remove)

    return splitted
