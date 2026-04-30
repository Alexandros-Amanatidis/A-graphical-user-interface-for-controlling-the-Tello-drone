# Εισαγωγή βιβλιοθηκών
from djitellopy import Tello  # Για τη χρήση ενσωματωμένων συναρτήσεων του tello drone σε python
from tkinter import messagebox  # Για την δημιουργία παραθύρου εισαγωγής δεδομένων από το χρήστη
from ultralytics import YOLO  # Για την ανίχνευση αντικειμένων
import tkinter as tk  # Για τη δημιουργεία GUI π.χ. παραθύρων και κουμπιών
from tkinter import Label, LEFT  # Για την εισαγωγή κειμένου σε παράθυρο
from datetime import datetime  # Για το χειρισμό ημερομηνίας και ώρας
from PIL import Image, ImageTk  # Για επεξεργασία εικόνας
import os  # Για την πρόσβαση στο λειτουργικό σύστημα
import subprocess  # Για την κωδικοποίηση βίντεο
import platform  # Πληροφορίες για το λειτουργικό σύστημα
import cv2  # Εισαγωγή βιβλιοθήκης OpenCV για την επεξεργασία εικόνας και βίντεο
import threading  # Για την ταυτόχρονη εκτέλεση συναρτήσεων του προγράμματος
import math  # Για τον υπολογισμό μαθηματικών συναρτήσεων
import time # Για τη μέτρηση χρόνου
import keyboard  # Για τον έλεγχο του πληκτρολογίου


# 1) H συνάρτηση buttons δέχεται παραμέτρους για να δημιουργήσει κουμπιά σε παράθυρο
def buttons(Window,Text,Width,Height,Font,Bg,Activebackground,Command,xx,yy):
    button = tk.Button(  # Δημιουργία κουμπιού
    Window,  # Το παράθυρο στο οποίο θα εμφανιστεί
    text=Text,  # Το κείμενο που θα αναγράφεται στο κουμπί
    width=Width,  # Το πλάτος του κουμπιού
    height=Height,  # Το ύψος του κουμπιού
    font=("Arial", Font, "bold"),  # Η γραμματοσειρά του κουμπιού
    bg=Bg,  # Το χρώμα φόντου του κουμπιού
    fg="black",  # Χρώμα γραμμάτων2
    activebackground=Activebackground,  # Χρώμα φόντου όταν πατηθεί το κουμπί
    activeforeground="black",  # Χρώμα γραμμάτων όταν πατηθεί το κουμπί
    bd=3,  # Πάχος περιγράμματος κουμπιού
    cursor="hand2",  # Πως θα εμφανίζεται το ποντίκι όταν είναι πάνω από το κουμπί
    command=Command  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
    )
    button.place(x=xx, y=yy)  # Συντεταγμένες στις οποίες θα τοποθετηθεί το κουμπί στο παράθυρο
    return button  # Στη μεταβλητή button αποθηκεύεται το εκάστοτε κουμπί ώστε αργότερα να παραμετροποιηθεί 


# 2) Η συνάρτηση data απεικονίζει δεδομένα του drone σε παράθυρο
def data(drone, label):
    try:
        while True:  # Ο βρόχος εκτελείται συνεχώς μέχρι να τερματιστεί το πρόγραμμα 
            vx = drone.get_speed_x()  # Παίρνουμε την ταχύτητα του drone στον x άξονα
            vy = drone.get_speed_y()  # Παίρνουμε την ταχύτητα του drone στον y άξονα
            vz = drone.get_speed_z()  # Παίρνουμε την ταχύτητα του drone στον z άξονα
            velocity = math.sqrt(vx**2 + vy**2 + vz**2)  # Υπολογίζουμε την συνολική διανυσματική ταχύτητα του drone
            # Εμφάνιση των παραπάνω σε παράθυρο
            data_text = f"Battery: {drone.get_battery()}% \n\n" \
                    f"Temperature: {drone.get_highest_temperature()} Celsius \n\n\n" \
                    f"Height: {(drone.get_distance_tof()-10)/100:.2f}m \n\n" \
                    f"Velocity: {velocity:.1f} cm/s \n\n" \
                    f"Total flight time: {drone.get_flight_time():.0f} s"
            label.config(text=data_text)  # Ανανέωση κειμένου ώστε να δείχνει κάθε φορά τις νέες τιμές
            time.sleep(0.7)  # Καθυστέρηση κατά 0,7 sec προτού ξαναδιαβαστούν και εμφανιστούν τα δεδομένα
    except Exception as e:
        print("error in data function",e)


# 3) Η συνάρτηση dimension διαβάζει τις διαστάσεις της εκάστοτε οθόνης 
def dimension(window):
    screen_width = window.winfo_screenwidth()  # Πλάτος οθόνης
    screen_height = window.winfo_screenheight()  # Ύψος οθόνης
    return screen_width, screen_height  # Επιστρέφει τις τιμές


# 4) Η συνάρτηση desktop_path βρίσκει το μονοπάτι της επιφάνειας εργασίας
def desktop_path():
    home = os.path.expanduser("~")  # Βρίσκει το Users account π.χ. C:\Users
    if platform.system() == "Windows":  # Ελέγχει αν το λειτουργικό είναι Windows
        return os.path.join(home, "Desktop")  # Επιστρέφει το μονοπάτι της επιφάνειας εργασίας
    elif platform.system() == "Darwin":  # Ελέγχει αν το λειτουργικό είναι macOS
        return os.path.join(home, "Desktop")  # Επιστρέφει το μονοπάτι της επιφάνειας εργασίας


# 5) Η συνάρτηση create_folders δημιουργεί τους φακέλους Videos, Images και Script στην επιφάνεια εργασίας
def create_folders():
    global videos_path, images_path, script_path
    path = desktop_path()  # Αποθηκεύει το μονοπάτι της επιφάνειας εργασίας στη μεταβλητή path
    videos_path = os.path.join(path, "Videos")  # Δημιουργεί τη θέση του φακέλου Videos
    images_path = os.path.join(path, "Images")   # Δημιουργεί τη θέση του φακέλου Images
    script_path = os.path.join(path, "Script")   # Δημιουργεί τη θέση του φακέλου Script

    if not os.path.exists(videos_path):  # Αν δεν υπάρχει ο φάκελος Videos στην επιφάνεια εργασίας το δημιουργεί
        os.makedirs(videos_path)

    if not os.path.exists(images_path):  # Αν δεν υπάρχει ο φάκελος Images στην επιφάνεια εργασίας το δημιουργεί
        os.makedirs(images_path)

    if not os.path.exists(script_path):  # Αν δεν υπάρχει ο φάκελος Script στην επιφάνεια εργασίας το δημιουργεί
        os.makedirs(script_path)


# 6) Η συνάρτηση open_folder ανοίγει τον φακέλο που θα επιλεχθεί 
def open_folder(path):
    if platform.system() == "Windows":  # Ελέγχει αν το λειτουργικό είναι Windows
        os.startfile(path)  # Άνοιγμα φακέλου στα Windows
    elif platform.system() == "Darwin":  # Ελέγχει αν το λειτουργικό είναι macOS
        subprocess.Popen(["open", path])  # Άνοιγμα φακέλου σε macOS


# 7) Η συνάρτηση counter είναι ένας μετρητής που μετρά τη διάρκεια του βίντεο
def counter():
    global recording
    label_counter = tk.Label(window2, text="00:00", font=("Arial", 30))  # Δημιουργεί ένα label για την εμφάνιση του χρονομέτρου
    screen_width, screen_height = dimension(window2)  # Παίρνει τις διαστάσεις τις οθόνης
    label_counter.place(x=int(0.45*screen_width),y=int(0.05*screen_height))  # Τοποθετείται το Label σε συγκεκριμένη θέση
    minutes = 0  # Η μεταβλητή minutes μετράει τα λεπτά
    seconds=0  # Η μεταβλητή seconds μετράει τα δευτερόλεπτα
    while recording:  # Όσο η μεταβλητή recording είναι True εκτελείται ο βρόχος 
        while seconds < 60:  # Όσο τα δευτερόλεπτα είναι κάτω από 60 συνέχισε το βρόχο
            label_counter.config(text=f"{minutes:02}:{seconds:02}")  # Ανανέωσε το χρονόμετρο
            seconds += 1  # Πρόσθεσε 1 sec
            time.sleep(1)  # Περίμενε 1 sec
            if recording==False:  #  Αν η μεταβλητή recording γίνει False τερμάτισε τους βρόχους 
                break
        minutes += 1  # Πρόσθεσε 1 min
    label_counter.config(text=f"00:00")  # Το χρονόμετρο μηδενίζεται με τον τερματισμό της συνάρτησης


