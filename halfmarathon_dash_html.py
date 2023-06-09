import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
from dash.dependencies import Input, Output
from dash import dash_table
import pandas as pd
import plotly.express as px

extrernal_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=extrernal_stylesheets)
app.config.suppress_callback_exceptions = True

url = 'https://raw.githubusercontent.com/rybinski92/halfmarathon_rzeszow/28031193fb3bd5bfc7a7692e31d891245ccc636c/all_halfmaraton.csv'
df = pd.read_csv(url, sep=(';'), encoding='windows-1250', index_col=0)

#df = pd.read_csv('./all_halfmaraton.csv', sep=(';'), encoding='windows-1250', index_col=0)

# zawodznicy w latach
zawodnicy_w_latach = df.groupby('rok').size()
zawodnicy_w_latach = pd.DataFrame(zawodnicy_w_latach, columns=['Ilosc'])
zawodnicy_w_latach = zawodnicy_w_latach.reset_index()

# podział na płeć
podzial_na_plec = df.groupby('rodzaj_plci').size()
podzial_na_plec = pd.DataFrame(podzial_na_plec, columns=['Ilosc'])
podzial_na_plec = podzial_na_plec.reset_index()

#podział zawodników w latach
zawodnicy_w_latach = df.groupby('rok').size()
zawodnicy_w_latach = pd.DataFrame(zawodnicy_w_latach, columns=['Ilosc'])
zawodnicy_w_latach = zawodnicy_w_latach.reset_index()

#podział kobiet na lata
kobiety = df.query("rodzaj_plci == 'K'")
kobiety_lata = kobiety.groupby('rok').size()
kobiety_lata = pd.DataFrame(kobiety_lata, columns=['Ilosc'])
kobiety_lata = kobiety_lata.reset_index()

# podział mężczyzn na lata
men = df.query("rodzaj_plci == 'M'")
men_lata = men.groupby('rok').size()
men_lata = pd.DataFrame(men_lata, columns=['Ilosc'])
men_lata = men_lata.reset_index()

# podział na kraj
podzial_na_kraj = df.groupby('kraj').size()
podzial_na_kraj = pd.DataFrame(podzial_na_kraj, columns=['Ilosc'])
podzial_na_kraj = podzial_na_kraj.reset_index()
podzial_na_kraj['Index'] = podzial_na_kraj.index
podzial_na_kraj['text'] = podzial_na_kraj.apply(lambda row: f'Liczba zawodników: {row["Ilosc"]}', axis=1)

# podział na kraje w latach
kraje_w_latach = df.groupby(['kraj', 'rok']).size()
kraje_w_latach = pd.DataFrame(kraje_w_latach, columns=['Ilosc'])
kraje_w_latach = kraje_w_latach.reset_index()

# podział zawodników na płeć i kategorie wiekowe
kabiety_kategorie = df.query("kat == ['K20', 'K30', 'K40', 'K50', 'K60']")
kabiety_kategorie = kabiety_kategorie.groupby('kat').size()
kabiety_kategorie = pd.DataFrame(kabiety_kategorie, columns=['Ilosc'])
kabiety_kategorie = kabiety_kategorie.reset_index()

men_kategorie = df.query("kat == ['M20', 'M30', 'M40', 'M50', 'M60']")
men_kategorie = men_kategorie.groupby('kat').size()
men_kategorie = pd.DataFrame(men_kategorie, columns=['Ilosc'])
men_kategorie = men_kategorie.reset_index()

# 10 najlepszych czasów
top_czas = df.sort_values('wynik').head(10)
top_czas = top_czas[['rok', 'miejsce', 'nazwisko', 'wynik', 'kraj']]

# 10 najgorszych czasów
worst_czas = df.sort_values('wynik', ascending=False).head(10)
worst_czas = worst_czas[['rok', 'miejsce', 'nazwisko', 'wynik', 'kraj']]

# średni czas
df['wynik'] = pd.to_datetime(df['wynik'], format='%H:%M:%S')
df['wynik'] = df['wynik'].dt.time
df['Time_sec'] = df['wynik'].apply(lambda x: x.hour * 3600 + x.minute * 60 + x.second)
srednia_czasu_sec = df['Time_sec'].mean()
srednia_czasu = pd.Timestamp('1900-01-01') + pd.Timedelta(seconds=srednia_czasu_sec)
srednia_czasu = srednia_czasu.time().strftime('%H:%M:%S')

