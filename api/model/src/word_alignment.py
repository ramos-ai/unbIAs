"""Usage:
    word_alignment.py --first_sentence=SOURCE --second_sentence=TARGET [--debug]
"""
# External imports
import logging
from docopt import docopt
from simalign import SentenceAligner

# Local imports
from spacy_utils import get_people_source, get_translation_with_punctuation

#matching-methods = "m: Max Weight Matching (mwmf), a: argmax (inter), i: itermax, f: forward (fwd), r: reverse (rev)"
def initialize(first_sentence, second_sentence, model, matching_methods, align):
    myaligner = SentenceAligner(model=model, token_type="bpe", matching_methods=matching_methods)
    alignments = myaligner.get_word_aligns(first_sentence, second_sentence)
    return alignments[align]

def get_word_alignment_pairs(first_sentence, second_sentence, model="bert-base-uncased", matching_methods = "i", align = "itermax"):
    source_tokens, target_tokens = format_sentences(first_sentence, second_sentence)
    sent1 = []
    sent2 = []
    print("Possible Alignments From SimAlign")
    print("Word in Sent 1 -----> Word in Sent 2")
    alignments = initialize(source_tokens, target_tokens, model, matching_methods, align)
    for item in alignments:
     print(source_tokens[item[0]],"---------->", target_tokens[item[1]])
     sent1.append(source_tokens[item[0]])
     sent2.append(target_tokens[item[1]])

    word_align_pairs = zip(sent1,sent2)
    return list(word_align_pairs) 

def format_sentences(first_sentence, second_sentence):
    sent1 = first_sentence.strip(".").split() if type(first_sentence) == str else first_sentence.text.strip(".").split()
    sent2 = second_sentence.strip(".").split() if type(second_sentence) == str else second_sentence.text.strip(".").split()

    return sent1, sent2

def get_align_people(source_sentence, translation_sentence):
    word_alignments = get_word_alignment_pairs(source_sentence.text_with_ws, translation_sentence.text_with_ws, model="bert", matching_methods = "i", align = "itermax")
    source_people = get_people_source(source_sentence)
    people = [token.text for token in source_people]
    people_align = []
    for sent1, sent2 in word_alignments:
        if sent1 in people: 
            people_align.append(sent2)
        elif sent2 in people:  
            people_align.append(sent1)  

    people_list = []
    for token in translation_sentence:
        if token.text in people_align:
            people_list.append(token)

    return people_list    

def get_translations_aligned_model_google(translation_google, translations_aligned, subj_translated):
        alignment_with_translation = get_word_alignment_pairs(translation_google.text, translations_aligned, model="bert", matching_methods = "i", align = "itermax")
        translated = ""
        subj_translated_split = subj_translated.split()
        
        for first_sentence, second_sentence in alignment_with_translation: 
            last_word = translated.strip().split(" ")[-1]
            if second_sentence in subj_translated_split and second_sentence != last_word and second_sentence not in translated:
                translated += second_sentence + " "
            elif first_sentence[:-1] != last_word[:-1] or len(translated) == 0:
                translated += first_sentence + " "

        translated_nlp = get_translation_with_punctuation(translated)
        return translated_nlp  

def get_people_model_people_control_model(source_sentence, translation_model_nlp, people_to_neutral_source, sub_split):
    alignment_model = get_word_alignment_pairs(source_sentence.text, translation_model_nlp.text, model="bert", matching_methods = "i", align = "itermax")
    people_model = ""
    people_control_model = ""
    
    for first_sentence, second_sentence in alignment_model:
        if first_sentence in people_to_neutral_source:
            people_control_model = second_sentence.strip(",").strip(".")
        if first_sentence == sub_split:
            people_model = second_sentence.strip(",").strip(".")

    return people_model, people_control_model

def get_people_google_people_to_neutral(source_sentence, translation_nlp, people_to_neutral_source, sub_split):
    people_to_neutral= []
    people_google = ""
    
    alignment = get_word_alignment_pairs(source_sentence.text, translation_nlp.text, model="bert", matching_methods = "i", align = "itermax")
    
    for first_sentence, second_sentence in alignment:
      first_sent = first_sentence.split('\'')[0]
      if first_sentence in people_to_neutral_source or first_sent in people_to_neutral_source:
        people_to_neutral.append(second_sentence.strip(",").strip("."))
      elif first_sentence == sub_split:
          people_google = second_sentence
          
    return people_google,  people_to_neutral  

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    first_sentence_fn = args["--first_sentence"]
    second_sentence_fn = args["--second_sentence"]
    debug = args["--debug"]

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    word_alignment = get_word_alignment_pairs(first_sentence_fn, second_sentence_fn)
    print(word_alignment)

    logging.info("DONE")    