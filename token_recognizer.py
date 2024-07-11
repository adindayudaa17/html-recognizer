import sys

class DFATokenRecognizer:
    def __init__(self):
        # Mendefinisikan state penerimaan untuk tag HTML
        self.accepting_states = {
            "<html>": True,
            "</html>": True,
            "<head>": True,
            "</head>": True,
            "<title>": True,
            "</title>": True,
            "<body>": True,
            "</body>": True,
            "<h1>": True,
            "</h1>": True,
            "<p>": True,
            "</p>": True,
            "<HTML>": True
        }
        
    def recognize(self, token):
        # Memeriksa apakah token berada di state penerimaan
        return self.accepting_states.get(token, False)

def main():
    # Membuat instance dari DFATokenRecognizer
    recognizer = DFATokenRecognizer()
    # Membaca input dari terminal
    for line in sys.stdin:
        token = line.strip()  # Menghapus spasi di awal dan akhir baris
        if recognizer.recognize(token):
            print(f"{token} Accepted")  # Mencetak "Accepted" jika token diterima
        else:
            print(f"{token} Rejected")  # Mencetak "Rejected" jika token ditolak

if __name__ == "__main__":
    main()
