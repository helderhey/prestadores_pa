import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import math
import plotly.graph_objects as go

df_scatter = pd.read_csv(
    'https://raw.githubusercontent.com/helderhey/prestadores_pa/main/df_scatter.csv', sep="@", low_memory=False)

select_class = pd.read_csv(
    'https://raw.githubusercontent.com/helderhey/prestadores_pa/main/select_class.csv', sep="@", low_memory=False)

select_prest_data = pd.read_csv(
    'https://raw.githubusercontent.com/helderhey/prestadores_pa/main/select_prests.csv', sep="@", low_memory=False)

list_data = pd.read_csv(
    'https://raw.githubusercontent.com/helderhey/prestadores_pa/main/mes_ano.csv', sep="@", low_memory=False)
list_m = list(list_data['MES_ANO'])
list_l = ['JULHO/2022', 'AGOSTO/2022', 'SETEMBRO/2022', 'OUTUBRO/2022', 'NOVEMBRO/2022', 'DEZEMBRO/2022',
          'JANEIRO/2023', 'FEVEREIRO/2023', 'MARÇO/2023', 'ABRIL/2023', 'MAIO/2023', 'JUNHO/2023']
l_z = list(zip(list_l, list_m))

table_data = pd.DataFrame()

for dt in range(len(list_data)):
    table = pd.read_csv(
        f'https://raw.githubusercontent.com/helderhey/prestadores_pa/main/table_data_{dt}.csv', sep="@", low_memory=False)
    table_data = pd.concat([table, table_data])

table_data['VALOR_PAGO'] = table_data['VALOR_PAGO'].apply(
    lambda x: "{:.2f}".format(x))
table_data['VALOR_UNIT'] = table_data['VALOR_UNIT'].apply(
    lambda x: "{:.2f}".format(x))

