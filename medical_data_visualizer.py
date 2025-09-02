#Aqui só importei as bibliotecas pra usar no código
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1: Eu chamo o df e atribuo a função pd.read_csv e então abro o parênteses e coloco o nome do arquivo para que ele leia o dataset que vou utilizar. 

df = pd.read_csv('medical_examination.csv')

# 2: Primeiramente eu vou converter a altura para metros, pois está em centímetros, e eu faço isso dividindo por 100.
# Aí de acordo com o enunciado eu preciso elevar essa altura em metros ao quadrado,  então dividir o peso (BMI) por isso.
# Então eu confiro se o valor é maior que 25, então atribuo o valor 1 caso a pessoa seja overweight e 0 caso não seja.
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int) 
# Nesse código, primeiro tem as operações matem´ticas entre peso e altura, e por último o "asype(int)" faz com que os valores booleanos de true/false virem 1 e 0, respectivamente.

# 3: Agora eu faço com que os valores 0 sejam sempre bons e 1 sempre ruins, nesse caso d condição de saúde de colesterol e glicose.
# Por isso eu chamo as duas funções do dataframe e confiro se é maior que 1, caso não seja ele retorna um falso, que vira 0(e nesse caso é o bom), caso seja verdadeiro ele retorna um true que vira 1 com o astype(int) e nesse caso é ruim.
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4
def draw_cat_plot():
    # 5: cria um novo dataframe chamado df_cat, então ele vai usar a função pd_melt que reorganiza os dados.
    # O id_cars vai fixar a coluna cardio, e vai transformar as colunas no value_vars em duas colunas onde uma vai ser esse nome da variável e a outra vai ser o valor correspondente a ela.
    df_cat = pd.melt (
        df, 
        id_vars=['cardio'], 
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # 6: Aqui é contado quantas vezes cada valor aparece nas colunas, o df cat tem 3 colunas e essa função conta quantas vezes cada combinação dessas três colunas ocorrem.
    # Isso faz com que seja retornado uma Series, onde o valor do índice é a contagem de quantas vezes determinada combinação acontece.
    # Depois eu uso o reset_index para transformar essa Series em um daaframe novamente, e aí eu renomeio a coluna de contagem para 'total'. (que é a quantidade de vezes que aquela combinação aparece no dataframe)
    df_cat = df_cat.value_counts().reset_index(name='total')
    

    # 7
    g = sns.catplot(
        data=df_cat,# Define qual dataframe vai usar
        x='variable', # Parte de variáveis categóricas
        y='total', # Eixo da contagem
        hue='value', # Separa as barras pelo valor 0 ou 1
        col='cardio', # Separa os gráficos pela condição de saúde cardio
        kind='bar', # Tipo de gráfico, que nesse caso é barra
        order=['active','alco','cholesterol','gluc','overweight','smoke'],
        hue_order=[0,1],
        col_order=[0,1]
    )

    # 8: Atribui a variável
    fig = g.fig
    
    # 9: essa parte salva a figura do gráfico catplot gerado em png, e retorna essa imagem no output.
    fig.savefig('catplot.png')
    plt.close(fig)
    return fig

# 10
def draw_heat_map():
    # 11: verifica os valores para filtrar os dados
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) & # Filtra toda a pressão arterial diastólica que é menor (olho isso por sinais matemáticos) que a pressão arterial sistólica
        (df['height'] >= df['height'].quantile(0.025)) & # Filtra toda a altura que é menor (olho isso por sinais matemáticos) que o quantil de 2,5% (olho isso pela parte "quantile(0.025)") 
        (df['height'] <= df['height'].quantile(0.975)) & # Filtra toda a altura que é maior que o quantil de 97,5%
        (df['weight'] >= df['weight'].quantile(0.025)) & # Filtra todo o peso que é menor que o quantil de 2,5%
        (df['weight'] <= df['weight'].quantile(0.975)) # Filtra todo o peso que é maior que o quantil de 97,5%
    ]

    # 12: Declara a correlação entre as colunas do dataframe
    corr = df_heat.corr(numeric_only=True).round(1)  # arredonda a 1 casa


    # 13: 
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # O mask é usado para mostrar só ma parte da matriz, porque a matriz corr é sempre simétrica, então para não ficar redundante, mostro só uma parte.
    # Nesse caso eu uso np_triu que mostra só a parte superior da matriz.
    # Esse np.ones_like cria uma matriz com o mesmo formato e tamanho que a corr, e define que os valores vão ser preenchidos com dados booleanos (true or false)

    # 14: Cria uma figura e uma ax, que é um eixo da ibliotec matplotlit, e logo em seguida define o tamanho dessa imagem.
    fig, ax = plt.subplots(figsize=(12, 10))

    # 15: Aqui os parâmetros desse gráfico são definidos.

    sns.heatmap( 
        corr, # é a matriz de correlação que vai ser utilizada
        mask=mask, #"esconde" os valores repetidos
        annot=True, #o valor numérico de cada correlação vai tá escrito em cda quadradiinho desse heatmap.
        fmt='.1f', #formata essa quantidade para ter apenas uma casa decimal depois da vírgula
        center=0, # a minha correlação pode ir de -1 a 1, então o centro dela é 0, isso faz com que minha escala de cores tenha 0 como ponto médio, então o que vem antes fica de uma cor e o que vem depois fica de outra.
        vmax=0.3, #define o valor máximo da escala de cores, que nesse caso é 0.3
        vmin=-0.1, #define o valor mínimo da escala de cores, que nesse caso é -0.1
        square=True, #faz com que cada cédula do mapa seja um quadrado
        linewidths=0.5,#adiciona linhas entre as cédulas do heatmap com largura de 0.5
    )

    # 16: salva a figura do gráfico gerado em png, e retorna essa imagem no output.
    fig.savefig('heatmap.png')
    return fig

#Explicando o código: o objetivo geral com este código é visualizar e entender padrões de saúde nesses dados. 
#No código inicialmente eu calculei o overweight pelo IMC, normalizei cholesterol e gluc (0/1) e, a partir disso, gerei um catplot por cardio e um heatmap de correlações (com dados filtrados) para identificar associações entre as variáveis.