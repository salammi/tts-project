```markdown
# AI Vision Camera Project

## Running the Full Pipeline Test

Follow these step-by-step instructions to run the AI object detection pipeline from start to finish and verify that both the database persistence and email notification systems are functioning correctly[cite: 1].

### Step 1: Start the Go Backend (Terminal 1)
Open a standard terminal in the project root directory. You do not need to activate the Python virtual environment for this step.

Start the database and gRPC server by running:
`go run main.go`

*Wait until you see the following output in the console:*
> `SQLite database initialized successfully.`
> `Go gRPC backend listening on [::]:50051`[cite: 1]

### Step 2: Start the Python Camera (Terminal 2)
Open a **second** terminal window in the project directory. Make sure your Python virtual environment is active (you should see `(ai-cam)` at the start of your prompt)[cite: 1]. 

Start the camera client by running:
`python detect.py`

*Wait until the webcam video window pops up on your screen.*[cite: 1]

### Step 3: Trigger the AI
1. Look at the webcam video window on your screen[cite: 1].
2. Step into the frame so the AI can clearly see your head and shoulders[cite: 1].
3. Wait for the green bounding box to appear with the word **"person"** above it[cite: 1].

### Step 4: Verify the Success Logs
The moment the "person" box appears in the video window, verify the outputs in both terminal windows to confirm the end-to-end connection:

**In the Python Terminal, you should instantly see:**
> `DEBUG: Attached image of size XXXXX bytes`[cite: 1]

**In the Go Terminal, you should instantly see:**
> `Saved 1 detections to SQLite...`
> `Person detected and image received. Triggering email...`
> `--> Real-time email alert with photo sent successfully!`[cite: 1]