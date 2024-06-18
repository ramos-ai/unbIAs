"""Usage:
    generate_neutral.py --sentence=SENTENCE [--debug]
"""

# External imports
import logging
from docopt import docopt

# Local imports
from spacy_utils import get_nlp_pt

def make_neutral(sentence):
    sentence = get_nlp_pt(sentence)
    new_sentence = ""
    for token in sentence:
        gender = token.morph.get("Gender")
        
        if len(gender) > 0 and token.text.lower() != "eu":
            if token.text.endswith("o") or token.text.endswith("a"):
                new_word = token.text[:-1] + "[x]"
                new_sentence += new_word + " "
            elif token.text.endswith("os") or token.text.endswith("as"):
                new_word = token.text[:-2] + "[x]s"
                new_sentence += new_word + " "
            elif token.text.lower() == "um" or token.text.lower() == "uma":
                new_word = "um[x]"
                new_sentence += new_word + " "
            elif token.text.lower() == "ele" or token.text.lower() == "ela":
                new_word = "el[x]"
                new_sentence += new_word + " "
            elif token.text.lower() == "eles" or token.text.lower() == "elas":
                new_word = "el[x]s"
                new_sentence += new_word
            elif token.tag_ == 'DET' and token.text.lower() == "a" or token.text.lower() == "o":
                new_word = "[x]"
                new_sentence += new_word + " " 
            elif token.text.lower() == "à" or token.text.lower() == "ao":
                new_word = "[x]"
                new_sentence += new_word + " "
            else:
                new_sentence += token.text_with_ws
        else:
            if token.pos_ == "ADP" and (token.text.lower() == "a" or token.text.lower() == "o"):
                new_word = "[x]"
                new_sentence += new_word + " "
            elif token.tag_ == 'PUNCT' or token.is_sent_end:
                new_sentence = new_sentence.strip() + token.text
            elif token.text.lower() == "homem" or token.text.lower() == "mulher":
                new_word = "pessoa"
                new_sentence += new_word + " "    
            else:  
                new_sentence += token.text_with_ws

    return new_sentence

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    sentence_fn = args["--sentence"]
    debug = args["--debug"]

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    neutral = make_neutral(sentence_fn)
    print(neutral)

    logging.info("DONE")
