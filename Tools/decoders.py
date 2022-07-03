from string import punctuation

check = lambda x: ''.join([i for i in x if i not in ' '.join(punctuation).split()])

class Decoder:

    def __init__(self):
        self.morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 
            'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..',
            'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-',
            'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..',
            '9': '----.', 'А': '.-', 'Б': '-...', 'В': '.--',
            'Г': '--.', 'Д': '-..', 'Е': '.', 'Ж': '...-',
            'З': '--..', 'И': '..', 'Й': '.---', 'К': '-.-',
            'Л': '.-..', 'М': '--', 'Н': '-.', 'О': '---',
            'П': '.--.', 'Р': '.-.', 'С': '...', 'Т': '-',
            'У': '..-', 'Ф': '..-.', 'Х': '....', 'Ц': '-.-.',
            'Ч': '---.', 'Ш': '----', 'Щ': '--.-', 'Ъ': '.--.-.',
            'Ы': '-.--', 'Ь': '-..-', 'Э': '..-..', 'Ю': '..--', 'Я': '.-.-'
        }
        self.morse_reverse = {value: key for key, value in self.morse_dict.items()}

    def to_morse(self, string):
        return " ".join(self.morse_dict.get(i.upper()) for i in check(string))        

    def from_morse(self, string):
        return "".join(self.morse_reverse.get(i.upper()) for i in string.split())
