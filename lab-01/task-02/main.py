import random
import json
import os
from typing import List, Optional

ALPHABET = list(range(256))  # 0–255


class Rotor:
    def __init__(self, wiring: List[int], notch: Optional[int] = None) -> None:
        if len(wiring) != 256 or set(wiring) != set(ALPHABET):
            raise ValueError("Ротор должен содержать перестановку чисел 0–255")
        self.wiring = wiring
        self.position = 0
        self.notch = notch

    def set_position(self, pos: int) -> None:
        self.position = pos % 256

    def encode_forward(self, c: int) -> int:
        idx = (c + self.position) % 256
        encoded = self.wiring[idx]
        return (encoded - self.position) % 256

    def encode_backward(self, c: int) -> int:
        idx = (c + self.position) % 256
        letter = ALPHABET[idx]
        encoded = self.wiring.index(letter)
        return (encoded - self.position) % 256

    def step(self) -> bool:
        self.position = (self.position + 1) % 256
        return self.notch is not None and self.position == self.notch


class Reflector:
    def __init__(self, wiring: List[int]) -> None:
        if len(wiring) != 256 or set(wiring) != set(ALPHABET):
            raise ValueError("Рефлектор должен быть перестановкой 0–255")

        for i, c in enumerate(ALPHABET):
            mapped = wiring[i]
            if wiring[mapped] != c or mapped == c:
                raise ValueError(f"Некорректный рефлектор: {c} ↔ {mapped}")
        self.wiring = wiring

    def reflect(self, c: int) -> int:
        return self.wiring[c]


class EnigmaMachine:
    def __init__(self, rotors: List[Rotor], reflector: Reflector) -> None:
        self.rotors = rotors
        self.reflector = reflector

    def rotate_rotors(self) -> None:
        rotate_next = self.rotors[0].step()
        for i in range(1, len(self.rotors)):
            if rotate_next:
                rotate_next = self.rotors[i].step()
            else:
                break

    def encrypt_char(self, c: int) -> int:
        if c not in ALPHABET:
            return c

        self.rotate_rotors()

        for rotor in self.rotors:
            c = rotor.encode_forward(c)

        c = self.reflector.reflect(c)

        for rotor in reversed(self.rotors):
            c = rotor.encode_backward(c)

        return c

    def run(self, data: List[int]) -> List[int]:
        return [self.encrypt_char(c) for c in data]


def random_permutation() -> List[int]:
    arr = ALPHABET[:]
    random.shuffle(arr)
    return arr


def generate_config(filename: str) -> dict:
    rotors = [random_permutation() for _ in range(3)]
    notches = [random.randint(0, 255) for _ in range(3)]
    positions = [random.randint(0, 255) for _ in range(3)]

    nums = ALPHABET[:]
    random.shuffle(nums)
    reflector_map = [0] * 256
    for i in range(0, 256, 2):
        a, b = nums[i], nums[i + 1]
        reflector_map[a] = b
        reflector_map[b] = a

    config = {
        "rotors": rotors,
        "notches": notches,
        "positions": positions,
        "reflector": reflector_map,
    }

    with open(filename, "w") as f:
        json.dump(config, f)
    return config


def load_config(filename: str) -> dict:
    with open(filename, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    CONFIG_FILE = "lab-01/task-02/enigma_config.json"

    if os.path.exists(CONFIG_FILE):
        config = load_config(CONFIG_FILE)
        print("Конфигурация загружена из файла.")
    else:
        config = generate_config(CONFIG_FILE)
        print("Сгенерирована новая конфигурация и сохранена в файл.")

    rotors = [Rotor(w, notch=n) for w, n in zip(config["rotors"], config["notches"])]
    reflector = Reflector(config["reflector"])
    enigma = EnigmaMachine(rotors, reflector)

    for rotor, pos in zip(enigma.rotors, config["positions"]):
        rotor.set_position(pos)

    msg = [65, 66, 67, 255, 128]
    encrypted = enigma.run(msg)

    for rotor, pos in zip(enigma.rotors, config["positions"]):
        rotor.set_position(pos)
    decrypted = enigma.run(encrypted)

    print("Исходное:    ", msg)
    print("Зашифровано: ", encrypted)
    print("Расшифровано:", decrypted)