external_stylesheets = [dbc.themes.GRID]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(children=[html.Hr(
                style={'border': '3px solid rgba(0, 0, 0, 0.3)',
                       'margin': '5px'}
            ),
                html.P('1. Selecione a Classe do Evento:',
                       style={'font-size': '20px',
                              'color': 'blue',
                              'font-weight': 'bold',
                              'font-family': 'Arial',
                              'text-align': 'left',
                              'vertical-align': 'top',
                              'margin': '5px',
                              'padding': '0px'}
                       ),
                html.Br(),
                dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i}
                         for i in list(select_class['DESC_CLASSE'])],
                value='Material de consumo',
                clearable=False,
                style={'font-size': '15px',
                       'font-family': 'Arial',
                       'font-weight': 'bold',
                       'background-color': 'rgba(102, 102, 255, 0.1)',
                       'height': '35px',
                       'margin-bottom': '5px',
                       'margin-right': '5px',
                       #    'border-style': 'solid',
                       #    'border-color': 'coral'
                       }
            ),
                dcc.Graph(id='indicator-graphic',
                          config={'displaylogo': False,
                                  'displayModeBar': False},
                          style={'margin-left': '20px'}),

                html.P('Obs.: valores normalizados.',
                       style={'font-size': '14px',
                              'font-family': 'Arial'}), ],
                # style={'border-style': 'solid',
                #        'border-color': 'coral'
                #        }
                #    ,
                lg=4),
            dbc.Col(children=[html.Hr(style={'border': '3px solid rgba(0, 0, 0, 0.3)', 'margin': '5px'}),
                              html.P('2. Escolha a Métrica:',
                                     style={
                                         'font-size': '20px',
                                         'font-family': 'Arial',
                                         'color': 'blue',
                                         'font-weight': 'bold',
                                         'text-align': 'left',
                                         'vertical-align': 'top',
                                         'margin': '5px',
                                         'padding': '0px', }),
                              html.Br(),
                              dcc.RadioItems(
                id='metrica',
                options=[{'label': 'Valor Médio Unitário/Evento (R$)', 'value': 'VMU_MES'},
                         {'label': 'Frequência Evento/Beneficiário (un)',
                          'value': 'FREQUENCIA_EVENTO_MES'},
                         {'label': 'Valor Médio Unitário/Beneficiário (R$)', 'value': 'VMU_BENEF_MES'}],
                value='VMU_MES',
                labelStyle={'font-size': '14px',
                            'font-family': 'Arial', 'font-weight': 'bold'},
                inputStyle={"margin-left": "15px"},
                style={'height': '35px',
                       'display': 'flex',
                       'align-items': 'center',
                       'justify-content': 'center',
                       'background-color': 'rgba(102, 102, 255, 0.2)',
                       #    'border-style': 'solid',
                       #    'border-color': 'coral'
                       }
            ),
                dcc.Graph(id='metrica_graph', config={
                    'displaylogo': False, 'displayModeBar': False}),
            ],
                #     style={
                #     'border-style': 'solid',
                #         'border-color': 'coral'
                # },
                lg=8),
        ],
        align="left", className="g-0"
    ),
    dbc.Row(
        [
            dbc.Col(children=[html.Hr(style={'border': '3px solid rgba(0, 0, 0, 0.3)', 'margin': '5px'}),
                              html.P('3. Escolha um Prestador:',
                                     style={
                                         'font-size': '20px',
                                         'font-family': 'Arial',
                                         'color': 'blue',
                                         'font-weight': 'bold',
                                         'text-align': 'left',
                                         'vertical-align': 'top',
                                         'margin': '5px',
                                         'padding': '0px', }),
                              html.Br(),
                              dcc.Dropdown(
                id='prest-column',
                options=[{'label': i, 'value': i}
                    for i in list(select_prest_data['NOME_RESUMIDO'])],
                value='STA LUCIA',
                clearable=False,
                style={'font-size': '15px',
                       'font-family': 'Arial', 'font-weight': 'bold',
                       'background-color': 'rgba(102, 102, 255, 0.1)',
                       'height': '35px', 'margin': '5px',
                       #    'border-style': 'solid',
                       #                    'border-color': 'coral'
                       }
            ), html.Br(),
                html.Hr(
                    style={'border': '3px solid rgba(0, 0, 0, 0.3)', 'margin': '5px'}),
                html.P('4. Selecione o Mês de interesse:',
                       style={
                           'font-size': '20px',
                           'font-family': 'Arial',
                           'text-align': 'left',
                           'color': 'blue',
                           'font-weight': 'bold',
                                         'vertical-align': 'top',
                                         'margin': '5px',
                                         'padding': '0px', }),
                html.Br(),
                dcc.RadioItems(
                    id='mes_ano',
                options=[{"label": l_z[x][0], "value": l_z[x][1]}
                         for x in range(len(l_z))],
                value='2021-07-01',
                inputStyle={'margin': '6px'},
                labelStyle={'display': 'block'},
                style={'align-items': 'center',
                       'font-size': '13px',
                       'font-family': 'Arial',
                       'text-align': 'left',
                       'margin-left': '80px',
                       "height": 320,
                       "width": 400}
            ),
                html.Br(),
            ],
                #     style={
                #     'border-style': 'solid',
                #         'border-color': 'coral'
                # },
                lg=4),
            dbc.Col(children=[html.Hr(style={'border': '3px solid rgba(0, 0, 0, 0.3)', 'margin': '5px'}),
                              html.P('5. Tabela Detalhada:',
                                     style={
                                         'font-size': '20px',
                                         'font-family': 'Arial',
                                         'color': 'blue',
                                         'font-weight': 'bold',
                                         'text-align': 'left',
                                         'vertical-align': 'top',
                                         'margin': '5px',
                                         'padding': '0px'}),
                              #   html.Br(),
                              dash_table.DataTable(id='table',
                                                   style_table={
                                                       'height': '420px',
                                                       'overflowY': 'auto',
                                                       'margin-left': '5px',
                                                       'margin-right': '5px',
                                                       'width': '860px'},
                                                   style_cell={
                                                       'textAlign': 'right',
                                                       'font-family': 'Arial',
                                                       'font-size': '12px',
                                                       'height': '10px'},
                                                   cell_selectable=False,
                                                   # fixed_rows={'headers': True, 'data': 0},
                                                   style_data={'width': '50px',
                                                               'maxWidth': '50px',
                                                               'minWidth': '50px'},
                                                   style_cell_conditional=[
                                                       {
                                                           'if': {'column_id': 'DESCRIÇÃO EVENTO'},
                                                           'width': '300px',
                                                           'text-align': 'left'
                                                           #     ,
                                                           # 'if': {'column_id': 'Nº GUIA'},
                                                           #     'width': '100px',
                                                           #     'text-align': 'right',
                                                       },
                                                   ],
                                                   #    style_as_list_view=True,
                                                   style_header={
                                                       'backgroundColor': 'rgba(102, 102, 255, 0.2)',
                                                       'font-weight': 'bold',
                                                       'text-align': 'center',
                                                       'height': 35
                                                   },
                                                   export_format="xlsx",),],
                    # style={
                    # 'border-style': 'solid',
                    # 'border-color': 'coral'
                    # },
                    lg=8),
        ],
        align="left", className="g-0"
    )
]
)


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value')])
def update_graph(select_class):

    df_scatter_filt = df_scatter[df_scatter['DESC_CLASSE'] == select_class]

    k1 = df_scatter_filt['X'].unique()[0]
    k2 = df_scatter_filt['Y'].unique()[0]
    ax_max = df_scatter_filt['ax_max'].unique()[0]
    ax_min = df_scatter_filt['ax_min'].unique()[0]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=[k1, k1, ax_max, ax_max], y=[k2, ax_max, ax_max, k2],
                             mode='markers',
                             marker=dict(size=1),
                             fill='tozeroy',
                             fillcolor='rgba(255, 0, 0, 0.2)',
                             hoverinfo='skip',
                             )
                  )

    fig.add_trace(go.Scatter(x=[ax_min, ax_min, k1, k1], y=[k2, ax_max, ax_max, k2],
                             mode='markers',
                             marker=dict(size=1),
                             fill='tozeroy',
                             fillcolor='rgba(255, 255, 0, 0.2)',
                             hoverinfo='skip')
                  )

    fig.add_trace(go.Scatter(x=[k1, ax_max, ax_max, k1], y=[k2, k2, ax_min, ax_min],
                             mode='markers',
                             marker=dict(size=1),
                             fill='tozeroy',
                             fillcolor='rgba(255, 255, 0, 0.2)',
                             hoverinfo='skip')
                  )

    fig.add_vline(x=k1, line_width=2, line_dash="dot", line_color="grey")
    fig.add_hline(y=k2, line_width=2, line_dash="dot", line_color="grey")

    df_c = df_scatter_filt.sort_values(['labels', 'dist'], ascending=[True, False]).groupby(
        'labels').head(1).reset_index(drop=True)

    x0 = []
    y0 = []
    x1 = []
    y1 = []
    dv = 0.2

    for x, y, d in zip(list(df_c['Centroids_X']), list(df_c['Centroids_Y']), list(df_c['dist'])):
        x0.append(x - d - dv)
        y0.append(y - d - dv)
        x1.append(x + d + dv)
        y1.append(y + d + dv)

    for c in range(len(x0)):
        if list(df_c['dist'])[c] > 0:
            fig.add_trace(go.Scatter(x=[list(df_c['Centroids_X'])[c]], y=[list(df_c['Centroids_Y'])[c]],
                                     mode='markers',
                                     marker_symbol=22,
                                     marker=dict(
                                         size=8, color='rgba(0, 0, 255, 0.4)'),
                                     hoverinfo='skip'
                                     )
                          )
        fig.add_shape(type="circle",
                      x0=x0[c], y0=y0[c], x1=x1[c], y1=y1[c],
                      line_color="rgba(0, 0, 0, 0.1)",
                      fillcolor='rgba(0, 0, 0, 0.05)'
                      )

    fig.add_trace(go.Scatter(x=df_scatter_filt['FREQ_Z_x'],
                             y=df_scatter_filt['VMU_Z_x'],
                             # text=list(df_indices_anual['NOME_PREST'][df_indices_anual['DESC_CLASSE']
                             #                                                      == cl_df['DESC_CLASSE'].iloc[select_class]]),
                             # textposition='top right',
                             # textfont=dict(color='#E58606'),
                             mode='markers',
                             marker=dict(size=10, color=df_scatter_filt['labels'].astype(
                                 float), line=dict(color='black', width=1)),
                             #  marker=dict(size=6, line=dict(color='black', width=1)),
                             hovertemplate='<b>' + \
                             df_scatter_filt['NOME_RESUMIDO'] + \
                             '</b>' + '<extra></extra>'
                             )
                  )

    fig.update_layout(
        # title_text='<b>Classe: ' + select_class +
        # '<br>(valores normalizados)</b>',
        titlefont=dict(size=20, color='black'),
        title_x=0.5,
        margin=dict(l=30, r=30, t=30, b=30),
        height=400,
        width=400,
        plot_bgcolor='whitesmoke',
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="tomato",
            font_size=12,
            namelength=0
        ),
        showlegend=False,
        yaxis=dict(
            title_text="<b>Média Valor Unitário</b>",
            titlefont=dict(size=18, color='black'),
            dtick=1,
            range=[ax_min, ax_max],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=3,
            linecolor='black'
        ),
        xaxis=dict(
            title_text="<b>Frequência / Beneficiário</b>",
            titlefont=dict(size=18, color='black'),
            dtick=1,
            range=[ax_min, ax_max],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=3,
            linecolor='black'
        )
    )

    # config = {'displayModeBar': False}

    # return fig.show(config=config)

    return fig