# analiza czasów
less_1_30 = df.query("Time_sec < 5400")
less_1_30 = len(less_1_30)
statystyka = df.query("Time_sec > 5400 and Time_sec < 7200")
statystyka = len(statystyka)
more_2h = df.query("Time_sec > 7200")
more_2h = len(more_2h)
analiza_czasow = pd.DataFrame(data=[less_1_30, statystyka, more_2h], columns=['liczba'])
analiza_czasow['opis'] = ['Poniżej 1:30', 'Między 1:30 a 2 godziny', 'Powyżej 2 godzin']

# winery
win_men = df.query("miejsce == 1 and rodzaj_plci == 'M'")
win_men = win_men[['rok', 'nazwisko', 'miasto', 'wynik']]
win_women = df.query("rodzaj_plci == 'K'")
win_women = win_women.loc[win_women.groupby('rok')['miejsce'].idxmin()]
win_women = win_women[['rok', 'nazwisko', 'miasto', 'wynik']]
win_men['lats'] = [49.8419, 0.5198, 0.5198, -1.2832, 0.5198, 50.4500, 51.3464, 48.1517, 50.4500, 51.3464]
win_men['lons'] = [24.0316, 35.2715, 35.2715, 36.8172, 35.2715, 30.5241, 21.2436, 17.1093, 30.5241, 21.2436]
win_men['kraj'] = ['Ukrainy', 'Kenii', 'Kenii', 'Kenii', 'Kenii', 'Ukrainy', 'Polski', 'Słowacji', 'Ukrainy', 'Polski']
win_women['lats'] = [50.4500, 0.5198, 0.5198, -1.2832, 47.5314, 0.5198, 50.0545, 49.6744, 52.5928, 51.1077]
win_women['lons'] = [30.5241, 35.2715, 35.2715, 36.8172, 21.6260, 35.2715, 22.5014, 21.8299, 21.4584, 20.7593]
mapa_win = pd.concat([win_men, win_women], axis=0)
win_men2 = win_men[['rok', 'nazwisko', 'miasto', 'wynik']]
win_women2 = win_women[['rok', 'nazwisko', 'miasto', 'wynik']]

# rzeszowianie
liczba_wierszy = df.shape[0]
rzeszowianie = df.query("miasto == 'RZESZÓW'")
liczba_rzesz =  rzeszowianie.shape[0]

win_rze_men = rzeszowianie.loc[rzeszowianie.groupby('rok')['miejsce'].idxmin()]
win_rze_men = win_rze_men[['rok', 'nazwisko', 'wynik', 'miejsce']]
rze_kobiety = rzeszowianie.query("rodzaj_plci == 'K'")
win_rze_women = rze_kobiety.loc[rze_kobiety.groupby('rok')['miejsce'].idxmin()]
win_rze_women = win_rze_women[['rok', 'nazwisko', 'wynik', 'miejsce']]

# podział na miasta
podział_na_miasta = df.groupby('miasto').size()
podział_na_miasta = pd.DataFrame(podział_na_miasta, columns=['Ilosc'])
podział_na_miasta = podział_na_miasta.reset_index()
podział_na_miasta = podział_na_miasta.sort_values('Ilosc', ascending=False)
podział_na_miasta = podział_na_miasta.head(15)
podział_na_miasta = podział_na_miasta.sort_values('Ilosc')

# podział na kluby
podział_na_kluby = df.groupby('klub').size()
podział_na_kluby = pd.DataFrame(podział_na_kluby, columns=['Ilosc'])
podział_na_kluby = podział_na_kluby.reset_index()
podział_na_kluby = podział_na_kluby.sort_values('Ilosc', ascending=False)
podział_na_kluby = podział_na_kluby.head(15)
podział_na_kluby = podział_na_kluby.sort_values('Ilosc')
podział_na_kluby = podział_na_kluby.drop([1338, 793, 1324, 0, 9])

# lojalność zawodników
zawodnicy_all = df.groupby('nazwisko').size()
zawodnicy_all = pd.DataFrame(zawodnicy_all, columns=['Ilość edycji'])
zawodnicy_all = zawodnicy_all.reset_index()
zawodnicy_all = zawodnicy_all.sort_values('Ilość edycji', ascending=False)
zawodnicy_all = zawodnicy_all.head(8)

