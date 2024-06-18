# Local imports
from split_sentence import split_on_subj_and_bsubj
from word_alignment import get_word_alignment_pairs
from generate_model_translation import generate_translation, generate_translation_with_gender_constrained, get_best_translation
from spacy_utils import get_nlp_en,  get_nlp_pt, get_translation_with_punctuation

def get_translation_constrained_and_aligned_different_gender(translation_nlp, people, source_sentence, subjects):
        constrained_splitted = split_on_subj_and_bsubj(translation_nlp, people)
        translations = []

        for constraints in constrained_splitted:
            constrained_translation = generate_translation_with_gender_constrained(source_sentence.text_with_ws, constraints)
            translation = check_constrained_translation(constraints, constrained_translation, source_sentence.text_with_ws)

            translations.append(translation)

        if len(translations) == 1:
            translations_aligned = translations[0]
        elif len(translations) == 2:
            translations_aligned = combine_contrained_translations(translations, constrained_splitted, source_sentence)
        elif len(translations) > 2:
            translation = ""
            trans_aligned = ""
            for index, translation in enumerate(translations):
                if index == 0:
                    trans_aligned = translations[0]
                elif index < len(translations)-1:
                    next_trans = translations[index+1]
                    trans = [trans_aligned, next_trans]
                    trans_aligned = combine_contrained_translations(trans, constrained_splitted, source_sentence)
                else:
                    translation = combine_contrained_translations([trans_aligned, translations[-1]], constrained_splitted, source_sentence)
                    translations_aligned =  translation

        alignment_with_constrained = get_word_alignment_pairs(source_sentence.text, translations_aligned, model="bert", matching_methods = "i", align = "itermax")
        
        sub_split = subjects[0].split()
        subj_translated = ""

        for first_sentence, second_sentence in alignment_with_constrained: 
            if first_sentence in sub_split:
                subj_translated += second_sentence + " "

        alignment_with_translation = get_word_alignment_pairs(translation_nlp.text, translations_aligned, model="bert", matching_methods = "i", align = "itermax")

        translated = ""
        subj_translated_split = subj_translated.split()
        for first_sentence, second_sentence in alignment_with_translation: 
            last_word = translated.strip().split(" ")[-1]
            if second_sentence in subj_translated_split and second_sentence != last_word and second_sentence not in translated:
                translated += second_sentence + " "
            elif first_sentence[:-1] != last_word[:-1] or len(translated) == 0:
                translated += first_sentence + " "

        translation_nlp = get_nlp_pt(translated)
        
        return translation_nlp

def get_translation_constrained_and_aligned_same_gender(people_google, translation_model_nlp, people_model, translation_nlp):
        head_google = [token for token in translation_nlp if token.head.text == people_google]
        head_model = [token for token in translation_model_nlp if token.head.text == people_model]
        
        gender_head_google = [token.morph.get("Gender").pop() for token in head_google if len(token.morph.get("Gender")) > 0]
        gender_head_model = [token.morph.get("Gender").pop() for token in head_model if len(token.morph.get("Gender")) > 0]
        
        if(set(gender_head_google) != set(gender_head_model)):
            lemmas_google = [token.lemma_ for token in head_google]
            lemmas_model = [token.lemma_ for token in head_model]

            if lemmas_google == lemmas_model:
                google_index = [token.i for token in head_google]
                new_translation = ""

                translation_split = translation_nlp.text.split(" ")
                for index, index_replace in enumerate(google_index):
                    translation_split[index_replace] = head_model[index].text

                new_translation = " ".join(translation_split)    
                translation_nlp = get_nlp_pt(new_translation)
        
        return translation_nlp

def get_constrained_subject_and_neutral(translation):
    constraints = ""

    for token in translation:
        if token.dep_ == 'ROOT':
            constraints = token.text  

    return constraints
    
def get_constrained_translation(translation, people):
    constrained_sentence = ""
    list_constrained = []

    for token in translation:
        if token in people and len(constrained_sentence) > 0:
            list_constrained.append(constrained_sentence.strip())
            constrained_sentence = ""
    
        elif token not in people:
            constrained_sentence += token.text_with_ws
            if token.is_sent_end and len(constrained_sentence) > 0:
                list_constrained.append(constrained_sentence.strip())
              
    
    if len(list_constrained) == 1 and len(translation.text_with_ws) == len(list_constrained[0]):
        return ""

    return list_constrained    

def align_with_model(model_alignment, new_sentence):
    new_sentence_model = ""

    for model_sentence, alignment_sentence in model_alignment:
        last_word = new_sentence_model.strip().split(" ")[-1]
        
        if model_sentence != alignment_sentence and model_sentence != last_word:
            token_model = get_nlp_pt(model_sentence)[0]
            token_alignment = get_nlp_pt(alignment_sentence)[0]
            
            if token_model.pos_ != token_alignment.pos_:
                new_sentence_model += model_sentence + " "
                           
        if model_sentence == alignment_sentence:
            new_sentence_model += new_sentence
            return new_sentence_model.strip()
    
    return new_sentence_model.strip()

