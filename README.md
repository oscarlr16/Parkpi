# ParkPi

A distributed parking access control system demonstrating MQTT-based communication between multiple components. This project showcases how different programs and devices can be integrated through a message broker to create a cohesive IoT solution.

## Overview

ParkPi implements an automated parking gate system that uses QR codes for access control. The system consists of three main components that communicate via MQTT protocol:

- **Camera Worker**: Captures and processes QR codes from vehicle access attempts
- **Access Server**: Manages user authentication and access decisions
- **Gate Controller**: Controls the physical barrier based on access decisions

## System Architecture

The system follows a microservices architecture where each component operates independently and communicates through MQTT topics:

```
[Camera] --QR--> [MQTT Broker] --Decision--> [Gate Controller]
                      |
                 [Access Server]
                 (Web Interface)
```

### MQTT Topics

- `access/requests`: QR codes detected by the camera
- `access/decisions`: Access control decisions
- `gate/cmd`: Commands to open/close the gate
- `gate/status`: Current gate status
- `vehicle/detected`: Vehicle presence detection

## Components

### Access Server (`access_server/`)

A Flask web application that serves as the central control unit:

- **User Management**: Web interface for adding/removing authorized users
- **Access Control**: Validates QR codes against the user database
- **Logging**: Records all access attempts with timestamps and decisions
- **MQTT Integration**: Listens for access requests and publishes gate commands

### Camera Worker (`camera_worker/`)

A computer vision component that handles QR code detection:

- **Video Capture**: Uses OpenCV to capture video from connected cameras
- **QR Detection**: Processes frames to detect and decode QR codes
- **Deduplication**: Prevents multiple publications of the same QR code
- **MQTT Publishing**: Sends detected codes to the access control system

### Gate Controller (`gate_controller/`)

An ESP32-based hardware controller for the physical gate:

- **WiFi Connectivity**: Connects to the local network
- **MQTT Communication**: Subscribes to gate commands
- **Gate Control**: Simulates barrier operation using built-in LED
- **Status Reporting**: Publishes gate status updates
- **Vehicle Detection**: Uses button input to simulate vehicle presence

## Tech Stack

- **Backend**: Flask, SQLAlchemy, SQLite
- **Computer Vision**: OpenCV, pyzbar
- **Hardware**: ESP32, PlatformIO
- **Communication**: MQTT (Paho client)
- **Frontend**: HTML, Jinja2

## Purpose

Educational project demonstrating:
- MQTT protocol integration
- Microservices architecture
- IoT system design
- Hardware-software integration
- Real-time image processing