merged_df = zawodnicy_all.merge(df, on='nazwisko')
merged_df = merged_df[['nazwisko', 'miasto']]
merged_df['Index'] = merged_df.index
merged_df = merged_df.loc[merged_df.groupby('nazwisko')['Index'].idxmin()]
merged_df = merged_df.merge(zawodnicy_all, on='nazwisko')
merged_df = merged_df[['nazwisko', 'miasto', 'Ilość edycji']]

# rzeszowianie na półmaratonie
liczba_rzeszowianow = df.query("miasto == 'RZESZÓW'")
liczba_rzeszowianow = liczba_rzeszowianow.groupby('rok').size()
liczba_rzeszowianow = pd.DataFrame(liczba_rzeszowianow, columns=['rzeszow'])
liczba_rzeszowianow = liczba_rzeszowianow.reset_index()

# przygotowanie tabeli do strony głownej
kobiety = df.query("rodzaj_plci == 'K'")
kobiety_sg = kobiety.groupby('rok').size()
kobiety_sg = pd.DataFrame(kobiety_sg, columns=['kobiet'])
kobiety_sg = kobiety_sg.reset_index()

men = df.query("rodzaj_plci == 'M'")
men_sg = men.groupby('rok').size()
men_sg = pd.DataFrame(men_sg, columns=['men'])
men_sg = men_sg.reset_index()

# strona główna - tabela
strona_glowna = pd.merge(zawodnicy_w_latach, kobiety_sg,  on='rok', how='inner')
strona_glowna = pd.merge(strona_glowna, men_sg,  on='rok', how='inner')
strona_glowna = pd.merge(strona_glowna, liczba_rzeszowianow,  on='rok', how='inner')
strona_glowna = pd.merge(strona_glowna, win_men,  on='rok', how='inner')

# =================================================================================

app.layout = html.Div([
    html.H2('Półmaraton Rzeszowski w latach 2014 - 2023'),
    #html.H2('Półmaratonu Rzeszowskiego - 10 edycji'),
    #html.Br(),
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content',
             style={'color': 'darkblue'}
             )
], style={
            'color': 'darkblue',
            'fontSize': 15,
            'background-color': '#C7C7C7',
            'text-align': 'center',
            'height': '100vh',
            'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.1)',
            'margin': '2px',
            'font-family': 'Arial, sans-serif'
            #'padding': '10px'
            #'border': '4px solid Gray',
            #'border-style': 'dashed'
        })


