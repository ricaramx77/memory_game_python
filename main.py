

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

IMAGES_PATH = "images"
CARD_SIZE = (100, 100)
BACK_IMAGE_COLOR = "#444"

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memorama - Superheroes")
        self.images = self.load_images()
        self.cards = self.images * 2
        random.shuffle(self.cards)
        self.buttons = []
        self.flipped = []
        self.matched = set()
        self.back_image = self.create_back_image()
        self.set_window_size()
        self.create_board()

    def set_window_size(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        total_cards = len(self.cards)
        cols = min(6, total_cards)
        rows = (total_cards + cols - 1) // cols
        w = min(cols * (CARD_SIZE[0] + 10), screen_w)
        h = min(rows * (CARD_SIZE[1] + 10), screen_h)
        self.root.geometry(f"{w}x{h}")

    def load_images(self):
        files = [f for f in os.listdir(IMAGES_PATH) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        images = []
        for file in files:
            img_path = os.path.join(IMAGES_PATH, file)
            img = Image.open(img_path).resize(CARD_SIZE)
            images.append(ImageTk.PhotoImage(img))
        return images

    def create_back_image(self):
        img = Image.new("RGB", CARD_SIZE, BACK_IMAGE_COLOR)
        return ImageTk.PhotoImage(img)

    def create_board(self):
        total_cards = len(self.cards)
        cols = min(6, total_cards)
        rows = (total_cards + cols - 1) // cols
        for i in range(total_cards):
            btn = tk.Button(self.root, width=CARD_SIZE[0], height=CARD_SIZE[1], image=self.back_image,
                            command=lambda idx=i: self.flip_card(idx))
            r = i // cols
            c = i % cols
            btn.grid(row=r, column=c, padx=5, pady=5)
            self.buttons.append(btn)

    def flip_card(self, idx):
        if idx in self.matched or idx in self.flipped:
            return
        self.buttons[idx].config(image=self.cards[idx])
        self.flipped.append(idx)
        if len(self.flipped) == 2:
            self.root.after(1000, self.check_match)

    def check_match(self):
        if len(self.flipped) != 2:
            return
        i1, i2 = self.flipped[:2]
        if self.cards[i1] == self.cards[i2]:
            self.matched.add(i1)
            self.matched.add(i2)
            if len(self.matched) == len(self.cards):
                messagebox.showinfo("¡Felicidades!", "¡Has encontrado todos los pares!")
                self.root.quit()
        else:
            self.buttons[i1].config(image=self.back_image)
            self.buttons[i2].config(image=self.back_image)
        self.flipped = []


if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
