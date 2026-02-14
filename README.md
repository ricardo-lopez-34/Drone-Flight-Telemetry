# Drone Flight Telemetry 🚁

A real-time flight data monitoring system that captures 6-axis motion dynamics and environmental telemetry for unmanned aerial vehicles (UAVs).

## Description
A flight data monitoring system capturing 6-axis motion dynamics and environmental telemetry for UAVs, visualized via a real-time analytics dashboard.

## Key Features
- **6-DOF Motion Tracking:** Real-time acquisition of Pitch, Roll, and Yaw using MPU6050.
- **Blackbox Logging:** High-speed data persistence for post-flight accident reconstruction.
- **Flight Stability Analytics:** Python-based visualization of vibration noise and tilt-compensation.

## Tech Stack
- **Language:** Python, C++
- **Libraries:** Streamlit, Plotly, Pandas, MPU6050-Lib
- **Model:** Complementary Filter Algorithm for sensor fusion

## Engineering Logic
- **Hardware:** The Raspberry Pi Pico uses I2C communication to sample the MPU6050 IMU at high frequencies.
- **Software:** Python implements a low-pass filter to remove engine vibration noise from the raw accelerometer data, providing a stable "Artificial Horizon" UI.