# 8) Η συνάρτηση video_recording καταγράφει βίντεο και το αποθηκεύει
def video_recording(drone):
    global recording, start_recording_button, results
    
    # Δημιουργία μοναδικού ονόματος αρχείου με βάση την ημερομηνία και ώρα
    day_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Στη μεταβλητή day_time αποθηκεύεται η μέρα και η ώρα
    file_name = f"tello_{day_time}.mp4"  # Ορίζεται το πλήρες όνομα του εκάστοτε βίντεο 
    file_path = os.path.join(videos_path, file_name)  # Καθορίζεται η θέση στην οποία θα αποθηκευτεί το βίντεο στον φάκελο Videos

    # Δημιουργείται ένα αντικείμενο εγγραφής βίντεο
    out = cv2.VideoWriter(
        file_path,  # Καθορίζεται ο φάκελος στον οποίο θα αποθηκευτεί 
        cv2.VideoWriter_fourcc(*'mp4v'),  # Καθορίζεται η μορφή του βίντεο σε mp4
        30,  # Τα καρέ του βίντεο θα είναι 30
        (960, 720)  # Καθορίζεται η ανάλυση στο βίντεο στα 960px πλάτος και 720px ύψος
    )

    threading.Thread(target=counter, daemon=True).start()  # Μέσω thread καλείται η συνάρτηση counter 
    # ώστε να εμφανίζεται η διάρκεια λήψης του βίντεο
    frame_read = drone.get_frame_read()  # Παίρνει το τρέχον frame από το βίντεο και το αποθηκεύει στη μεταβλητή frame_read 
    last_time = time.time()  # Στη μεταβλητή last_time αποθηκεύεται η προηγούμενη τιμή του χρόνου
    while recording:  # Όσο η μεταβλητή recording είναι True εκτελείται ο βρόχος 
        try:
            # Περιμένουμε μέχρι να περάσουν ~1/30 δευτερόλεπτα
            current_time = time.time()  # Στη μεταβλητή current_time αποθηκεύεται η τωρινή τιμή του χρόνου
            if current_time - last_time >= 1/30:  # Περιμένουμε 0,033 sec ώστε να έχουμε 30 καρέ το δευτερόλεπτο        
                frame = frame_read.frame  # Παίρνουμε το τρέχον καρέ από το βίντεο και το αποθηκεύουμε στη μεταβλητή frame
                if recognition == True:  # Αν πατήθηκε το πλήκτρο button_lemons_recognition
                    frame = results[0].plot()  # Δημιουργεί annotated καρέ με bounding boxes και labels για το τρέχον frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Διορθόνονται τα χρώματα από BGR μορφή σε RGB μορφή
                out.write(frame_rgb)  # Aποθηκεύεται το τρέχον καρέ στο αρχείο του βίντεο
                last_time = current_time  # Ως προηγούμενη τιμή του χρόνου αποθηκεύεται η τωρινή τιμή του χρόνου
            else:
                time.sleep(0.001)  # Μικρή αναμονή μεχρι να φτάσουμε τα 0,001 sec
        except Exception as e:  # Σε περίπτωση σφάλματος
            print("Video recording error",e)  # Εμφάνισε στο terminal τη συνάρτηση που δημιουργεί το σφάλμα
            break


# 9) Η συνάρτηση start_stop_recording καθορίζει το πότε θα σταματά και ξεκινά η καταγραφή βίντεο
def start_stop_recording():
    global recording,button_video
    if recording == False:  # Αν δεν έχει ξεκινήσει η καταγραφή 
        recording = True  # Εκχώρισε στη μεταβλητή recording την τιμή True ώστε να ξεκινήσει η καταγραφή βίντεο
        button_video.config(  # Το κουμπί  button_video αλλάζει 
            text="Stop Recording",  # Το κείμενο που θα εμφανιστεί όταν καταγράφει βίντεο
            bg="red",  # Το χρώμα φώντου όταν καταγράφει βίντεο
            command=start_stop_recording,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            activebackground="red")  # Το χρώμα φόντου όταν πατηθεί το κουμπί
        threading.Thread(target=video_recording, args=(drone,), daemon=True).start()  # Μέσω thread καλείται η συνάρτηση 
        # video_recording ώστε να ξεκινήσει η καταγραφή βίντεο
    else:  # Αν έχει ξεκινήσει η καταγραφή 
        button_video.config(  # Το κουμπί  button_video αλλάζει 
            text="Start Recording",  # Το κείμενο που θα εμφανιστεί όταν δεν καταγράφεται βίντεο
            bg="green",  # Το χρώμα φόντου όταν δεν καταγράφει βίντεο
            command=start_stop_recording,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            activebackground="green")  # Το χρώμα φόντου όταν πατηθεί το κουμπί
        recording = False  # Εκχώρισε στη μεταβλητή recording την τιμή False ώστε να σταματήσει η καταγραφή βίντεο


# 10) Η συνάρτηση photo_thread συμβάλλει στη λήψη φωτογραφίας
def photo_thread():
    threading.Thread(target=photo, daemon=True).start()  # Μέσω thread καλούμε τη συνάρτηση photo


# 11) Η συνάρτηση photo τραβά μια φωτογραφία και την αποθηκεύει στον φάκελο Images
def photo():
    global images_path, frame1, recognition
    frame = drone.get_frame_read().frame  # Παίρνει το τρέχον καρέ και το αποθηκεύει στη μεταβλητή frame
    if recognition == True:  # Aν πατήθηκε το κουμπί button_lemons_recognition
        frame = frame1  # Τοποθέτησε στη μεταβλητή frame το annotated frame1
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Διορθόνονται τα χρώματα από BGR μορφή σε RGB μορφή
    # Δημιουργία μοναδικού ονόματος αρχείου με βάση την ημερομηνία και ώρα
    day_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Στη μεταβλητή day_time αποθηκεύεται η ημερομηνία και η ώρα
    file_name = f"tello_{day_time}.jpg"  # Στη μεταβλητή file_name αποθηκεύεται το όναμα της εκάστοτε φωτογραφίας
    file_path = os.path.join(images_path, file_name)  # Δημιουργείται η φωτογραφία
    cv2.imwrite(file_path, frame_rgb)  # Η φωτογραφία και αποθηκεύεται στο φάκελο Images


# 12) Η συνάρτηση live_stream εμφανίζει στην οθόνη τη live μετάδοση εικόνας από την κάμερα.
def live_stream(label):
    global recognition, model, lemons, label_lemon, frame1, results
    while True:  # Βρόχος που σταματά με το τερματισμό του προγράμματος
        try:
            frame = drone.get_frame_read().frame  # Παίρνει το τρέχον καρέ από την κάμερα
            if recognition == True:  # Αν πατήθηκε το πλήκτρο αναγνώρισης λεμονιού
                results = model(  # Τρέχουμε το YOLOv11 για ανίχνευση αντικειμένων. Χρησιμοποιούμε το εκπαιδευμένο μοντέλο best.pt
                    frame,  # Πάρε το τρέχον καρέ από την κάμερα 
                    imgsz=640,  # Κάνε resize το καρέ σε 640p x 640p
                    conf=0.65,  # Αντικείμενα με ποσοστό αναγνώρησης μικρότερο από 45% θα αγνοηθούν
                    device="cpu",  # Η αναγνώριση θα γίνει από την CPU
                    verbose=False)  # Eμφανίζει πληροφορίες για τα αντικείμενα που αναγνωρίζει στο terminal
                frame = results[0].plot()  # Δημιουργεί annotated καρέ με bounding boxes και labels για το τρέχον frame
                lemons = len(results[0].boxes)  # Ο μετρητής lemons μετρά πόσα λεμόνια ανιχνεύθηκαν
                label_lemon.config(text=f"Number of Lemons: {lemons}")  # Ανανεώνεται ο αριθμός των λεμονιών στην οθόνη
                frame1 = frame  # Τοποθέτησε στη μεταβλητή frame1 το annotated frame
         
            img = ImageTk.PhotoImage(Image.fromarray(frame))  # Μετατροπή της εικόνας PIL σε αντικείμενο 
            # που μπορεί να εμφανιστεί σε παράθυρο Tkinter
            label.config(image=img)  # Εμφάνιση της εικόνας
            label.image = img  # Η εικόνα αποθηκεύεται ώστε να μη χαθεί
        except Exception as e:  # Σε περίπτωση σφάλματος
            print("Live stream error",e)  # Εμφάνισε στο terminal τη συνάρτηση που δημιουργεί το σφάλμα
            break  # Σταμάτα την εκτέλεση του βρόχου


