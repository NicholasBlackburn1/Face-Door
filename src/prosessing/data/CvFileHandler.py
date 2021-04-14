"""
This class is for Handling Cv Files and etc
"""


class CvFileHandler():

# handles adding data to lists so i can tuppleize it

    # sends Person count info to subscribers


    def send_person_count(self,face_encodings, sock,logging):
        logging.info("[SOCKET PERSON] sending Seen Persons")
        sock.send_string("FACE")
        sock.send_json({"face": str(len(face_encodings))})
        logging.info("[SOCKET PERSON] Sent Seen Persons")

    
    def send_face_compare(self,face_distance, sock,logging):
        logging.info("[SOCKET FACEMATCH] sending Seen Persons")
        sock.send_string("COMPARE")
        sock.send_json({"compare": face_distance})
        logging.info("[SOCKET FACEMATCH] Sent Seen Persons")

    # sends person name to subsecriber
    def send_person_name(sock, name,logging):
        logging.info("[SOCKET Name] Sending person seen name")
        sock.send_string("NAME")
        sock.send_json({"name": name})
        logging.info("[SOCKET Name] Sent Person name")

   