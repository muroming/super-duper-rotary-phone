import os

import face_recognition
import matplotlib.pyplot as plt
import numpy as np

import cv2

encodings = []
names = []
person_faces_amount = 200
percentage_to_auhtorize = 0.8


def extract_images_from_video(label, video_path, save_path):
    cap = cv2.VideoCapture(video_path)
    ind = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imsave(os.path.join(save_path, label + str(ind)), frame)
        ind += 1
        print('Saving %s' % (label + str(ind)))


def extract_face_from_image(image, detection_type=0):
    """
    Params:
        image - RGB 3 dim array
    Output:
        face encoding: 1-dim array (1, 128) or empty if face not found
    """
    encoding = []
    face = face_recognition.face_locations(image, detection_type)
    if (len(face) != 0):
        encoding = face_recognition.face_encodings(image, face)

    return encoding


def add_person(label, dataset_path, detection_type=0):
    imgs = []
    for path in os.listdir(dataset_path):
        if label in path:
            img = cv2.imread(os.path.join(dataset_path, path))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgs.append(img)

    encodings = []
    for i, img in enumerate(imgs):
        faces = face_recognition.face_locations(img, detection_type)
        encoding = face_recognition.face_encodings(img, faces)
        encodings.append(encoding)
        print("Encodings for %s %i/%i" % (label, i + 1, len(imgs)))

    encodings = np.array(encodings)
    encodings = np.reshape(encodings, (encodings.shape[0], 128))
    np.save('./encodings/%s.npy' % label, encodings)

    print("Done")


def load_encodings(path):
    global encodings
    global names
    for path in os.listdir('./encodings'):
        enc = np.load(os.path.join('./encodings', path))
        name = path.split('.')[0]
        for e in enc:
            encodings.append(e)
            names.append(name)


def validate_person(image, detection_type=0):  # Assuming image is RGB
    if len(encodings) == 0:
        raise RuntimeError("No encodings loaded")

    faces = face_recognition.face_locations(image, detection_type)
    encoding = face_recognition.face_encodings(image, faces)

    ns = []
    name = "unknown"
    for enc in encoding:
        matches = face_recognition.compare_faces(encodings, enc)

        if np.any(matches):
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = names[i]
                counts[name] = counts.get(name, 0) + 1

            if max(counts.values()) >= person_faces_amount * percentage_to_auhtorize:
                name = max(counts, key=counts.get)

        ns.append(name)

    for ((top, right, bottom, left), name) in zip(faces, ns):
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

    return image

# load_encodings('./encodings')
# print("D")
#
# cap = cv2.VideoCapture(0)
# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     frame = validate_person(frame)
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()
