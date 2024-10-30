import asyncio
import websockets
import json
import pyaudio
import wave
import base64
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000

# WebSocket configuration
WS_URL = os.getenv("WS_URL")
MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
"""
This important message is lost with all log information:
Enter 't' for text, 'a' for audio, or 'q' to quit:
"""

class RealtimeClient:
    def __init__(self):
        logger.info("Initializing RealtimeClient")
        self.ws = None
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.audio_buffer = b''

    async def connect(self):
        logger.info(f"Connecting to WebSocket: {WS_URL}")
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
        self.ws = await websockets.connect(f"{WS_URL}?model={MODEL}", extra_headers=headers)
        logger.info("Successfully connected to OpenAI Realtime API")

    async def send_event(self, event):
        logger.debug(f"Sending event: {event}")
        await self.ws.send(json.dumps(event))
        logger.debug("Event sent successfully")

    async def receive_events(self):
        logger.info("Starting to receive events")
        async for message in self.ws:
            logger.debug(f"Received raw message: {message}")
            event = json.loads(message)
            await self.handle_event(event)

    async def handle_event(self, event):
        event_type = event.get("type")
        logger.info(f"Handling event of type: {event_type}")

        if event_type == "error":
            logger.error(f"Error event received: {event['error']['message']}")
        elif event_type == "response.text.delta":
            logger.debug(f"Text delta received: {event['delta']}")
            print(event["delta"], end="", flush=True)
        elif event_type == "response.audio.delta":
            logger.debug(f"Audio delta received, length: {len(event['delta'])}")
            audio_data = base64.b64decode(event["delta"])
            self.audio_buffer += audio_data
        
        elif event_type == "response.audio.done":
            logger.info("Audio response complete, playing audio")
           
            self.play_audio(self.audio_buffer)
            self.audio_buffer = b''
        else:
            logger.info(f"Received other event type: {event_type}")


    def start_audio_stream(self):
        logger.info("Starting audio input stream")
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)
        logger.debug("Audio input stream started successfully")

    def stop_audio_stream(self):
        logger.info("Stopping audio input stream")
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        logger.debug("Audio input stream stopped successfully")

    def record_audio(self, duration):
        logger.info(f"Recording audio for {duration} seconds")
        frames = []
        for i in range(0, int(RATE / CHUNK * duration)):
            data = self.stream.read(CHUNK)
            frames.append(data)
            if i % 10 == 0:  # Log every 10th frame
                logger.debug(f"Recorded frame {i}")
        audio_data = b''.join(frames)
        logger.info(f"Audio recording complete, total size: {len(audio_data)} bytes")
        return audio_data

    def play_audio(self, audio_data):
        logger.info(f"Playing audio, size: {len(audio_data)} bytes")
        stream = self.p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             output=True)
        stream.write(audio_data)
        stream.stop_stream()
        stream.close()
        logger.debug("Audio playback complete")

        
    async def send_audio(self, duration):
        logger.info(f"Preparing to send audio of duration: {duration} seconds")
        self.start_audio_stream()
        audio_data = self.record_audio(duration)
        self.stop_audio_stream()

        base64_audio = base64.b64encode(audio_data).decode('utf-8')
        logger.debug(f"Audio encoded to base64, length: {len(base64_audio)}")
        
        event = {
            "type": "input_audio_buffer.append",
            "audio": base64_audio
        }
        await self.send_event(event)
        logger.debug("Audio buffer appended, committing buffer")
        await self.send_event({"type": "input_audio_buffer.commit"})
        logger.debug("Audio buffer committed, creating response")
        await self.send_event({"type": "response.create"})

    async def run(self):#isko call browser
        logger.info("Starting RealtimeClient run")
        await self.connect()
        
        # Create a task for receiving events
        receive_task = asyncio.create_task(self.receive_events())
        
        logger.info("Sending initial message to start the conversation")
        await self.send_event({
            "type": "response.create",
            "response": {
                "modalities": ["text", "audio"],
                "instructions": "You are a helpful AI assistant. Respond to the user's messages.",
            }
        })

        try:
            while True:
                
                logger.info("Audio input selected")
                print("Recording for 5 seconds...")
                await self.send_audio(5)
                

                # Give some time for the response to be processed
                await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            logger.info("Ending conversation and closing connection")
            receive_task.cancel()
            try:
                await receive_task
            except asyncio.CancelledError:
                pass
            await self.ws.close()

async def main():
    logger.info("Starting main function")
    client = RealtimeClient()
    try:
        await client.run()
    except Exception as e:
        logger.error(f"An error occurred in main: {e}")
    finally:
        logger.info("Main function completed")

if __name__ == "__main__":
    logger.info("Script started")
    asyncio.run(main())
    logger.info("Script completed")