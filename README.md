# dextra-challenge
desafio big data da dextra


# para fazer pull da imagem
docker pull tsandesfernandes/cinqchallenge

# para fazer build
docker build -t cinqchallenge .


# rodar o build 
docker run --rm -it -p 8000:8000 tsandesfernandes/cinqchallenge

# git clone
https://github.com/tsandesfernandes/dextra-challenge.git

# testes unitários
python -m unittest -v teste.py
