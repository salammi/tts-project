AI Vision Camera

AI-powered real-time object detection pipeline using a Python camera client and a Go backend.

The system:

Captures video from a webcam.
Detects objects in real time using AI.
Sends detection results and the captured image to a Go backend over gRPC.
Stores detection results in SQLite.
Sends an email alert with the captured image when a person is detected.
Architecture
┌──────────────┐
│    Webcam    │
└──────┬───────┘
       │
       ▼
┌────────────────────────┐
│ Python Detection Client│
└──────────┬─────────────┘
           │
           │ gRPC + Image
           ▼
┌────────────────────────┐
│      Go Backend        │
└───────┬────────┬───────┘
        │        │
        ▼        ▼
   ┌────────┐  ┌──────────────┐
   │ SQLite │  │ Email Alert  │
   └────────┘  └──────────────┘

Requirements

Make sure the following are installed and configured:

Go
Python 3
A working webcam
Python virtual environment
Required Python dependencies
Required Go dependencies
Email credentials/configuration for the backend
Running the Full Pipeline

Follow these steps to test the complete pipeline from webcam capture to database persistence and email notification.

1. Start the Go Backend

Open a terminal in the project root.

You do not need to activate the Python virtual environment for this step.

go run main.go


Wait until you see messages similar to:

SQLite database initialized successfully.
Go gRPC backend listening on [::]:50051


The backend and SQLite database are now ready.

2. Start the Python Camera

Open a second terminal in the project directory.

Activate the Python virtual environment:

source .venv/bin/activate


Your terminal prompt should show the environment name, for example:

(ai-cam)


Then start the camera client:

python detect.py


A webcam window should appear showing the live camera feed.

Keep both terminals open so you can monitor the Python client and Go backend.

3. Trigger Object Detection

With the webcam window open:

Stand in front of the camera.
Make sure your head and shoulders are clearly visible.
Ensure there is sufficient lighting.
Wait for the AI model to detect you.

When a person is detected, you should see a green bounding box around the person with a person label.

Example:

┌─────────────────────────┐
│                         │
│      ┌───────────┐      │
│      │  person   │      │
│      │     👤    │      │
│      └───────────┘      │
│                         │
└─────────────────────────┘

4. Verify the Logs

Once the person is detected, check both terminal windows.

Python Client

You should see:

DEBUG: Attached image of size XXXXX bytes


The exact image size will vary depending on the captured frame.

Go Backend

You should see:

Saved 1 detections to SQLite...
Person detected and image received. Triggering email...
--> Real-time email alert with photo sent successfully!

Successful End-to-End Flow

If all of the expected messages appear, the complete pipeline is working:

Webcam
  │
  ▼
AI Object Detection
  │
  ▼
Python Client
  │
  │ gRPC + Image
  ▼
Go Backend
  │
  ├──► SQLite
  │
  └──► Email + Captured Image


The following components have been verified:

✅ Webcam capture
✅ Real-time AI object detection
✅ Python-to-Go gRPC communication
✅ Detection persistence in SQLite
✅ Image transfer
✅ Person detection handling
✅ Email notification
✅ Email attachment with captured image
Troubleshooting
Go Backend Does Not Start

Make sure you are running the command from the project root:

go run main.go


If the backend still fails to start, verify that the required Go dependencies are installed.

Python Camera Does Not Start

Make sure the virtual environment is activated:

source .venv/bin/activate


Then run:

python detect.py


Also verify that your webcam is connected and accessible.

No Person Detection

Check the following:

The webcam is connected and working.
The camera window is displaying a live feed.
Your head and shoulders are clearly visible.
There is sufficient lighting.
The AI model has loaded successfully.
No Python errors are shown in the terminal.
Python Does Not Show the Image Attachment Log

Verify that the Go backend is already running before starting the Python client.

The correct startup order is:

1. Start Go backend
2. Start Python camera
3. Person enters camera frame
4. AI detects the person
5. Image is sent to Go
6. Detection is saved to SQLite
7. Email alert is triggered

Email Notification Is Not Sent

Check the Go terminal for:

Person detected and image received. Triggering email...


If this message appears but the following message does not:

--> Real-time email alert with photo sent successfully!


check the backend's email configuration and credentials.

Quick Start

For subsequent runs, you only need two terminals.

Terminal 1 — Go Backend

go run main.go


Terminal 2 — Python Camera

source .venv/bin/activate
python detect.py


Then step into the camera frame and wait for the person detection.

Expected Result

A successful test should produce output similar to:

Python

DEBUG: Attached image of size XXXXX bytes


Go

Saved 1 detections to SQLite...
Person detected and image received. Triggering email...
--> Real-time email alert with photo sent successfully!


At this point, the AI Vision Camera pipeline has successfully completed an end-to-end test covering:

Detection → gRPC → SQLite → Image Transfer → Email Notification
