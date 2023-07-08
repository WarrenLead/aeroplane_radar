from guizero import App, Drawing, Text, TextBox
from time import sleep

#Lat +/- .07 = 5 miles
#Long +/- .086 = 5 miles @ -32

a = (-32.78074, 152.08868) # Home
b = (-32.751687, 151.99168) # Home
#b = (-32.70912, 152.00304) # loc 1 Left Top
#b = (-32.70912, 152.17432) # loc 2 Right Top
#b = (-32.85236, 152.00304) # loc 3 Left Bot
#b = (-32.85236, 152.17432) # loc 4 Right Bot

ee = 3490
e = 2919
x = int(abs((a[1] - b[1]) * e - 250))
y = int(abs((a[0] - b[0]) * ee + 250 ))

print (x, y)
print (a[0] - b[0], a[1] - b[1])

aa = App()
#top = Text(aa, "top_text")
d = Drawing(aa, width="fill", height="fill")
id = d.oval(0, 0, 500, 500, color="grey", outline=True, outline_color="black")
id = d.oval(50, 50, 450, 450, color="grey", outline=True, outline_color="black")
id = d.oval(100, 100, 400, 400, color="grey", outline=True, outline_color="black")
id = d.oval(150, 150, 350, 350, color="grey", outline=True, outline_color="black")
id = d.oval(200, 200, 300, 300, color="grey", outline=True, outline_color="black")
#d.oval(x-5, y-5, x+5, y+5, color="white", outline=True)#PLANE
id= d.oval(245, 245, 255, 255, color="red", outline=True)#US
#d.triangle(240, 255, 250, 240, 260, 255, color="black")
id = d.line(0, 250, 500, 250, color="red", width=1)
id = d.line(250, 0, 250, 500, color="red", width=1)
id = d.text(250, 1, "N", font="times new roman", size=14)
id = d.text(250, 51, "4", font="times new roman", size=14)
id = d.text(250, 101, "3", font="times new roman", size=14)
id = d.text(250, 151, "2", font="times new roman", size=14)
id = d.text(250, 201, "1", font="times new roman", size=14)
id = d.text(230, 250, "Test", font="times new roman", size=14)

aa.update()
d.delete(id)

for i in range(90):
        id = d.oval(x-5, y-5, x+5, y+5, color="white", outline=True)#PLANE
        x += 5
        sleep (1)
        d.delete(id-1)
        aa.update()