# strona główna
index_page = html.Div([
    html.Div([
        html.Br(),
        html.H3('Wybierz rok:'),
        dcc.Slider(
            id='my-slider',
            min=strona_glowna['rok'].min(),
            max=strona_glowna['rok'].max(),
            step=1,
            value=strona_glowna['rok'].min(),
            marks={str(rok): str(rok) for rok in strona_glowna['rok']},
            # marks={i: f'{i//1000}k' for i in range(2014, 2024, 1)},
            tooltip={'always_visible': False},
            #font=dict(size=12)
        ),
        html.Br(),
        html.H3('MENU:'),
        dcc.Link('Informacje ogólne', href='/ogolne'),
        html.Br(),
        dcc.Link('Kategrie wiekowe', href='/wiekowe'),
        html.Br(),
        dcc.Link('Analiza czasów', href='/czasy'),
        html.Br(),
        dcc.Link('Zwycięzcy w Półmaratonie Rzeszowskim', href='/win'),
        html.Br(),
        dcc.Link('Rzeszów na półmaratonie', href='/rzeszow'),
        html.Br(),
        dcc.Link('3 ciekawostki', href='/fun'),
        html.Br(),
        dcc.Link('Podsumowanie / autor', href='/adam'),
        html.Br(),
        html.Br()
        #html.Br()
    ],
    style={'width': '26%', 'float': 'left', 'background-color': 'lightgray', 'text-align': 'left',
           'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.1)', 'margin': '5px', 'padding': '5px', 'height':575}),

    html.Div([
        #html.Br(),
        #html.Div(id='text-output', style={'background-color': 'lightgray'}),
        html.Div([
            #html.Div(id='text-output', style={'background-color': 'lightgray'}),
            dcc.Graph(id='my-graph'),
            dcc.Graph(id='pie-chart-container')
            #html.Br(),
        ], style={'width': '34%', 'float': 'left', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'}),
        html.Div([
            #html.Div(id='text-output', style={'background-color': 'lightgray'}),
            dcc.Graph(id='my-graph2'),
            dcc.Graph(id='my-scattergeo')
            #dcc.Graph(id='pie-chart-container'),

        ], style={'width': '65%', 'float': 'right', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'})

    ],
    style={'width': '71%', 'float': 'right', 'margin': '5px', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'}),

])

@app.callback(
    #Output('wartosc-output', 'children'),
    [Output('my-graph', 'figure'),
     Output('pie-chart-container', 'figure'),
     Output('my-graph2', 'figure'),
     #Output('text-output', 'children'),
     Output('my-scattergeo', 'figure')],
    [Input('my-slider', 'value')]
)
def update_wartosc_i_wykres(rok):
    wartosc = strona_glowna[strona_glowna['rok'] == rok]['Ilosc'].values[0]
    wartosc_kobiety = strona_glowna[strona_glowna['rok'] == rok]['kobiet'].values[0]
    wartosc_men = strona_glowna[strona_glowna['rok'] == rok]['men'].values[0]
    wartosc_rzeszow = strona_glowna[strona_glowna['rok'] == rok]['rzeszow'].values[0]
    wartosc_mapa = strona_glowna[strona_glowna['rok'] == rok]
    nazwisko = strona_glowna[strona_glowna['rok'] == rok]['nazwisko'].values[0]
    wartosc_wynik = strona_glowna[strona_glowna['rok'] == rok]['wynik'].values[0]
    wartosc_kraj = strona_glowna[strona_glowna['rok'] == rok]['kraj'].values[0]


    data = go.Bar(
        x=[rok],
        y=[wartosc],
        name='Wykres',
        showlegend=False
    )

    layout = go.Layout(
        title=f'Liczba zawodników w {rok} roku',
        title_font=dict(size=15),
        showlegend=True,
        height=275,
        #width=420,
        paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
            # bargap=0.5,
            # width=500,
        hovermode='closest',
        xaxis={'title': f'Rok {rok}', 'tickvals': [1], 'ticktext': ['1']},
        yaxis={'title': 'Ilość', 'range': [0, 1400]}
    )

    data2 = go.Pie(
        labels=['Kobiet', 'Mężczyzn'],
        values=[wartosc_kobiety, wartosc_men],
        name='Wykres',
        showlegend=False
     )

    layout2 = go.Layout(
        title=f'Podział zawodników na płeć',
        title_font=dict(size=15),
        height=310,
        #width=420,
        showlegend=True,
            # bargap=0.5,
            # width=500,
        hovermode='closest',
        paper_bgcolor='lightgray',
        xaxis={'title': f'Rok {rok}', 'tickvals': [1], 'ticktext': ['1']},
        yaxis={'title': 'Ilość', 'range': [0, 1400]}
    )

    figure3 = go.Figure(data=go.Indicator(
        mode='number+gauge',
        title={'text': f"Liczba Rzeszowian w {rok} roku"},
        title_font=dict(size=15),
        value=wartosc_rzeszow,
        number=dict(prefix='', suffix=''),
        gauge=dict(
            axis=dict(range=[None, 1000]),
            bar=dict(color='blue'),
            bgcolor='lightgray',
            borderwidth=2,
            bordercolor='gray',
            steps=[
                dict(range=[0, 0], color='green'),
                dict(range=[0, 1000], color='lightgray')
            ],
            threshold=dict(line=dict(color="darkblue", width=4), thickness=0.75, value=wartosc_rzeszow)
        )
    ))

    figure3.update_layout(height=225, paper_bgcolor='lightgray')

    figure4 = go.Figure(data=go.Scattergeo(
        lat=wartosc_mapa['lats'],
        lon=wartosc_mapa['lons'],
        text=wartosc_mapa['miasto'],
        hoverinfo='text',
        marker=dict(
            #size=data['Marker Size'],
            sizemode='diameter',
            sizeref=0.5,
            color='blue'
        )
    ))

    figure4.update_layout(
        paper_bgcolor='lightgray',
        height=360,
        geo=dict(
            #height=545,
            scope='world',
            showcountries=True,
            showland=True,
            showframe=False,
            showcoastlines=False,
            landcolor='lightgray',
            countrycolor='white',
            coastlinecolor='white',
            projection_type='equirectangular',
            showlakes=True,
            lakecolor='white',
            showocean=False,
            oceancolor='white'
        ),
        title_text=f"1. miejsce w {rok} roku zdobył {nazwisko} z czasem {wartosc_wynik}.<br>Zwycięzca pochodził z {wartosc_kraj}.",
        title_x=0.5,
        title_font=dict(size=13)
    )


    figure = {'data': [data], 'layout': layout}
    figure2 = {'data': [data2], 'layout': layout2}

    return  figure, figure2, figure3, figure4




# dekorator do linków w MENU
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/ogolne':
        return ogolne_leyout
    elif pathname == '/wiekowe':
        return wiekowe_leyout
    elif pathname == '/czasy':
        return czasy_leyout
    elif pathname == '/win':
        return win_leyout
    elif pathname == '/rzeszow':
        return rzeszow_leyout
    elif pathname == '/fun':
        return fun_leyout
    elif pathname == '/adam':
        return adam_leyout
    else:
        return index_page

# pierwsza zakładka z MENU - ogólne informacje
ogolne_leyout = html.Div([

    html.Div([
        html.Div([
            html.H5('Suma zawodników z podziałem na płeć'),

            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Pie(labels=podzial_na_plec['rodzaj_plci'], values=podzial_na_plec['Ilosc'], hole=0.4,
                               # marker=dict(colors=['darkblue', 'blue']),
                               )
                    ],
                    layout=go.Layout(
                        height=350,
                        title_text='Wszystkich uczestników: 10207',
                        showlegend=True
                    )
                )
            )
        ], style={'width': '39%', 'float': 'left', 'background-color': 'lightgray', 'text-align': 'center',
                  'margin': '5px'}),

        html.Div([
            html.H5('Rozkład zawodników z podziałem na płeć'),
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=kobiety_lata.rok,
                            y=kobiety_lata.Ilosc,
                            # text='kobiety',
                            name='kobiety',
                            marker=dict(color='#BF4400')

                        ),
                        go.Bar(
                            x=men_lata.rok,
                            y=men_lata.Ilosc,
                            name='mężczyźni',
                            marker=dict(color='#6075FF')
                        )
                    ],
                    layout=go.Layout(
                        height=350,
                        # title_text='Rozkład zawodników z podziałem na płeć ',
                        showlegend=False,
                        xaxis=dict(title='Lata'),
                        yaxis=dict(title='Ilość zawodników'),
                        # barmode='group'
                    )
                ),
            ),
        ], style={'width': '59%', 'float': 'right', 'background-color': 'lightgray', 'text-align': 'center',
                  'margin': '5px'}),
    ]),

    html.H5('Podział zawodników na lata'),
    dcc.Graph(
        # id='ogolne-1-graph',
        figure=go.Figure(
            data=[
                go.Bar(
                    x=zawodnicy_w_latach.rok,
                    y=zawodnicy_w_latach.Ilosc,
                    # name='Podział zawodników na lata'
                    # marker=dict(color='darkblue')

                )
            ],
            layout=go.Layout(
                height=400,
                # title_text='Podział zawodników na lata',
                showlegend=False,
                xaxis=dict(title='Lata'),
                yaxis=dict(title='Ilość zawodników'),
                barmode='group'
            )
        ),
    ),



    html.H5('Rozkład zawodników z podziałem na państwa'),
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Choropleth(
                    locations=podzial_na_kraj['kraj'],
                    colorscale='Viridis',
                    z=podzial_na_kraj['Index'],
                    hovertext=podzial_na_kraj['text']
                    #colorbar=False

                ),

            ],
            layout=go.Layout(
                height=600,
                #title_text='Rozkład zawodników z podziałem na państwa',
                #coloraxis=dict(colorbar=dict(showticklabels=False)),
                geo=dict(
                        showframe=False,
                        showcoastlines=False,
                        projection_type='equirectangular'
                    )

            )
        ),
    ),


    html.Div(id='ogolne-1-div'),
    html.Br(),
    dcc.Link('Wróc do MENU', href='/')
], style={
            'color': 'darkblue',
            'fontSize': 15,
            'background-color': 'lightgray',
            'text-align': 'center',
            'border': '4px solid Gray',
            'border-style': 'dashed',
            'height': '100%'
        })

