from tkinter import *
from tkinter import simpledialog
from random import randint
from PIL import Image, ImageTk

class MultiplicationApp:
    
    def __init__(self, fenetre):
        self.username = None
        self.score = 0
        self.errors = 0
        self.meilleure_suite = 0
        self.current_streak = 0
        self.load_user()
        
        self.fenetre = fenetre
        fenetre.title("Jeu de Multiplications")

        self.tag = Label(fenetre, text=f"Vous jouez sur le compte de '✨{self.username}✨'", bg="MediumOrchid1")
        self.tag.pack(padx=50)

        self.thumb_up_img = Image.open("thumb_up.png")
        self.thumb_up_img = self.thumb_up_img.resize((50, 50), Image.LANCZOS)
        self.thumb_up_img = ImageTk.PhotoImage(self.thumb_up_img)

        self.thumb_down_img = Image.open("thumb_down.png")
        self.thumb_down_img = self.thumb_down_img.resize((50, 50), Image.LANCZOS)
        self.thumb_down_img = ImageTk.PhotoImage(self.thumb_down_img)

        self.thumb_label = Label(fenetre, image=None, bg="MediumOrchid1")
        self.thumb_label.pack(expand=1)

        self.a = randint(2, 9)
        self.b = randint(2, 9)
        self.reponse = self.a * self.b

        self.question = Label(fenetre, text=f"Combien font {self.a} x {self.b} ?", bg="MediumOrchid1")
        self.question.pack(expand=1)

        self.reponse_entry = Entry(fenetre)
        self.reponse_entry.pack(expand=1)

        self.bouton = Label(fenetre, text="Appuyez sur 'Entrée' pour vérifier", bg="MediumOrchid1")
        self.bouton.pack(expand=1)
        self.fenetre.bind("<Return>", self.rep)

        self.retry_button = Button(fenetre, text="Recommencer", command=self.retry)
        self.retry_button.pack(expand=1)

        self.score_label = Label(fenetre, text=f"Score: {self.score}/{self.errors+self.score}", bg="MediumOrchid1")
        self.score_label.pack(expand=1)

        self.streak_label = Label(fenetre, text=f"Meilleure Suite: {self.meilleure_suite}", bg="MediumOrchid1")
        self.streak_label.pack(expand=1)

        self.result_label = Label(fenetre, text="", bg="MediumOrchid1")
        self.result_label.pack(expand=1)
    
    def load_user(self):
        self.username = simpledialog.askstring("Connexion", "Entrez votre nom d'utilisateur:")
        if self.username is None or self.username.strip() == "":
            self.username = "Invité"
        self.load_stats()
        self.load_streak()
    
    def load_stats(self):
        try:
            with open(f"{self.username}_stats.txt", 'r') as f:
                stats = f.read().split("/")
                self.score = int(stats[0])
                self.errors = int(stats[1])
        except FileNotFoundError:
            pass
    
    def save_stats(self):
        with open(f"{self.username}_stats.txt", 'w') as f:
            f.write(f"{self.score}/{self.errors}")
    
    def load_streak(self):
        try:
            with open(f"{self.username}_streak.txt", 'r') as f:
                streak = f.read()
                self.meilleure_suite = int(streak)
        except FileNotFoundError:
            pass
    
    def save_streak(self):
        with open(f"{self.username}_streak.txt", 'w') as f:
            f.write(f"{self.meilleure_suite}")
    
    def rep(self, event):
        user_reponse = self.reponse_entry.get()
        try:
            user_reponse = int(user_reponse)
        except ValueError:
            self.result_label.config(text="Veuillez entrer un nombre valide", bg="MediumOrchid1")
            return
        
        if user_reponse == self.reponse:
            self.score += 1
            self.current_streak += 1
            if self.current_streak > self.meilleure_suite:
                self.meilleure_suite = self.current_streak
            result_text = "Correct !"
            thumb_img = self.thumb_up_img
            root.configure(bg='green')
        else:
            self.errors += 1
            result_text = f"Faux!!! La bonne réponse {self.a} x {self.b} est {self.reponse}"
            thumb_img = self.thumb_down_img
            root.configure(bg='red')
            self.current_streak = 0
            
        self.result_label.config(text=result_text, bg="MediumOrchid1")
        self.thumb_label.config(image=thumb_img)
        self.fenetre.update()
        
        self.save_stats()
        self.save_streak()
        self.a = randint(2, 9)
        self.b = randint(2, 9)
        self.reponse = self.a * self.b
        self.question.config(text=f"Combien font {self.a} x {self.b} ?", bg="MediumOrchid1")
        self.reponse_entry.delete(0, END)
        self.score_label.config(text=f"Score: {self.score}/{self.errors+self.score}", bg="MediumOrchid1")
        self.streak_label.config(text=f"Meilleure Suite: {self.meilleure_suite}", bg="MediumOrchid1")
    
    def retry(self):
        root.configure(bg='white smoke')
        self.score = 0
        self.errors = 0
        self.current_streak = 0
        self.thumb_label.config(image=None)
        self.save_stats()
        self.save_streak()
        self.score_label.config(text=f"Score: {self.score}/{self.errors+self.score}", bg="MediumOrchid1")
        self.result_label.config(text="", bg="MediumOrchid1")
        self.streak_label.config(text=f"Meilleure Suite: {self.meilleure_suite}", bg="MediumOrchid1")

root = Tk()
root.geometry('350x400')
app = MultiplicationApp(root)
root.mainloop()
