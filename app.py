import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import random

st.set_page_config(page_title="AeroTelemetry Ground Station", layout="wide", page_icon="🚁")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

if 'flight_data' not in st.session_state:
    st.session_state.flight_data = pd.DataFrame(columns=['Time', 'Roll', 'Pitch', 'G-Force', 'Alt'])

st.sidebar.title("🎮 Ground Station Control")
logging_rate = st.sidebar.select_slider("Sampling Rate (Hz)", options=[10, 20, 50], value=20)
is_recording = st.sidebar.toggle("Start Blackbox Recording")
if st.sidebar.button("Reset IMU Calibration"):
    st.session_state.flight_data = pd.DataFrame(columns=['Time', 'Roll', 'Pitch', 'G-Force', 'Alt'])

st.title("🚁 UAV Flight Telemetry - Ground Station")
st.write("Live Telemetry Stream | Controller: RPi Pico | Protocol: UART-Serial")

placeholder = st.empty()

for i in range(100):
    roll = round(np.sin(i/10) * 15 + np.random.normal(0, 0.8), 2)
    pitch = round(np.cos(i/12) * 10 + np.random.normal(0, 0.8), 2)
    g_force = round(1.0 + abs(np.random.normal(0, 0.15)), 2)
    alt = round(120.5 + (i * 0.4), 1)
    
    new_row = pd.DataFrame([[datetime.now().strftime("%H:%M:%S.%f")[:-3], roll, pitch, g_force, alt]], 
                            columns=st.session_state.flight_data.columns)
    st.session_state.flight_data = pd.concat([st.session_state.flight_data, new_row]).tail(40)

    with placeholder.container():
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Roll Angle", f"{roll}°")
        m2.metric("Pitch Angle", f"{pitch}°")
        m3.metric("G-Load", f"{g_force} G")
        m4.metric("Altitude", f"{alt} m")

        c_left, c_right = st.columns([1, 2])
        
        with c_left:
            st.subheader("Artificial Horizon")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = roll,
                title = {'text': "Roll Stability"},
                gauge = {'axis': {'range': [-90, 90]}, 'bar': {'color': "#3498db"},
                         'steps': [{'range': [-90, -30], 'color': "red"}, {'range': [30, 90], 'color': "red"}]}
            ))
            fig_gauge.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with c_right:
            st.subheader("Attitude Stability Trend")
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(x=st.session_state.flight_data['Time'], 
                                           y=st.session_state.flight_data['Roll'], name="Roll", line_color="#3498db"))
            fig_trend.add_trace(go.Scatter(x=st.session_state.flight_data['Time'], 
                                           y=st.session_state.flight_data['Pitch'], name="Pitch", line_color="#e67e22"))
            fig_trend.update_layout(template="plotly_dark", height=300,
                                     paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_trend, use_container_width=True)

        st.divider()
        st.subheader("📋 Flight Blackbox Data")
        st.dataframe(st.session_state.flight_data, use_container_width=True)
        
        st.caption("Incoming Packet Frame:")
        st.code(f"RAW_UART >> R:{roll}|P:{pitch}|G:{g_force}|A:{alt}|CRC:{random.randint(100,999)}")

    time.sleep(1/logging_rate)
