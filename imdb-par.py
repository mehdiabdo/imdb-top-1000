import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import font
from tkinter import messagebox
import os

# initializing app
root = Tk()
root.title("IMDB PARSER")
root.resizable(False, False)
root.geometry("300x150+450+150")
root.configure(bg="white")

year = ""


# url function
def get_url():
    txt = txt_var.get()
    global year
    year = txt
    if year == "" or year == "0": error()
    else:
        entry.delete(0, "end")
        if year == "" or year == "0":
            error()
        else:
            try:
                movies = list()
                for i in range(1, 1001, 50):
                    url = f"https://www.imdb.com/search/title/?title_type=feature&year={year}-01-01,{year}-12-31&start={i}&ref_=adv_nxt"
                    req = requests.get(url)
                    soup = BeautifulSoup(req.content, "html.parser")
                    cons = soup.findAll(class_='lister-item-content')
                    for item in cons:
                        name = item.h3.a.text

                        if item.strong is not None:
                            rating = item.strong.text
                        else:
                            rating = 0
                        movies.append((name, float(rating)))
                movies_sor = sorted(movies, key=lambda x: x[1], reverse=True)
                with open("movies.txt", "a") as file:
                    for mo in movies_sor:
                        if mo[1] != 0:
                            file.write(f"{mo[0]} : {mo[1]}\n")
                        else:
                            file.write(f"{mo[0]} : Not yet rated\n")
                    file.write("\n")

            except:
                print("Error getting right request")

        messagebox.showinfo("Done", "Done!!!\nchck the file named\"movies.txt\" in the same directory")
def error():
    messagebox.showerror("Error","Please enter the year")

# label
bold_font = font.Font(family="Georgia", size=17, weight="bold")
Label(text="Enter the year", font=bold_font, bg="white", fg="black").pack()

# Entry
txt_var = StringVar()
entry = Entry(root, textvariable=txt_var, width=10, border=5, bg="white")
entry.pack(pady=10)
# Button
b_font = font.Font(family="Comic Sans MS", size=15, weight="bold")
Button(text="Parse", font=b_font, bg="#F5C518", command=get_url).pack(pady=7)
# running app
root.mainloop()