# druga zakładka z MENU - kategorie wiekowe
wiekowe_leyout = html.Div([
    html.H4('Półmaraton Rzeszowski - analiza zawodników z podziałem na kategorie wiekowe'),
    dcc.Tabs(
        id='wiekowe-1-tabs',
        children=[
            dcc.Tab(label='Kobiety', value='tab-1'),
            dcc.Tab(label='Mężczyźni', value='tab-2')
        ],
        value='tab-1'
    ),

    html.Div(id='wiekowe-1-div'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Link('Wróc do MENU', href='/')

], style={
            'color': 'darkblue',
            'fontSize': 15,
            'background-color': 'lightgray',
            'text-align': 'center',
            'border': '4px solid Gray',
            'border-style': 'dashed',
            'height': '100%'
        })

#dekorator do 2 zakładki
@app.callback(
    Output('wiekowe-1-div', 'children'),
    [Input('wiekowe-1-tabs', 'value')]
)
def tech_1_tabs(value):
    if value == 'tab-1':
        return html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Pie(labels=kabiety_kategorie.kat, values=kabiety_kategorie.Ilosc,
                               )
                    ],
                    layout=go.Layout(
                        height=400,
                        title_text='Podział na kategorie',
                        showlegend=True
                    )
                )
            )
        ])
    elif value == 'tab-2':
        return html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Pie(labels=men_kategorie.kat, values=men_kategorie.Ilosc)
                    ],
                    layout=go.Layout(
                        height=400,
                        title_text='Podział na kategorie',
                        showlegend=True

                    )
                )
            )
        ])