# 13) H συνάρτηση lemon_recognition διαμορφώνει εκ νέου το κουμπί button_lemons_recognition για ανίχνευση λεμονιού
def lemon_recognition():
    global recognition
    if recognition == False:  # Έλεγξε τη τιμή της μεταβλητής recognition ώστε να την αλλάξεις
        recognition = True  # Το πλήκτρο Enable pomegranate recognision πατήθηκε
        button_lemons_recognition.config(  # Διαμόρφωση κουμπιού button_lemon_recognition
            text="Disable lemon recognition",  # Το κείμενο του κουμπιού 
            bg="lightgrey",  # Το χρώμα φόντου του κουμπιού γίνεται πράσινο
            command=lemon_recognition,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            activebackground="green")  # Το χρώμα φόντου όταν πατηθεί το κουμπί
    else:  # Έλεγξε τη τιμή της μεταβλητής recognition ώστε να την αλλάξεις
        recognition = False  # Το πλήκτο Disable pomegranate recognision πατήθηκε
        button_lemons_recognition.config(  # Διαμόρφωση κουμπιού button_lemon_recognition
            text="Enable lemon recognition",  # Το κείμενο του κουμπιού
            bg="lightgrey",  # Το χρώμα φόντου του κουμπιού
            command=lemon_recognition,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            activebackground="green")  # Το χρώμα φόντου όταν πατηθεί το κουμπί


# 14) H συνάρτηση takeoff_landing_thread απογειώνει και προσγειώνει το drone
def takeoff_landing_thread():
    if drone.is_flying==False:  # Αν το drone είναι προσγειωμένο θα το απογειώσουμε
        global flag
        flag=True  # Η μεταβλητή flag όταν είναι True σημαίνει έχει απογειωθεί το drone
        threading.Thread(target = drone.takeoff, daemon=True).start()  # Μέσσω thread απογειώνεται το drone

        button_take0ff_landing.config(  # Διαμόρφωση κουμπιού button_take0ff_landing
            text="Landing",  # Το κείμενο του κουμπιού γίνεται Landing
            bg="green",  # Το χρώμα φόντου του κουμπιού γίνεται πράσινο
            command=takeoff_landing_thread,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            activebackground="lightgrey")  # Το χρώμα φόντου όταν πατηθεί το κουμπί
        
        threading.Thread(target=check_keys, args=(drone,), daemon=True).start()  # Γίνεται εκκίνηση της συνάρτησης 
        # check_keys που ελέγχει τις κινήσεις του drone
    else:  # Αν το drone είναι απογειωμένο θα το προσγειώσουμε
        threading.Thread(target = drone.land, daemon=True).start()  # Μέσσω thread προσγειώνεται το drone

        button_take0ff_landing.config(  # Διαμόρφωση κουμπιού button_take0ff_landing
            text="Take off",  # Το κείμενο του κουμπιού
            bg="lightgrey",  # Το χρώμα φόντου του κουμπιού
            command=takeoff_landing_thread,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            activebackground="green")  # Το χρώμα φόντου όταν πατηθεί το κουμπί
        flag=False  # Η μεταβλητή flag όταν είναι False σημαίνει έχει προσγειωθεί το drone


# 15) Η συνάρτηση check_keys ελέγχει αν πατήθηκε κάποιο πλήκτρο από το πληκτρολόγιο και στέλνει εντολές στο drone
def check_keys(drone):
    global SPEED, flag
    SPEED=30  # Η ταχύτητα ορίζεται από προεπιλογή στα 30 cm/s
    while flag:  # Όσο το drone ίπταται
        try:
            if keyboard.is_pressed('up'):  # Έλεγξε αν πατήθηκε το πλήκτρο '↑'
                drone.send_rc_control(0, SPEED, 0, 0)  # Κινείται προς τα επάνω με ταχύτητα SPEED
            elif keyboard.is_pressed('down'):  # Έλεγξε αν πατήθηκε το πλήκτρο '↓'
                drone.send_rc_control(0, -SPEED, 0, 0)  # Κινείται προς τα κάτω με ταχύτητα SPEED
            elif keyboard.is_pressed('left'):  # Έλεγξε αν πατήθηκε το πλήκτρο '←'
                drone.send_rc_control(0, 0, 0, -SPEED)  # Εκτελεί την κίνηση Υaw προς τα αριστερά με ταχύτητα SPEED
            elif keyboard.is_pressed('right'):  # Έλεγξε αν πατήθηκε το πλήκτρο '→'
                drone.send_rc_control(0, 0, 0, SPEED)   # Εκτελεί την κίνηση Υaw προς τα δεξιά με ταχύτητα SPEED
            elif keyboard.is_pressed('w'):  # Έλεγξε αν πατήθηκε το πλήκτρο 'W'
                drone.send_rc_control(0, 0, SPEED, 0)   # Κινείται προς τα εμπρός με ταχύτητα SPEED
            elif keyboard.is_pressed('s'):  # Έλεγξε αν πατήθηκε το πλήκτρο 'S'
                drone.send_rc_control(0, 0, -SPEED, 0)  # Κινείται προς τα πίσω με ταχύτητα SPEED
            elif keyboard.is_pressed('a'):  # Έλεγξε αν πατήθηκε το πλήκτρο 'A'
                drone.send_rc_control(-SPEED, 0, 0, 0)  # Κινείται προς τα πίσω με ταχύτητα SPEED
            elif keyboard.is_pressed('d'):  # Έλεγξε αν πατήθηκε το πλήκτρο 'D'
                drone.send_rc_control(SPEED, 0, 0, 0) # Κινείται προς τα πίσω με ταχύτητα SPEED
            else:  # Aν δεν πατηθεί κανένα κουμπί
                drone.send_rc_control(0, 0, 0, 0)  # Μηδένισε την ταχύτητα του drone
        except Exception as e:  # Σε περίπτωση σφάλματος
            print("Error in check_keys function",e)  # Εμφάνισε στο terminal τη συνάρτηση που δημιουργεί το σφάλμα
            break
        time.sleep(0.3)  # Μικρή καθυστέρηση κατά 0,3 sec για τον επόμενο έλεγχο των πλήκτρων


