# unbIAs: Enhancing Gender Accuracy in Machine Translation

## Overview

The unbIAs project introduces a model designed to achieve high gender accuracy in machine translation. Leveraging advanced linguistic analysis with spaCy and entity recognition with RoBERTa, this model utilizes Constrained Beam Search to maintain the syntactical structure of sentences derived from commercial models while substituting the correct gender as identified by our model. The final output is refined using the SimAlign tool.

This approach has achieved a BLEU score of 48.39. Compared to Google Translate, our model has improved gender accuracy from 68.75 to 70.09, a 15.7% improvement in gender entity accuracy disparity between male and female entities, and a 43% reduction in stereotypical translations.

## System Pipeline

Here is the pipeline diagram showing how the unbIAs system processes translations to ensure gender accuracy:

![System Pipeline](images/pipeline.jpeg)

## Application Screenshots

### Translation Interface

The unbIAs application provides a user-friendly interface for inputting text and displaying gender-accurate translations. Here are some examples of the interface in action:

#### Example 1: Lawyer and Hairdresser

![Lawyer and Hairdresser Translation](images/model-lawyer.png)

#### Example 2: Doctor Finishing Work

![Doctor Translation](images/model-miti.png)

#### Example 3: Neutral Gender Option

For texts where gender neutrality is preferred or applicable, the application offers a neutral option:

![Neutral Gender Translation](images/modelneutro.png)

## Usage

The unbIAs project is divided into two main components: the API, built with Python 3.8, and the application, developed with React. To utilize this project, follow these installation steps:

1. Install dependencies:

   ```bash
   ./install.sh
   ```

2. Inside the `APP` directory, install the necessary packages:

   ```bash
   npm install
   ```

3. To run the project, navigate to the `API` directory and execute:

   ```bash
   flask run -p 8000
   ```

4. In the APP directory, start the application:
   ```bash
   npm start
   ```
   The project will be accessible at http://localhost:3000/.

## License

This project uses the following license: [MIT](https://github.com/ramos-ai/unbIAs?tab=MIT-1-ov-file).