# trzecia zakładka z MENU - analiza czasów
czasy_leyout = html.Div([
    html.H4('Półmaraton Rzeszowski - analiza czasów'),
    #html.P(f'Średni czas jaki uzyzkują zawodnicy na Półmaratonie Rzeszowskim to: {srednia_czasu}'),
    html.Span(f'Średni czas jaki uzyzkują zawodnicy na Półmaratonie Rzeszowskim to: {srednia_czasu}', style={'font-weight': 'bold', 'color': 'blue'}),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Pie(labels=analiza_czasow.opis, values=analiza_czasow.liczba)
            ],
            layout=go.Layout(
                height=400,
                title_text='Analiza czasów',
                showlegend=True
            )
        )
    ),


    dcc.RadioItems(
        id='radio-1',
        options=[
            {'label': '10 najlepszych czasów', 'value': 'top'},
            {'label': '10 najgorszych czasów', 'value': 'worst'}
        ],
        value='top'
    ),
    html.Div(id='czasy-1-div'),
    html.Br(),
    dcc.Link('Wróc do MENU', href='/')
], style={
            'color': 'darkblue',
            'fontSize': 15,
            'background-color': 'lightgray',
            'text-align': 'center',
            'border': '4px solid Gray',
            'border-style': 'dashed',
            'height': '100%'
        })

@app.callback(
    Output(component_id='czasy-1-div', component_property='children'),
    [Input(component_id='radio-1', component_property='value')]
)
def tech_1_tabs(value):
    if value == 'top':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in top_czas.columns],
                data=top_czas.to_dict('records')
            )
        ])
    elif value == 'worst':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in worst_czas.columns],
                data=worst_czas.to_dict('records')
            )
        ])

# 4 zakładka z MENU - zwycięzcy
win_leyout = html.Div([

    html.H4('Półmaraton Rzeszowski - pochodzenie zwycięzców'),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Scattergeo(
                    lat=mapa_win['lats'],
                    lon=mapa_win['lons'],
                    text=mapa_win['miasto'],
                    mode='markers',
                    marker=dict(size=7, color='blue', symbol='circle'),
                    #color=win_men['miasto']
                    hoverinfo='text'
                    #hovertext=mapa_win['nazwisko']

                ),

            ],
            layout=go.Layout(
                height=600,
                #title_text='Pochodzenie zwycięzców',
                # coloraxis=dict(colorbar=dict(showticklabels=False)),
                geo=dict(
                    scope='world',
                    showland=True,
                    showcountries=True,
                    landcolor='rgb(217, 217, 217)',
                    countrycolor='rgb(255, 255, 255)',
                    showframe=True,
                    showcoastlines=False
                )

            )
        ),
    ),

    html.H4('Półmaraton Rzeszowski - zwycięzcy'),

    dcc.Tabs(
        id='win-1-tabs',
        children=[
            dcc.Tab(label='Mężczyźni', value='tab-1'),
            dcc.Tab(label='Kobiety', value='tab-2')
        ],
        value='tab-1'
    ),


    html.Div(id='win-1-div'),
    html.Br(),
    dcc.Link('Wróc do MENU', href='/')

], style={
            'color': 'darkblue',
            'fontSize': 15,
            'background-color': 'lightgray',
            'text-align': 'center',
            'border': '4px solid Gray',
            'border-style': 'dashed',
            'height': '100%'
        })

