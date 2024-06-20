import pickle
import glob
import os
import face_recognition

class EncodeImage:
    def __init__(self):
        self.encodes = []
        self.encodeId = []
        try:
            files = glob.glob('./static/*.pkl');
            for file in files:
                face = EncodeImage.load(file);
                if(face is not False): 
                    self.encodes.append(face)
                    self.encodeId.append(os.path.splitext(os.path.basename(file))[0])
                
        except Exception as e:
            print(e)
            return False
    
    def dump(self, encode, id):
        try:

            dumpFile = open(f'./static/{id}.pkl', 'wb')
            pickle.dump(encode, dumpFile)
            self.encodes.append(encode)
            self.encodeId.append(id)
            dumpFile.close()
            return True
        except Exception as e:
            print(e)
            return False
    
    def search(self, face_encodings):
        try:
            if(len(face_encodings)):          
                face_distances = face_recognition.face_distance(self.encodes, face_encodings[0])
                if(len(face_distances)):
                    matches = list(enumerate(face_distances));
                    matches = sorted(matches, key=lambda x: x[1])[0]
                    if(matches[1] < 0.5):
                        return self.encodeId[matches[0]]
                     
            return False
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def load(file):
        try:
            loadFile = open(file, 'rb')
            data = pickle.load(loadFile)
            loadFile.close()
            return data
        except Exception as e:
            print(e)
            return False
           
encode_image = EncodeImage();