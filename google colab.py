#   lemons  yolo11
#   https://universe.roboflow.com/limonsayma/doktora_tez/dataset/13


# ----- Εισαγωγή κώδικα από το Roboflow -----
!pip install roboflow ultralytics # Εγκατάσταση βιβλιοθηκών 
from roboflow import Roboflow
rf = Roboflow(api_key="Put here your API key") # Δημιουργεί αντικείμενο Roboflow με το API key του χρήστη
project = rf.workspace("limonsayma").project("doktora_tez")  # Τοποθετούνται τα ονόματα του workspace και του project
version = project.version(13) # Φορτώνεται η 13η έκδοση του project
dataset = version.download("yolov11") # Λήψη του dataset έτοιμο για YOLOv11
# ----- Εισαγωγή κώδικα από το Roboflow -----

from ultralytics import YOLO  # Εισαγωγή της κλάσης YOLO

model = YOLO("yolo11n.pt")  # Θα εκπαιδευτεί το μοντέλο YOLOv11-nano

model.train(  # Εκπαίδευση
    data=dataset.location + "/data.yaml",  # Χρησιμοποίησε το data.yaml από το dataset
    epochs=100,  # Πλήθος εποχών εκπαίδευσης
    imgsz=640,  # Μέγεθος εισόδου εικόνας (640x640 pixels)
    batch=16)  # Πόσες εικόνες Θα επεξεργαστούν ανά βήμα εκπαίδευσης
from google.colab import files  # Εισαγωγή εργαλείου για κατέβασμα αρχείων από Colab
files.download("runs/detect/train/weights/best.pt")  # Λήψη του εκπαιδευμένου μοντέλου με όνομα best.pt

results = model.predict(
    source=dataset.location + "/valid/images",  # Εντοπισμός εικόνων
    conf=0.25,  # Ποσοστό εμπιστοσύνης 25%
    show=True)  # Επισήμανε τα αναγνωρισμένα αντικείμενα στις εικόνες