#dekorator do 4 zakładki
@app.callback(
    Output('win-1-div', 'children'),
    [Input('win-1-tabs', 'value')]
)
def tech_1_tabs(value):
    if value == 'tab-1':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in win_men2.columns],
                data=win_men2.to_dict('records')
            )
        ])
    elif value == 'tab-2':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in win_women2.columns],
                data=win_women2.to_dict('records')
            )
        ])

# 5 zakładka rzeszów
rzeszow_leyout = html.Div([
    html.H5('Liczba Rzeszowian na Półmaratonie Rzeszowskim'),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Indicator(
                    mode="gauge",
                    value=liczba_rzesz,
                    title={'text': "Liczba Rzeszowian"},
                    #number={'format': 's'},
                    #delta={'reference': 4000, 'relative': True},
                    gauge={
                        'axis': {'range': [0, liczba_wierszy]},
                        'bar': {'color': 'blue'},
                        'steps': [
                            {'range': [0, 0], 'color': "lightgray"},
                            {'range': [0, liczba_wierszy], 'color': "lightgray"}
                        ],
                        'threshold': {
                            'line': {'color': "darkblue", 'width': 4},
                            'thickness': 0.75,
                            'value': liczba_rzesz
                        }
                    }
                )
            ],
            layout=go.Layout(
                height=400,
                title_text=f'Wszystkich uczestników: {liczba_wierszy}<br>Rzeszowianów: {liczba_rzesz}',
                showlegend=True
            )
        )
    ),

    html.H5('Najlepsi Rzeszowianie'),

    dcc.Tabs(
        id='rzeszow-1-tabs',
        children=[
            dcc.Tab(label='Mężczyźni', value='tab-1'),
            dcc.Tab(label='Kobiety', value='tab-2')
        ],
        value='tab-1'
    ),

    html.Div(id='rzeszow-1-div'),
    html.Br(),
    dcc.Link('Wróc do MENU', href='/')
], style={
            'color': 'darkblue',
            'fontSize': 15,
            'background-color': 'lightgray',
            'text-align': 'center',
            'border': '4px solid Gray',
            'border-style': 'dashed',
            'height': '100%'
        })

#dekorator do 5 zakładki
@app.callback(
    Output('rzeszow-1-div', 'children'),
    [Input('rzeszow-1-tabs', 'value')]
)
def tech_1_tabs(value):
    if value == 'tab-1':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in win_rze_men.columns],
                data=win_rze_men.to_dict('records')
            )
        ])
    elif value == 'tab-2':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in win_rze_women.columns],
                data=win_rze_women.to_dict('records')
            )
        ])


# 6 zakładka
fun_leyout = html.Div([
    html.Div([
html.H5('Najpopularniejsze miasta'),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=podział_na_miasta.Ilosc,
                    y=podział_na_miasta.miasto,
                    #text='kobiety',
                    name='kobiety',
                    marker=dict(color='blue'),
                    orientation='h'
                ),

            ],
            layout=go.Layout(
                height=450,
                title_text='Suma wszystkich miejscowości: 1115',
                showlegend=False,
                xaxis=dict(title='Ilość zawodników'),
                yaxis=dict(title='Miasto'),
                #barmode='group'
            )
        ),
    ),
    ], style={'width': '49%', 'float': 'left', 'background-color': 'lightgray', 'text-align': 'center', 'margin': '5px'}),

    html.Div([
html.H5('Najpopularniejsze kluby sportowe'),
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=podział_na_kluby.Ilosc,
                    y=podział_na_kluby.klub,
                    # text='kobiety',
                    name='kobiety',
                    marker=dict(color='blue'),
                    orientation='h'
                ),

            ],
            layout=go.Layout(
                height=450,
                title_text='Suma wszystkich klubów: 2064',
                showlegend=False,
                xaxis=dict(title='Ilość zawodników'),
                yaxis=dict(title='Miasto'),
                # barmode='group'
            )
        ),
    ),
    ], style={'width': '49%', 'float': 'right', 'background-color': 'lightgray', 'text-align': 'center', 'margin': '5px'}),




    html.H5('Lojalność zawodników: 8 zawodników brało udział we wszystkich 10. ostatnich edycjach biegu'),

    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in merged_df.columns],
        #title="zawodników brało ",
        data=merged_df.to_dict('records')
    ),


    html.Div(id='fun-1-div'),
    html.Br(),
    dcc.Link('Wróc do MENU', href='/')
], style={
            'color': 'darkblue',
            'fontSize': 15,
            'background-color': 'lightgray',
            'text-align': 'center',
            'border': '4px solid Gray',
            'border-style': 'dashed',
            'height': '100%'
        })


