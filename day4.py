import cv2
from deepface import DeepFace
import imutils

# Load OpenCV's Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for better processing speed
    frame = imutils.resize(frame, width=600)

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        # Extract face region
        face_roi = frame[y:y+h, x:x+w]

        try:
            # Analyze emotion using DeepFace
            analysis = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

            # Extract emotion and confidence score
            emotion = analysis[0]['dominant_emotion']
            confidence = analysis[0]['emotion'][emotion]

            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display emotion and confidence
            text = f"{emotion.capitalize()} ({confidence:.2f}%)"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        except Exception as e:
            print("Error in emotion detection:", str(e))

    # Show the frame
    cv2.imshow("Face & Emotion Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
