# IMPORTS

import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
import plotly.figure_factory as ff
import dash
import plotly.graph_objs as go


# HELPER FUNCTIONS

def create_dash_app():
    app = dash.Dash()
    server = app.server  # just for deployment, not needed locally
    return app, server

def load_data(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df

def prepare_data(df):
    # Based on the column "age", create a new column "ageGroup" with the following bins
    bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ["0-18", "19-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
    return df

def create_filter_options(df):
    sex_options = ["All"] + list(df["sex"].unique())
    age_options = ["All"] + list(df["age_group"].unique())
    model_options = ["All"] + list(df["model_version"].unique())
    month_options = pd.date_range('2022-07', '2023-02', freq='MS').strftime("%B %Y")
    run_id_options = ["All"] + list(df["run_id"].unique())
    site_options = ["All"] + list(df["site"].unique())
    op_type_options = ["All"] + list(df["op_type"].unique())

    return sex_options, age_options, model_options, month_options, run_id_options, site_options, op_type_options

def calculate_average_shap_values(df):
    shap_columns = [col for col in df.columns if col.startswith("SHAP_")]
    avg_shap_values = df[shap_columns].mean()
    sorted_shap_values = avg_shap_values.sort_values(ascending=False)[:5]
    return sorted_shap_values

def filter_df(df, sex, age, model, start_month, end_month, run_id, site, op_type):
    filtered_df = df.copy()
    if sex != "All":
        filtered_df = filtered_df[filtered_df["sex"] == sex]
    if age != "All":
        filtered_df = filtered_df[filtered_df["age_group"] == age]
    if model != "All":
        filtered_df = filtered_df[filtered_df["model_version"] == model]
    if run_id != "All":
        filtered_df = filtered_df[filtered_df["run_id"] == run_id]
    if site != "All":
        filtered_df = filtered_df[filtered_df["site"] == site]
    if op_type != "All":
        filtered_df = filtered_df[filtered_df["op_type"] == op_type]

    filtered_df["date"] = pd.to_datetime(filtered_df["date"])

    filtered_df = filtered_df[(filtered_df["date"] >= start_month) & (filtered_df["date"] <= end_month)]

    return filtered_df

def auroc_if_possible(x):
        if len(x['outcome'].unique()) < 2:
            return None  # Placeholder value when the ROC AUC score is not defined
        else:
            return roc_auc_score(x['outcome'], x['pred_prob'])

def sensitivity_specificity_if_possible(x, threshold=0.075):
    if len(x['outcome'].unique()) < 2:
        return pd.Series({"sensitivity": None, "specificity": None})
    else:
        tn, fp, fn, tp = confusion_matrix(x['outcome'], x['pred_prob'] > threshold).ravel()
        sensitivity = tp / (tp + fn)
        specificity = tn / (tn + fp)
        return pd.Series({"sensitivity": sensitivity, "specificity": specificity})


def calculate_metrics(filtered_df, cutoff_threshold):
    # Calculate average fraction of complications
    avg_complications = filtered_df["outcome"].mean()

    # Check if there is only one unique class in the outcome column
    if len(filtered_df["outcome"].unique()) < 2:
        auroc = -1  # Placeholder value when the ROC AUC score is not defined
    else:
        # Calculate AUROC
        auroc = roc_auc_score(filtered_df["outcome"], filtered_df["pred_prob"])

    # Calculate monthly AUROC values
    filtered_df['month'] = filtered_df['date'].dt.to_period('M')
    monthly_auroc = filtered_df.groupby('month').apply(auroc_if_possible)

    monthly_sensitivity_specificity = filtered_df.groupby('month').apply(sensitivity_specificity_if_possible, threshold=cutoff_threshold)

    return avg_complications, auroc, monthly_auroc, monthly_sensitivity_specificity

def create_records_figure(filtered_df):
    fontsize_title = 20
    fontsize_label = 40

    records_figure = go.Figure(go.Indicator(
        mode="number",
        value=len(filtered_df),
        number={"valueformat": ",.0f", "font": {"size": fontsize_label}},
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Records", "font": {"size": fontsize_title}},
    ))
    records_figure.update_layout(
        height=200,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return records_figure


def create_complications_figure(avg_complications):
    fontsize_title = 20
    fontsize_label = 40

    complications_figure = go.Figure(go.Indicator(
        mode="number",
        value=avg_complications * 100,
        number={"valueformat": ".1f", "suffix": "%", "font": {"size": fontsize_label}},
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Rate of Complications", "font": {"size": fontsize_title}},
    ))
    complications_figure.update_layout(
        height=200,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return complications_figure


def create_auroc_figure(auroc):
    fontsize_title = 20
    fontsize_label = 40

    auroc_figure = go.Figure(go.Indicator(
        mode="number",
        value=auroc,
        number={"valueformat": ".2f", "font": {"size": fontsize_label}},
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "AUROC", "font": {"size": fontsize_title}},
    ))
    auroc_figure.update_layout(
        height=200,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    if pd.isna(auroc):
        auroc_figure.add_annotation(
            text="N/A",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=fontsize_label)
        )
    return auroc_figure


def create_timeline_figure(monthly_auroc, monthly_sensitivity_specificity, selected_metrics):
    timeline_figure = go.Figure()

    if "auroc" in selected_metrics:
        timeline_figure.add_trace(go.Scatter(
            x=monthly_auroc.index.to_timestamp(),
            y=monthly_auroc.values,
            mode='lines+markers',
            name="AUROC",
        ))

    if "sensitivity" in selected_metrics:
        timeline_figure.add_trace(go.Scatter(
            x=monthly_sensitivity_specificity.index.to_timestamp(),
            y=monthly_sensitivity_specificity['sensitivity'].values,
            mode='lines+markers',
            name="Sensitivity",
        ))

    if "specificity" in selected_metrics:
        timeline_figure.add_trace(go.Scatter(
            x=monthly_sensitivity_specificity.index.to_timestamp(),
            y=monthly_sensitivity_specificity['specificity'].values,
            mode='lines+markers',
            name="Specificity",
        ))

    timeline_figure.update_layout(
        xaxis={"title": "Date", 'fixedrange': True},
        yaxis={"title": "Metrics", 'fixedrange': True, 'range': [0, 1]},
        showlegend=True,
        legend=dict(x=0, y=1.2, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,255)', orientation='h'),
        paper_bgcolor='rgba(0,0,0,0)' 
    )
    return timeline_figure


def create_shap_barplot(filtered_df):
    # Calculate average SHAP values for each feature
    shap_columns = [col for col in filtered_df.columns if col.startswith("SHAP_")]
    shap_values = filtered_df[shap_columns].mean().sort_values(ascending=False)
    top_shap_values = shap_values.head(5)

    # Create SHAP bar plot
    shap_barplot = go.Figure(go.Bar(
        x=top_shap_values.index.str.replace("SHAP_", ""),
        y=top_shap_values.values
    ))

    shap_barplot.update_layout(
        xaxis={"title": "Feature"},
        yaxis={"title": "Average SHAP value"},
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)'  
    )

    return shap_barplot

def create_confusion_matrix(filtered_df, cutoff_threshold):
    y_true = filtered_df['outcome']
    y_pred = (filtered_df['pred_prob'] >= cutoff_threshold).astype(int)

    cm = confusion_matrix(y_true, y_pred)
    cm_plot = ff.create_annotated_heatmap(
        z=cm,
        x=['Predicted low risk', 'Predicted high risk'],
        y=['Successful surgery', 'Complication'],
        colorscale='Blues',
        showscale=True,
    )

    cm_plot.update_layout(
        title=f'Confusion Matrix (Threshold: {cutoff_threshold:.3f})',
        xaxis={"title": "Predicted Value"},
        yaxis={"title": "Actual Value", "autorange": "reversed"},
        paper_bgcolor='rgba(0,0,0,0)' 
    )

    return cm_plot