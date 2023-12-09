import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition  # Import face_recognition module

def capture_face(username, password):
    video_capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = video_capture.read()
        if not ret:
            messagebox.showerror(title="Error", message="Failed to capture video.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite(f"{username}.jpg", frame[y:y + h, x:x + w])
            break

        cv2.imshow('Face Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    signup(username, password)

def signup(username, password):
    with open("user_credentials.txt", "a") as file:
        file.write(f"{username}:{password}\n")
    messagebox.showinfo(title="Sign Up Success", message="You have signed up successfully.")

def login_using_face():
    def compare_face():
        username = username_entry.get()
        try:
            saved_image = face_recognition.load_image_file(f"{username}.jpg")
            saved_image_encoding = face_recognition.face_encodings(saved_image)[0]
        except (FileNotFoundError, IndexError):
            messagebox.showerror(title="Error", message="No face found for this username.")
            return

        webcam_video = cv2.VideoCapture(0)
        while True:
            ret, frame = webcam_video.read()

            if not ret:
                messagebox.showerror(title="Error", message="Failed to capture video.")
                break

            webcam_face_encodings = face_recognition.face_encodings(frame)

            if webcam_face_encodings:
                webcam_face_encoding = webcam_face_encodings[0]

                results = face_recognition.compare_faces([saved_image_encoding], webcam_face_encoding)

                if results[0]:
                    messagebox.showinfo(title="Login Success", message=f"Welcome, {username}!")
                    break

            cv2.imshow('Face Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        webcam_video.release()
        cv2.destroyAllWindows()

    login_face_window = tk.Toplevel(window)
    login_face_window.title("Login using Face")
    login_face_window.geometry('340x220')

    login_face_frame = tk.Frame(login_face_window, bg='#333333')
    login_face_frame.pack()

    login_face_label = tk.Label(login_face_frame, text="Login using Face", bg='#333333', fg="#FF3399", font=("Arial", 30))
    login_face_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=20)

    username_label = tk.Label(login_face_frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    username_label.grid(row=1, column=0)
    global username_entry
    username_entry = tk.Entry(login_face_frame, font=("Arial", 16))
    username_entry.grid(row=1, column=1, pady=10)

    compare_button = tk.Button(login_face_frame, text="Compare Face", bg="#4CAF50", fg="#FFFFFF", font=("Arial", 16), command=compare_face)
    compare_button.grid(row=2, column=0, columnspan=2, pady=10)

def signin():
    signin_window = tk.Toplevel(window)
    signin_window.title("Sign In")
    signin_window.geometry('340x220')

    signin_frame = tk.Frame(signin_window, bg='#333333')
    signin_frame.pack()

    signin_label = tk.Label(signin_frame, text="Sign In", bg='#333333', fg="#FF3399", font=("Arial", 30))
    signin_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=20)

    username_label = tk.Label(signin_frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    username_label.grid(row=1, column=0)
    username_entry = tk.Entry(signin_frame, font=("Arial", 16))
    username_entry.grid(row=1, column=1, pady=10)

    password_label = tk.Label(signin_frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    password_label.grid(row=2, column=0)
    password_entry = tk.Entry(signin_frame, show="*", font=("Arial", 16))
    password_entry.grid(row=2, column=1, pady=10)

    # Function to capture face during sign-in
    def perform_signin():
        # Call capture_face function with the entered username and password
        capture_face(username_entry.get(), password_entry.get())

    signin_button = tk.Button(signin_frame, text="Sign In", bg="#4CAF50", fg="#FFFFFF", font=("Arial", 16),
                              command=perform_signin)
    signin_button.grid(row=3, column=0, columnspan=2, pady=10)

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        with open("user_credentials.txt", "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(':')
                if username == stored_username and password == stored_password:
                    welcome_window = tk.Toplevel(window)
                    welcome_window.title("Welcome")
                    welcome_window.geometry('300x200')

                    welcome_frame = tk.Frame(welcome_window, bg='#333333')
                    welcome_frame.pack()

                    welcome_label = tk.Label(welcome_frame, text=f"Welcome, {username}!", bg='#333333', fg="#FFFFFF",
                                             font=("Arial", 20))
                    welcome_label.pack(pady=50)
                    return

        messagebox.showerror(title="Error", message="Invalid login.")
    else:
        messagebox.showerror(title="Error", message="Please enter both username and password.")

window = tk.Tk()
window.title("Login form")
window.geometry('340x440')
window.configure(bg='#333333')

frame = tk.Frame(window, bg='#333333')
frame.pack()

login_label = tk.Label(frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)

username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_label.grid(row=1, column=0)
username_entry = tk.Entry(frame, font=("Arial", 16))
username_entry.grid(row=1, column=1, pady=20)

password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
password_label.grid(row=2, column=0)
password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
password_entry.grid(row=2, column=1, pady=20)

login_button = tk.Button(frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

signin_button = tk.Button(frame, text="Sign Up", bg="#4CAF50", fg="#FFFFFF", font=("Arial", 16), command=signin)
signin_button.grid(row=4, column=0, columnspan=2, pady=10)

login_with_face_button = tk.Button(frame, text="Login with Face", bg="#3366FF", fg="#FFFFFF", font=("Arial", 16), command=login_using_face)
login_with_face_button.grid(row=5, column=0, columnspan=2, pady=10)

window.mainloop()