list_color = [["STA HELENA (D'OR)", 'rgb(209,187,215)'],
              ['MARIA AUXILIADORA', 'rgb(174,118,163)'],
              ['HOSP DO CORACAO', 'rgb(136,46,114)'],
              ['ANCHIETA', 'rgb(25,101,176)'],
              ['MAT BRASILIA', 'rgb(82,137,199)'],
              ['PRONTONORTE', 'rgb(123,175,222)'],
              ['DF STAR', 'rgb(78,178,101)'],
              ['STA LUCIA', 'rgb(144,201,135)'],
              ['DAHER', 'rgb(202,224,171)'],
              ['SIRIO LIBANES', 'rgb(247,240,86)'],
              ['STA LUZIA', 'rgb(246,193,65)'],
              ['HOME', 'rgb(241,147,45)'],
              ['BRASILIA', 'rgb(232,96,28)'],
              ['AGUAS CLARAS', 'rgb(220,5,12)']]

@app.callback(
    Output('metrica_graph', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('metrica', 'value')])
def update_graph_2(classe, metrica):

    met_freq = pd.read_csv(
        'https://raw.githubusercontent.com/helderhey/prestadores_pa/main/FREQUENCIA_EVENTO_MES.csv', sep="@", low_memory=False)

    met_vmu_benef = pd.read_csv(
        'https://raw.githubusercontent.com/helderhey/prestadores_pa/main/VMU_BENEF_MES.csv', sep="@", low_memory=False)

    met_vmu = pd.read_csv(
        'https://raw.githubusercontent.com/helderhey/prestadores_pa/main/VMU_MES.csv', sep="@", low_memory=False)

    # select_metrica = pd.read_csv(
    #     f'C:/Users/helde/OneDrive/Trabalho/DIACO/HOSPITAIS/Projeto Final/dados/{metrica}.csv', sep="@", low_memory=False)

    if metrica == 'VMU_MES':
        select_metrica = met_vmu
    elif metrica == 'FREQUENCIA_EVENTO_MES':
        select_metrica = met_freq
    elif metrica == 'VMU_BENEF_MES':
        select_metrica = met_vmu_benef

    prest_df = select_prest_data

    df_f_filt = select_metrica[select_metrica['DESC_CLASSE'] == classe]

    dict_text = {'VMU_MES': 'Valor Médio Unitário p/ Evento',
                 'FREQUENCIA_EVENTO_MES': 'Frequência Eventos p/ Beneficiário',
                 'VMU_BENEF_MES': 'Valor Médio Unitário p/ Beneficiário'}

    fig = go.Figure()

    for select_prest in range(prest_df.size):

        df_indices_prest = df_f_filt[['NOME_RESUMIDO', 'MES_ANO', metrica]][df_f_filt['NOME_RESUMIDO']
                                                                            == prest_df['NOME_RESUMIDO'].iloc[select_prest]].sort_values('MES_ANO')

        if df_indices_prest.size > 0:

            fig.add_trace(go.Scatter(x=df_indices_prest['MES_ANO'],
                                     y=df_indices_prest[metrica],
                                     marker=dict(size=20, color=list_color[select_prest][1], line=dict(
                                         color='black', width=1)),
                                     name="<b>" +
                                     df_indices_prest['NOME_RESUMIDO'].unique()[
                0] + "</b>",
                mode='markers', hovertemplate="<b>" + df_indices_prest['NOME_RESUMIDO'] + "</b><extra></extra><br>" +
                "<b>Qtde.: " +
                df_indices_prest[metrica].map(
                                         '{:.1f}'.format).astype(str) + "</b>"
            )
            )

            fig.update_layout(
                # title_text='<b>' + dict_text[metrica] + ' - Classe: ' + select_class,
                titlefont=dict(size=20, color='black'),
                title_x=0.5,
                margin=dict(l=20, r=20, t=30, b=30),
                height=420,
                width=900,
                plot_bgcolor='rgba(145, 181, 255, 0.4)',
                hovermode='closest',
                hoverlabel=dict(
                    bgcolor='rgb(145, 181, 255)',
                    font_size=12,
                    namelength=0
                ),
                legend=dict(font=dict(family="Arial Narrow",
                            size=12, color="black")),
                legend_title_text='<b>Prestador</b>',
                legend_title=dict(
                    font=dict(family="Arial Narrow", size=15, color="black")),
                yaxis=dict(
                    tickprefix="<b>",
                    ticksuffix="</b><br>",
                    gridwidth=3,
                    zeroline=False,
                    showline=True,
                    linewidth=2,
                    mirror=True,
                    linecolor='grey',
                    rangemode='tozero'
                ),
                xaxis=dict(
                    color='black',
                    tickmode='array',
                    # tickvals=list(np.datetime_as_string(
                    #     df_f_filt['MES_ANO'].sort_values().unique(), unit='D')),
                    tickvals=list(df_f_filt['MES_ANO'].sort_values().unique()),
                    ticktext=['<b>Jul<br>2022</b>', '<b>Ago<br>2022</b>', '<b>Set<br>2022</b>', '<b>Out<br>2022</b>',
                              '<b>Nov<br>2022</b>', '<b>Dez<br>2022</b>', '<b>Jan<br>2023</b>', '<b>Fev<br>2023</b>',
                              '<b>Mar<br>2023</b>', '<b>Abr<br>2023</b>', '<b>Mai<br>2023</b>', '<b>Jun<br>2023</b>'],
                    showgrid=False,
                    zeroline=False,
                    showline=True,
                    linewidth=2,
                    mirror=True,
                    linecolor='grey'
                )
            )

            fig.update_xaxes(showspikes=True)
            fig.update_yaxes(showspikes=True)

    # config = {'displayModeBar': False}

    # return fig.show(config=config)

    return fig


