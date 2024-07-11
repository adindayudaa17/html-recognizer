import sys
from token_recognizer import DFATokenRecognizer

class PDAHTMLParser:
    def __init__(self):
        # Inisialisasi stack untuk melacak tag HTML
        self.stack = []

        # Mendefinisikan tag pembuka dan penutup yang valid
        self.valid_tags = {
            "html": "/html",
            "head": "/head",
            "title": "/title",
            "body": "/body",
            "h1": "/h1",
            "p": "/p"
        }

        # Membuat instance dari DFATokenRecognizer
        self.token_recognizer = DFATokenRecognizer()

    def parse(self, line, isHead):
        # Menandai apakah tag <head> ada dalam dokumen
        isHeadExist = False
        i = 0  # Inisialisasi indeks karakter
        while i < len(line):
            if line[i] == '<':  # Jika menemukan karakter pembuka tag
                j = i + 1
                # Cari karakter penutup tag
                while j < len(line) and line[j] != '>':
                    j += 1
                if j < len(line):
                    tag = line[i+1:j]  # Ambil nama tag tanpa '<' dan '>'
                    full_tag = f"<{tag}>"  # Bangun kembali tag lengkap
                    # Memeriksa apakah tag dikenali oleh DFA Token Recognizer
                    if not self.token_recognizer.recognize(full_tag):
                        return f"{full_tag} Rejected", isHeadExist
                    # Jika tag bukan penutup
                    if not tag.startswith('/'):
                        if tag in self.valid_tags:  # Jika tag valid
                            # Periksa aturan struktur HTML
                            if tag == "html" and self.stack:
                                return f"{full_tag} Rejected - <html> should be the root tag", isHeadExist
                            if tag == "head" and ("html" not in self.stack or "body" in self.stack):
                                return f"{full_tag} Rejected - <head> should be inside <html> and before <body>", isHeadExist
                            if tag == "body" and ("html" not in self.stack or not isHead):
                                return f"{full_tag} Rejected - <body> should be inside <html> and after <head>", isHeadExist
                            if tag == "title" and "head" not in self.stack:
                                return f"{full_tag} Rejected - <title> should be inside <head>", isHeadExist
                            # Tambahkan tag ke stack
                            self.stack.append(tag)
                            print(f"Tag: <{tag}> - Stack: {self.stack}")
                        else:
                            return f"<{tag}> Rejected", isHeadExist
                    else:  # Jika tag penutup
                        if self.stack and self.valid_tags.get(self.stack[-1]) == tag:
                            if tag == "/head":
                                isHeadExist = True
                            # Hapus tag pembuka dari stack
                            self.stack.pop()
                            print(f"Tag: <{tag}> - Stack: {self.stack}")
                        else:
                            return f"<{tag}> Rejected", isHeadExist
                i = j  # Lanjutkan ke karakter setelah tag
            i += 1  # Lanjutkan ke karakter berikutnya
        # Jika dokumen valid, kembalikan status diterima
        return "Accepted", isHeadExist

    def finalize(self):
        # Jika stack tidak kosong, berarti ada tag pembuka tanpa penutup
        if self.stack:
            return "Rejected"
        return "Accepted"

def main():
    # Membuat instance dari PDAHTMLParser
    parser = PDAHTMLParser()
    isHead = False

    for line in sys.stdin:
        line = line.strip()  # Menghapus spasi di awal dan akhir baris
        result, isHead = parser.parse(line, isHead)  # Parse setiap baris dalam file
        if result != "Accepted":
            print(result)
            return  # Jika ada baris yang ditolak, hentikan parsing
    final_result = parser.finalize()  # Periksa akhir stack
    print(final_result)  # Tampilkan hasil akhir

if __name__ == "__main__":
    main()
