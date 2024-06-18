import sobre from "../assets/sobre.png";

import "../styles/sobre.css";

export function Sobre() {
  return (
    <div className='sobre-page'>
      <div className='msg-sobre'>
        <h1>Sobre</h1>
        <div className='msg-sobre-text'>
          O uso da inteligência artificial no nosso cotidiano é uma realidade.
          Ela é capaz de realizar tarefas mais simples como a sugestão de uma
          palavra ao escrevermos no celular quanto tarefas mais complexas como o
          diagnóstico de uma doença. Esta área resolve problemas que têm alto
          impacto social e tem o poder de tomar decisões sem preconceitos ou
          estigmas sociais.
          <br></br>
          <br></br>
          Porém, a aprendizagem de máquina já concluiu erroneamente que
          <a href='https://www.theguardian.com/technology/2016/sep/08/artificial-intelligence-beauty-contest-doesnt-like-black-people'>
            {" "}
            pele mais escura é pouco atraente
          </a>
          ,
          <a href='https://www.reuters.com/article/us-amazon-com-jobs-automation-insight-idUSKCN1MK08G'>
            {" "}
            mulheres são menos qualificadas que homens
          </a>
          ,
          <a href='https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing'>
            {" "}
            negros têm mais chance de reincidir
          </a>{" "}
          e criou um chatbot neo-nazista em poucas horas
          <a href='https://www.technologyreview.com/2018/03/27/144290/microsofts-neo-nazi-sexbot-was-a-great-lesson-for-makers-of-ai-assistants/'>
            {" "}
            criou um chatbot neo-nazista em poucas horas
          </a>
          .<br></br>
          <br></br>
          Com o crescimento do uso de aprendizagem de máquina, também aumentam
          as preocupações com a justiça algorítmica. Já é comprovado que ele
          pode ser prejudicial contra grupos sub-representados, já que o
          algoritmo pode ser treinado com vieses ou até mesmo pode herdar vieses
          sociais de quem os programa.
          <br></br>
          <br></br>
          Os sistemas de tradução utilizam a aprendizagem de máquina e correm
          também esse risco. O sistema de tradução mais usado no mundo é o
          Google Tradutor. São mais de 500 milhões de usuários diários no site,
          sendo que o Brasil é o país que mais o utiliza{" "}
          <a href='https://blog.google/products/translate/ten-years-of-google-translate/'>
            {" "}
            Brasil é o país que mais o utiliza.
          </a>
          <br></br>
          <br></br>Este trabalho foi criado como parte do{" "}
          <a href='https://www.overleaf.com/read/wsgqggxtxnky'>
            Trabalho de Conclusão de Curso
          </a>{" "}
          de Ciência da Computação da Unisinos. Foi desenvolvido um modelo de
          tradução para diminuir o viés de gênero do Google Tradutor.
          <br></br>
          <br></br>
        </div>
      </div>
      <div className='div-img'>
        <img className='img-sobre' src={sobre} alt='sobre' />
        <div>
          <h3>Como?</h3>
          Foi criado um modelo com uma alta acurácia de gênero. É feita uma
          análise linguística com a ferramenta spaCy e identificação de entidade
          com roBERTa. É utilizada a técnica de Constrained Beam Search para se
          manter a estrutura da frase do modelo comercial, porém com a
          substituição para o gênero correto apontado pelo modelo criado. A
          frase final é resultado de alinhamento feito com a ferramenta
          SimAlign. A técnica implementada pelo artigo, apresenta pontuação BLEU
          de 48.39. Em relação ao Google Tradutor, o modelo obteve uma melhora
          de 68.75 para 70.09 na acurácia de gênero, uma melhora de 15.7% na
          pontuação que mede a diferença de acerto entre entidades masculinas e
          femininas e uma melhora de 43% em relação à traduções estereotipadas.
        </div>
      </div>
    </div>
  );
}