@app.callback(
    [Output("table", "data"), Output('table', 'columns')],
    [Input('xaxis-column', 'value'),
     Input('prest-column', 'value'),
     Input('mes_ano', 'value')])
def update_table(classe, prestador, mes_ano):
    table = table_data[(table_data['DESC_CLASSE'] == classe) & (table_data['MES_ANO'] == mes_ano) & (
        table_data['NOME_RESUMIDO'] == prestador)].sort_values(['NUM_PEG', 'NUM_GUIA'], ascending=[True, True])
    table.drop(columns=['NOME_RESUMIDO', 'MES_ANO',
               'DESC_CLASSE'], inplace=True)
    table.rename(columns={'NUM_PEG': 'Nº PEG',
                          'NUM_GUIA': 'Nº GUIA',
                          'MES_ANO': 'MÊS/ANO',
                          'DESC_TGE': 'DESCRIÇÃO EVENTO',
                          'NOME_RESUMIDO': 'PRESTADOR',
                          'VALOR_PAGO': 'VALOR PAGO',
                          'VALOR_UNIT': 'VALOR UNITÁRIO'}, inplace=True)
    # table["Nº PEG"] = table['Nº PEG'].map("{:.0f}".format)
    # table["VALOR PAGO"] = table['VALOR PAGO'].map("{:.2f}".format).astype(str).str.replace('.', ',')
    # table["VALOR UNITÁRIO"] = table['VALOR UNITÁRIO'].map("{:.2f}".format).astype(str).str.replace('.', ',')
    # table["VALOR PAGO"] = table['VALOR PAGO'].round(2)
    # table["VALOR UNITÁRIO"] = table['VALOR UNITÁRIO'].round(2)
    tab_dict = table.to_dict('records'), [
        {"name": i, "id": i} for i in table.columns]
    return tab_dict


if __name__ == '__main__':
    app.run_server(debug=True)
