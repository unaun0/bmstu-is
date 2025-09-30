import string
from typing import List, Union

ALPHABET: str = string.ascii_uppercase

class Rotor:
    def __init__(self, wiring: str, notch: Union[str, None] = None) -> None:
        if len(wiring) != 26 or set(wiring) != set(ALPHABET):
            raise ValueError("Ротор должен содержать все 26 уникальных букв A–Z")
        self.wiring: str = wiring
        self.position: int = 0
        self.notch: Union[str, None] = None
        if notch is not None:
            self.set_notch(notch)

    def set_notch(self, notch: str) -> None:
        if notch not in ALPHABET:
            raise ValueError("Notch должен быть буквой A-Z")
        self.notch = notch

    def set_position(self, pos: Union[int, str]) -> None:
        if isinstance(pos, str):
            pos = ALPHABET.index(pos.upper())
        self.position = pos % 26

    def encode_forward(self, c: str) -> str:
        idx: int = (ALPHABET.index(c) + self.position) % 26
        encoded: str = self.wiring[idx]
        return ALPHABET[(ALPHABET.index(encoded) - self.position) % 26]

    def encode_backward(self, c: str) -> str:
        idx: int = (ALPHABET.index(c) + self.position) % 26
        letter: str = ALPHABET[idx]
        encoded: str = ALPHABET[self.wiring.index(letter)]
        return ALPHABET[(ALPHABET.index(encoded) - self.position) % 26]

    def step(self) -> bool:
        self.position = (self.position + 1) % 26
        return self.notch is not None and ALPHABET[self.position] == self.notch


class Reflector:
    def __init__(self, wiring: str) -> None:
        if len(wiring) != 26 or set(wiring) != set(ALPHABET):
            raise ValueError("Рефлектор должен содержать все 26 уникальных букв A–Z")

        for i, c in enumerate(ALPHABET):
            mapped = wiring[i]
            j = ALPHABET.index(mapped)
            if wiring[j] != c or mapped == c:
                raise ValueError(f"Некорректный рефлектор: {c}↔{mapped}")

        self.wiring: str = wiring

    def reflect(self, c: str) -> str:
        return self.wiring[ALPHABET.index(c)]


class EnigmaMachine:
    def __init__(self, rotors: List[Rotor], reflector: Reflector) -> None:
        self.rotors: List[Rotor] = rotors
        self.reflector: Reflector = reflector

    def rotate_rotors(self) -> None:
        rotate_next: bool = self.rotors[0].step()
        for i in range(1, len(self.rotors)):
            if rotate_next:
                rotate_next = self.rotors[i].step()
            else:
                break

    def encrypt_char(self, c: str) -> str:
        if c not in ALPHABET:
            return c

        self.rotate_rotors()

        for rotor in self.rotors:
            c = rotor.encode_forward(c)

        c = self.reflector.reflect(c)

        for rotor in reversed(self.rotors):
            c = rotor.encode_backward(c)

        return c

    def run(self, text: str) -> str:
        return ''.join(self.encrypt_char(c) for c in text.upper())


if __name__ == "__main__":
    rotor_I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch="R")
    rotor_II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", notch="F")
    rotor_III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", notch="W")

    reflector_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    enigma = EnigmaMachine([rotor_I, rotor_II, rotor_III], reflector_B)
# 0 - 256
# заполнение случайно загоняем в файл для проверки + начальные установки _ зашифровка
    rotor_I.set_position("Q")
    rotor_II.set_position("U")
    rotor_III.set_position("C")

    msg = "ARBUZIKI"
    encrypted = enigma.run(msg)

    rotor_I.set_position("Q")
    rotor_II.set_position("U")
    rotor_III.set_position("C")

    decrypted = enigma.run(encrypted)

    print("Исходное:    ", msg)
    print("Зашифровано: ", encrypted)
    print("Расшифровано:", decrypted)