# 16) Η συνάρτηση button_how2fly εμφανίζει και αποκρύπτει στο παράθυρο 2 τα εικονικά πλήκτρα που ελέγχουν τις κινήσεις του drone 
def button_how2fly():
    global HOW2FLY  # Η μεταβλητή HOW2FLY καθορίζει αν πατήθηκε ή όχι το πλήκτρο για την εμφάνιση ή απόκρυψη των πλήκτρων
    screen_width, screen_height = dimension(window2)  # Παίρνουμε τις διαστάσεις του παραθύρου
    if HOW2FLY==True:  # Aν πατήθηκε το κουμπί για την εμφάνιση των εικονικών πλήκτρων να τα εμφανίσεις
        # Α
        text1.place(x=int(0.352*screen_width), y=int(0.7*screen_height))  # Τοποθέτηση την ετικέτα 1
        button1.place(x=int(0.355*screen_width), y=int(0.73*screen_height))  # Τοποθέτησε το εικονικό κουμπί 1

        # W
        text2.place(x=int(0.402*screen_width), y=int(0.64*screen_height))  # Τοποθέτηση την ετικέτα 2
        button2.place(x=int(0.404*screen_width), y=int(0.67*screen_height))  # Τοποθέτησε το εικονικό κουμπί 2

        # S
        text3.place(x=int(0.395*screen_width), y=int(0.76*screen_height))  # Τοποθέτηση την ετικέτα 3
        button3.place(x=int(0.404*screen_width), y=int(0.79*screen_height))  # Τοποθέτησε το εικονικό κουμπί 3

        # D
        text4.place(x=int(0.447*screen_width), y=int(0.7*screen_height))  # Τοποθέτηση την ετικέτα 4
        button4.place(x=int(0.452*screen_width), y=int(0.73*screen_height))  # Τοποθέτησε το εικονικό κουμπί 4
 
        # ↑
        text5.place(x=int(0.563*screen_width), y=int(0.64*screen_height))  # Τοποθέτηση την ετικέτα 5
        button5.place(x=int(0.575*screen_width), y=int(0.67*screen_height))  # Τοποθέτησε το εικονικό κουμπί 5

        # ←
        text6.place(x=int(0.525*screen_width), y=int(0.7*screen_height))  # Τοποθέτηση την ετικέτα 6
        button6.place(x=int(0.525*screen_width), y=int(0.73*screen_height))  # Τοποθέτησε το εικονικό κουμπί 6

        # →
        text7.place(x=int(0.622*screen_width), y=int(0.7*screen_height))  # Τοποθέτηση την ετικέτα 7
        button7.place(x=int(0.625*screen_width), y=int(0.73*screen_height))  # Τοποθέτησε το εικονικό κουμπί 7

        # ↓
        text8.place(x=int(0.56*screen_width), y=int(0.76*screen_height))  # Τοποθέτηση την ετικέτα 8
        button8.place(x=int(0.575*screen_width), y=int(0.79*screen_height))  # Τοποθέτησε το εικονικό κουμπί 8
        HOW2FLY=False  # Απόκρυψη των ειονικών πλήκτρων 
    else:  # Aν πατήθηκε το κουμπί για την απόκρυψη των εικονικών πλήκτρων να τα αποκρύψεις
        text1.place_forget()  # Να αποκρύψεις την ετικέτα 1
        button1.place_forget()  # Να αποκρύψεις το εικονικό κουμπί 1
    
        text2.place_forget()  # Να αποκρύψεις την ετικέτα 2
        button2.place_forget()  # Να αποκρύψεις το εικονικό κουμπί 2
  
        text3.place_forget()  # Να αποκρύψεις την ετικέτα 3
        button3.place_forget()  # Να αποκρύψεις το εικονικό κουμπί 3

        text4.place_forget()  # Να αποκρύψεις την ετικέτα 4
        button4.place_forget()  # Να αποκρύψεις το εικονικό κουμπί 4

        text5.place_forget()  # Να αποκρύψεις την ετικέτα 5
        button5.place_forget()  # Να αποκρύψεις το εικονικό κουμπί 5

        text6.place_forget()  # Να αποκρύψεις την ετικέτα 6
        button6.place_forget()  # Να αποκρύψεις το εικονικό κουμπί 6

        text7.place_forget()  # Να αποκρύψεις την ετικέτα 7
        button7.place_forget()  # Να αποκρύψεις το εικονικό κουμπί 7

        text8.place_forget()  # Να αποκρύψεις την ετικέτα 8
        button8.place_forget()  # Να αποκρύψεις το εικονικό κουμπί 8
        HOW2FLY=True


# 17) Η συνάρτηση set_speed καθορίζει τη ταχύτητα του drone
def set_speed(value):
    global SPEED  # Στη μεταβλητή SPEED θα εκχωρηθεί η τιμή της ταχύτητας 
    SPEED = value # που επέλεξε ο χειριστής του drone


