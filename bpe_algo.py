import json
import re

class Encoder:
    def __init__(self):
        self.encoder = {}
        self.decoder = {}
        self.byte_encode = {}
        self.byte_decode = {}
        self.bpe_ranks = {}

    @staticmethod
    def rune_slice_from_string(s):
        return list(s)

    @classmethod
    def get_encoder(cls, filename_encoder, filename_bpe):
        encoder_instance = cls()

        with open(filename_encoder, 'r', encoding='utf-8') as file:
            f_encoder = json.load(file)

        encoder_instance.encoder = f_encoder
        encoder_instance.decoder = {v: k for k, v in f_encoder.items()}

        with open(filename_bpe, 'r', encoding='utf-8') as file2:
            f_bpe = file2.read().split("\n")[1:]
        
        bpe_merges = {}
        for i, merge_str in enumerate(f_bpe):
            s = merge_str.split()
            if len(s) == 2:
                bpe_merges[(s[0], s[1])] = i

        encoder_instance.bpe_ranks = bpe_merges

        # Simplified byte encoding and decoding (this part needs more attention)
        for i in range(256):
            encoder_instance.byte_encode[chr(i)] = chr(i)
            encoder_instance.byte_decode[chr(i)] = chr(i)

        return encoder_instance

    @staticmethod
    def get_pairs(word):
        runes = list(word)
        return [(runes[i-1], runes[i]) for i in range(1, len(runes))]

    def bpe(self, token):
        word = list(token)
        pairs = self.get_pairs(token)
        iteration_count = 0  # Add a counter

        while pairs and iteration_count < 1000:  # Limit to 1000 iterations
            print("Word:", word)  # Debug print
            print("Pairs:", pairs)  # Debug print

            bigram_exists = False
            for pair in pairs:
                if pair in self.bpe_ranks:
                    bigram_exists = True
                    first, second = pair
                    new_word = []
                    i = 0
                    while i < len(word):
                        if word[i] == first and i+1 < len(word) and word[i+1] == second:
                            new_word.append(first + second)
                            i += 2
                        else:
                            new_word.append(word[i])
                            i += 1
                    word = new_word
                    break
            if not bigram_exists:
                break
            pairs = self.get_pairs("".join(word))
            iteration_count += 1  # Increment the counter

        return " ".join(word)

    def encode(self, text):
        tokens = re.findall(r'\w+|\s+|\S', text)
        bpe_tokens = []
        for token in tokens:
            encoded = "".join([self.byte_encode.get(r, r) for r in token])
            bpe_encoded = self.bpe(encoded)
            for s in bpe_encoded.split():
                bpe_tokens.append(self.encoder.get(s, s))
        return bpe_tokens

    def decode(self, tokens):
        text = "".join([self.decoder.get(token, token) for token in tokens])
        decoded = "".join([self.byte_decode.get(r, r) for r in text])
        return decoded

if __name__ == "__main__":
    encoder = Encoder.get_encoder("C:\\Users\\admin\\Documents\\Codes\\Python\\BPE-Encoder\\encoder.json", "C:\\Users\\admin\\Documents\\Codes\\Python\\BPE-Encoder\\vocab.bpe")
    encoded_text = encoder.encode("hello world! This is a test string.")
    print("Encoded:", encoded_text)
    decoded_text = encoder.decode(encoded_text)
    print("Decoded:", decoded_text)
