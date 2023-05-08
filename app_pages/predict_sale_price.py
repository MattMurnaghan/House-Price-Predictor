import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.manage_files import load_clean_data, load_pkl_file
from src.pipeline_performance import regression_performance
from src.pipeline_performance import regression_plots


def predict_sale_price_body():

    # load sale price pipeline files
    version = 'v1'
    path = f"outputs/pipelines/predict_saleprice/{version}"
    sale_price_pipeline = load_pkl_file(f"{path}/best_regressor_pipeline.pkl")
    feature_importance = pd.read_csv(f"{path}/feature_importance.csv")
    feature_importance_plot = plt.imread(f"{path}/feature_importance.png")
    X_train = pd.read_csv(f"{path}/X_train.csv")
    X_test = pd.read_csv(f"{path}/X_test.csv")
    y_train = pd.read_csv(f"{path}/y_train.csv")
    y_test = pd.read_csv(f"{path}/y_test.csv")

    st.write("### ML Pipeline: Predict House Sale Price")
    # display pipeline training summary conclusions
    st.warning(
        f"The Regressor Model employed in this prediction is the RandomForrest Regressor.\n"
        f"* Both feature selection and PCA produced similar results and meet "
        f"business requirement 1.\n"
        f"* Feature selection achieved an R2 Score: 0.861 on the train set and "
        f"0.836 on the test set.\n"
        f"* The Client has required an R2 Score of 0.75+.\n"
        )
    st.write("---")

    # show pipeline steps
    st.write("### ML pipeline to predict sale price")
    st.info(sale_price_pipeline)
    st.write("---")

    # show best features
    st.write("### The features used to train the model and their importance:")
    cnt = 0
    for feat_str in feature_importance['Feature'].sort_values():
        if cnt == 0:
            new_str = feat_str
            cnt = 1
        else:
            new_str = new_str + ', ' + feat_str

    st.write(new_str)
    st.image(feature_importance_plot)
    st.write("---")

    # evaluate pipeline performance
    st.write("### Evaluating the Pipeline Performance.")
    regression_performance(X_train, y_train, X_test, y_test, sale_price_pipeline)
    regression_plots = plt.imread(f"{path}/regression_evaluation_plots.png")
    st.image(sale_price_pipeline)
    st.write("---")