# 18) Η συνάρτηση close_pop_up ελέγχει πια εντολή επέλεξε ο χρήστης και την αποθηκεύει καλώντας τη συνάρτηση add_command
def close_pop_up():
    global info_command

    if info_command == "Start Recording":  # Αν επιλέχθηκε έναξη καταγραφής βίντεο 
        show_list.append("  Start Recording")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
        add_command(f"start_stop_recording({True})")  # Κάλεσε τη συνάρτηση add_command ώστε να αποθηκευτεί η εντολή στο αρχείο py

    elif info_command == "Stop Recording":  # Αν επιλέχθηκε τερματισμός καταγραφής βίντεο 
        show_list.append("  Stop Recording")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
        add_command(f"start_stop_recording({False})")  # Κάλεσε τη συνάρτηση add_command ώστε να αποθηκευτεί η εντολή στο αρχείο py

    elif info_command == "Take a photo":  # Αν επιλέχθηκε λήψη φωτογραφίας 
        show_list.append("  Take a photo")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
        add_command(f"photo()")  # Κάλεσε τη συνάρτηση add_command ώστε να αποθηκευτεί η εντολή στο αρχείο py

    else:

        value = input_data.get()  # Παίρνει τη τιμή που έγραψε ο χρήστης
        if info_command == "Set speed":  # Αν επιλέχθηκε η εντολή ρύθμισης ταχύτητας
            show_list.append(f"  Set speed ({value} cm/s)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"drone.set_speed({value})")  # Κάλεσε τη συνάρτηση add_command ώστε να αποθηκευτεί η εντολή στο αρχείο py

        elif info_command == "Wait":  # Αν επιλέχθηκε η εντολή "περίμενε"
            show_list.append(f"  Wait ({value} sec)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"time.sleep({value})")  # Κάλεσε τη συνάρτηση add_command ώστε να αποθηκευτεί η εντολή στο αρχείο py

        elif info_command == "Move up":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα πάνω"
            show_list.append(f"  Move up ({value} cm)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"drone.move_up({value})")  # Κάλεσε τη συνάρτηση add_command ώστε να αποθηκευτεί η εντολή στο αρχείο py

        elif info_command == "Move down":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα κάτω"
            show_list.append(f"  Move down ({value} cm)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"drone.move_down({value})")  # Κάλεσε τη συνάρτηση add_command ώστε να αποθηκευτεί η εντολή στο αρχείο py

        elif info_command == "Move right":  # Αν επιλέχθηκε η εντολή "κινήσου προς δεξιά"
            show_list.append(f"  Move right ({value} cm)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"drone.move_right({value})")  # Κάλεσε τη συνάρτηση add_command ώστε να αποθηκευτεί η εντολή στο αρχείο py

        elif info_command == "Move left":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα αριστερά"
            show_list.append(f"  Move left ({value} cm)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"drone.move_left({value})")  # Κάλεσε τη συνάρτηση add_command ώστε να αποθηκευτεί η εντολή στο αρχείο py

        elif info_command == "Move forward":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα μπροστά"
            show_list.append(f"  Move forward ({value} cm)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"drone.move_forward({value})")  # Κάλεσε τη συνάρτηση add_command ώστε 
            # να αποθηκευτεί η εντολή στο αρχείο py

        elif info_command == "Move backward":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα πίσω"
            show_list.append(f"  Move backward ({value} cm)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"drone.move_back({value})")  # Κάλεσε τη συνάρτηση add_command ώστε 
            # να αποθηκευτεί η εντολή στο αρχείο py

        elif info_command == "Yaw right":  # Αν επιλέχθηκε η εντολή "δεξιά περιστροφή"
            show_list.append(f"  Yaw right ({value}°)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"drone.rotate_clockwise({value})")  # Κάλεσε τη συνάρτηση add_command ώστε 
            # να αποθηκευτεί η εντολή στο αρχείο py

        elif info_command == "Yaw left":  # Αν επιλέχθηκε η εντολή "αριστερή περιστροφή"
            show_list.append(f"  Yaw left ({value}°)")  # Αποθήκευσε στη λίστα show_list τι επέλεξε ο χρήστης
            add_command(f"drone.rotate_counter_clockwise({value})")  # Κάλεσε τη συνάρτηση add_command ώστε 
            # να αποθηκευτεί η εντολή στο αρχείο py

        pop_up_window.destroy()  # Κλείσε το παράθυρο pop_up_window


# 19) Η συνάρτηση pop_up δημιουργεί ένα αναδυόμενο παράθυρο ώστε ο χρήστης να εκχωρίσει την επιθυμητή τιμή
def pop_up(Text):
    global pop_up_window,input_data
    screen_width, screen_height = dimension(window3)  # Παίρνει τις διαστάσεις της οθόνης
    pop_up_window = tk.Toplevel(window3)  # Δημιουργείται το παράθυρο pop_up_window το οποίο θα εμφανίζεται πάνω από το παράθυρο 3
    pop_up_window.title("Input data")  # Ο τίτλος του παραθύρου pop_up_window

    label = tk.Label(  # Δημιουργεί κειμένου 
        pop_up_window,  # Το παράθυρο που θα εμφανιστεί
        text=Text,  # Το κείμενο που θα εμφανίζει
        font=("Arial", 14, "bold"))  # Γραμματοσειρά
    label.pack(pady=5)  # Τοποθέτηση του κειμένου στο παράθυρο. Πάνω και κάτω από το κείμενο θα υπάρχει περιθώριο 5 pixels

    input_data = tk.Entry(  # Δημιουργία πεδίου εισαγωγής κειμένου input_data
        pop_up_window,  # Το παράθυρο στο οποίο θα εμφανιστεί
        width=3,  # Το πλάτος του θα είναι 3 χαρακτήρες
        font=("Arial", 15))  # Η γραμματοσειρά
    input_data.pack(pady=5)  # Τοποθέτηση του πεδίου στο παράθυρο. Πάνω και κάτω από το κείμενο θα υπάρχει περιθώριο 5 pixels
    
    buttons(  # Κλήση της συνάρτησης buttons
        pop_up_window,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
        "Ok",  # Το κείμενο του κουμπιού
        8,1,9,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
        "lightgrey",  # Το χρώμα φόντου του κουμπιού
        "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
        close_pop_up,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
        int(0.08*screen_width),int(0.1*screen_height))
          
    x=int(0.43 * screen_width)
    y=int(0.45 * screen_height)
    pop_up_window.geometry(f"316x120+{x}+{y}")  # Ορίζεται το μέγεθος του παραθύρου pop_up_window και τοποθετείται στο παράθυρο 3


# 20) Η συνάρτηση add_command προσθέτει μία μία τις εντολές που επιλέγει ο χρήστης στη λίστα command_list
# Επίσης τις εμφανίζει σε πλαίσιο κειμένου στο παράθυρο 3
def add_command(command):
    command_list.append(command)  # Θα προστεθεί η εκάστοτε εντολή στη λίστα command_list
    command_text.delete("1.0", tk.END)  # Το πλαίσιο κειμένου command_text καθαρίζεται ώστε να εμφανιστούν οι νέες εντολές 
    command_text.insert(tk.END, "\n\n".join(show_list))  # Στο πλαίσιο κειμένου θα εμφανιστούν τα περιεχόμενα 
    # της λίστας show_list και όχι της command_list


# 21) H συνάρτηση store δημιουργεί το όνομα του αρχείου python και το αποθηκεύει στο φάκελο Script
def store(extension, folder_path):
    day_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Στη μεταβλητή day_time αποθηκεύεται η ημερομηνία και η ώρα
    file_name = f"tello_program_{day_time}.{extension}"  # Στη μεταβλητή file_name αποθηκεύεται το όναμα της εκάστοτε φωτογραφίας
    file_path = os.path.join(folder_path, file_name)  # Καθορίζεται η θέση στην οποία θα αποθηκευτεί το αρχείο
    # python στο φάκελο Script
    return file_path


# 22) Η συνάρτηση finish είναι υπεύθυνη για την συρραφή και αποθήκευση του προγράμματος που δημιουργεί ο χρήστης 
def finish():
    code = (  # Η μεταβλητή code είναι τύπου string και περιέχει εντολές που αποτελλόυν το βασικό κορμό του προγράμματος
        "from djitellopy import Tello \n"
        "from datetime import datetime \n"
        "import time,cv2,threading \n\n"

        "drone=Tello() \n"
        "drone.connect() \n"
        "print(f\"Μπαταρία: {drone.get_battery()}%\") \n"
        "drone.takeoff() \n\n"


        "# ---- Functions ----\n"
        "def photo(): \n"
            "    drone.streamon() \n"
            "    time.sleep(3) \n"
            "    frame_read = drone.get_frame_read() \n"
            "    time.sleep(0.3) \n"
            "    frame = frame_read.frame \n"
            "    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)\n"
            "    day_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') \n"
            "    file_name = f\"tello_{day_time}.jpg\" \n"
            "    cv2.imwrite(file_name, frame_rgb) \n\n"


        "def start_stop_recording(answer): \n"
        "    global recording,drone \n"
        "    recording = answer \n"
        "    if recording == True: \n"
        "        drone.streamon() \n"
        "        time.sleep(3) \n"
        "        threading.Thread(target=video_recording, args=(drone,), daemon=True).start() \n"
        "    else: \n"
        "        drone.streamoff() \n\n"
        
        "def video_recording(drone): \n"
        "    video_name = f\"tello_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4\" \n"
        "    out = cv2.VideoWriter(video_name,cv2.VideoWriter_fourcc(*'mp4v'),30,(960, 720)) \n"
        "    frame_read = drone.get_frame_read() \n"
        "    time.sleep(0.3) \n"
        "    last_time = time.time()  \n"
        "    while recording:  \n"
        "        current_time = time.time() \n"
        "        if current_time - last_time >= 1/30: \n"
        "            frame = frame_read.frame \n"
        "            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) \n"
        "            out.write(frame_rgb) \n"
        "            last_time = current_time \n"
        "        else:\n"
        "            time.sleep(0.002) \n"
        "    out.release()\n"
        "# ---- Functions ----\n\n\n"


        "# ---- User Commands ---- \n")
    
    code += "\n".join(command_list) + "\n# ---- User Commands ---- \n\n\ndrone.land() \ndrone.end()"  # Πρόσθεση της λίστας
    # command_list στη μεταβλητή code 
    file_path = store("py", script_path)  # Αποθήκευση του προγράμματος με καθορισμένο όνομα και θέση
    with open(file_path, "w", encoding="utf-8") as f:  # Δημιουργεί το αρχείο python με UTF-8 κωδικοποίηση
        f.write(code)  # Αποθηκεύεται το περιεχόμενο της μεταβλητής code στο αρχείο python που δημιουργείται
    messagebox.showinfo("Storage", f"Saved in the Script folder")  # Ο χρήστης ειδοποιείται με αναδυόμενο παράθυρο 
    # πως το πρόγραμμά του αποθηκεύτηκε στον φάκελο Script 


# 23) Η συνάρτηση scratch ελέγχει πιο εικονικό κουμπί πατήθηκε ώστε να αποθηκευτεί η εντολή που επέλεξε ο χρήστης
def scratch(command1):
    global info_command  # Στη μεταβλητή info_command αποθηκεύεται η εντολή που επέλεξε ο χρήστης
    
    if command1 == "Start Recording":  # Αν επιλέχθηκε έναξη καταγραφής βίντεο 
        info_command = "Start Recording"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        close_pop_up()  # Κάλεσε τη συνάρτηση close_pop_up ώστε να αποθηκευτεί η εντολή
    
    elif command1 == "Stop Recording":  # Αν επιλέχθηκε τερματισμός καταγραφής βίντεο 
        info_command = "Stop Recording"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        close_pop_up()  # Κάλεσε τη συνάρτηση close_pop_up ώστε να αποθηκευτεί η εντολή

    elif command1 == "Take a photo":  # Αν επιλέχθηκε λήψη φωτογραφίας 
        info_command = "Take a photo"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        close_pop_up()  # Κάλεσε τη συνάρτηση close_pop_up ώστε να αποθηκευτεί η εντολή
        
    elif command1 == "Set speed":  # Αν επιλέχθηκε η εντολή ρύθμισης ταχύτητας
        info_command = "Set speed"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Set speed: 10–100 cm/s")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Wait":  # Αν επιλέχθηκε η εντολή "Περίμενε"
        info_command = "Wait"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Waiting time in seconds")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Move up":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα πάνω"
        info_command = "Move up"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Move up: 20-500 cm")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Move down":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα κάτω"
        info_command = "Move down"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Move down: 20-500 cm")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Move right":  # Αν επιλέχθηκε η εντολή "κινήσου προς δεξιά"
        info_command = "Move right"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Move right: 20-500 cm")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Move left":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα αριστερά"
        info_command = "Move left"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Move left: 20-500 cm")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Move forward":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα μπροστά"
        info_command = "Move forward"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Move forward: 20-500 cm")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Move backward":  # Αν επιλέχθηκε η εντολή "κινήσου προς τα πίσω"
        info_command = "Move backward"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Move backward: 20-500 cm")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Yaw right":  # Αν επιλέχθηκε η εντολή "δεξιά περιστροφή"
        info_command = "Yaw right"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Set rotation to the right: 1°–360°")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Yaw left":  # Αν επιλέχθηκε η εντολή "αριστερή περιστροφή"
        info_command = "Yaw left"  # Αποθήκευσε στη λίστα info_command τι επέλεξε ο χρήστης
        pop_up("Set rotation to the left: 1°–360°")  # Κάλεσε τη συνάτηση pop_up ώστε να πληκτρολογίσει ο χρήστης την επιθυμητή τιμή

    elif command1 == "Finish":  # Αν επιλέχθηκε η εντολή "αποθήκευση προγράμματος"
        finish()  # Κάλεσε τη συνάρτηση finish ώστε να αποθηκευτεί το πρόγραμμα


# 24) H συνάρτηση win3 εμφανίζει το παράθυρο 3 και όλα τα γραφικά στοιχεία που περιέχει
def win3():
    global window3, command_text, command_list, show_list
    window1.destroy()  # Κλείνει το παράθυρο 1
    window3 = tk.Tk()  # Δημιουργεί το παράθυρο 3
    window3.title('Write your program')  # Αποδίδεται τίτλος στο παράθυρο 3
    screen_width, screen_height = dimension(window3)  # Παίρνει τις διαστάσεις της οθόνης
    window3.geometry(f"{screen_width}x{screen_height}+0+0")  # Καθορίζει το μέγεθος του παραθύρου 3 σε pixels
    window3.configure(background="black")  # Θέτει ως χρώμα φόντου του παραθύρου 3 το μαύρο 
    window3.resizable(width=True, height=True)  # Το παράθυρο 3 θα μπορεί ο χρήστης να του αλλάξει διαστάσεις
    info_label= tk.Label(  # Επιγραφή με οδηγίες για τη δημιουργία νέου προγράμματος από το χρήστη
        window3,  # Σε ποιό παράθυρο θα εμφανιστεί
        text="Select the order in which the commands will run. \nPress the 'Finish' button to save the program. \n" \
        "Note: The first command to be executed is takeoff and the last command is landing.",  # Το κέιμενο που θα αναγράφει
        font=("Arial", 22,"bold"),  # Γραμματοσειρά
        fg="white",  # Χρώμα γραμματοσειράς
        bg="black")  # Χρώμα φόντου)
    info_label.place(x=int(0.08*screen_width), y=int(0.04*screen_height))  # Τοποθέτηση κειμένου στο παράθυρο 3
    command_list = []  # Η λίστα με τις εντολές του προγράμματος που τοποθετεί ο χρήστης
    show_list = []  # Παρόμοια με τη λίστα command_list. Τα περιεχόμενά της θα απεικονίζονται στο πλαίσιο κειμένου

    command_text = tk.Text( # Δημιουργία πλαισίου κειμένου
        window3,  # Το παράθυρο που θα εμφανιστεί
        width=34,  # Το πλάτος του σε χαρακτήρες
        height=22,  # Το ύψος του σε γραμμές
        font=("Arial", 14, "bold"))  # Η γραμματοσειρά
    
    command_text.place(x=int(0.655*screen_width), y=int(0.25*screen_height))  # Τοποθέτηση του πλαισίου 
    # κειμένου command_text στο παράθυρο 3

    scrollbar = tk.Scrollbar(window3, command=command_text.yview)  # Δημιουργία κάθετης μπάρας κύλισης
    scrollbar.place(x=int(0.89*screen_width), y=int(0.25*screen_height), height=486)  # Τοποθέτηση της μπάρας
    command_text.config(yscrollcommand=scrollbar.set)  # Σύνδεση της μπάρας με το πλαίσιο κειμένου


    # Button Start Recording
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Start Recording",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Start Recording"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.1*screen_width),int(0.25*screen_height))
    
    # Button Stop Recording
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Stop Recording",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Stop Recording"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.1*screen_width),int(0.32*screen_height))
    
    # Button Take a photo
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Take a photo",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Take a photo"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.1*screen_width),int(0.42*screen_height))
    
    # Button Set speed
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Set speed",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Set speed"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.1*screen_width),int(0.51*screen_height))
    
    # Button Wait
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Wait",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Wait"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.1*screen_width),int(0.60*screen_height))
    
    # Button Finish
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Finish",  # Το κείμενο του κουμπιού
            13,2,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "grey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Finish"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.1*screen_width),int(0.69*screen_height))
    
    # Button Move up
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Move up",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Move up"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.3*screen_width),int(0.25*screen_height))
    
    # Button Move down
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Move down",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch( "Move down"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.3*screen_width),int(0.32*screen_height))
    
    # Button Move right
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Move right",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Move right"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.3*screen_width),int(0.42*screen_height))
    
    # Button Move left
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Move left",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch( "Move left"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.3*screen_width),int(0.49*screen_height))
    
    # Button Move forward
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Move forward",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Move forward"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.3*screen_width),int(0.59*screen_height))
    
    # Button Move backword
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Move backword",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Move backward"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.3*screen_width),int(0.66*screen_height))
    
    # Button Yaw right
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Yaw right",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Yaw right"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.3*screen_width),int(0.76*screen_height))
    
    # Button Yaw left
    buttons(window3,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Yaw left",  # Το κείμενο του κουμπιού
            13,1,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: scratch("Yaw left"),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.3*screen_width),int(0.83*screen_height))
    
    window3.mainloop()  # Διατηρεί το παράθυρο 3 ανοιχτό μέχρι να το κλείσει ο χρήστης


