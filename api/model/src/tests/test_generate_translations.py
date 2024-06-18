

from generate_translations import generate_translations

def test_translate_one_word():
    sentence = "Cat."
    google_translation = "gato"
    possible_words = generate_translations(sentence, google_translation)

    assert possible_words['possible_words'] == ['Gato', 'Gata', 'Gat[x]']

def test_translate_one_word_plural():
    sentence = "Cats."
    google_translation = "gatos"
    possible_words = generate_translations(sentence, google_translation)

    assert possible_words['possible_words'] == ['Gatos', 'Gatas', 'Gat[x]s']

def test_translate_one_sub():
    sentence = "The doctor finished her work."
    google_translation = "A médica terminou seu trabalho."
    translation = generate_translations(sentence, google_translation)

    assert translation['more_likely'] == 'A médica terminou seu trabalho.'
    assert translation['less_likely'] == 'O médico terminou seu trabalho.'
    assert translation['neutral'] == '[x] médic[x] terminou seu trabalho.'

def test_translate_one_sub_neutral():
    sentence = "The nurse talked a lot"
    google_translation = "A enfermeira falou muito"
    translation = generate_translations(sentence, google_translation)
 
    assert translation['first_option'] == 'A enfermeira falou muito.'
    assert translation['second_option'] == 'O enfermeiro falou muito.'
    assert translation['neutral'] == '[x] enfermeir[x] falou muito.'

def test_translate_one_they():
    sentence = "they are great"
    google_translation = "eles são ótimos"
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'Eles são ótimos.'
    assert translation['second_option'] == 'Elas são ótimas.'
    assert translation['neutral'] == 'El[x]s são ótim[x]s.'

def test_translate_neutral():
    sentence = "I am tired and I like to read a lot"
    google_translation = "Estou cansado e gosto muito de ler"
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'Eu estou cansada e gosto muito de ler.'
    assert translation['second_option'] == 'Eu estou cansado e gosto muito de ler.'
    assert translation['neutral'] == 'Eu estou cansad[x] e gosto muito de ler.'    

def test_translate_she():
    sentence = "She is a good doctor."
    google_translation = "Ela é uma boa médica."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['translation'] == 'Ela é uma boa médica.'
    assert translation['neutral'] == 'El[x] é um[x] bo[x] médic[x].'   

def test_translate_he():
    sentence = "He is a great nurse."
    google_translation = "Ele é um ótimo enfermeiro."
    translation = generate_translations(sentence, google_translation)

    assert translation['more_likely'] == 'Ele é um ótimo enfermeiro.'
    assert translation['neutral'] == 'É um[x] ótimo enfermeir[x].'     

def test_translate_two_subj_one_pronoun():
    sentence = "The developer argued with the designer because she did not like the design."
    google_translation = "O desenvolvedor discutiu com o designer porque ela não gostou do design."
    translation = generate_translations(sentence, google_translation)

    assert translation['first_option'] == 'A desenvolvedora discutiu com o designer porque ela não gostou do design.'
    assert translation['second_option'] == 'A desenvolvedora discutiu com a designer porque ela não gostou do design.'
    assert translation['neutral'] == 'A desenvolvedora discutiu com [x] designer porque ela não gostou do design.'    

def test_translate_more_than_one_gender():
    sentence = "The doctor finished her work but the nurse was still eating his lunch"
    google_translation = "O médico terminou seu trabalho, mas a enfermeira ainda estava almoçando"
    translation = generate_translations(sentence, google_translation)

    assert translation['translation'] == 'A médica terminou seu trabalho mas o enfermeiro ainda estava almoçando.'
    assert translation['neutral'] == '[x] médic[x] terminou seu trabalho mas [x] enfermeir[x] ainda estava almoçando.'

def test_translate_with_it():
    sentence = "The trophy would not fit in the brown suitcase because it was too big."
    google_translation = "O troféu não cabia na mala marrom porque era muito grande."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['translation_it'] == 'O troféu não cabia na mala marrom porque era muito grande.'

def test_translation_guard():
    sentence = "The guard hated the hairdresser because she charged too much."
    google_translation = "O guarda odiava a cabeleireira porque ela cobrava demais."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'O guarda odiava a cabeleireira porque ela cobrava demais.'
    assert translation['second_option'] == 'A guarda odiava a cabeleireira porque ela cobrava demais.'
    assert translation['neutral'] == '[x] guarda odiava a cabeleireira porque ela cobrava demais.'        

def test_translation_manager():
    sentence = "The manager meets the counselor every week because he wants to make sure everything follows the law"
    google_translation = "O gerente se encontra com o conselheiro toda semana porque quer ter certeza de que tudo está de acordo com a lei"
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'O gestor reúne o conselheiro toda semana porque quer certeza que tudo está acordo a lei.'
    assert translation['second_option'] == 'O gestor reúne a conselheira toda semana porque quer certeza que tudo está acordo a lei.'
    assert translation['neutral'] == 'O gestor reúne [x] conselheir[x] toda semana porque quer certeza que tudo está acordo a lei.'


