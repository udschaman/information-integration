from tkinter import *
import collections
import webbrowser
import gui_dicts
import wikipedia as wiki
from tkinter.ttk import *

#import io
import base64
from urllib.request import urlopen

def get_input():
    get_wikipedia()
    get_gm_image()
    
def get_wikipedia():
    city = city_entry.get()
    state = state_options.get()
    try:
        page = wiki.summary(city + ", " + state, auto_suggest=False)
    except:
        page = wiki.summary(state, auto_suggest=False)
    wikipedia_text.delete(1.0, END)
    wikipedia_text.insert(1.0, page)

def get_gm_image():
    url_state = state_options.get().replace(" ", "+")
    url_city = city_entry.get().replace(" ", "+")
	
    image_url = "https://maps.googleapis.com/maps/api/staticmap?center=" + url_city + "," + url_state + "&size=640x480&key=AIzaSyCF4AO5iTPfrK-4X0uWVb_7ztpP_Ze9r7Q"

    image_byt = urlopen(image_url).read()
    image_b64 = base64.encodestring(image_byt)
    gm_image = PhotoImage(data=image_b64)
    googlemaps_image.config(image=gm_image)
    googlemaps_image.image = gm_image


def open_googlemaps():
    url_state = state_options.get().replace(" ", "+")
    url_city = city_entry.get().replace(" ", "+")
    url = "https://www.google.de/maps/place/" + url_city + "," + url_state
    webbrowser.open(url,True)

##Master-Frame
root = Tk()
root.title("UFO sightings")

screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (screen_width, screen_height))

##Frames for grids
entry_frame = Frame(root)
entry_frame.grid(row=0, column=0)

googlemap_frame = Frame(root)
googlemap_frame.grid(row=1, column=1)

sightings_frame = Frame(root)
sightings_frame.grid(row=0, column=1)

wikipedia_frame = Frame(root)
wikipedia_frame.grid(row=1, column=0)

#input grid
input_name = Label(entry_frame, text="Input for sightings", font="Arial 14 underline")
input_name.grid()

##city grid
city_name = Label(entry_frame, text="City:", font="Arial 14")
city_name.grid()

city_entry = Entry(entry_frame, width=20)
city_entry.grid()

##state grid
STATE_OPTIONS = collections.OrderedDict(sorted(gui_dicts.state_dict.items()))

state_options = StringVar(entry_frame)

state_name= Label(entry_frame, text="State:", font="Arial 14")
state_name.grid()

state_option_menu = OptionMenu(entry_frame, state_options, *STATE_OPTIONS.values())
state_option_menu.grid()

#area grid
area_options = StringVar(entry_frame)

area_name= Label(entry_frame, text="Airports in range of km:", font="Arial 14")
area_name.grid()

area_option_menu = OptionMenu(entry_frame, area_options, *gui_dicts.area_range)
area_option_menu.grid()

#shapes grid
shapes_options = StringVar(entry_frame)

shapes_name= Label(entry_frame, text="Shape:", font="Arial 14")
shapes_name.grid()

shapes_option_menu = OptionMenu(entry_frame, shapes_options, *gui_dicts.shapes_list)
shapes_option_menu.grid()

#date grid
date_name = Label(entry_frame, text="Date:", font="Arial 14")
date_name.grid()

date_entry = Entry(entry_frame, width=20)
date_entry.grid()
date_entry.insert(0, "DD.MM.YYYY")

#run button grid
run_button_name= Label(entry_frame, text="Start execution", font="Arial 14 underline")
run_button_name.grid()

run_button = Button(entry_frame, text="Run", width=15, command=get_input)
run_button.grid( columnspan=2)

#sightings grid
sightings_name = Label(sightings_frame, text="All Sightings for the City:", font="Arial 14")
sightings_name.grid()

sightings = Treeview(sightings_frame)
sightings["columns"]=("City", "State", "Shape", "Duration", "Summary", "URL")
sightings.heading("#0", text="Date")
sightings.column("#0", width=150)
sightings.heading("City", text="City")
sightings.column("City", width=75)
sightings.heading("State", text="State")
sightings.column("State", width=50)
sightings.heading("Shape", text="Shape")
sightings.column("Shape", width=75)
sightings.heading("Duration", text="Duration")
sightings.column("Duration", width=75)
sightings.heading("Summary", text="Summary")
sightings.column("Summary", width=300)
sightings.heading("URL", text="URL")
sightings.column("URL", width=100)

for i in range(0, 100):
   sightings.insert("", "end", text="20.09.1990 04:32", values=("New York", "NY", "circle", "1 second" , "i saw a fucking ufo. they are going to kill us all", i))

sightings.grid()

#wikipedia grid
wikipedia_article= Label(wikipedia_frame, text="Wikipedia Article for the City or the State", font="Arial 14")
wikipedia_article.grid()

wikipedia_text = Text(wikipedia_frame, font="Arial 14", wrap=WORD)
wikipedia_text.grid()

#googlemap grid
googlemaps = Label(googlemap_frame, text="Google Maps", font="Arial 14")
googlemaps.grid()

gm_image = None
googlemaps_image = Label(googlemap_frame, image=gm_image)
googlemaps_image.image = gm_image
googlemaps_image.grid()

run_button = Button(googlemap_frame, text="Interactive Map", width=15, command=open_googlemaps)
run_button.grid()
root.mainloop()
