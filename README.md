# unbIAs

### O que é 
Foi criado um modelo com uma alta acurácia de gênero. É feita uma análise linguística com a ferramenta spaCy e identificação de entidade com roBERTa. É utilizada a técnica de Constrained Beam Search para se manter a estrutura da frase do modelo comercial, porém com a substituição para o gênero correto apontado pelo modelo criado. A frase final é resultado de alinhamento feito com a ferramenta SimAlign. A técnica implementada pelo artigo, apresenta pontuação BLEU de 48.39. Em relação ao Google Tradutor, o modelo obteve uma melhora de 68.75 para 70.09 na acurácia de gênero, uma melhora de 15.7% na pontuação que mede a diferença de acerto entre entidades masculinas e femininas e uma melhora de 43% em relação à traduções estereotipadas.

### Como utilizar 
O projeto está dividido entre a API, criado com Python 3.8 e o APP criado com React. Para utilizar, basta instalar as dependências 

```
./install.sh
````
E na pasta APP rodar:
```
npm install

```

Depois para rodar o projeto é necessário rodar dentro da pasta API
```
flask run -p 8000
```

e dentro da pasta APP
```
npm start
```

O projeto irá abrir em http://localhost:3000/ .


### Sobre
O uso da inteligência artificial no nosso cotidiano é uma realidade. Ela é capaz de realizar tarefas mais simples como a sugestão de uma palavra ao escrevermos no celular quanto tarefas mais complexas como o diagnóstico de uma doença. Esta área resolve problemas que têm alto impacto social e tem o poder de tomar decisões sem preconceitos ou estigmas sociais.

Porém, a aprendizagem de máquina já concluiu erroneamente que pele mais escura é pouco atraente, mulheres são menos qualificadas que homens, negros têm mais chance de reincidir e criou um chatbot neo-nazista em poucas horas criou um chatbot neo-nazista em poucas horas.

Com o crescimento do uso de aprendizagem de máquina, também aumentam as preocupações com a justiça algorítmica. Já é comprovado que ele pode ser prejudicial contra grupos sub-representados, já que o algoritmo pode ser treinado com vieses ou até mesmo pode herdar vieses sociais de quem os programa.

Os sistemas de tradução utilizam a aprendizagem de máquina e correm também esse risco. O sistema de tradução mais usado no mundo é o Google Tradutor. São mais de 500 milhões de usuários diários no site, sendo que o Brasil é o país que mais o utiliza Brasil é o país que mais o utiliza.

Este trabalho foi criado como parte do Trabalho de Conclusão de Curso de Ciência da Computação da Unisinos. Foi desenvolvido um modelo de tradução para diminuir o viés de gênero do Google Tradutor.