def test_translation_librarian():
    sentence = "The salesperson sold some books to the librarian because he wanted to learn."
    google_translation = "O vendedor vendeu alguns livros ao bibliotecário porque queria aprender."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'O vendedor vendeu alguns livros ao bibliotecário porque queria aprender.'
    assert translation['second_option'] == 'A vendedora vendeu alguns livros ao bibliotecário porque queria aprender.'
    assert translation['neutral'] == '[x] vendedor vendeu alguns livros ao bibliotecário porque queria aprender.'  

def test_translation_laywer():
    sentence = "The lawyer yelled at the hairdresser because he did a bad job."
    google_translation = "O advogado gritou com o cabeleireiro porque ele fez um péssimo trabalho."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'O advogado gritou com o cabeleireiro porque fez um péssimo trabalho.'
    assert translation['second_option'] == 'A advogada gritou com o cabeleireiro porque fez um péssimo trabalho.'
    assert translation['neutral'] == '[x] advogad[x] gritou com o cabeleireiro porque fez um péssimo trabalho.' 

def test_translation_wino_1():
    sentence = "The developer argued with the designer because she did not like the design."
    google_translation = "O desenvolvedor discutiu com o designer porque ela não gostou do design."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'A desenvolvedora discutiu com a designer porque ela não gostou do design.'
    assert translation['second_option'] == 'A desenvolvedora discutiu com o designer porque ela não gostou do design.'
    assert translation['neutral'] == 'A desenvolvedora discutiu com [x] designer porque ela não gostou do design.' 

def test_translation_wino_2():
    sentence = "The developer argued with the designer because his idea cannot be implemented."
    google_translation = "O desenvolvedor discutiu com o designer porque sua ideia não pode ser implementada."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'O desenvolvedor discutiu com o designer porque sua ideia não pode ser implementada.'
    assert translation['second_option'] == 'O desenvolvedor discutiu com a designer porque sua ideia não pode ser implementada.'
    assert translation['neutral'] == 'O desenvolvedor discutiu com [x] designer porque sua ideia não pode ser implementada.' 

def test_translation_wino_3():
    sentence = "The mechanic gave the clerk a present because she won the lottery."
    google_translation = "O mecânico deu um presente para a balconista porque ela ganhou na loteria."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'O mecânico deu um presente à balconista porque ela ganhou na loteria.'
    assert translation['second_option'] == 'O mecânico deu um presente ao balconista porque ela ganhou na loteria.'
    assert translation['neutral'] == 'O mecânico deu um presente [x] balconista porque ela ganhou na loteria.' 
    
def test_translation_wino_4():
    sentence = "The mechanic gave the clerk a present because it was his birthday."
    google_translation = "O mecânico deu um presente ao balconista porque era seu aniversário."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'O mecânico deu um presente ao balconista porque era seu aniversário.'
    assert translation['second_option'] == 'A mecânica deu um presente ao balconista porque era seu aniversário.'
    assert translation['neutral'] == '[x] mecânic[x] deu um presente ao balconista porque era seu aniversário.'
    
def test_translation_wino_5():
    sentence = "The assistant scanned documents for the analyst because she asked."
    google_translation = "A assistente digitalizou documentos para a analista porque ela pediu."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'A assistente digitalizou documentos para a analista porque ela pediu.'
    assert translation['second_option'] == 'O assistente digitalizou documentos para a analista porque ela pediu.'
    assert translation['neutral'] == '[x] assistente digitalizou documentos para a analista porque ela pediu.'
       
def test_translation_wino_6():
    sentence = "The assistant scanned documents for the analyst because he knows how to use the scan machine."
    google_translation = "O assistente digitalizou documentos para o analista porque ele sabe usar a máquina de digitalização."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'O assistente digitalizou documentos para o analista porque ele sabe usar a máquina de digitalização.'
    assert translation['second_option'] == 'O assistente digitalizou documentos para a analista porque ele sabe usar a máquina de digitalização.'
    assert translation['neutral'] == 'O assistente digitalizou documentos para [x] analista porque ele sabe usar a máquina de digitalização.'    

def test_translation_wino_7():
    sentence = "The chief gave the housekeeper a tip because she was satisfied."
    google_translation = "O chefe deu uma gorjeta à governanta porque ela estava satisfeita."
    translation = generate_translations(sentence, google_translation)
    
    assert translation['first_option'] == 'A chefe deu uma gorjeta à governanta porque ela estava satisfeita.'
    assert translation['second_option'] == 'A chefe deu uma gorjeta ao governante porque ela estava satisfeita.'
    assert translation['neutral'] == 'A chefe deu uma gorjeta [x] governant[x] porque ela estava satisfeita.'    

    