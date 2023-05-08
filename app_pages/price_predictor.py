'''
This file's contents were taken from the
 Churnometer walk through Project 2 and customized for
 this project
'''
import streamlit as st
import pandas as pd
from src.manage_files import load_clean_data, load_pkl_file
from src.predictive_analysis_ui import predict_sale_price


def price_predictor_body():

    # load predict sale price files
    version = 'v1'
    path = f"outputs/ml_pipeline/predict_saleprice/{version}"

    price_pipeline = load_pkl_file(f"{path}/best_regressor_pipeline.pkl")
    price_features = (pd.read_csv(f"{path}/X_train.csv")
                        .columns
                        .to_list()
                        )
    feature_importance = list(pd.read_csv
                                (f"{path}/feature_importance.csv")['Feature'])

    st.write("### Sale Price Prediction for the refurbished houses:")
    st.success(
        f"* The Client is interested in predicting the house sales price"
        f" for 6 newly refurbished houses, and any other house "
        f"in Ames, Iowa."
        )
    st.write("---")

    st.write("### Refurbished houses price prediction")
    st.info(
        f"* Below are the details of the refurbished "
        f"houses and their respective sale price predictions."
        )
    total_price = predict_refurbished_house_price(price_pipeline, price_features)
    total_price = "%.2f" % total_price
    st.success(
        f"The sum total sale price for all 6 refurbished "
        f"properties is \u0024{total_price}."
        )
    st.write("---")

    # Generate Live Data
    check = False
    if check:
        check_variables_for_UI(price_features)

    st.write("### Houses Price Predictor")
    st.warning(
        f"* Enter your values for the property for "
        f"which you require a **price prediction**.\n\n"
        f"Legend: \n\n"
        f"* 1stFlrSF - First Floor measured in square feet.\n"
        f"* GrLivArea - Above grade (ground) living area square feet.\n"
        f"* GarageArea - Size of garage in square feet.\n"
        f"* YearBuilt - Original construction date."
        )
    X_live = DrawInputsWidgets()

    # predict on live data
    if st.button("Run Predictive Analysis"):
        price_prediction = predict_sale_price(X_live,
                                              price_features,
                                              price_pipeline)
        # logic to display the sale price
        statement = (
            f"The predicted selling price for this house "
            f"is \u0024{price_prediction}"
            )

        st.success(statement)


def predict_refurbished_house_price(price_pipeline, price_features):
    refurbished = load_clean_data("refurbished")
    row_count = len(refurbished)
    refurbished.index = range(1, row_count+1)
    total_price = 0
    for x in range(row_count):
        X_live = refurbished.iloc[[x]]
        st.write(X_live)
        price_prediction = predict_sale_price(X_live,
                                              price_features,
                                              price_pipeline)
        price_prediction = "%.2f" % price_prediction
        statement = (
            f"* The predicted selling price for house "
            f"{x+1} is \u0024{price_prediction}"
            )
        total_price += float(price_prediction)
        st.write(statement)

    return total_price


def check_variables_for_UI(price_features):
    import itertools

    combined_features = set(
        list(
            itertools.chain(price_features)
            )
        )
    st.write(f"* There are {len(combined_features)} features "
             f"for the UI: \n\n {combined_features}")


def DrawInputsWidgets():

    # load dataset
    df = load_clean_data("clean")
    percentageMin, percentageMax = 0.4, 2.0

    # we create input widgets for all features
    col1, col2 = st.beta_columns(2)
    col3, col4 = st.beta_columns(2)

    # We are using these features to feed the ML pipeline
    # - values copied from check_variables_for_UI() result
    # 'OverallQual', 'GrLivArea', 'GarageArea', 'YearBuilt'

    # create an empty DataFrame, which will be the live data
    X_live = pd.DataFrame([], index=[0])

    # from here on we draw the widget based on the variable
    # type (numerical or categorical) and set initial values
    with col1:
        feature = "OverallQual"
        st_widget = st.number_input(
            label=feature,
            min_value=df[feature].min()*percentageMin,
            max_value=df[feature].max()*percentageMax,
            value=df[feature].median()
            )
        X_live[feature] = st_widget

    with col2:
        feature = "GrLivArea"
        st_widget = st.number_input(
            label=feature,
            min_value=df[feature].min()*percentageMin,
            max_value=df[feature].max()*percentageMax,
            value=df[feature].median()
            )
        X_live[feature] = st_widget

    with col3:
        feature = "GarageArea"
        st_widget = st.number_input(
            label=feature,
            min_value=df[feature].min()*percentageMin,
            max_value=df[feature].max()*percentageMax,
            value=df[feature].median()
            )
        X_live[feature] = st_widget

    with col4:
        feature = "YearBuilt"
        st_widget = st.number_input(
            label=feature,
            min_value=df[feature].min()*percentageMin,
            max_value=df[feature].max()*percentageMax,
            value=df[feature].median()
            )
        X_live[feature] = st_widget

    st.write(X_live)

    return X_live