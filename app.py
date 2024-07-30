import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Carregar dados

df = pd.read_excel("data/Rating.xlsx")

df_pivot = df.pivot_table(index='Nome', columns='Filme', values='Rating', fill_value=0)

st.title('Avaliação de Filmes para Novos Usuários')

filmes = df['Filme'].unique()
novo_usuario = st.text_input('Nome')

avaliacoes = {}
for filme in filmes[:4]:  
    avaliacoes[filme] = st.slider(f'Avalie o filme "{filme}"', 1, 5, 3)

if st.button('Salvar Avaliações'):
    novo_df = pd.DataFrame([{
        'Nome': novo_usuario,
        'Filme': filme,
        'Rating': rating
    } for filme, rating in avaliacoes.items()])
    
    
    df = pd.concat([df, novo_df])
    df_pivot = df.pivot_table(index='Nome', columns='Filme', values='Rating', fill_value=0)
    
    
    matriz_similaridade = cosine_similarity(df_pivot)
    df_similaridade = pd.DataFrame(matriz_similaridade, index=df_pivot.index, columns=df_pivot.index)
    
    
    similaridade = df_similaridade[novo_usuario].sort_values(ascending=False)[1:4] 
    st.write(f'Usuários mais similares a {novo_usuario}:', similaridade)

    
    filmes_avaliados = novo_df['Filme'].unique()

    
    recomendacoes_usuarios_similares = df_pivot.loc[similaridade.index]
    media_recomendacoes = recomendacoes_usuarios_similares.mean().sort_values(ascending=False)

    
    recomendacoes_finais = media_recomendacoes.drop(filmes_avaliados)
    st.write('Filmes recomendados:', recomendacoes_finais.head(5))