def combine_contrained_translations(translations, constrained_splitted, source_sentence, model="bert", matching_methods = "i", align = "itermax", people_model = []):
    punctuation = constrained_splitted[-1][-1]
    first, second = translations
    
    word_alignments = get_word_alignment_pairs(first.strip(), second.strip(), model=model, matching_methods=matching_methods, align=align)
    new_sentence = ""
    for first_sentence, second_sentence in word_alignments:
        last_word = new_sentence.strip().split(" ")[-1]
        if (first_sentence == second_sentence or first_sentence.strip(",") == second_sentence.strip(",") or first_sentence.strip(".") == second_sentence.strip(".")) and first_sentence != last_word:
            new_sentence += first_sentence + " "
        
        elif len(people_model) > 0 and first_sentence != second_sentence and first_sentence in people_model and first_sentence != last_word:
            new_sentence += first_sentence + " " 
            
        elif len(people_model) > 0 and first_sentence != second_sentence and second_sentence in people_model and second_sentence != last_word:
            new_sentence += second_sentence + " "      

        elif any(first_sentence in word for word in constrained_splitted) and first_sentence != last_word:
            new_sentence += first_sentence + " "
        
        elif any(second_sentence in word for word in constrained_splitted) and second_sentence != last_word:
            new_sentence += second_sentence + " "  
        
        elif first_sentence != second_sentence and first_sentence != last_word:
            first_token = get_nlp_pt(first_sentence)[0]
            second_token = get_nlp_pt(second_sentence)[0]

            if first_token.lemma_ == second_token.lemma_ or first_token.text[:-1] == second_token.text:
                new_sentence += first_sentence + " "
            
    if len(new_sentence.strip().split(' ')) < len(word_alignments):
        model_translation = get_best_translation(source_sentence)
        model_alignment = get_word_alignment_pairs(model_translation.strip("."), new_sentence, matching_methods="m", align="mwmf")
        return align_with_model(model_alignment, new_sentence)
    
    sentence =  get_translation_with_punctuation(new_sentence, punctuation)
    return sentence.text

def get_word_to_add(word):
    w = get_nlp_en(word)
    for token in w:
        if token.is_punct:
            return token.text

    word_translatted =  generate_translation(word)
    return word_translatted

def check_constrained_translation(constraints, constrained_translation, source_sentence):
    if len(constrained_translation) > (2*len(source_sentence)) and constrained_translation.endswith(constraints):
        translation = generate_translation(source_sentence)
            
        return translation
    else:
        return constrained_translation   

def get_constraints_one_subj(translation, people):
    constrained_sentence = ""
    list_constrained = []

    for token in translation:
        ancestors = [ancestor for ancestor in token.ancestors]
        children = [child for child in token.children]

        if not any(item in ancestors for item in people) and not any(item in children for item in people) and token not in people:
            if token.pos_ != "PUNCT" or len(constrained_sentence) > 0:
                constrained_sentence += token.text_with_ws
        
        elif token.text.lower() != 'eu' and len(constrained_sentence) > 0:
            list_constrained.append(constrained_sentence.strip())
            constrained_sentence = ""

        if token.is_sent_end and len(constrained_sentence) > 0:
            list_constrained.append(constrained_sentence.strip())
    
    if len(list_constrained) == 1 and len(translation.text_with_ws) == len(list_constrained[0]):
        return ""

    return list_constrained

def get_constraints_without_people(google_translation):
    constrained_splitted = []
    sentence = ""
    for token in google_translation:       
        if token.dep_ == "nsubj" and len(sentence) > 0:
            constrained_splitted.append(sentence.strip())
            sentence = ""
        
        elif token.morph.get("Gender") == ['Masc'] or token.morph.get("Gender") == ['Fem']:
                sentence += token.text_with_ws
                constrained_splitted.append(sentence.strip())
                sentence = ""   
            
        else:
            sentence += token.text_with_ws
            if token.is_sent_end and len(sentence) > 0:  
                constrained_splitted.append(sentence.strip())
                sentence = ""
        
    return constrained_splitted      

        
def get_translations_aligned(translations, constrained_splitted, source_sentence):
        translations_aligned = ""
        if len(translations) == 1:
            translations_aligned = translations[0]
        elif len(translations) == 2:
            translations_aligned = combine_contrained_translations(translations, constrained_splitted, source_sentence)
        elif len(translations) > 2:
            translation = ""
            trans_aligned = ""
            for index, translation in enumerate(translations):
                if index == 0:
                    trans_aligned = translations[0]
                elif index < len(translations)-1:
                    next_trans = translations[index+1]
                    trans = [trans_aligned, next_trans]
                    trans_aligned = combine_contrained_translations(trans, constrained_splitted, source_sentence)
                else:
                    translation = combine_contrained_translations([trans_aligned, translations[-1]], constrained_splitted, source_sentence)
                    translations_aligned =  translation
        
        translation = get_translation_with_punctuation(translations_aligned)
        return translation        