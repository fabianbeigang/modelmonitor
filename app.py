## IMPORTS

import os
from datetime import datetime

from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
import dash

from layout import create_layout
from helpers import (
    create_dash_app,
    load_data,
    prepare_data,
    create_filter_options,
    calculate_average_shap_values,
    filter_df,
    calculate_metrics,
    create_records_figure,
    create_complications_figure,
    create_auroc_figure,
    create_timeline_figure,
    create_shap_barplot,
    create_confusion_matrix
)


## SETUP

# Create Dash app
app, server = create_dash_app()

# Load and prepare data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(BASE_DIR, 'sample_data_0504.csv')
df = load_data(csv_file_path)
df = prepare_data(df)

# Create filter options
sex_options, age_options, model_options, month_options, run_id_options, site_options, op_type_options = create_filter_options(df)

# Calculate average SHAP values
sorted_shap_values = calculate_average_shap_values(df)


## LAYOUT
app.layout = create_layout(month_options, sex_options, age_options, site_options, op_type_options, model_options, run_id_options)


## CALLBACK FUNCTION

@app.callback(
    [dash.dependencies.Output("indicator-records", "figure"),
     dash.dependencies.Output("indicator-complications", "figure"),
     dash.dependencies.Output("indicator-auroc", "figure"),
     dash.dependencies.Output("timeline", "figure"),
     dash.dependencies.Output("shap-barplot", "figure"),
     dash.dependencies.Output("confusion-matrix", "figure")], 
    [dash.dependencies.Input("sex-dropdown", "value"),
     dash.dependencies.Input("age-dropdown", "value"),
     dash.dependencies.Input("model-dropdown", "value"),
     dash.dependencies.Input("start-month-dropdown", "value"),
     dash.dependencies.Input("end-month-dropdown", "value"),
     dash.dependencies.Input("run-id-dropdown", "value"),
     dash.dependencies.Input("site-dropdown", "value"),
     dash.dependencies.Input("op-type-dropdown", "value"),
     dash.dependencies.Input("cutoff-slider", "value"),
     dash.dependencies.Input("cutoff-slider-2", "value"),
     dash.dependencies.Input("metrics-checkboxes", "value")])

def update_graph(sex, age, model, start_month, end_month, run_id, site, op_type, cutoff_threshold_cm, cutoff_threshold_timeline, selected_metrics):
    if datetime.strptime(start_month, "%B %Y") > datetime.strptime(end_month, "%B %Y"):
        return dash.no_update, dcc.alert(
            "Start month must be smaller or equal to end month",
            id="month-range-alert",
            color="danger",
            style={"display": "block"}
        )

    filtered_df = filter_df(df, sex, age, model, start_month, end_month, run_id, site, op_type)
    avg_complications, auroc, monthly_auroc, monthly_sensitivity_specificity = calculate_metrics(filtered_df, cutoff_threshold_timeline)

    records_figure = create_records_figure(filtered_df)
    complications_figure = create_complications_figure(avg_complications)
    auroc_figure = create_auroc_figure(auroc)
    timeline_figure = create_timeline_figure(monthly_auroc, monthly_sensitivity_specificity, selected_metrics)
    shap_barplot = create_shap_barplot(filtered_df)
    confusion_matrix_figure = create_confusion_matrix(filtered_df, cutoff_threshold_cm)

    return records_figure, complications_figure, auroc_figure, timeline_figure, shap_barplot, confusion_matrix_figure



## START APP

# if __name__ == '__main__':
#     app.run_server(debug=False)

# Create Dash app
app = dash.Dash(__name__)

# For Gunicorn to run the app correctly
server = app.server


       