# 25) H συνάρτηση win2 εμφανίζει το παράθυρο 2 και όλα τα γραφικά στοιχεία που περιέχει
def win2():
    global recording, window2, button_video, button_take0ff_landing, button_video
    global button_lemons_recognition, HOW2FLY, drone, recognition, model, lemons, label_lemon
    lemon = 0  # Μετρητής λεμονιών
    model = YOLO("best.pt")  # Φορτόνουμαι το αρχείο best.pt που είναι το εκπαιδευμένο μοντέλο του Yolo
    drone = Tello()  # Δημιουργείται ένα αντικείμενο drone της κλάσης Tello
    drone.connect()  # Πραγματοποιείται σύνδεση drone-Η/Υ μέσω Wi-fi
    print(f"Μπαταρία: {drone.get_battery()}%")  # Απεικονίζεται η στάθμη της μπαταρίας
    recording = False  # Η μεταβλητή recording καθορίζει το αν θα καταγράφεται βίντεο
    HOW2FLY = True  # Η μεταβλητή HOW2FLY καθορίζει αν πατήθηκε ή όχι το πλήκτρο για την εμφάνιση ή απόκρυψη των πλήκτρων
    recognition = False  # Η μεταβλητή recognition καθορίζει αν πατήθηκε ή όχι το πλήκτρο για την αναγνώρηση των ροδιών
    window1.destroy()  # Κλείνει το παράθυρο 1
    window2 = tk.Tk()  # Δημιουργεί το παράθυρο 2
    window2.title('Flight Control Interface')  # Ονοματίζει το παράθυρο 2
    screen_width, screen_height = dimension(window2)  # Παίρνει τις διαστάσεις τις οθόνης
    window2.geometry(f"{screen_width}x{screen_height}+0+0")  # Καθορίζει το μέγεθος του παραθύρου 2 σε pixels
    window2.configure(background="black")  # Θέτει ως χρώμα φόντου του παραθύρου 2 το μαύρο 
    window2.resizable(width=True, height=True)  # Το παράθυρο 2 θα μπορεί ο χρήστης να του αλλάξει διαστάσεις

    drone.streamon()  # Η κάμερα του drone  μεταδίδει την εικόνα από την κάμερά του
  
    frame_read = drone.get_frame_read()  # Παίρνει το τρέχον καρέ από την κάμερα

    # Δημιουργία Label για εμφάνιση εικόνας από την κάμερα
    label1 = tk.Label(window2, bg="black")
    label1.pack()  # Στο label1 θα εμφανιστεί η ζωντανή μετάδοση 
    # της εικόνας από την κάμερα του drone μέσα στο παράθυρο 2

    label_lemon = tk.Label(window2, text="Number of lemons: 0", font=("Arial", 18, "bold"), fg="yellow")  # Η Ετικέτα που εμφανίζει 
    # το πλήθος των λεμονιών
    label_lemon.place (x=int(0.45*screen_width), y=int(0.85*screen_height))  # Τοποθετείται στο παράθυρο 2

    live_stream_thread = threading.Thread(target=live_stream, args=(label1,), daemon=True).start()  # Μέσω thread ξεκινά 
    # η ζωντανή μετάδοση της εικόνας του drone
      
    button_video=buttons(  # Κουμπί για έναρξη βίντεο
        window2,  # Σε ποιο παράθυρο θα εμφανιστεί
        "Start Recording",  # Το κείμενο που θα αναγράφει 
        13,2,20,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
        "lightgrey",  # Το χρώμα φόντου του κουμπιού
        "red",  # Χρώμα φόντου όταν πατηθεί το κουμπί
        start_stop_recording,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
        int(0.02*screen_width),int(0.5*screen_height)) # Τοποθέτηση του κουμιού στο παράθυρο

    buttons(  # Κουμπί για λήψη φωτογραφίας
        window2,  # Σε ποιο παράθυρο θα εμφανιστεί
        "Photo"  # Το κείμενο που θα αναγράφει
        ,10,2,20,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
        "lightgrey",  # Το χρώμα φόντου του κουμπιού
        "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
        photo_thread,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
        int(0.04*screen_width),int(0.7*screen_height))  # Τοποθέτηση του κουμιού στο παράθυρο

    button_take0ff_landing=buttons( # Κουμπί για απογείωση/προσγείωση
        window2,  # Σε ποιο παράθυρο θα εμφανιστεί
        "Take off",  # Το κείμενο που θα αναγράφει
        10,2,20,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
        "lightgrey",  # Το χρώμα φόντου του κουμπιού
        "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
        takeoff_landing_thread,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
        int(0.85*screen_width),int(0.3*screen_height))  # Τοποθέτηση του κουμιού στο παράθυρο
    
    button_lemons_recognition=buttons( # Κουμπί για απογείωση/προσγείωση
        window2,  # Σε ποιο παράθυρο θα εμφανιστεί
        "Enable lemon recognition",  # Το κείμενο που θα αναγράφει
        20,2,14,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
        "lightgrey",  # Το χρώμα φόντου του κουμπιού
        "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
        lemon_recognition,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
        int(0.821*screen_width),int(0.175*screen_height))  # Τοποθέτηση του κουμπιού στο παράθυρο
   
    label2 = Label(window2, fg="white", bg="black", justify=LEFT, font=("Arial", 14))  # Στο label2 θα εμφανιστούν τα
    label2.place(x=20, y=30)  # δεδομένα της συνάρτησης data. Τοποθετείται στο παράθυρο 2
    
    threading.Thread(target=data, args=(drone, label2), daemon=True).start()  # Μέσω thead καλείται η συνάρτηση
    # data για την απεικόνιση δεδομένων στην οθόνη

    buttons(  # Κουμπί για την εμφάνιση των εικονικών πλήκτρων που κινούν το drone
        window2,  # Σε ποιο παράθυρο θα εμφανιστεί
        "How to fly",  # Το κείμενο που θα αναγράφει
        10,2,20,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
        "lightgrey",  # Το χρώμα φόντου του κουμπιού
        "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
        button_how2fly,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
        int(0.85*screen_width),int(0.45*screen_height))  # Τοποθέτηση του κουμπιού στο παράθυρο
    
    # Δημιουργούνται τα εικονικά κουμπιά και τις ετικέτες τους στο παράθυρο 2 αλλά δεν τα εμφανίζει στο παράθυρο.
    #  Η συνάρτηση που τα εμφανίζει και τα εξαφανίζει είναι η συνάρτηση 
    global text1,text2,text3,text4,text5,text6,text7,text8
    global button1,button2,button3,button4,button5,button6,button7,button8

    text1 = tk.Label(window2, text="Move left", font=("Arial", 10,"bold"))
    button1 = tk.Label(window2, text="A", font=("Arial", 14,"bold"), width=4, height=2, relief="raised", borderwidth=3)

    text2 = tk.Label(window2, text="Move up", font=("Arial", 10,"bold"))
    button2 = tk.Label(window2, text="W", font=("Arial", 14,"bold"), width=4, height=2, relief="raised", borderwidth=2)

    text3 = tk.Label(window2, text="Move down", font=("Arial", 10,"bold"))
    button3 = tk.Label(window2, text="S", font=("Arial", 14,"bold"), width=4, height=2, relief="raised", borderwidth=2)

    text4 = tk.Label(window2, text="Move right", font=("Arial", 10,"bold"))
    button4 = tk.Label(window2, text="D", font=("Arial", 14,"bold"), width=4, height=2, relief="raised", borderwidth=2)

    text5 = tk.Label(window2, text="Move forward", font=("Arial", 10,"bold"))
    button5 = tk.Label(window2, text="↑", font=("Arial", 14,"bold"), width=4, height=2, relief="raised", borderwidth=2)

    text6 = tk.Label(window2, text="Yaw left", font=("Arial", 10,"bold"))
    button6 = tk.Label(window2, text="←", font=("Arial", 14,"bold"), width=4, height=2, relief="raised", borderwidth=2)

    text7 = tk.Label(window2, text="Yaw right", font=("Arial", 10,"bold"))
    button7 = tk.Label(window2, text="→", font=("Arial", 14,"bold"), width=4, height=2, relief="raised", borderwidth=2)

    text8 = tk.Label(window2, text="Move backward", font=("Arial", 10,"bold"))
    button8 = tk.Label(window2, text="↓", font=("Arial", 14,"bold"), width=4, height=2, relief="raised", borderwidth=2)

    speed_var = tk.IntVar(value=1)  # Ορίζεται η προεπιλεγμένη ταχύτητα του drone να είναι 30 cm/sec

    tk.Label(  # Ετικέτα που εμφανίζεται στο παράθυρο 2 για να επιλέξουμε την ταχύτητα του drone  
        window2,  # Σε ποιό παράθυρο θα εμφανιστεί
        text="Set the speed",  # Το κέιμενο που θα αναγράφει
        font=("Arial", 20, "bold"),  # η γραμματοσειρά του κουμπιού
        ).place(x=int(0.85*screen_width),y=int(0.6*screen_height))  # Η θέση που θα τοποθετηθεί στο παράθυρο

    # Τρεις επιλογές RadioButton για την ρύθμιση της ταχύτητας του drone   
    tk.Radiobutton(  # Το κουμπί RadioButton που θέτει την ταχύτητα του drone 30 cm/sec
        window2,  # Σε ποιό παράθυρο θα εμφανιστεί
        text="Low 30 cm/s",  # Το κέιμενο που θα αναγράφει
        variable=speed_var,  # Κοινή μεταβλητή των Radiobutton 
        fg="white",  # Χρώμα γραμματοσειράς
        bg="black",  # Χρώμα φόντου
        selectcolor="black",    # Το χρώμα που θα γεμίζει το "κυκλάκι" όταν το Radiobutton είναι επιλεγμένο
        font=("Arial", 16, "bold"),   # Γραμματοσειρά
        value=1,# Η τιμή που θα πάρει η μεταβλητή speed_var όταν επιλεχθεί αυτό το Radiobutton
        command=lambda:set_speed(30)  # Συνάρτηση που θα εκτελεστεί όταν πατηθεί
        ).place(x=int(0.85*screen_width),y=int(0.65*screen_height))  # Τοποθέτηση του κουμπιού στο παράθυρο

    tk.Radiobutton(# Το κουμπί RadioButton που θέτει την ταχύτητα του drone 50 cm/sec
        window2,  # Σε ποιό παράθυρο θα εμφανιστεί
        text="Medium 50 cm/s",  # Το κέιμενο που θα αναγράφει
        variable=speed_var,  # Κοινή μεταβλητή των Radiobutton 
        fg="white",  # Χρώμα γραμματοσειράς
        bg="black",  # Χρώμα φόντου
        selectcolor="black",  # Το χρώμα που θα γεμίζει το "κυκλάκι" όταν το Radiobutton είναι επιλεγμένο
        font=("Arial", 16, "bold"),  # Γραμματοσειρά
        value=2,# Η τιμή που θα πάρει η μεταβλητή speed_var όταν επιλεχθεί αυτό το Radiobutton
        command=lambda:set_speed(50)  # Συνάρτηση που θα εκτελεστεί όταν πατηθεί
        ).place(x=int(0.85*screen_width),y=int(0.7*screen_height))  # Τοποθέτηση του κουμπιού στο παράθυρο

    tk.Radiobutton(# Το κουμπί RadioButton που θέτει την ταχύτητα του drone 100 cm/sec
        window2,  # Σε ποιό παράθυρο θα εμφανιστεί
        text="High 100 cm/s",  # Το κέιμενο που θα αναγράφει
        variable=speed_var,  # Κοινή μεταβλητή των Radiobutton 
        fg="white",  # Χρώμα γραμματοσειράς
        bg="black",  # Χρώμα φόντου
        selectcolor="black",  # Το χρώμα που θα γεμίζει το "κυκλάκι" όταν το Radiobutton είναι επιλεγμένο
        font=("Arial", 16, "bold"),  # Γραμματοσειρά
        value=3,  # Η τιμή που θα πάρει η μεταβλητή speed_var όταν επιλεχθεί αυτό το Radiobutton
        command=lambda:set_speed(100)  # Συνάρτηση που θα εκτελεστεί όταν πατηθεί
        ).place(x=int(0.85*screen_width),y=int(0.75*screen_height))  # Τοποθέτηση του κουμπιού στο παράθυρο

    window2.mainloop()  # Διατηρεί το παράθυρο 2 ανοιχτό μέχρι να το κλείσει ο χρήστης


