from dash import dcc
from dash import html

def create_header():
    return html.H1(
        children="NHS OpenPredictor Model Monitoring",
        style={
            "textAlign": "center",
            "backgroundColor": "#005EB8",  # NHS blue
            "color": "white",
            "padding": "7px",  # Add padding for better appearance
        },
    )

def create_sidebar(month_options, sex_options, age_options, site_options, op_type_options, model_options, run_id_options):
    return html.Div(
        [
            html.H4("Timeframe", style={"padding-bottom": "10px"}),
            html.Label("Start Month"),
            dcc.Dropdown(
                id="start-month-dropdown",
                clearable=False,
                options=[{"label": month, "value": month} for month in month_options],
                value=month_options[0],
            ),
            html.Label("End Month"),
            dcc.Dropdown(
                id="end-month-dropdown",
                clearable=False,
                options=[{"label": month, "value": month} for month in month_options],
                value=month_options[-1],
            ),
            html.Div(style={"height": "20px"}),
            html.H4("Filters", style={"padding-bottom": "10px"}),
            html.Label("Sex"),
            dcc.Dropdown(
                id="sex-dropdown",
                clearable=False,
                options=[{"label": sex, "value": sex} for sex in sex_options],
                value="All",
            ),
            html.Label("Age Group"),
            dcc.Dropdown(
                id="age-dropdown",
                clearable=False,
                options=[{"label": age, "value": age} for age in age_options],
                value="All",
            ),
            html.Div(style={"height": "40px"}),
            html.Label("Site"),
            dcc.Dropdown(
                id="site-dropdown",
                clearable=False,
                options=[{"label": site, "value": site} for site in site_options],
                value="All",
            ),
            html.Label("Operation Type"),
            dcc.Dropdown(
                id="op-type-dropdown",
                clearable=False,
                options=[{"label": op_type, "value": op_type} for op_type in op_type_options],
                value="All",
            ),
            html.Div(style={"height": "40px"}),
            html.Label("Model Version"),
            dcc.Dropdown(
                id="model-dropdown",
                clearable=False,
                options=[{"label": model, "value": model} for model in model_options],
                value="All",
            ),
            html.Label("Run ID"),
            dcc.Dropdown(
                id="run-id-dropdown",
                clearable=False,
                options=[{"label": run_id, "value": run_id} for run_id in run_id_options],
                value="All",
            ),
        ],
        style={
            "width": "20%",
            "display": "inline-block",
            "vertical-align": "top",
            "padding-left": "20px",
            "padding-right": "20px",
        },
    )


def create_overview_tab():
    return dcc.Tab(
        label="Overview",
        children=[
            html.Div(
                [
                    dcc.Graph(
                        id="indicator-records",
                        config={"displayModeBar": False},
                    ),
                ],
                style={
                    "width": "30%",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin": "10px",
                },
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="indicator-complications",
                        config={"displayModeBar": False},
                    ),
                ],
                style={
                    "width": "30%",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin": "10px",
                },
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="indicator-auroc",
                        config={"displayModeBar": False},
                    ),
                ],
                style={
                    "width": "30%",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin": "10px",
                },
            ),
        ],
    )


# def create_performance_tab():
#     return dcc.Tab(
#         label="Performance",
#         children=[
#             html.Div(
#                 [
#                     html.Label("Cutoff Threshold: "),
#                     dcc.Slider(
#                         id="cutoff-slider-2",
#                         min=0,
#                         max=1,
#                         step=0.005,
#                         value=0.075,
#                         marks={i / 10: f"{i / 10:.1f}" for i in range(0, 11)},
#                     ),
#                 ],
#                 style={"width": "100%", "padding": "20px 20px 0px 20px"},
#             ),
#             html.Div(
#                 [
#                     dcc.Graph(
#                         id="timeline",
#                         config={"displayModeBar": False},
#                     ),
#                 ],
#                 style={
#                     "width": "100%",
#                     "display": "inline-block",
#                     "vertical-align": "top",
#                     "margin-top": "10px",
#                     "margin-bottom": "10px",
#                 },
#             ),
#         ],
#     )

