"""Usage:
    generate_model_translation.py --sentence=SENTENCE [--constraints=CONSTRAINTS][--debug]
"""

# External imports
import logging
from docopt import docopt
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = 'VanessaSchenkel/pt-unicamp-handcrafted'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_translation(source_sentence, num_return_sequences = 1):
    translation_model = get_best_translation(
        source_sentence, num_return_sequences)
    return translation_model


def get_best_translation(source_sentence, num_return_sequences=1):
    if type(source_sentence) == str:
        source_sentence = source_sentence.strip(",")
    else:
        source_sentence = source_sentence.text

    input_ids = tokenizer(source_sentence, return_tensors="pt").input_ids

    outputs = model.generate(
        input_ids,
        num_beams=10,
        num_return_sequences=num_return_sequences,
        max_new_tokens=20
    )

    if num_return_sequences == 1:
        return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

    translation_model = []

    for output in outputs:
        translation_model.append(tokenizer.decode(
            output, skip_special_tokens=True))

    return translation_model

def generate_translation_with_constraints(source_sentence, constrained_gender):
    constrained_gender = constrained_gender.strip()
    input_ids = tokenizer(source_sentence, return_tensors="pt").input_ids
    
    force_words_ids = tokenizer(
        [constrained_gender], add_special_tokens=False).input_ids

    outputs = model.generate(
        input_ids,
        force_words_ids=force_words_ids,
        num_beams=20,
        num_return_sequences=2,
        max_new_tokens=20
    )

    most_likely = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return most_likely

def generate_translation_with_gender_constrained(source_sentence, constrained_gender):
    constrained_gender = constrained_gender.strip(",").strip()
    
    input_ids = tokenizer(source_sentence, return_tensors="pt").input_ids
    
    force_words_ids = tokenizer(
        [constrained_gender], add_special_tokens=False).input_ids

    outputs = model.generate(
        input_ids,
        force_words_ids=force_words_ids,
        num_beams=30,
        num_return_sequences=2,
        max_new_tokens=50,
    )

    most_likely = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return most_likely


if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    sentence_fn = args["--sentence"]
    constrained_fn = args["--constraints"]
    debug = args["--debug"]

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if constrained_fn:
        translation = generate_translation_with_gender_constrained(sentence_fn, constrained_fn)
        print("Constrained model:", translation)
    
    translation = generate_translation(sentence_fn, 1)
    print("Model: ", translation)

    logging.info("DONE")