# 26) H συνάρτηση main εμφανίζει το παράθυρο 1 και όλα τα γραφικά στοιχεία που περιέχει
def main(): 
    global window1
    window1 = tk.Tk()  # Δημιουργία παραθύρου 1
    window1.title('GUI for Tello drone')  # Τίτλος παραθύρου
    screen_width, screen_height = dimension(window1)  # Παίρνουμε τις διαστάσεις της οθόνης
    window1.geometry(f"{screen_width}x{screen_height}+0+0")  # Ορίζουμε τις διαστάσεις του παραθύρου
    window1.configure(background="black")  # Ορίζουμε το χρώμα του φόντου του παραθύρου
    window1.resizable(width=True, height=True)  # Ο χρήστης θα μπορεί να αλλάξει τις διαστάσεις του παραθύρου

    label_1 = tk.Label(  # Επιγραφή καλωσορίσματος
        window1,  # Σε ποιό παράθυρο θα εμφανιστεί
        text="Welcome back! Time to fly the Tello!",  # Το κέιμενο που θα αναγράφει
        font=("Helvetica", 36, "bold"),  # Γραμματοσειρά
        fg="white",  # Χρώμα γραμματοσειράς
        bg="black"  # Χρώμα φόντου
    )
    label_1.pack(pady=70)  # Δημιουργείται ένα περιθώριο 70 pixels  πάνω και κάτω από το label_1

    # Εμφάνιση της εικόνας του tello drone 
    try:
        image_pil = Image.open("tello-drone.png")  # Ανοίγει το αρχείο εικόνας "tello-drone.png" με τη βιβλιοθήκη PIL
        image_tk = ImageTk.PhotoImage(image_pil)  # Μετατρέπει την εικόνα από PIL σε αντικείμενο που καταλαβαίνει το Tkinter

        label_2 = tk.Label(window1, image=image_tk, bg="black")  # Δημιουργείται ένα label μέσα στο οποίο θα εμφανίζεται 
        # η εικόνα του tello drone
        label_2.image = image_tk  # Η εικόνα θα παραμείνει στο παράθυρο 
        label_2.pack()  # Τοποθετείται το label_2 μέσα στο παράθυρο 1
    except:  # Σε περίπτωση που η εικόνα του tello drone δεν είναι αποθηκευμένη στον ίδιο φάκελο 
        # με το πρόγραμμα δεν θα εμφανιστεί στο παράθυρο 1
        label_3 = tk.Label(  # Ετικέτα που καθοδηγεί για την αποθήκευση της εικόνας του tello drone 
            window1,  # Σε ποιό παράθυρο θα εμφανιστεί η ετικέτα label_3
            text="Αποθήκευσε τη φωτογραφία tello-drone στον ίδιο φάκελο με το πρόγραμμα για να εμφανιστεί",  # Το κείμενο της
            font=("Helvetica", 20, "bold"),  # Η γραμματοσειρά της ετικέτας
            fg="white",  # Χρώμα γραμμάτων 
            bg="black"  # Χρώμα φόντου
        )
        label_3.pack(pady=100)  # Δημιουργείται ένα περιθώριο 100 pixels πάνω και κάτω από το label_3

    create_folders()  # Καλείται η συνάρτηση που θα δημιουργείσει τους φακέλους Videos και Images

    # Κουμπί Images
    buttons(window1,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Images",  # Το κείμενο του κουμπιού
            10,2,20,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: open_folder(images_path),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.13*screen_width),int(0.7*screen_height))

    # Κουμπί για ζωντανή μετάδοση
    buttons(window1,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Live Stream",  # Το κείμενο του κουμπιού
            11,2,23,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "grey",  # Το χρώμα φόντου του κουμπιού
            "red",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            win2,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.4*screen_width),int(0.7*screen_height))

    # Κουμπί για να προγραμματίσεις το tello drone
    buttons(window1,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Create your program",  # Το κείμενο του κουμπιού
            18,2,19,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "grey",  # Το χρώμα φόντου του κουμπιού
            "red",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            win3,  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.11*screen_width),int(0.4*screen_height))
    
    # Κουμπί Script
    buttons(window1,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Script",  # Το κείμενο του κουμπιού
            16,2,19,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "grey",  # Το χρώμα φόντου του κουμπιού
            "red",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: open_folder(script_path),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.74*screen_width),int(0.4*screen_height))

    # Κουμπί Videos
    buttons(window1,  # Το παράθυρο στο οποίο θα εμφανιστεί το κουμπί
            "Videos",  # Το κείμενο του κουμπιού
            10,2,20,  # Πλάτος κουμπιού, ύψος κουμπιού, μέγεθος γραμματοσειράς
            "lightgrey",  # Το χρώμα φόντου του κουμπιού
            "green",  # Χρώμα φόντου όταν πατηθεί το κουμπί
            lambda: open_folder(videos_path),  # Η συνάρτηση που θα εκτελεστεί όταν πατηθεί το κουμπί
            int(0.7*screen_width),int(0.7*screen_height))

    window1.mainloop()  # Διατηρεί το παράθυρο 1 ανοιχτό μέχρι να το κλείσει ο χρήστης


if __name__ == '__main__':  # Με την έναρξη του προγράματος τρέχει πρώτα η συνάρτηση main
    main()