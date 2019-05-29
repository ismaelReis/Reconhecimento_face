import numpy as np
import cv2
import face_recognition
import datetime
from matplotlib import pyplot as plt


plt.rcParams['figure.figsize'] = (224, 224)

face_cascade = cv2.CascadeClassifier('modelo/haarcascade_frontalface_default.xml')

imagem_rosto = cv2.imread('snoop.jpg')

cap = cv2.VideoCapture('video.mp4')



# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
out = cv2.VideoWriter('output_media.avi',fourcc, 20, (640,360))

#coisas do face
face_encoding = face_recognition.face_encodings(imagem_rosto)[0]

faces_conhecidas = [
    face_encoding
]

face_locations = []
emCena = False
segundos = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
       # frame = cv2.blur(frame, ( 100, 100))#cv2.flip(frame,0)
        imagem2 = frame
        rgb_frame = imagem2[:, :, ::-1]
        
        #Detecta todas as faces em uma imagem
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        #aqui vai a loucura
        face_names = []
        for face_encoding in face_encodings:
           # Compara a imagem de busca com todos os rostos existentes na imagem atual.
           match = face_recognition.compare_faces(faces_conhecidas, face_encoding,tolerance=0.60)
        
        segundos+=1
       
        name = "Desconhecido"
        if match != [False]:
          name = "Snoop Dogg"
          if emCena == False:
              print('['+str(datetime.timedelta(seconds=round(segundos/20,0)))+'] Entrou em cena')
              emCena = True
        else:
            if emCena == True:
                print('['+str(datetime.timedelta(seconds=round(segundos/20,0)))+'] Saiu de cena')
                print('')
                emCena = False
              
        
        face_names.append(name)
        
        #Aplica a label nas faces encontradas
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if not name:
               continue
        
            #Desenha um retangulo  em torno da face
            cv2.rectangle(imagem2, (left, top), (right, bottom), (0, 127, 255), 2)
            
            #Inclui o nome da face identificada
            cv2.rectangle(imagem2, (left, bottom - 25), (right, bottom), (0, 127, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(imagem2, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        

        #fim da loucura
        
        

        cv2.imshow('Video',imagem2)
         # write the flipped frame
        out.write(imagem2)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()