# def create_performance_tab():
#     return dcc.Tab(
#         label="Performance",
#         children=[
#             html.Div(
#                 [
#                     html.Label("Cutoff Threshold: "),
#                     dcc.Slider(
#                         id="cutoff-slider-2",
#                         min=0,
#                         max=1,
#                         step=0.005,
#                         value=0.075,
#                         marks={i / 10: f"{i / 10:.1f}" for i in range(0, 11)},
#                     ),
#                 ],
#                 style={"width": "100%", "padding": "20px 20px 0px 20px"},
#             ),
#             html.Div(
#                 [
#                     html.Label("Select Metrics: "),
#                     dcc.Checklist(
#                         id="metrics-checkboxes",
#                         options=[
#                             {"label": "AUROC", "value": "auroc"},
#                             {"label": "Sensitivity", "value": "sensitivity"},
#                             {"label": "Specificity", "value": "specificity"},
#                         ],
#                         value=["auroc", "sensitivity", "specificity"],
#                     ),
#                 ],
#                 style={"width": "100%", "padding": "10px 20px 0px 20px"},
#             ),
#             html.Div(
#                 [
#                     dcc.Graph(
#                         id="timeline",
#                         config={"displayModeBar": False},
#                     ),
#                 ],
#                 style={
#                     "width": "100%",
#                     "display": "inline-block",
#                     "vertical-align": "top",
#                     "margin-top": "10px",
#                     "margin-bottom": "10px",
#                 },
#             ),
#         ],
#     )

def create_performance_tab():
    return dcc.Tab(
        label="Performance",
        children=[
            html.Div(
                [
                    html.Label("Cutoff Threshold: "),
                    dcc.Slider(
                        id="cutoff-slider-2",
                        min=0,
                        max=1,
                        step=0.005,
                        value=0.075,
                        marks={i / 10: f"{i / 10:.1f}" for i in range(0, 11)},
                    ),
                ],
                style={"width": "100%", "padding": "20px 20px 0px 20px"},
            ),
            html.Div(
                [   html.Label("Display metrics: "),
                    dcc.Checklist(
                        id="metrics-checkboxes",
                        options=[
                            {'label': 'AUROC', 'value': 'auroc'},
                            {'label': 'Sensitivity', 'value': 'sensitivity'},
                            {'label': 'Specificity', 'value': 'specificity'},
                        ],
                        value=['auroc', 'sensitivity', 'specificity'],
                        inline=True,
                        labelStyle={'display': 'inline-block', 'margin-left': '25px'}
                    ),
                ],
                style={
                    "width": "100%",
                    "padding": "20px 20px 0px 20px",
                    "display": "flex",
                    "justify-content": "center",
                },
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="timeline",
                        config={"displayModeBar": False},
                    ),
                ],
                style={
                    "width": "100%",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin-top": "10px",
                    "margin-bottom": "10px",
                },
            ),
        ],
    )



def create_explainability_tab():
    return dcc.Tab(
        label="Explainability",
        children=[
            html.Div(
                [
                    dcc.Graph(
                        id="shap-barplot",
                        config={"displayModeBar": False},
                    ),
                ],
                style={
                    "width": "100%",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin-top": "10px",
                    "margin-bottom": "10px",
                },
            ),
        ],
    )

def create_confusion_matrix_tab():
    return dcc.Tab(
        label="Confusion Matrix",
        children=[
            html.Div(
                [
                    html.Label("Cutoff Threshold: "),
                    dcc.Slider(
                        id="cutoff-slider",
                        min=0,
                        max=1,
                        step=0.005,
                        value=0.5,
                        marks={i / 10: f"{i / 10:.1f}" for i in range(0, 11)},
                    ),
                ],
                style={"width": "100%", "padding": "20px 20px 0px 20px"},
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="confusion-matrix",
                        config={"displayModeBar": False},
                    ),
                ],
                style={
                    "width": "100%",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin-top": "0px",
                    "margin-bottom": "10px",
                },
            ),
        ],
    )

def create_main_content():
    return html.Div(
        [
            dcc.Tabs(
                [
                    create_overview_tab(),
                    create_performance_tab(),
                    create_explainability_tab(),
                    create_confusion_matrix_tab(),
                ]
            )
        ]
    )

        

def create_layout(month_options, sex_options, age_options, site_options, op_type_options, model_options, run_id_options):
    layout = html.Div(
        [
            create_header(),
            html.Div(
                [
                    create_sidebar(month_options, sex_options, age_options, site_options, op_type_options, model_options, run_id_options),
                    html.Div(
                        create_main_content(),
                        style={
                            "width": "75%",
                            "display": "inline-block",
                            "vertical-align": "top",
                            "padding-left": "0px",
                            "padding-top": "0px",
                        },
                    ),
                ],
                style={
                    "width": "100%",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "padding-left": "0px",
                    "padding-top": "0px",
                },
            ),
        ]
    )
    return layout


