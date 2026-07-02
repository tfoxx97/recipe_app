import pdfplumber

class Parser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.extract_text_from_pdf(pdf_path=self.pdf_path)

    @staticmethod
    def calc_accuracy_between_font_lines(prev, next, accuracy=90):
        accuracy_test = (1 - (abs(prev - next) / next)) * 100
        if accuracy_test >= accuracy:
            return True
        else:
            return False

    # I would like this function to return a list of chunks(lists of lines) that are grouped together based on their font size. 
    # I want to pop the first item, then iterate through data and compare the font size of the line to the previous line.
    #  If the font size is similar enough, then I want to add it to the current chunk. 
    # If not, then I want to start a new chunk with the current line added first. 
    # I want to continue this process until all lines have been processed.
    def extract_text_from_pdf(self, pdf_path: str):
        chunks = []
        current_chunk = []
        data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for i in range(len(pdf.pages)):
                text = pdf.pages[i].extract_text_lines()
                for i, txt in enumerate(text, start=1):
                    if i >= 1:
                        font_size = txt['chars'][0]['size']
                        data.append({txt['text']: font_size})

        # Group lines by similar font size into chunks
        # Convert data to list of tuples for easier handling: [(line, size), ...]
        data_tuples = [(list(d.keys())[0], list(d.values())[0]) for d in data]

        if not data_tuples:
            return []

        prev_line, prev_size = data_tuples.pop(0)
        current_chunk = [prev_line]

        for line, size in data_tuples:
            if self.calc_accuracy_between_font_lines(prev_size, size) or prev_size > size:
                current_chunk.append(line)
                prev_size = size # move to next line and compare to current line
            elif size > prev_size:
                chunks.append(current_chunk)
                current_chunk = [line]
                prev_size = size

        if current_chunk:
            chunks.append(current_chunk)

        return chunks