# 7 zakładka - podsumowanie / autor
adam_leyout = html.Div([

    html.Div([
    html.H5('Podsumowanie / wnioski', style={'background-color':'white', 'font-size': '30px', 'text-align': 'center'}),
    dcc.Markdown(
        "Projekt ma na celu przeanalizowanie biegów długodystansowych w Rzeszowie na przykładzie Półmaratonu Rzeszowskiego w ostatnich 10 latach. "
        "W projekcie pokazano m.in. statystyki dotyczące: liczby uczestników, podział na płeć, kategorie wiekowe, najlepsze i najgorsze czasy czy "
        "informacje skąd pochodzili zawodnicy. Dane z których korzystałem przy pisaniu tego projektu pochodzą ze strony: https://runrzeszow.pl/wyniki/polmaraton/. "
        "Patrząc na otrzymywane wyniki można wysnuć kilka wniosków: od 2014 do 2019 roku półmaraton zwiększał swoją "
        "liczebność oraz nie brakowało zawodników spoza Europy. Lata w okresie pandemii można skomentować krótko: bardzo mało zawodników, zawodnicy tylko z Polski, "
        "słabsze czasy wśród zwycięzców. Aktualnie Półmaraton w Rzeszowie wrócił do liczebności z najlepszych lat, najwięcej bo ok. 30% zawodników pochodzi z Rzeszowa, "
        "spora część zawodników przyjeżdża do stolicy podkarpacia z: Przemyśla, Dębicy, Krakowa, Stalowej Woli oraz z Lublina czy Warszawy. Obcokrajowcy natomiast "
        "pojawiają się tylko z krajów ościennych. "
        "Kobiet na półmaratonie jest zawsze niecałe 20% wszystkich uczestników. Najliczniejszą grupą wiekową są zawodnicy z przedziału 30-39 lat. Ponad 60% zawodników "
        "pokonuje ten dystans w przedziale 1:30 - 2 godziny, średnia to 1:51:44. ", style={'margin': '5px'}
    )

    ], style={'width': '49%', 'float': 'left', 'background-color': 'white', 'text-align': 'left', 'margin': '5px', 'height': '90vh'}),

    #html.H5('Autor - Adam Rybiński'),
    html.Div([
    html.H5('Autor', style={'background-color':'white', 'font-size': '30px', 'text-align': 'center'}),
    dcc.Markdown(
        "**Adam Rybiński** - absolwent Politechniki Rzeszowskiej im. Ignacego Łukasiewicza na kierunku: Matematyka. Aktualnie student "
        "studiów podyplomowych na kierunku: Big Data. Inżynieria Danych, uczelnia: Uniwersytet WSB Merito w Gdańsku. Projekt został napisany jako praca dyplomowa, "
        "temat nie został wybrany przypadkowo, od kilku lat trenuję bieganie i w ostatnich dwóch edycjach Półmaratonu Rzeszowskiego zdobyłem "
        "1. miejsce w kategorii Najlepszy Rzeszowianin.", style={'margin': '5px'}

    ),
        html.Img(src='https://github.com/rybinski92/halfmarathon_rzeszow/blob/main/ar%20mielec.jpg?raw=true',
                 style={'height':'300px', 'position': 'absolute', 'left':'62%', 'margin': '20px'})

    ], style={'width': '49%', 'float': 'right', 'background-color': 'white', 'text-align': 'left', 'margin': '5px',  'height': '90vh'}),




    html.Div(id='adam-1-div'),
    html.Br(),
    dcc.Link('Wróc do MENU', href='/')
], style={
            'color': 'darkblue',
            'fontSize': 15,
            'background-color': 'lightgray',
            'text-align': 'center',
            'border': '4px solid Gray',
            'border-style': 'dashed',
            'height': '100%'
        })

if __name__ == '__main__':
    app.run_server(debug=True)

