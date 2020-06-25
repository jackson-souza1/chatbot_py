# -*- coding: utf-8 -*-
"""Chatbot python

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZPVDumbo6LzCZQi6ThaG6LP_9jK4pHFg
"""

import bs4 as bs
import urllib.request
import re
import nltk
import numpy as np
import random
import string

nltk.download('punkt')

#!pip install spacy --upgrade

import spacy
spacy.__version__

nltk.__version__

#!python3 -m spacy download pt

dados = urllib.request.urlopen('https://pt.wikipedia.org/wiki/Intelig%C3%AAncia_artificial')

dados = dados.read()

dados

dados_html = bs.BeautifulSoup(dados, 'lxml')
dados_html

paragrafos = dados_html.find_all('p')

len(paragrafos)

paragrafos[0]

paragrafos[0].tex

conteudo = ''
for p in paragrafos:
  conteudo += p.text

conteudo

type(conteudo)

conteudo = conteudo.lower()
conteudo

lista_sentencas = nltk.sent_tokenize(conteudo)
lista_sentencas

type(lista_sentencas)

len(lista_sentencas)

pln = spacy.load('pt')
pln

stop_words = spacy.lang.pt.stop_words.STOP_WORDS

print(stop_words)

type(stop_words)

len(stop_words)

string.punctuation

def preprocessamento(texto):
    #URLS
    texto = re.sub(r'https?://[A-za-z0-9./]+', ' ', texto)

    #Espacos em branco
    texto = re.sub(r' +', ' ', texto)
    documento = pln(texto)
    lista = []
  
    for token in documento:
      lista.append(token.lemma_)

    lista = [palavra for palavra in lista if palavra not in stop_words and palavra not in string.punctuation ]
    lista = ' '.join([str(elemento) for elemento in lista if not elemento.isdigit()])

    return lista

texto_teste = 'https://www.iaexpert.com.br ' + lista_sentencas[0]
texto_teste

resultado = preprocessamento(texto_teste)
resultado

lista_sentencas_preprocessada = []
for i in range(len(lista_sentencas)):
  lista_sentencas_preprocessada.append(preprocessamento(lista_sentencas[i]))

for _ in range(5):
  i = random.randint(0, len(lista_sentencas) -1)
  print(lista_sentencas[i])
  print(lista_sentencas_preprocessada[i])
  print('-------------')



"""Etapa 3 Frases de boas-vindas"""

texto_boas_vindas = ('hey', 'olá', 'opa', 'oi', 'eae')
texto_boas_vindas_respostas = ('Oi tudo bem?', 'olá', 'bem-vindo', 'oi', 'como você está?')

def responder_saudacao(texto):
  for palavra in texto.split():
    if palavra.lower() in texto_boas_vindas:
      return random.choice(texto_boas_vindas_respostas)

responder_saudacao('oi')

"""# 4 Entendimento TF-IDF(Team frequency - inverse documento frequency)"""

from sklearn.feature_extraction.text import TfidfVectorizer

frases_teste = lista_sentencas_preprocessada[:3]
frases_teste

frases_teste.append(frases_teste[0])
frases_teste

vetores_palavras = TfidfVectorizer()
palavras_vetorizadas = vetores_palavras.fit_transform(frases_teste)

type(palavras_vetorizadas)

palavras_vetorizadas

print(vetores_palavras.get_feature_names())

len(vetores_palavras.get_feature_names())

print(vetores_palavras.vocabulary_)

print(vetores_palavras.idf_)

palavras_vetorizadas.todense()

palavras_vetorizadas.todense().shape

from sklearn.metrics.pairwise import  cosine_similarity

palavras_vetorizadas[0].todense()

cosine_similarity(palavras_vetorizadas[0], palavras_vetorizadas[1])

cosine_similarity(palavras_vetorizadas[0], palavras_vetorizadas[3])

similaridade = cosine_similarity(palavras_vetorizadas[0], palavras_vetorizadas)
similaridade

similaridade.argsort()

i = similaridade.argsort(0)[0][-2]
i

i = i.flatten()

i

def responder(texto_usuario):
  resposta_chatbot = ''
  lista_sentencas_preprocessada.append(texto_usuario)

  tfidf = TfidfVectorizer()
  palavras_vetorizadas = tfidf.fit_transform(lista_sentencas_preprocessada)

  similaridade = cosine_similarity(palavras_vetorizadas[-1], palavras_vetorizadas)

  indice_sentenca = similaridade.argsort()[0][-2]
  vetor_similar = similaridade.flatten()
  vetor_similar.sort()
  vetor_encontrado = vetor_similar[-2]

  if (vetor_encontrado == 0):
    resposta_chatbot = resposta_chatbot + 'Desculpe, mas não entendi!'
    return resposta_chatbot
  else:
    resposta_chatbot = resposta_chatbot + lista_sentencas[indice_sentenca]
    return resposta_chatbot



"""Etapa 7: Conversação"""

continuar = True
print('Olá, sou um chatbot e vou responder perguntas sobre inteligência artificial: ')
while (continuar == True):
  texto_usuario = input()
  texto_usuario = texto_usuario.lower()
  if (texto_usuario != 'sair'):
    if (responder_saudacao(texto_usuario) != None):
      print('Chatbot: ' + responder_saudacao(texto_usuario))
    else:
      print('Chatbot: ')
      print(responder(preprocessamento(texto_usuario)))
      lista_sentencas_preprocessada.remove(preprocessamento(texto_usuario))
  else:
    continuar = False
    print('Chatbot: Até breve!')

