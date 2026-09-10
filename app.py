# -*- coding: utf-8 -*-

import streamlit as st
import pickle
import numpy as np
import pandas as pd


# ==============================
# Load Model and Dataset
# ==============================

pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))


# ==============================
# Streamlit App
# ==============================

st.title("Laptop Predictor")


# ==============================
# Brand
# ==============================

company = st.selectbox(
    'Brand',
    df['Company'].unique()
)


# ==============================
# Laptop Type
# ==============================

type = st.selectbox(
    'Type',
    df['TypeName'].unique()
)


# ==============================
# RAM
# ==============================

ram = st.selectbox(
    'RAM(in GB)',
    [2, 4, 6, 8, 12, 16, 24, 32, 64]
)


# ==============================
# Weight
# ==============================

weight = st.number_input(
    'Weight of the Laptop',
    min_value=0.0,
    value=1.5,
    step=0.1
)


# ==============================
# Touchscreen
# ==============================

touchscreen = st.selectbox(
    'Touchscreen',
    ['No', 'Yes']
)


# ==============================
# IPS
# ==============================

ips = st.selectbox(
    'IPS',
    ['No', 'Yes']
)


# ==============================
# Screen Size
# ==============================

screen_size = st.slider(
    'Screen size in inches',
    10.0,
    18.0,
    13.0
)


# ==============================
# Screen Resolution
# ==============================

resolution = st.selectbox(
    'Screen Resolution',
    [
        '1920x1080',
        '1366x768',
        '1600x900',
        '3840x2160',
        '3200x1800',
        '2880x1800',
        '2560x1600',
        '2560x1440',
        '2304x1440'
    ]
)


# ==============================
# CPU
# ==============================

cpu = st.selectbox(
    'CPU',
    df['Cpu brand'].unique()
)


# ==============================
# HDD
# ==============================

hdd = st.selectbox(
    'HDD(in GB)',
    [0, 128, 256, 512, 1024, 2048]
)


# ==============================
# SSD
# ==============================

ssd = st.selectbox(
    'SSD(in GB)',
    [0, 8, 128, 256, 512, 1024]
)


# ==============================
# GPU
# ==============================

gpu = st.selectbox(
    'GPU',
    df['Gpu brand'].unique()
)


# ==============================
# Operating System
# ==============================

os = st.selectbox(
    'OS',
    df['os'].unique()
)


# ==============================
# Prediction
# ==============================

if st.button('Predict Price'):

    # Convert Yes/No into 1/0
    touchscreen_value = 1 if touchscreen == 'Yes' else 0
    ips_value = 1 if ips == 'Yes' else 0


    # ==========================
    # Calculate PPI
    # ==========================

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])

    ppi = (
        (X_res ** 2 + Y_res ** 2) ** 0.5
        / screen_size
    )


    # ==========================
    # Create Query DataFrame
    # ==========================

    query = pd.DataFrame(
        [[
            company,
            type,
            ram,
            weight,
            touchscreen_value,
            ips_value,
            ppi,
            cpu,
            hdd,
            ssd,
            gpu,
            os
        ]],
        columns=[
            'Company',
            'TypeName',
            'Ram',
            'Weight',
            'Touchscreen',
            'Ips',
            'ppi',
            'Cpu brand',
            'HDD',
            'SSD',
            'Gpu brand',
            'os'
        ]
    )


    # ==========================
    # Make Prediction
    # ==========================

    try:

        prediction = pipe.predict(query)[0]

        # Convert log prediction back to actual price
        price = int(np.exp(prediction))


        # ======================
        # Display Result
        # ======================

        st.success(
            f"The predicted price of this configuration is ₹ {price:,}"
        )

    except Exception as e:

        st.error("Prediction failed.")

        st.exception(e)


