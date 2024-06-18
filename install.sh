#!/bin/sh
# ./install.sh
## Install required python packages and downloads resources

# install packages
pip install -r ./requirements.txt

# download spacy language support
python -m spacy download pt_core_news_lg
python -m spacy download en_core_web_lg