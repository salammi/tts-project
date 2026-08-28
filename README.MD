AI Vision Camera Project

AI-powered real-time object detection pipeline using a Python camera client and a Go backend. The pipeline detects objects from a webcam feed, stores detection results in SQLite, and sends an email alert with the captured image when a person is detected.

Pipeline Overview
Webcam
   │
   ▼
Python Detection Client
   │
   │  gRPC + Detection Image
   ▼
Go Backend
   │
   ├──► SQLite Database
   │
   └──► Email Notification

Running the Full Pipeline Test

Follow these steps to run the AI object detection pipeline from start to finish and verify that database persistence and email notifications are working correctly.

Step 1: Start the Go Backend

Open a terminal in the project root directory.

Note: You do not need to activate the Python virtual environment for this step.

Run:

go run main.go


Wait until the backend displays messages similar to:

SQLite database initialized successfully.
Go gRPC backend listening on [::]:50051


Once these messages appear, the Go backend and SQLite database are ready.

Step 2: Start the Python Camera

Open a second terminal in the project directory.

Activate your Python virtual environment. You should see (ai-cam) at the beginning of your terminal prompt.

Then run:

python detect.py


Wait for the webcam video window to appear.

Tip: Keep both terminal windows open so you can monitor the Python client and Go backend simultaneously.

Step 3: Trigger AI Object Detection

With the webcam window open:

Look directly at the webcam.
Step into the camera frame so your head and shoulders are clearly visible.
Wait for the AI to detect you.
Confirm that a green bounding box appears around you with person displayed above it.

Example:

┌─────────────────────────┐
│                         │
│      ┌───────────┐      │
│      │   person  │      │
│      │     👤    │      │
│      └───────────┘      │
│                         │
└─────────────────────────┘

Step 4: Verify the Success Logs

When the person detection appears, check both terminal windows.

Python Terminal

The Python detection client should immediately display:

DEBUG: Attached image of size XXXXX bytes


The exact image size will vary depending on the captured frame.

Go Terminal

The Go backend should immediately display:

Saved 1 detections to SQLite...
Person detected and image received. Triggering email...
--> Real-time email alert with photo sent successfully!

Successful End-to-End Flow

If all of the above messages appear, the complete pipeline is working:

✅ Webcam capture is working
✅ AI object detection is working
✅ Python client is communicating with the Go backend
✅ Detection data is being persisted to SQLite
✅ The detected image is being transferred successfully
✅ Person detection triggers the email notification
✅ Email notification with the captured photo is sent successfully
Troubleshooting
Go backend does not start

Make sure you are running the command from the project root:

go run main.go


Also verify that the required Go dependencies are installed.

Python camera does not start

Make sure the virtual environment is activated:

# Example
source .venv/bin/activate


Then run:

python detect.py

No person detection appears

Make sure:

Your webcam is connected and accessible.
Your head and shoulders are clearly visible.
There is sufficient lighting.
The camera window is open and displaying a live feed.
Python shows no image attachment log

Verify that the Go backend is already running before starting the Python client.

The expected startup order is:

1. Go backend
2. Python camera
3. Person enters camera frame
4. Detection occurs
5. Image is sent to Go
6. Detection is saved to SQLite
7. Email alert is triggered

Email notification is not sent

Check the Go terminal for:

Person detected and image received. Triggering email...


If this message appears but the success message does not, check the email configuration and credentials used by the backend.

Quick Start

For subsequent runs, the process is simply:

Terminal 1

go run main.go


Terminal 2

python detect.py


Then step into the camera frame and wait for the person detection.

Expected Result

A successful test should produce the following sequence:

Python:
DEBUG: Attached image of size XXXXX bytes

Go:
Saved 1 detections to SQLite...
Person detected and image received. Triggering email...
--> Real-time email alert with photo sent successfully!


At this point, the AI Vision Camera pipeline has successfully completed an end-to-end detection, persistence, and notification test.
