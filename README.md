# Real-Time Speech-to-Speech Voice Assistant

This project is a real-time speech-to-speech voice assistant built using OpenAI's Realtime API. The assistant listens to your voice input, sends it to OpenAI's API for processing, and plays back the response as audio output. It is designed to handle both text and audio responses, leveraging WebSockets to communicate with the OpenAI Realtime API for seamless voice interaction.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [OpenAI Realtime API Qualities](#openai-realtime-api-qualities)
- [Project Structure](#project-structure)
- [Logging and Debugging](#logging-and-debugging)
- [License](#license)

---

## Features
- **Voice Input**: Records your voice input in real-time.
- **Text and Audio Response**: Processes responses in both text and audio formats.
- **WebSocket Communication**: Utilizes OpenAI's WebSocket API for efficient and interactive communication.
- **Audio Playback**: Plays the audio response received from the assistant in real-time.
- **Customizable Models**: Allows the use of different OpenAI models via environment variable configuration.

---

## Requirements
- Python 3.10+
- **Libraries**:
  - `pyaudio`
  - `websockets`
  - `dotenv`
  - `poetry`
  - `wave`
  - `base64`
  - `json`
  - `logging`

Ensure you have these dependencies installed. If not, they will be installed automatically with `poetry`.

---

## Installation
1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install dependencies using `poetry`:
    ```bash
    poetry lock
    poetry install
    ```

3. Ensure `.env` file is configured (see [Environment Variables](#environment-variables) below).

---

## Usage
1. **Run the application**:
    ```bash
    python3 Speech2Speech.py
    ```
   
2. **Interaction**:
   - You will be prompted to start speaking. The assistant will record your voice input, process it, and respond in audio form.

---

## Environment Variables
Create a `.env` file in the project root with the following variables:

```env
WS_URL="<OpenAI_WebSocket_URL>"
MODEL="<OpenAI_Model_Name>"
OPENAI_API_KEY="<Your_OpenAI_API_Key>"
```

- **WS_URL**: WebSocket endpoint for the OpenAI Realtime API.
- **MODEL**: Name of the OpenAI model you intend to use.
- **OPENAI_API_KEY**: Your OpenAI API key to authenticate requests.

---

## OpenAI Realtime API Qualities

The OpenAI Realtime API provides powerful capabilities for building interactive, real-time applications. Key qualities include:

- **Low Latency**: Optimized for low-latency interactions, allowing near-instantaneous feedback for a smooth, conversational experience.
- **Streamed Responses**: Delivers responses as they are generated, enabling real-time feedback and dynamic interactions in text, audio, or combined formats.
- **Multi-Modal Responses**: Supports a mix of text and audio modalities, allowing the assistant to respond in a format best suited to the user’s needs.
- **Flexible Customization**: The API allows for dynamic instruction and model behavior changes, enabling more tailored interactions and enhanced user experience.
- **Efficient WebSocket Protocol**: Leveraging WebSocket technology, the Realtime API maintains a continuous, efficient connection for uninterrupted interaction.
- **Error Handling and Event Management**: The API includes structured error and event types to facilitate robust interaction management, making it easier to handle various response types and errors in real time.

---

## Project Structure

- **Speech2Speech.py**: Main script to run the assistant. Contains the `RealtimeClient` class which manages the WebSocket connection, audio recording, and playback.
- **Environment Configuration**: `.env` file holds sensitive keys and URLs.
- **Audio Functions**:
  - **start_audio_stream**: Initializes the audio stream for recording.
  - **record_audio**: Captures audio input for a specified duration.
  - **play_audio**: Plays back the audio response.

---

## Logging and Debugging
The application uses Python’s built-in `logging` module to capture detailed logs for debugging. Logging levels can be set in the script for more granular output:
- **INFO**: High-level events such as connection status and response types.
- **DEBUG**: Detailed information including data encoding, event processing, and buffer handling.


--- 

