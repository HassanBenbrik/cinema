from tkinter import ttk, filedialog, messagebox
from tkinter import *
from tkinter import colorchooser
import os
import sqlite3
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import re
import webbrowser
import socket
from io import BytesIO
import datetime
from PIL import Image, ImageTk
from zipfile import ZipFile
import winsound
import threading
import sys
# import concurrent.futures

# with concurrent.futures.ThreadPoolExecutor() as executor:
	# secs = [5, 4, 3, 2, 1]
	# results = executor.map(do_something, secs)

# try:
# except ModuleNotFoundError:
# 	os.startfile("READ ME!.txt")
# 	if messagebox.askokcancel("Install Modules", "Do you want to install required modules ?"):
# 		os.system('cmd /k "pip install Pillow bs4 requests"')
# 	else:
# 		exit()

os.makedirs("Movies Images/", exist_ok=True)

os.makedirs("Deleted Movies/", exist_ok=True)


Profile = {1 : ""}

field = "name"
etat_command = True
results = ""
the_full_movie_s_name = []
etat_replace_movies = False
id_Select1 = name_Select1 = year_Select1 = rating_Select1 = language_Select1 = movie_other_name_Select1 = picture_Select1 = story_Select1 = trailer_Select1 = the_type_Select1 = watched_Select1 = linkEgybest_Select1 = linkYTS_Select1 = actors_Select1 = id_Select2 = name_Select2 = year_Select2 = rating_Select2 = language_Select2 = movie_other_name_Select2 = picture_Select2 = story_Select2 = trailer_Select2 = the_type_Select2 = watched_Select2 = linkEgybest_Select2 = linkYTS_Select2 = actors_Select2 = id_Select_1 = name_Select_1 = year_Select_1 = rating_Select_1 = language_Select_1 = movie_other_name_Select_1 = picture_Select_1 = story_Select_1 = trailer_Select_1 = the_type_Select_1 = watched_Select_1 = linkEgybest_Select_1 = linkYTS_Select_1 = actors_Select_1 = id_Select_2 = name_Select_2 = year_Select_2 = rating_Select_2 = language_Select_2 = movie_other_name_Select_2 = picture_Select_2 = story_Select_2 = trailer_Select_2 = the_type_Select_2 = watched_Select_2 = linkEgybest_Select_2 = linkYTS_Select_2 = actors_Select_2 = ""
etat_get_watched_movies = True



chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

fenetre = Tk()
fenetre.title("Movies")
fenetre.geometry("1110x720")
fenetre.minsize(1110, 720)
fenetre.maxsize(1110, 720)

def create_database():
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS Movies(id INTEGER, name TEXT, year INTEGER, rating TEXT, language TEXT, movie_other_name TEXT, picture TEXT, story TEXT, trailer TEXT, the_type TEXT, watched TEXT, linkEgybest TEXT, linkYTS TEXT, actors TEXT)")
	conn.commit()
	conn.close()

def lengthSelect():
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	select = list(cursor.execute("SELECT * FROM Movies"))
	lenSelect = len(select)
	conn.close()
	return lenSelect

def watched_movies():
	nbr_of_watched_movies = 0
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	la_selection = cursor.execute("SELECT watched FROM Movies")
	for watched_movie in list(la_selection):
		if "True" in watched_movie:
			nbr_of_watched_movies += 1
	conn.close()
	print("Watched movies :", nbr_of_watched_movies)
	return nbr_of_watched_movies

def get_watched_movies():
	global etat_get_watched_movies
	for i in tree.get_children():
		tree.delete(i)
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	if etat_get_watched_movies:
		selection = list(cursor.execute("SELECT * FROM Movies WHERE watched='True' ORDER BY id DESC"))
	else:
		selection = list(cursor.execute("SELECT * FROM Movies WHERE watched='False' ORDER BY id DESC"))
	for row in selection:
		tree.insert("", END, value=row, tags=(str(row[1]) + " " + str(row[2]),))
	conn.close()
	etat_get_watched_movies = not etat_get_watched_movies

def last_update():
	lastUpdate = open("Movies Last Update.txt", "w")
	date = datetime.datetime.now()
	now = "Movies Last Update : {TheDay}-{TheMonth}-{TheYear} {TheHour}:{TheMinute}:{TheSecond}\n".format(TheYear=date.year, TheMonth=date.month, TheDay=date.day, TheHour=date.hour, TheMinute=date.minute, TheSecond=date.second)
	print(now)
	lastUpdate.write(now)
	lastUpdate.close()

	allMovies = open("All Movies.txt", "w")
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	select = cursor.execute("SELECT name, year, rating, language, trailer FROM Movies ORDER BY name ASC")
	select = list(select)
	for i in range(len(select)):
		movieSelected = str(i+1) + "- " + str(select[i][0]) + ", " + str(select[i][1]) + ", " + str(select[i][2]) + ", " + str(select[i][3]) + ", " + str(select[i][4].replace("?autoplay=1","") + "\n")
		allMovies.write(movieSelected)
	allMovies.write(now)
	conn.close()
	allMovies.close()

def download_with_progress(link_name, fileName, fileExtension):
	file_name = "{}{}".format(fileName, fileExtension)
	with open(file_name, "wb") as f:
	    print("Downloading %s" % file_name)
	    response = requests.get(link_name, stream=True)
	    total_length = response.headers.get('content-length')

	    if total_length is None: # no content length header
	        f.write(response.content)
	    else:
	        dl = 0
	        total_length = int(total_length)
	        for data in response.iter_content(chunk_size=4096):
	            dl += len(data)
	            f.write(data)
	            done = int(100 * dl / total_length)
	            sys.stdout.write(str("\r[%s%s]" % ('.' * done, ' ' * (100-done))) + " " + str(done) + "%")
	            sys.stdout.flush()

def search_for_movie_s_year(name_movie):
	global the_full_movie_s_name
	right_url = False
	year_movie = ""
	movie = name_movie.replace(" ", "-").lower()
	while not right_url:
		for the_year in range(2021, 1919, -1):
			try:
				movie = "https://teer.egybest.com/movie/{}-{}".format(name_movie.replace(" ", "-").lower(), the_year)
				print(the_year)
				req = Request(movie, headers = {"User-Agent": "Mozilla/5.0"})
				html = urlopen(req)
				the_full_movie_name = str(name_movie.replace(" ", "-").lower()) + "-" + str(the_year)
				print(the_full_movie_name)
				the_full_movie_s_name.append(the_full_movie_name)
				print(the_full_movie_s_name)
			except:
				pass
			if the_year == 1920 and not(the_full_movie_s_name):
				return messagebox.showerror(title="ERROR", message="An Error has Occurred\nPlease Check One of These :\n• Internet Connection\n• Movie's Name or Year\n• If Trailer Exists")
		if len(the_full_movie_s_name) > 1:
			with open("the full movie's name.txt", "a") as full_movie_name:
				for i in the_full_movie_s_name:
					full_movie_name.write(str(i).replace("-", " ").title() + "\n")
			os.startfile("the full movie's name.txt")
		return the_full_movie_s_name[-1]
		right_url = True
		break
	return exit()

def downloadSubtitles(movieSubtitle):
	os.makedirs("Subtitles Databases/", exist_ok=True)
		
	film = str(movieSubtitle.replace("-", " ").title())
	if str(film) + ".db" in os.listdir("Subtitles Databases/"):
		print("Subtitles Database already exist :", film)
		return 1
	print("Please wait ...")
	url = f"https://yts.mx/movies/{movieSubtitle}"
	try:
		html = requests.get(url)
		bs = BeautifulSoup(html.content, "html.parser")
		lien = bs.find_all("a", class_="button")
		url = lien[0]["href"]
	except:
		print("No Subtitles :", film)
		return 1
	print("Start downloading :", film)
	print("Please wait ...")

	html = requests.get(url)
	bs = BeautifulSoup(html.content, "html.parser")
	print("Movie Exists :", film)

	Rating = bs.find_all("span", class_="label")
	Language = bs.find_all("span", class_="sub-lang")
	Link = bs.find_all("a")
	the_zip_list = []

	Rating = [valeur.text for valeur in Rating]
	Language = [valeur.text for valeur in Language]
	Subtitles = [valeur.text.replace("subtitle", "") for valeur in Link if "/subtitles/" in valeur["href"]]
	Link = ["https://yifysubtitles.org" + str(valeur["href"]) for valeur in Link if "/subtitles/" in valeur["href"]]
	print("Subtitles Exist :", film)

	for zipFile in Link:
		html = requests.get(zipFile)
		bs = BeautifulSoup(html.content, "html.parser")
		the_zip_file = bs.find_all("a", class_="btn-icon download-subtitle")
		print("https://yifysubtitles.org" + str(the_zip_file[0]["href"]))
		the_zip_list.append("https://yifysubtitles.org" + str(the_zip_file[0]["href"]))
	print("Zip Downloaded :", film)

	conn = sqlite3.connect("Subtitles Databases/{}.db".format(film))
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS Subtitles")
	conn.commit()
	conn.close()

	conn = sqlite3.connect("Subtitles Databases/{}.db".format(film))
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS Subtitles(id INTEGER PRIMARY KEY, Rating TEXT, Language TEXT, Subtitle_name TEXT, Link TEXT, Zip_File TEXT)")
	conn.close()

	print("Add Values :", film)
	# Add values :
	for i in range(len(Rating)):
		conn = sqlite3.connect("Subtitles Databases/{}.db".format(film))
		cursor = conn.cursor()
		print(Rating[i], Language[i], Link[i], Subtitles[i])
		cursor.execute("INSERT INTO Subtitles(Rating, Language, Subtitle_name, Link, Zip_File) VALUES(?,?,?,?,?)", (Rating[i], Language[i], Subtitles[i].strip(), Link[i], the_zip_list[i]))
		conn.commit()
		conn.close()
	print("Download Finished :", film)
	print("\n")

# def get_actors(movieActors):
# 	pass

def download_movie_s_infos(movie, etat):
	les_images = []
	rating = []
	the_stoory = []
	if not movie[-4:].isdigit():
		movie = search_for_movie_s_year(movie)
	movie = movie.replace(" ", "-").lower()
	req = ""
	linkEgybest = "https://teer.egybest.com/movie/" + movie
	if etat:
		req = Request(str(tree.item(tree.selection())["values"][11]), headers = {"User-Agent": "Mozilla/5.0"})
	else:
		req = Request(linkEgybest, headers = {"User-Agent": "Mozilla/5.0"})
	html = urlopen(req)
	bs = BeautifulSoup(html, 'html.parser')
	images = bs.find_all('img', {'src':re.compile('.jpg')})
	ratiing = bs.find_all('span', itemprop="ratingValue")
	languages = bs.find_all('td')
	the_story = bs.findAll("div", {"class": "pda"})
	try:
		the_trailer = bs.findAll("div", {"class": "play p api"})
		the_trailer = str(list(the_trailer))
		the_trailer = the_trailer.split(" ")
		the_url = []
		for i in the_trailer:
			if "url" in i:
				the_url.append(i)
		the_url = the_url[0].split("\"")
		the_trailer = str(the_url[1])
	except:
		print("trailer doesn't exist!")
		the_trailer = None
	les_types = bs.find_all('td')
	for story in the_story:
		the_stoory.append(story.text)
	the_story = the_stoory[3]
	the_stoory = []
	for image in images:
		les_images.append(image['src'])
		rating.append(ratiing)
	language = languages[2].a["href"].split("/")
	language = language[-1]
	le_type = str(les_types[6].find_all("a")).split('/">')
	les_types = []
	for i, j in enumerate(le_type):
		les_types.append(j.split("/")[-1])
	les_types.pop(-1)

	movieYTS = "https://yts.mx/movies/{}/".format(movie)
	req = requests.get(movieYTS)
	bs = BeautifulSoup(req.content, "html.parser")
	lien = bs.find_all("a", class_="button")
	try:
		url = lien[0]["href"]
		linkYTS = movieYTS
	except:
		linkYTS = ""

	emplacement = "Actors Images/{}/".format(movie.replace("-", " ").title())
	if not os.path.exists(emplacement):
		os.makedirs(emplacement, exist_ok=True)
		req = requests.get(linkEgybest)
		bs = BeautifulSoup(req.content, "html.parser")
		list_actors = []
		actors = bs.select("div.cast_item a")
		images = bs.select("div.cast_item img")
		for i in actors:
			if i.text:
				list_actors.append(i.text)
		for j in range(len(list_actors)):
			# downloaded = "%.2f" % (100 * nbr/total)
			nom = str(list_actors[j]) + ".jpg"
			if not nom in os.listdir(emplacement):
				# r = requests.get(images[j]["src"], allow_redirects=True)
				# open(emplacement + nom, 'wb').write(r.content)
				download_with_progress(images[j]["src"], emplacement + nom, "")

	path_picture = "Movies Images/"
	picture_path = ""
	response = requests.get(str(les_images[0]))
	# print("response OK")
	load = Image.open(BytesIO(response.content))
	# print("load OK")
	picture_path = "{}.jpg".format(movie.replace("-", " ").title())
	path_picture += picture_path
	im1 = load.save(path_picture)
	# print(path_picture)
	image_url = les_images[0]
	print(type(rating))
	print(rating)
	print()
	# rating = rating[0][0].text # need to solve this problem
	rating = 0.0
	name_movie = movie[:-5].replace("-", " ").title()
	year_movie = movie[-4:]
	language_movie = language.title()
	les_types = ",".join(les_types)
	movieSubtitles = str(name_movie).replace(" ", "-").lower() + "-" + str(year_movie)
	movieActors = str(name_movie).replace("-", " ").title() + " " + str(year_movie)
	# actors = get_actors(movieActors)
	actorsSelection = os.listdir(emplacement)
	actorsSelection = ",".join(actorsSelection)
	actors = actorsSelection.replace(".jpg", "")
	downloadSubtitles(movieSubtitles)
	return str(name_movie), int(year_movie), str(rating), str(language_movie), str(picture_path), str(les_types), str(the_story), str(the_trailer), str(linkEgybest), str(linkYTS), str(actors)
	
def treeActionSelect(event):
	global label_image
	global label_story
	# global label_title
	button_thriller["fg"] = "blue"
	button_thriller["bg"] = "white"
	button_action["fg"] = "blue"
	button_action["bg"] = "white"
	button_animation["fg"] = "blue"
	button_animation["bg"] = "white"
	button_history["fg"] = "blue"
	button_history["bg"] = "white"
	button_crime["fg"] = "blue"
	button_crime["bg"] = "white"
	button_fantasy["fg"] = "blue"
	button_fantasy["bg"] = "white"
	button_scifi["fg"] = "blue"
	button_scifi["bg"] = "white"
	button_horror["fg"] = "blue"
	button_horror["bg"] = "white"
	button_romance["fg"] = "blue"
	button_romance["bg"] = "white"
	button_sport["fg"] = "blue"
	button_sport["bg"] = "white"
	button_biography["fg"] = "blue"
	button_biography["bg"] = "white"
	button_family["fg"] = "blue"
	button_family["bg"] = "white"
	button_western["fg"] = "blue"
	button_western["bg"] = "white"
	button_mystery["fg"] = "blue"
	button_mystery["bg"] = "white"
	button_short["fg"] = "blue"
	button_short["bg"] = "white"
	button_comedy["fg"] = "blue"
	button_comedy["bg"] = "white"
	button_adventure["fg"] = "blue"
	button_adventure["bg"] = "white"
	button_musical["fg"] = "blue"
	button_musical["bg"] = "white"
	button_documentary["fg"] = "blue"
	button_documentary["bg"] = "white"
	button_drama["fg"] = "blue"
	button_drama["bg"] = "white"
	button_war["fg"] = "blue"
	button_war["bg"] = "white"
	if len(tree.selection()) == 1:
		label_image.destroy()
		idSelect = tree.item(tree.selection())["values"][0]
		nameSelect = tree.item(tree.selection())["values"][1]
		yearSelect = tree.item(tree.selection())["values"][2]
		ratingSelect = tree.item(tree.selection())["values"][3]
		languageSelect = tree.item(tree.selection())["values"][4]
		otherNameSelect = tree.item(tree.selection())["values"][5]
		photoSelect = tree.item(tree.selection())["values"][6]
		storySelect = tree.item(tree.selection())["values"][7]
		trailerSelect = tree.item(tree.selection())["values"][8]
		le_type = tree.item(tree.selection())["values"][9]
		var_name.set(nameSelect)
		var_year.set(yearSelect)
		var_rating.set(ratingSelect)
		var_language.set(languageSelect)
		le_type = le_type.split(",")
		for i in le_type:
			selectType(i)
		# label_title["text"] = ""
		
		texte = []
		cnt = 1
		for i in storySelect:
			texte.append(i)
			if i == " ":
				cnt += 1
			if cnt%15 == 0:
				texte.append("\n")
				cnt += 1
		texte = "".join(texte)
			
		label_story["text"] = texte
		if len(otherNameSelect):
			var_other_name.set(otherNameSelect)
			entry_other_name["bg"] = "white"
		else:
			var_other_name.set("")
			entry_other_name["bg"] = "red"
		if languageSelect == "-" or languageSelect == "":
			var_language.set("")
			entry_language["bg"] = "red"
		else:
			var_language.set(languageSelect)
			entry_language["bg"] = "white"

		var_photo.set(photoSelect)
		button_update["state"] = "normal"
		button_delete["state"] = "normal"
		# button_egybest["state"] = "normal"
		button_torrent["state"] = "normal"
		if trailerSelect:
			button_watch_trailer["state"] = "normal"
		else:
			button_watch_trailer["state"] = "disabled"

		# print(photoSelect)
		if photoSelect:
			try:
				load = Image.open("Movies Images/{}".format(photoSelect))
				load.thumbnail((600, 350))
				photo = ImageTk.PhotoImage(load)
				Profile[1] = photo
				label_image = Label(fenetre, image=photo, height=600)
				label_image.place(x=770, y=0, width=350)
			except:
				load = Image.open("default.jpg")
				load.thumbnail((600, 350))
				photo = ImageTk.PhotoImage(load)
				Profile[1] = photo
				label_image = Label(fenetre, image=photo, height=600)
				label_image.place(x=770, y=0, width=350)
		else:
			load = Image.open("/default.jpg")
			load.thumbnail((600, 350))
			photo = ImageTk.PhotoImage(load)
			Profile[1] = photo
			label_image = Label(fenetre, image=photo, height=600)
			label_image.place(x=770, y=0, width=350)
			# label_image.bind("<ButtonRelease>", show_picture_onclick)
	else:
		load = Image.open(os.path.dirname(os.path.abspath(__file__)) + "/default1.jpg")
		load.thumbnail((600, 300))
		photo = ImageTk.PhotoImage(load)
		Profile[1] = photo
		label_image = Label(fenetre, image=photo, height=600)
		label_image.place(x=770, y=0, width=350)
		var_name.set("")
		var_year.set("")
		var_rating.set("")
		var_other_name.set("")
		var_language.set("")
		var_photo.set("")
		entry_other_name["bg"] = "white"
		label_story["text"] = ""

def selectType(le_type):
	if le_type == "thriller":
		button_thriller["bg"] = "blue"
		button_thriller["fg"] = "white"
	if le_type == "action":
		button_action["bg"] = "blue"
		button_action["fg"] = "white"
	if le_type == "animation":
		button_animation["bg"] = "blue"
		button_animation["fg"] = "white"
	if le_type == "history":
		button_history["bg"] = "blue"
		button_history["fg"] = "white"
	if le_type == "crime":
		button_crime["bg"] = "blue"
		button_crime["fg"] = "white"
	if le_type == "fantasy":
		button_fantasy["bg"] = "blue"
		button_fantasy["fg"] = "white"
	if le_type == "scifi":
		button_scifi["bg"] = "blue"
		button_scifi["fg"] = "white"
	if le_type == "horror":
		button_horror["bg"] = "blue"
		button_horror["fg"] = "white"
	if le_type == "romance":
		button_romance["bg"] = "blue"
		button_romance["fg"] = "white"
	if le_type == "sport":
		button_sport["bg"] = "blue"
		button_sport["fg"] = "white"
	if le_type == "biography":
		button_biography["bg"] = "blue"
		button_biography["fg"] = "white"
	if le_type == "family":
		button_family["bg"] = "blue"
		button_family["fg"] = "white"
	if le_type == "western":
		button_western["bg"] = "blue"
		button_western["fg"] = "white"
	if le_type == "mystery":
		button_mystery["bg"] = "blue"
		button_mystery["fg"] = "white"
	if le_type == "short":
		button_short["bg"] = "blue"
		button_short["fg"] = "white"
	if le_type == "comedy":
		button_comedy["bg"] = "blue"
		button_comedy["fg"] = "white"
	if le_type == "adventure":
		button_adventure["bg"] = "blue"
		button_adventure["fg"] = "white"
	if le_type == "musical":
		button_musical["bg"] = "blue"
		button_musical["fg"] = "white"
	if le_type == "documentary":
		button_documentary["bg"] = "blue"
		button_documentary["fg"] = "white"
	if le_type == "drama":
		button_drama["bg"] = "blue"
		button_drama["fg"] = "white"
	if le_type == "war":
		button_war["bg"] = "blue"
		button_war["fg"] = "white"

###########################################################################
def new_movie(event):
	var_name.set("")
	entry_name.focus()
def add_movie():
	global the_full_movie_s_name
	if the_full_movie_s_name:
		the_full_movie_s_name.pop(-1)
		moviesNumber = the_full_movie_s_name[-1].replace(", ", ",").strip().split(",")
	else:
		moviesNumber = var_name.get().replace(", ", ",").strip().split(",")
	for movieNbr in moviesNumber:
		print(movieNbr)
		try:
			movie_name, movie_year, movie_rating, movie_language, movie_picture, movie_type, movie_story, movie_trailer, linkEgybest, linkYTS, actors = download_movie_s_infos(movieNbr, False)
		except:
			if moviesNumber == 1:
				return messagebox.showerror(title="ERROR", message="An Error has Occurred\nPlease Check One of These :\n• Internet Connection\n• Movie's Name or Year\n• If Trailer Exists")
			elif moviesNumber > 1:
				print("An Error has Occurred\nPlease Check One of These :\n• Internet Connection\n• Movie's Name or Year\n• If Trailer Exists")
		if len(entry_other_name.get()):
			movie_other_name = entry_other_name.get()
		else:
			movie_other_name = ""

		if var_checkbutton_name.get() == 1:
			movie_watched = "True"
		else:
			movie_watched = "False"
		conn = sqlite3.connect("MOVIES.db")
		cursor = conn.cursor()
		select = cursor.execute("SELECT name, year from Movies")
		select = list(select)
		len_select = len(select)
		len_select += 1
		new_movie = str(movie_name) + " " + str(movie_year)
		movie_exists = False
		for i in select:
			full_name = str(i[0]) + " " + str(i[1])
			if new_movie == full_name:
				movie_exists = True
				print("{} already exists".format(movieNbr))
				if len(moviesNumber) == 1:
					return messagebox.showerror(title="Already exists", message="Movie already exists")
		if not(movie_exists):
			cursor.execute("INSERT INTO Movies(id, name, year, rating, language, movie_other_name, picture, story, trailer, the_type, watched, linkEgybest, linkYTS, actors) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (len_select, movie_name, movie_year, movie_rating, movie_language, movie_other_name, movie_picture, movie_story, movie_trailer, movie_type, movie_watched, linkEgybest, linkYTS, actors))
			conn.commit()
			conn.close()
			display_movies()
			treeFocus("event")
			print("{} Has Added Successfuly".format(movieNbr))
			if len(moviesNumber) == 1 and len(the_full_movie_s_name) == 1:
				return messagebox.showinfo(title="Success", message="{} Has Added Successfuly".format(movieNbr))
			elif len(the_full_movie_s_name) > 1:
				print("{} Has Added Successfuly".format(movieNbr))
				display_movies()
				add_movie()
		conn = sqlite3.connect("MOVIES.db")
		cursor = conn.cursor()
		select = cursor.execute("SELECT * FROM Movies ORDER BY id DESC")
		treeFocus("event")
		watched_or_not(select)
		conn.close()
	add_movie_threading.join()
	print("The end of file!")

add_movie_threading = threading.Thread(target=add_movie, args=())

def update_the_movie(event):
	if messagebox.askokcancel("Update","Are you sure ?"):
		update_movie()
def update_movie():
	idSelect = tree.item(tree.selection())["values"][0]
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	if var_checkbutton_name.get() == 1:
		watched = "True"
	else:
		watched = "False"
	cursor.execute("UPDATE Movies SET name=?, year=?, rating=?, language=?, movie_other_name=?, picture=?, watched=? WHERE id=?", (entry_name.get(), entry_year.get(), entry_rating.get(), entry_language.get(), entry_other_name.get(), var_photo.get(), watched, idSelect))
	conn.commit()
	conn.close()
	if watched == "True":
		replace_the_movies(idSelect)
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	select = cursor.execute("SELECT * FROM Movies ORDER BY id DESC")
	watched_or_not(select)
	conn.close()
	########################
	# _iid = tree.get_children()[tree.item(tree.selection())["values"][0]]
	# tree.focus(_iid)
	# tree.selection_set(_iid)
	########################
	len_the_types()
	messagebox.showinfo("Update", "The Item Has Updated Successfuly!")

def event_button_delete(event):
	delete_movie()

def delete_movie():
	if messagebox.askokcancel("Delete","Are you sure ?"):
		idSelect = tree.item(tree.selection())["values"][0]
		pictureSelect = tree.item(tree.selection())["values"][6]
		conn = sqlite3.connect("MOVIES.db")
		cursor = conn.cursor()
		
		main_path = os.path.dirname(os.path.abspath(__file__)) # get the cutrrent path
		
		pictures_path = main_path + "/Movies Images/"
		subtitles_path = main_path + "/Subtitles Databases/"
		zip_path = main_path + "/Download ZIPs/"
		actors_path = main_path + "/Actors Images/"

		pictures_list = os.listdir(pictures_path)
		subtitles_list = os.listdir(subtitles_path)
		zip_list = os.listdir(zip_path)
		actors_list = os.listdir(actors_path)

		if pictureSelect in pictures_list:
			os.makedirs(main_path + "/Deleted Movies/Images/", exist_ok=True)
			imagesDestinationPath = main_path + "/Deleted Movies/Images"
			pictures_path = main_path + "/Movies Images/"
			if not pictureSelect in os.listdir(imagesDestinationPath):
				os.rename(pictures_path + pictureSelect, imagesDestinationPath + pictureSelect)
			else:
				os.rename(pictures_path + pictureSelect, imagesDestinationPath + "(Already Exists) " + pictureSelect)
		
		# if subtitleSelect in subtitles_list:
		# 	os.makedirs(main_path + "/Deleted Movies/Subtitles/", exist_ok=True)
		# 	imagesDestinationPath = main_path + "/Deleted Movies/"
		# 	subtitles_path = main_path + "/Movies Images/"
		# 	if not subtitleSelect in os.listdir(imagesDestinationPath):
		# 		os.rename(subtitles_path + subtitleSelect, imagesDestinationPath + subtitleSelect)
		
		# if zipSelect in pictures_list:
		# 	os.makedirs(main_path + "/Deleted Movies/ZIPs/", exist_ok=True)
		# 	zipDestinationPath = main_path + "/Deleted Movies/"
		# 	zip_path = main_path + "/Movies Images/"
		# 	if not zipSelect in os.listdir(zipDestinationPath):
		# 		os.rename(zip_path + zipSelect, zipDestinationPath + zipSelect)
		
		# if actorsSelect in pictures_list:
		# 	os.makedirs(main_path + "/Deleted Movies/Actors/", exist_ok=True)
		# 	actorsDestinationPath = main_path + "/Deleted Movies/"
		# 	actors_path = main_path + "/Movies Images/"
		# 	if not actorsSelect in os.listdir(actorsDestinationPath):
		# 		os.rename(actors_path + actorsSelect, actorsDestinationPath + actorsSelect)
		
		cursor.execute("DELETE FROM Movies WHERE id = {}".format(idSelect))
		conn.commit()
		conn.close()
		tree.delete(tree.selection())
		get_IDs()
		display_movies()
		treeFocus("event")
		return messagebox.showinfo(title="Delete Success", message="Movie Has Deleted Successfuly")

def open_youtube(event):
	watch_trailer()
def watch_trailer():
	trailerSelect = tree.item(tree.selection())["values"][8]
	if trailerSelect:
		if messagebox.askokcancel("Open on Youtube", "Do you want to watch the trailer on Youtube ?"):
			webbrowser.open(trailerSelect)
			# webbrowser.get(chrome_path).open(trailerSelect)
	else:
		messagebox.showerror("Open on Youtube", "Sorry, the trailer doesn't exist!")

def select_types(select_type):
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	the_selection = cursor.execute("SELECT * FROM Movies WHERE the_type LIKE '%{}%'".format(select_type))
	the_selection = list(the_selection)
	watched_or_not(the_selection)
	conn.close()

def visit_website(choise):
	link = ""
	if choise == "egybest":
		link = str(tree.item(tree.selection())["values"][11])
	elif choise == "torrent":
		link = str(tree.item(tree.selection())["values"][12])
	if link:
		webbrowser.open(link)
		# webbrowser.get(chrome_path).open(link)
	else:
		messagebox.showerror("Error", "Torrent doesn't exist")

def EgyBest(event):
	if messagebox.askokcancel("EgyBest","Do you want to open EgyBest website in browser ?"):
		visit_website("egybest")
def Torrent(event):
	if messagebox.askokcancel("Torrent","Do you want to open Torrent website in browser ?"):
		visit_website("torrent")

def replace_the_movies(the_id):
	global id_Select_1, name_Select_1, year_Select_1, rating_Select_1, language_Select_1, movie_other_name_Select_1, picture_Select_1, story_Select_1, trailer_Select_1, the_type_Select_1, watched_Select_1, linkEgybest_Select_1, linkYTS_Select_1, actors_Select_1, id_Select_2, name_Select_2, year_Select_2, rating_Select_2, language_Select_2, movie_other_name_Select_2, picture_Select_2, story_Select_2, trailer_Select_2, the_type_Select_2, watched_Select_2, linkEgybest_Select_2, linkYTS_Select_2, actors_Select_2
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	la_selection1 = list(cursor.execute("SELECT * FROM Movies WHERE id=={}".format(watched_movies())))
	print(la_selection1[0][1])
	id_Select_1 = la_selection1[0][0]
	name_Select_1 = la_selection1[0][1]
	year_Select_1 = la_selection1[0][2]
	rating_Select_1 = la_selection1[0][3]
	language_Select_1 = la_selection1[0][4]
	movie_other_name_Select_1 = la_selection1[0][5]
	picture_Select_1 = la_selection1[0][6]
	story_Select_1 = la_selection1[0][7]
	trailer_Select_1 = la_selection1[0][8]
	the_type_Select_1 = la_selection1[0][9]
	watched_Select_1 = la_selection1[0][10]
	linkEgybest_Select_1 = la_selection1[0][11]
	linkYTS_Select_1 = la_selection1[0][12]
	actors_Select_1 = la_selection1[0][13]
	conn.close()
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	la_selection2 = list(cursor.execute("SELECT * FROM Movies WHERE id=={}".format(the_id)))
	id_Select_2 = str(la_selection2[0][0])
	name_Select_2 = str(la_selection2[0][1])
	year_Select_2 = int(la_selection2[0][2])
	rating_Select_2 = str(la_selection2[0][3])
	language_Select_2 = str(la_selection2[0][4])
	movie_other_name_Select_2 = str(la_selection2[0][5])
	picture_Select_2 = str(la_selection2[0][6])
	story_Select_2 = str(la_selection2[0][7])
	trailer_Select_2 = str(la_selection2[0][8])
	the_type_Select_2 = str(la_selection2[0][9])
	watched_Select_2 = "True"
	linkEgybest_Select_2 = str(la_selection2[0][11])
	linkYTS_Select_2 = str(la_selection2[0][12])
	actors_Select_2 = str(la_selection2[0][13])
	conn.close()
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	cursor.execute("UPDATE Movies SET name=?, year=?, rating=?, language=?, movie_other_name=?, picture=?, story=?, trailer=?, the_type=?, watched=?, linkEgybest=?, linkYTS=?, actors=? WHERE id=?", (name_Select_1, year_Select_1, rating_Select_1, language_Select_1, movie_other_name_Select_1, picture_Select_1, story_Select_1, trailer_Select_1, the_type_Select_1, watched_Select_1, linkEgybest_Select_1, linkYTS_Select_1, actors_Select_1, id_Select_2))
	conn.commit()
	conn.close()
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	cursor.execute("UPDATE Movies SET name=?, year=?, rating=?, language=?, movie_other_name=?, picture=?, story=?, trailer=?, the_type=?, watched=?, linkEgybest=?, linkYTS=?, actors=? WHERE id=?", (name_Select_2, year_Select_2, rating_Select_2, language_Select_2, movie_other_name_Select_2, picture_Select_2, story_Select_2, trailer_Select_2, the_type_Select_2, watched_Select_2, linkEgybest_Select_2, linkYTS_Select_2, actors_Select_2, id_Select_1))
	conn.commit()
	conn.close()
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	movies_res = cursor.execute("SELECT * FROM Movies")
	for row in movies_res:
			tree.insert("", END, value=row, tags=(str(row[1]) + " " + str(row[2]),))
			if row[10] == "True":
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="green", foreground="black")
			elif row[10] == "False":
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="red", foreground="black")
			else:
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="blue", foreground="black")
	conn.close()
	tree.tag_configure(str(name_Select_1) + " " + str(year_Select_1), foreground="white")
	tree.tag_configure(str(name_Select_2) + " " + str(year_Select_2), foreground="white")
	print("{} <---> {}".format(name_Select_1, name_Select_2))

def watched_already(event):
	idSelect = tree.item(tree.selection())["values"][0]
	watchedSelect = tree.item(tree.selection())["values"][10]
	if watchedSelect == "False":
		conn = sqlite3.connect("MOVIES.db")
		cursor = conn.cursor()
		cursor.execute("UPDATE Movies SET watched=? WHERE id=?", ("True", idSelect))
		conn.commit()
		conn.close()
		replace_the_movies(idSelect)
		conn = sqlite3.connect("MOVIES.db")
		cursor = conn.cursor()
		select = cursor.execute("SELECT * FROM Movies ORDER BY id DESC")
		watched_or_not(select)
		conn.close()
		messagebox.showinfo("Update", "The Item Has Updated Successfuly!")
	display_movies()

def show_in_file():
	selected_movies = open("Selected Movies.txt", "w")
	curItems = tree.selection()
	nameSelect = [str(tree.item(i)['values'][1]) for i in curItems]
	yearSelect = [str(tree.item(i)['values'][2]) for i in curItems]
	ratingSelect = [str(tree.item(i)['values'][3]) for i in curItems]
	languageSelect = [str(tree.item(i)['values'][4]) for i in curItems]
	trailerSelect = [str(tree.item(i)['values'][8]) for i in curItems]
	# le_type = [str(tree.item(i)['values'][9]) for i in curItems] # for future purposes
	watchedSelect = [str(tree.item(i)['values'][10]) for i in curItems]
	sort_movies = []
	for film in range(len(nameSelect)):
		waitingList = ""
		if watchedSelect[film] == "False":
			waitingList = '["Waiting List"].'
		le_film = str(waitingList) + str(nameSelect[film]) + " (" + str(yearSelect[film]) + ") " + str(ratingSelect[film]) + " " + str(languageSelect[film]) + " " + str(trailerSelect[film])
		print(le_film)
		sort_movies.append(le_film)
	sort_movies.sort()
	for theMovie in range(len(sort_movies)):
		selected_movies.write(str(theMovie+1) + "- " + sort_movies[theMovie] + "\n")
	selected_movies.close()
	print(str(os.path.dirname(os.path.abspath(__file__)) + "/Selected Movies.txt"))
	os.startfile(str(os.path.dirname(os.path.abspath(__file__)) + "/Selected Movies.txt"))

###########################################################################
# Zone Colors
var_color = StringVar()
buttonForegroundColor = Radiobutton(fenetre, text="Foreground", value="fg", variable=var_color, bg="white", fg="darkblue")
buttonForegroundColor.place(x=10, y=0)
buttonBackgroundColor = Radiobutton(fenetre, text="Background", value="bg", variable=var_color, bg="white", fg="darkblue")
buttonBackgroundColor.place(x=10, y=20)
if not "Colors.txt" in os.listdir(os.path.dirname(os.path.abspath(__file__))):
	colors = open("Colors.txt", "w")
	colors.write("yellow" + "\n" + "darkblue" + "\n" + "fg" + "\n")
	colors.close()

colorValues = ["aqua", "beige", "black", "blue", "brown", "cyan", "darkblue", "gold", "gray", "green", "indigo", "lime", "magenta", "maroon", "navy", "olive", "orange", "pink", "purple", "red", "silver", "teal", "violet", "white", "yellow"]
# colorValues.sort()
colorOptions = ttk.Combobox(fenetre, values=colorValues, state="readonly", font=("Times", 11))
colorOptions.place(x=110, y=5)

colors = open("Colors.txt", "r")
theColors = colors.readlines()
if len(theColors) == 3:
	foregroundColor = theColors[0][:-1]
	backgroundColor = theColors[1][:-1]
	lastGround = theColors[2][:-1]
	var_color.set(lastGround)
	if lastGround == "fg":
		colorOptions.current(colorValues.index(foregroundColor))
	if lastGround == "bg":
		colorOptions.current(colorValues.index(backgroundColor))
	colors.close()
else:
	colors.close()
	colors = open("Colors.txt", "w")
	colors.write("yellow" + "\n" + "darkblue" + "\n" + "fg" + "\n")
	colors.close()

# def other_colors():
# 	other_foregroundColor = "yellow"
# 	other_backgroundColor = "darkblue"
# 	if var_color.get() == "fg":
# 		rgb_color, other_foregroundColor = colorchooser.askcolor(parent=fenetre, initialcolor=(255, 0, 0))
# 	if var_color.get() == "bg":
# 		rgb_color, other_backgroundColor = colorchooser.askcolor(parent=fenetre, initialcolor=(255, 0, 0))
# 	lastGround = var_color.get()
# 	button_add["fg"] = other_foregroundColor
# 	button_add["bg"] = other_backgroundColor
# 	button_update["fg"] = other_foregroundColor
# 	button_update["bg"] = other_backgroundColor
# 	button_delete["fg"] = other_foregroundColor
# 	button_delete["bg"] = other_backgroundColor
# 	button_watch_trailer["fg"] = other_foregroundColor
# 	button_watch_trailer["bg"] = other_backgroundColor
# 	button_egybest["fg"] = other_foregroundColor
# 	button_egybest["bg"] = other_backgroundColor
# 	button_torrent["fg"] = other_foregroundColor
# 	button_torrent["bg"] = other_backgroundColor
# 	button_wrtie_in_file["fg"] = other_foregroundColor
# 	button_wrtie_in_file["bg"] = other_backgroundColor
# 	button_exit["fg"] = other_foregroundColor
# 	button_exit["bg"] = other_backgroundColor
# 	button_drive["fg"] = other_foregroundColor
# 	button_drive["bg"] = other_backgroundColor
# 	button_get_watched_movies["fg"] = other_foregroundColor
# 	button_get_watched_movies["bg"] = other_backgroundColor

	# colors = open("Other Colors.txt", "w")
	# colors.write(str(foregroundColor) + "\n" + str(backgroundColor) + "\n" + str(lastGround) + "\n")
	# colors.close()
# otherColors = Button(fenetre, text="Other colors", font=("Times", 11), command=other_colors)
# otherColors.place(x=110, y=25)

def afficher(event):
	global lastGround, foregroundColor, backgroundColor
	# print(var_color.get())
	# print(colorOptions.get())
	colors = open("Colors.txt", "r")
	theColors = colors.readlines()
	if len(theColors) == 3:
		foregroundColor = theColors[0][:-1]
		backgroundColor = theColors[1][:-1]
		lastGround = theColors[2][:-1]
		colors.close()
		button_add[var_color.get()] = colorOptions.get()
		button_update[var_color.get()] = colorOptions.get()
		button_delete[var_color.get()] = colorOptions.get()
		button_watch_trailer[var_color.get()] = colorOptions.get()
		button_egybest[var_color.get()] = colorOptions.get()
		button_torrent[var_color.get()] = colorOptions.get()
		button_wrtie_in_file[var_color.get()] = colorOptions.get()
		button_exit[var_color.get()] = colorOptions.get()
		button_drive[var_color.get()] = colorOptions.get()
		button_get_watched_movies[var_color.get()] = colorOptions.get()
	if var_color.get() == "fg":
		foregroundColor = colorOptions.get()
	if var_color.get() == "bg":
		backgroundColor = colorOptions.get()
	lastGround = var_color.get()
	colors = open("Colors.txt", "w")
	colors.write(str(foregroundColor) + "\n" + str(backgroundColor) + "\n" + str(lastGround) + "\n")
	colors.close()

colorOptions.bind("<FocusIn>", afficher)
# colorOptions.bind("<FocusOut>", afficher)

def google_drive():
	google_drive_file = open("Google Drive.txt", "w")
	date = datetime.datetime.now()
	now = "Google Drive Last Update : {TheDay}-{TheMonth}-{TheYear} {TheHour}:{TheMinute}:{TheSecond}\n".format(TheYear=date.year, TheMonth=date.month, TheDay=date.day, TheHour=date.hour, TheMinute=date.minute, TheSecond=date.second)
	print(now)
	google_drive_file.write(now)
	google_drive_file.close()
	webbrowser.open("https://drive.google.com/drive/folders/1hXSCgntTPTB9svyEtC3tAjfU3UMF5hI2")
	# webbrowser.get(chrome_path).open("https://drive.google.com/drive/folders/1hXSCgntTPTB9svyEtC3tAjfU3UMF5hI2")
	# fenetre.destroy()
def open_google_drive(event):
	google_drive()

def update_infos(event):
	idSelect = tree.item(tree.selection())["values"][0]
	nameSelect = tree.item(tree.selection())["values"][1]
	yearSelect = tree.item(tree.selection())["values"][2]
	movie_name, movie_year, movie_rating, movie_language, movie_picture, movie_type, movie_story, movie_trailer, linkEgybest, linkYTS, actors = download_movie_s_infos(str(tree.item(tree.selection())["values"][1]) + " " + str(tree.item(tree.selection())["values"][2]), True)
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	cursor.execute("UPDATE Movies SET name=?, year=?, rating=?, language=?, picture=?, the_type=?, story=?, trailer=?, watched=?, linkEgybest=?, linkYTS=?, actors=? WHERE id=?", (movie_name, movie_year, movie_rating, movie_language, movie_picture, movie_type, movie_story, movie_trailer, str(tree.item(tree.selection())["values"][10]), linkEgybest, linkYTS, actors, int(tree.item(tree.selection())["values"][0])))
	conn.commit()
	conn.close()
	display_movies()
	tree.tag_configure(str(nameSelect) + " " + str(yearSelect), foreground="yellow")
	return messagebox.showinfo(title="Success", message="{} Has Updated Successfuly".format( str(nameSelect) + " " + str(yearSelect)))


###########################################################################
# Zone Search By
search_x = 370
step_search_x = 60
var_choix = StringVar()
label_searchBy = Label(fenetre, text="Search by : (Ctrl+F)", bg="darkblue", fg="white")
label_searchBy.place(x=250, y=0, width=120)
checkbutton_search_by_name = Radiobutton(fenetre, text="Name", variable=var_choix, value="name", bg="white", fg="darkblue")
checkbutton_search_by_name.place(x=search_x + 0*step_search_x, y=0)
checkbutton_search_by_year = Radiobutton(fenetre, text="Year", variable=var_choix, value="year", bg="white", fg="darkblue")
checkbutton_search_by_year.place(x=search_x + 1*step_search_x, y=0)
checkbutton_search_by_rating = Radiobutton(fenetre, text="Rating", variable=var_choix, value="rating", bg="white", fg="darkblue")
checkbutton_search_by_rating.place(x=search_x + 2*step_search_x, y=0)
checkbutton_search_by_language = Radiobutton(fenetre, text="Language", variable=var_choix, value="language", bg="white", fg="darkblue")
checkbutton_search_by_language.place(x=search_x + 3*step_search_x, y=0)
var_choix.set("name")

# Search area
label_search_by = Label(fenetre, text="Search by name :", bg="darkblue", fg="white")
label_search_by.place(x=250, y=25, width=120)
entry_search = Entry(fenetre)
entry_search.place(x=375, y=30, width=140)
label_found_movies = Label(fenetre, fg="green", font=("Times", 13))
label_found_movies.place(x=520, y=25)

# label name
label_name = Label(fenetre, text="Name", bg="black", fg="yellow")
label_name.place(x=5, y=50, width=135)
var_name = StringVar()
entry_name = Entry(fenetre, textvariable=var_name)
entry_name.place(x=140, y=50, width=500)
var_checkbutton_name = IntVar()
checkbutton_name = Checkbutton(fenetre, text="Already (W)atched ?", variable=var_checkbutton_name)
checkbutton_name.place(x=650, y=50)

# label year
label_year = Label(fenetre, text="Year", bg="black", fg="yellow")
label_year.place(x=5, y=80, width=135)
var_year = IntVar()
entry_year = Entry(fenetre, textvariable=var_year)
entry_year.place(x=140, y=80, width=200)
var_year.set("")

# label rating
label_rating = Label(fenetre, text="Rating", bg="black", fg="yellow")
label_rating.place(x=5, y=110, width=135)
var_rating = StringVar()
entry_rating = Entry(fenetre, textvariable=var_rating)
entry_rating.place(x=140, y=110, width=550)

# label language
label_language = Label(fenetre, text="Language", bg="black", fg="yellow")
label_language.place(x=350, y=80, width=135)
var_language = StringVar()
entry_language = Entry(fenetre, textvariable=var_language)
entry_language.place(x=490, y=80, width=200)
var_language.set("")

# label photo
label_photo = Label(fenetre, text="Picture", bg="black", fg="yellow")
label_photo.place(x=5, y=140, width=135)
var_photo = StringVar()
entry_photo = Entry(fenetre, textvariable=var_photo)
entry_photo.place(x=140, y=140, width=500)
# button_photo = Button(fenetre, text="Browse", bg="black", fg="yellow", activebackground="green")
# button_photo.place(x=650, y=140, height=25)

# label other name
label_other_name = Label(fenetre, text="Other name", bg="black", fg="yellow")
label_other_name.place(x=5, y=170, width=135)
var_other_name = StringVar()
entry_other_name = Entry(fenetre, textvariable=var_other_name)
entry_other_name.place(x=140, y=170, width=550)

# command Button
y = 205
step = 35
button_add = Button(fenetre, text="Add Movie (F2)", bg="darkblue", fg="yellow", command=lambda: add_movie_threading.start(), activebackground="green")
button_add.place(x=5, y=y + 0*step, width=155, height=30)
button_update = Button(fenetre, text="Update Movie (Ctrl+U)", bg="darkblue", fg="yellow", state=DISABLED, command=update_movie, activebackground="green")
button_update.place(x=5, y=y + 1*step, width=155, height=30)
button_delete = Button(fenetre, text="(Delete) Movie", bg="darkblue", fg="yellow", state=DISABLED, command=delete_movie, activebackground="green")
button_delete.place(x=5, y=y + 2*step, width=155, height=30)
button_watch_trailer = Button(fenetre, text="Watch Trailer on (Y)outube", bg="darkblue", fg="yellow", state=DISABLED, command=watch_trailer, activebackground="green")
button_watch_trailer.place(x=5, y=y + 3*step, width=155, height=30)
button_egybest = Button(fenetre, text="(E)gyBest", bg="darkblue", fg="yellow", state=DISABLED, command=lambda: visit_website("egybest"), activebackground="green")
button_egybest.place(x=5, y=y + 4*step, width=155, height=30)
button_torrent = Button(fenetre, text="Search (T)orrent", bg="darkblue", fg="yellow", state=DISABLED, command=lambda: visit_website("torrent"), activebackground="green")
button_torrent.place(x=5, y=y + 5*step, width=155, height=30)
button_wrtie_in_file = Button(fenetre, text="Show in file", bg="darkblue", fg="yellow", command=show_in_file, activebackground="green")
button_wrtie_in_file.place(x=5, y=y + 6*step, width=155, height=30)
button_drive = Button(fenetre, text="Open Google (D)rive", bg="darkblue", fg="yellow", command=google_drive, activebackground="green", state=DISABLED)
button_drive.place(x=5, y=y + 7*step, width=155, height=30)
button_get_watched_movies = Button(fenetre, text="Watched/Not watched", bg="darkblue", fg="yellow", command=get_watched_movies, activebackground="green")
button_get_watched_movies.place(x=5, y=y + 8*step, width=155, height=30)
button_exit = Button(fenetre, text="Exit (Escape)", bg="darkblue", fg="yellow", command=fenetre.quit, activebackground="green")
button_exit.place(x=5, y=y + 9*step, width=155, height=30)

# display infos
# label_title = Label(fenetre, text="label_title", font=("Times", 15))
# label_title.place(x=180, y=550)
label_story = Label(fenetre, text="", font=("Times", 15))
label_story.place(x=5, y=550, width=740, height=110)

# Type Buttons
x1 = 160
y1 = 450
step_x = 85
step_y = 30
button_thriller = Button(fenetre, text="thriller (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("thriller"), activebackground="green")
button_thriller.place(x=x1 + 0*step_x, y=y1 + 0*step_y)
button_action = Button(fenetre, text="action (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("action"), activebackground="green")
button_action.place(x=x1 + 1*step_x, y=y1 + 0*step_y)
button_animation = Button(fenetre, text="animation (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("animation"), activebackground="green")
button_animation.place(x=x1 + 2*step_x, y=y1 + 0*step_y)
button_history = Button(fenetre, text="history (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("history"), activebackground="green")
button_history.place(x=x1 + 3*step_x, y=y1 + 0*step_y)
button_war = Button(fenetre, text="war (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("war"), activebackground="green")
button_war.place(x=x1 + 4*step_x, y=y1 + 0*step_y)
button_crime = Button(fenetre, text="crime (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("crime"), activebackground="green")
button_crime.place(x=x1 + 5*step_x, y=y1 + 0*step_y)
button_musical = Button(fenetre, text="musical (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("musical"), activebackground="green")
button_musical.place(x=x1 + 6*step_x, y=y1 + 0*step_y)
button_horror = Button(fenetre, text="horror (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("horror"), activebackground="green")
button_horror.place(x=x1 + 0*step_x, y=y1 + 1*step_y)
button_romance = Button(fenetre, text="romance (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("romance"), activebackground="green")
button_romance.place(x=x1 + 1*step_x, y=y1 + 1*step_y)
button_adventure = Button(fenetre, text="adventure (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("adventure"), activebackground="green")
button_adventure.place(x=x1 + 2*step_x, y=y1 + 1*step_y)
button_biography = Button(fenetre, text="biography (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("biography"), activebackground="green")
button_biography.place(x=x1 + 3*step_x, y=y1 + 1*step_y)
button_family = Button(fenetre, text="family (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("family"), activebackground="green")
button_family.place(x=x1 + 4*step_x, y=y1 + 1*step_y)
button_western = Button(fenetre, text="western (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("western"), activebackground="green")
button_western.place(x=x1 + 5*step_x, y=y1 + 1*step_y)
button_mystery = Button(fenetre, text="mystery (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("mystery"), activebackground="green")
button_mystery.place(x=x1 + 6*step_x, y=y1 + 1*step_y)
button_scifi = Button(fenetre, text="Science Fiction (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("scifi"), activebackground="green")
button_scifi.place(x=x1 + 0*step_x-5, y=y1 + 2*step_y)
button_comedy = Button(fenetre, text="comedy (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("comedy"), activebackground="green")
button_comedy.place(x=x1 + 1*step_x+25, y=y1 + 2*step_y)
button_documentary = Button(fenetre, text="documentary (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("documentary"), activebackground="green")
button_documentary.place(x=x1 + 2*step_x+15, y=y1 + 2*step_y)
button_sport = Button(fenetre, text="sport (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("sport"), activebackground="green")
button_sport.place(x=x1 + 3*step_x+25, y=y1 + 2*step_y)
button_fantasy = Button(fenetre, text="fantasy (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("fantasy"), activebackground="green")
button_fantasy.place(x=x1 + 4*step_x+10, y=y1 + 2*step_y)
button_drama = Button(fenetre, text="drama (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("drama"), activebackground="green")
button_drama.place(x=x1 + 5*step_x+10, y=y1 + 2*step_y)
button_short = Button(fenetre, text="short (0)".title(), bg="white", fg="darkblue", command=lambda: select_types("short"), activebackground="green")
button_short.place(x=x1 + 6*step_x, y=y1 + 2*step_y)


# Load images
load = Image.open(os.path.dirname(os.path.abspath(__file__)) + "/default1.jpg")
load.thumbnail((600, 300))
photo = ImageTk.PhotoImage(load)
Profile[1] = photo
label_image = Label(fenetre, image=photo, height=600)
label_image.place(x=770, y=0, width=350)

# Add TreeView
tree = ttk.Treeview(fenetre, columns=(1, 2, 3, 4, 5), height=5, show="headings")
tree.place(x=165, y=200, width=580, height=250)
Scroll_bar = Scrollbar(fenetre)
Scroll_bar.place(x=750, y=210, height=380)
tree.configure(yscrollcommand=Scroll_bar.set)
Scroll_bar.configure(command=tree.yview)

# Add Headings
tree.heading(1, text="ID", command=lambda: commands("ID"))
tree.heading(2, text="Name", command=lambda: commands("Name"))
tree.heading(3, text="Year", command=lambda: commands("Year"))
tree.heading(4, text="Rating", command=lambda: commands("Rating"))
tree.heading(5, text="Language", command=lambda: commands("Language"))

# define colunms width
tree.column(1, width=10, anchor="center")
tree.column(2, width=300, anchor="center")
tree.column(3, width=20, anchor="center")
tree.column(4, width=20, anchor="center")
tree.column(5, width=20, anchor="center")

# style = ttk.Style()
# style.configure("Treeview", rowheight=40)

def found_movies(len_found_movie):
	print("len_found_movie :", len_found_movie)
	if len_found_movie == 0:
		label_found_movies["text"] = "no found movie"
		label_found_movies["fg"] = "red"
	elif len_found_movie == 1:
		label_found_movies["text"] = str(len_found_movie) + " movie found"
		label_found_movies["fg"] = "green"
	elif len_found_movie == lengthSelect():
		label_found_movies["text"] = str(lengthSelect()) + " movies"
	else:
		label_found_movies["text"] = str(len_found_movie) + " movies found"
		label_found_movies["fg"] = "green"

def search_by(event):
	global field
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	if field == "name":
		res = cursor.execute("SELECT * FROM Movies WHERE name LIKE '%{}%' OR movie_other_name LIKE '%{}%'".format(entry_search.get(), entry_search.get()))
		watched_or_not(res)
		ress = cursor.execute("SELECT * FROM Movies WHERE name LIKE '%{}%' OR movie_other_name LIKE '%{}%'".format(entry_search.get(), entry_search.get()))
		found_movies(len(list(ress)))
	elif field == "year":
		res = cursor.execute("SELECT * FROM Movies WHERE year LIKE '%{}%'".format(entry_search.get()))
		watched_or_not(res)
		ress = cursor.execute("SELECT * FROM Movies WHERE year LIKE '%{}%'".format(entry_search.get()))
		found_movies(len(list(ress)))
	elif field == "rating":
		res = cursor.execute("SELECT * FROM Movies WHERE rating LIKE '{}%'".format(entry_search.get()))
		watched_or_not(res)
		ress = cursor.execute("SELECT * FROM Movies WHERE rating LIKE '{}%'".format(entry_search.get()))
		found_movies(len(list(ress)))
	elif field == "language":
		res = cursor.execute("SELECT * FROM Movies WHERE language LIKE '{}%'".format(entry_search.get()))
		watched_or_not(res)
		ress = cursor.execute("SELECT * FROM Movies WHERE language LIKE '{}%'".format(entry_search.get()))
		found_movies(len(list(ress)))
	conn.close()
	try:
		child_id = tree.get_children()[0] # for instance the first element in tuple
		tree.focus(child_id)
		tree.selection_set(child_id)
	except:
		pass


def treeFocus(event):
	child_id = tree.get_children()[0] # for instance the first element in tuple
	tree.focus(child_id)
	tree.selection_set(child_id)
entry_search.bind("<Return>", treeFocus)


#####################################################
def last_focus(event):
	# _iid = tree.identify_row(event.y)
	_iid = tree.get_children()[lengthSelect()-tree.item(tree.selection())["values"][0]]
	tree.focus(_iid)
	tree.selection_set(_iid)
	# print(lengthSelect()-tree.item(tree.selection())["values"][0])

# tree.bind("<ButtonRelease>", last_focus)
#####################################################

create_database()
last_update()

def len_the_types():
	dictionnatyTypes = {
		"thriller" : 0,
		"action" : 0,
		"animation" : 0,
		"history" : 0,
		"crime" : 0,
		"fantasy" : 0,
		"scifi" : 0,
		"horror" : 0,
		"romance" : 0,
		"sport" : 0,
		"biography" : 0,
		"family" : 0,
		"western" : 0,
		"mystery" : 0,
		"short" : 0,
		"comedy" : 0,
		"adventure" : 0,
		"musical" : 0,
		"war" : 0,
		"drama" : 0,
		"documentary" : 0
	}
	theTypesList1 = []
	theTypesList2 = []
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	theTypes = cursor.execute("SELECT the_type FROM Movies")
	theTypes = list(theTypes)
	for i in theTypes:
		theType = i[0].split(",")
		theTypesList1.append(theType)
	for j in theTypesList1:
		theTypesList2.append(" ".join(j))
	theTypesList = " ".join(theTypesList2)
	theTypesList = theTypesList.split(" ")
	for i in theTypesList:
		dictionnatyTypes[i] += 1
	conn.close()
	button_thriller["text"] = "thriller".title() + "(" + str(dictionnatyTypes["thriller"]) + ")"
	button_action["text"] = "action".title() + "(" + str(dictionnatyTypes["action"]) + ")"
	button_animation["text"] = "animation".title() + "(" + str(dictionnatyTypes["animation"]) + ")"
	button_history["text"] = "history".title() + "(" + str(dictionnatyTypes["history"]) + ")"
	button_crime["text"] = "crime".title() + "(" + str(dictionnatyTypes["crime"]) + ")"
	button_fantasy["text"] = "fantasy".title() + "(" + str(dictionnatyTypes["fantasy"]) + ")"
	button_scifi["text"] = "science Fiction".title() + "(" + str(dictionnatyTypes["scifi"]) + ")"
	button_horror["text"] = "horror".title() + "(" + str(dictionnatyTypes["horror"]) + ")"
	button_romance["text"] = "romance".title() + "(" + str(dictionnatyTypes["romance"]) + ")"
	button_sport["text"] = "sport".title() + "(" + str(dictionnatyTypes["sport"]) + ")"
	button_biography["text"] = "biography".title() + "(" + str(dictionnatyTypes["biography"]) + ")"
	button_family["text"] = "family".title() + "(" + str(dictionnatyTypes["family"]) + ")"
	button_western["text"] = "western".title() + "(" + str(dictionnatyTypes["western"]) + ")"
	button_mystery["text"] = "mystery".title() + "(" + str(dictionnatyTypes["mystery"]) + ")"
	button_short["text"] = "short".title() + "(" + str(dictionnatyTypes["short"]) + ")"
	button_comedy["text"] = "comedy".title() + "(" + str(dictionnatyTypes["comedy"]) + ")"
	button_adventure["text"] = "adventure".title() + "(" + str(dictionnatyTypes["adventure"]) + ")"
	button_musical["text"] = "musical".title() + "(" + str(dictionnatyTypes["musical"]) + ")"
	button_war["text"] = "war".title() + "(" + str(dictionnatyTypes["war"]) + ")"
	button_drama["text"] = "drama".title() + "(" + str(dictionnatyTypes["drama"]) + ")"
	button_documentary["text"] = "documentary".title() + "(" + str(dictionnatyTypes["documentary"]) + ")"

def func_checkbutton_search_by_name(event):
	global field
	field = "name"
	label_search_by["text"] = "Search by {} :".format(field)
def func_checkbutton_search_by_year(event):
	global field
	field = "year"
	label_search_by["text"] = "Search by {} :".format(field)
def func_checkbutton_search_by_rating(event):
	global field
	field = "rating"
	label_search_by["text"] = "Search by {} :".format(field)
def func_checkbutton_search_by_language(event):
	global field
	field = "language"
	label_search_by["text"] = "Search by {} :".format(field)

def commands(the_command):
	global etat_command
	global results
	# clear the Tree View
	for i in tree.get_children():
		tree.delete(i)
	# create connection
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	if etat_command:
		results = cursor.execute("SELECT * FROM Movies ORDER BY {} ASC".format(the_command))
	else:
		results = cursor.execute("SELECT * FROM Movies ORDER BY {} DESC".format(the_command))
	
	if len(entry_search.get()):
		movie = entry_search.get()
		if etat_command:
			movie_res = cursor.execute("SELECT * FROM Movies WHERE {} LIKE '{}%' ORDER BY {} ASC".format(var_choix.get(), movie, the_command))
		else:
			movie_res = cursor.execute("SELECT * FROM Movies WHERE {} LIKE '{}%' ORDER BY {} DESC".format(var_choix.get(), movie, the_command))
		movie_res = list(movie_res)
		for row in movie_res:
			tree.insert("", END, value=row, tags=(str(row[1]) + " " + str(row[2]),))
			if row[10] == "True":
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="green")
			elif row[10] == "False":
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="red")
			else:
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="blue")
	else:
		for row in results:
			tree.insert("", END, value=row, tags=(str(row[1]) + " " + str(row[2]),))
			if row[10] == "True":
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="green")
			elif row[10] == "False":
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="red")
			else:
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="blue")

	etat_command = not(etat_command)
	conn.close()
# Get good IDs
def get_IDs():
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	the_IDs = cursor.execute("SELECT * FROM Movies")
	the_IDs = list(the_IDs)
	print(str(len(the_IDs)) + " movies found!")
	for i, j in enumerate(the_IDs):
		if not i+1 == j[0]:
			print(str(j[0]) + "-----> " + str(i+1))
			cursor.execute("UPDATE Movies SET id=? WHERE id=?", (i+1, j[0]))
			conn.commit()
	conn.close()
get_IDs()

def refresh(event):
	get_IDs()

def watched_or_not(selection):
	for i in tree.get_children():
		tree.delete(i)
	for row in selection:
		tree.insert("", END, value=row, tags=(str(row[1]) + " " + str(row[2]),))
		if row[10] == "True":
			tree.tag_configure(str(row[1]) + " " + str(row[2]), background="green")
		elif row[10] == "False":
			tree.tag_configure(str(row[1]) + " " + str(row[2]), background="red")
		else:
			tree.tag_configure(str(row[1]) + " " + str(row[2]), background="blue")

def display_movies():
	# display data in treeview object
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	select = cursor.execute("SELECT * FROM Movies ORDER BY id DESC")
	watched_or_not(select)
	conn.close()
	if lengthSelect():
		len_the_types()
	colors = open("Colors.txt", "r")
	theColors = colors.readlines()
	if len(theColors) == 3:
		foregroundColor = theColors[0][:-1]
		backgroundColor = theColors[1][:-1]
		button_add["fg"] = foregroundColor
		button_add["bg"] = backgroundColor
		button_update["fg"] = foregroundColor
		button_update["bg"] = backgroundColor
		button_delete["fg"] = foregroundColor
		button_delete["bg"] = backgroundColor
		button_watch_trailer["fg"] = foregroundColor
		button_watch_trailer["bg"] = backgroundColor
		button_egybest["fg"] = foregroundColor
		button_egybest["bg"] = backgroundColor
		button_torrent["fg"] = foregroundColor
		button_torrent["bg"] = backgroundColor
		button_wrtie_in_file["fg"] = foregroundColor
		button_wrtie_in_file["bg"] = backgroundColor
		button_exit["fg"] = foregroundColor
		button_exit["bg"] = backgroundColor
		button_drive["fg"] = foregroundColor
		button_drive["bg"] = backgroundColor
		button_get_watched_movies["fg"] = foregroundColor
		button_get_watched_movies["bg"] = backgroundColor
	# conn = sqlite3.connect("MOVIES.db")
	# cursor = conn.cursor()
	# actors = list(cursor.execute("SELECT name, year, actors FROM Movies"))
	# for i in actors:
	# 	if len(i[2].split(",")) != 6:
	# 		print(i[0], i[1], len(i[2].split(",")))
	# conn.close()
	colors.close()
	treeFocus("event")

display_movies()

def add_the_movie(event):
	# add_movie()
	add_movie_threading.start()

tree.focus()
entry_name.bind("<Return>", add_the_movie)

############################################################################################
def openTop(event):
	fenetre2 = Toplevel(fenetre)
	fenetre2.focus()
	Profile_subtitles = {1 : ""}
	idSelect = tree.item(tree.selection())["values"][0]
	nameSelect = tree.item(tree.selection())["values"][1]
	yearSelect = tree.item(tree.selection())["values"][2]
	ratingSelect = tree.item(tree.selection())["values"][3]
	languageSelect = tree.item(tree.selection())["values"][4]
	photoSelect = tree.item(tree.selection())["values"][6]
	storySelect = tree.item(tree.selection())["values"][7]
	typeSelect = tree.item(tree.selection())["values"][9]
	fenetre2.title("{} {}".format(tree.item(tree.selection())["values"][1], tree.item(tree.selection())["values"][2]))
	fenetre2.geometry("900x700")
	print(tree.item(tree.selection())["values"][0])
	load = Image.open(os.path.dirname(os.path.abspath(__file__)) + "/Movies Images/{}".format(photoSelect))
	load.thumbnail((600, 350))
	photo = ImageTk.PhotoImage(load)
	Profile_subtitles[1] = photo
	label_picture_1 = Label(fenetre2, image=photo)
	label_picture_1.place(x=350, y=0)
	label_name_1 = Label(fenetre2, text="Name", font=("Times", 12))
	label_name_1.place(x=5, y=380)
	name_1 = Label(fenetre2, text=str(nameSelect) + " (" + str(yearSelect) + ")", font=("Times", 14))
	name_1.place(x=60, y=380)
	label_type_1 = Label(fenetre2, text="Type", font=("Times", 12))
	label_type_1.place(x=5, y=420)
	type_1 = Label(fenetre2, text=str(typeSelect).replace(",", " - ").replace("scifi", "Science Fiction").title(), font=("Times", 14))
	type_1.place(x=60, y=420)
	label_rating_1 = Label(fenetre2, text="Rating", font=("Times", 12))
	label_rating_1.place(x=490, y=420)
	rating_1 = Label(fenetre2, text=str(ratingSelect) + "/10", font=("Times", 14))
	rating_1.place(x=540, y=420)
	label_language_1 = Label(fenetre2, text="Language", font=("Times", 12))
	label_language_1.place(x=680, y=420)
	language_1 = Label(fenetre2, text=str(languageSelect), font=("Times", 14))
	language_1.place(x=750, y=420)
	label_story_1 = Label(fenetre2, text="Story", font=("Times", 12))
	label_story_1.place(x=350, y=470)
	story_1 = Text(fenetre2, font=("Times", 14))
	story_1.place(x=5, y=500)
	story_1.insert(END, str(storySelect))
	def theExit(event):
		fenetre2.destroy()
		child_id = tree.get_children()[lengthSelect()-idSelect] # for instance the first element in tuple
		tree.focus(child_id)
		tree.selection_set(child_id)
		tree.focus()
	def view_subtitles():
		nameSelect = tree.item(tree.selection())["values"][1]
		yearSelect = tree.item(tree.selection())["values"][2]
		
		fenetre_subtitles = Toplevel(fenetre2)
		fenetre_subtitles.geometry("830x600")
		fenetre_subtitles.focus()
		
		os.makedirs("Subtitles Databases/", exist_ok=True)

		if "{} {}.db".format(nameSelect, yearSelect) in os.listdir("Subtitles Databases/"):

			def treeSubtitlesSelect(event):
				button_download["state"] = "normal"
			def get_the_subtitle():
				link = tree_subtitles.item(tree_subtitles.selection())["values"][5]
				print(link)
				os.makedirs("Download ZIPs/{} {}/".format(nameSelect, yearSelect), exist_ok=True)
				if link.split("/")[-1] in os.listdir("Download ZIPs/{} {}".format(nameSelect, yearSelect)):
					print(str(os.path.dirname(os.path.abspath(__file__)) + "/Download ZIPs/{} {}/{}".format(nameSelect, yearSelect, link.split("/")[-1])).replace("\\", "/"))
					with ZipFile(str(os.path.dirname(os.path.abspath(__file__)) + "/Download ZIPs/{} {}/{}".format(nameSelect, yearSelect, link.split("/")[-1])).replace("\\", "/"), "r") as zipObj:
						os.makedirs(str(os.path.dirname(os.path.abspath(__file__)) + "/Download ZIPs/{} {}/".format(nameSelect, yearSelect)).replace("\\", "/") + str(link.split("/")[-1][:-3]), exist_ok=True)
						zipObj.extractall(str(os.path.dirname(os.path.abspath(__file__)) + "/Download ZIPs/{} {}/".format(nameSelect, yearSelect)).replace("\\", "/") + str(link.split("/")[-1][:-3]))
						os.startfile(str(os.path.dirname(os.path.abspath(__file__)) + "/Download ZIPs/{} {}/".format(nameSelect, yearSelect)).replace("\\", "/") + str(link.split("/")[-1][:-3]))

					# os.startfile(str(os.path.dirname(os.path.abspath(__file__)) + "/Download ZIPs/{} {}/".format(nameSelect, yearSelect)).replace("\\", "/"))
					# os.startfile(str(os.path.dirname(os.path.abspath(__file__)) + "/Download ZIPs/{} {}/{}".format(nameSelect, yearSelect, link.split("/")[-1])).replace("\\", "/"))
				else:
					if messagebox.askokcancel(title="No subtitles", message="Download Subtitles ?"):
						if messagebox.askokcancel(title="All Subtitles", message="Download all Subtitles ?\nAll subtitles : OK\nJust this one : Cancel"):
							movie_database = "{} {}".format(nameSelect, yearSelect)
							print(movie_database)
							conn = sqlite3.connect("Subtitles Databases/" + str(movie_database) + ".db")
							cursor = conn.cursor()
							select = list(cursor.execute("SELECT Zip_File FROM Subtitles"))
							if len(os.listdir("Download ZIPs/{}/".format(movie_database))) < len(select):
								for i in select:
									theUrl = str(i[0])
									nom = i[0].split("/")[-1]
									if not nom in os.listdir("Download ZIPs/{}/".format(movie_database)):
										print(nom)
										# r = requests.get(theUrl, allow_redirects=True)
										# open('Download ZIPs/{}/{}'.format(movie_database, nom), 'wb').write(r.content)
										download_with_progress(theUrl, 'Download ZIPs/{}/{}'.format(movie_database, nom), "." + str(nom.split(".")[-1]))
								conn.close()
								print("Subtitles are downloaded")
								messagebox.showinfo("Success", "Subtitles are downloaded successfuly")
								# winsound.Beep(300, 750)
							else:
								print("EXIST deja")
						else:
							movie_database = "{} {}".format(nameSelect, yearSelect)
							nom = link.split("/")[-1]
							# r = requests.get(link, allow_redirects=True)
							# open('Download ZIPs/{}/{}'.format(movie_database, nom), 'wb').write(r.content)
							download_with_progress(link, 'Download ZIPs/{}/{}'.format(movie_database, nom), "." + str(nom.split(".")[-1]))
							print("Subtitle downloaded")
							messagebox.showinfo("Success", "Subtitle downloaded successfuly")
					else:
						fenetre_subtitles.focus()
			def getTheSubtitle(event):
				get_the_subtitle()

			# Add TreeView
			tree_subtitles = ttk.Treeview(fenetre_subtitles, columns=(1, 2, 3, 4), height=5, show="headings")
			tree_subtitles.place(x=5, y=20, width=800, height=450)
			tree_subtitles.bind("<<TreeviewSelect>>", treeSubtitlesSelect)
			Scroll_bar = Scrollbar(fenetre_subtitles)
			Scroll_bar.place(x=810, y=20, height=450)
			tree_subtitles.configure(yscrollcommand=Scroll_bar.set)
			Scroll_bar.configure(command=tree_subtitles.yview)
			# Add Headings
			tree_subtitles.heading(1, text="id")
			tree_subtitles.heading(2, text="Rating")
			tree_subtitles.heading(3, text="Language")
			tree_subtitles.heading(4, text="Subtitle")
			# define colunms width
			tree_subtitles.column(1, width=5, anchor="center")
			tree_subtitles.column(2, width=5, anchor="center")
			tree_subtitles.column(3, width=10, anchor="center")
			tree_subtitles.column(4, width=300, anchor="center")

			button_download = Button(fenetre_subtitles, text="Download subtitle", command=get_the_subtitle, state=DISABLED, font=("Arial", 15))
			button_download.place(x=300, y=480)

			# display values :
			for i in tree_subtitles.get_children():
				tree_subtitles.delete(i)
				tree_subtitles.delete(i)
			conn = sqlite3.connect("Subtitles Databases/{} {}.db".format(nameSelect, yearSelect))
			cursor = conn.cursor()
			selection = list(cursor.execute("SELECT * FROM Subtitles ORDER BY Language ASC"))
			for row in selection:
				tree_subtitles.insert("", END, value=row, tags=(str(row[0]),))
			conn.close()
			tree_subtitles.bind("<Return>", getTheSubtitle)
			tree_subtitles.bind("<Double-Button-1>", getTheSubtitle)
		else:
			label_error = Label(fenetre_subtitles, text="NO EXIST SUBTITLES", font=("Times", 45))
			label_error.pack()
			print("NO EXIST SUBTITLES")

		fenetre_subtitles.bind("<Escape>", lambda _: fenetre_subtitles.destroy())
		fenetre_subtitles.mainloop()
	def view_actors():
		nameSelect = tree.item(tree.selection())["values"][1]
		yearSelect = tree.item(tree.selection())["values"][2]
		# ****************************************************************************
		fenetre_actors = Toplevel(fenetre)
		Profile_actors = {1 : ""}

		os.makedirs("Actors Images/", exist_ok=True)

		the_folder = str(nameSelect) + " " + str(yearSelect)
		fenetre_actors.title(the_folder)
		def load_photo(photoSelect):
			load = Image.open("Actors Images/{}/{}".format(str(nameSelect) + " " + str(yearSelect), photoSelect))
			load.thumbnail((120, 120))
			photo = ImageTk.PhotoImage(load)
			Profile_actors[0] = photo
			return photo

		images = [img for img in os.listdir("Actors Images/{}".format(the_folder))]

		def movies_actor(nbr):
			print(images[nbr][:-4])
			for i in tree.get_children():
				tree.delete(i)
			conn = sqlite3.connect("MOVIES.db")
			cursor = conn.cursor()
			movies_res = cursor.execute("SELECT * FROM Movies WHERE actors LIKE '%{}%'".format(images[nbr][:-4]))
			print(len(list(movies_res)), "Movies")
			movies_actors = list(cursor.execute("SELECT * FROM Movies WHERE actors LIKE '%{}%'".format(images[nbr][:-4])))
			for actor in movies_actors:
				tree.insert("", END, value=actor, tags=(str(actor[1]) + " " + str(actor[2]),))
				print(str(actor[2]) + " : " + str(actor[1]))
			conn.close()
			fenetre.focus()

		if len(images) >= 1:
			photo1 = load_photo(images[0])
			Profile_actors[1] = photo1
			photo_actor_1 = Label(fenetre_actors, image=photo1)
			photo_actor_1.grid(row=0, column=0)
			actor_1 = Button(fenetre_actors, text=images[0][:-4], font=("Times", 15), command=lambda: movies_actor(0))
			actor_1.grid(row=1, column=0)
			photo_actor_1.bind("<Double-Button-1>", lambda _: movies_actor(0))

		if len(images) >= 2:
			photo2 = load_photo(images[1])
			Profile_actors[2] = photo2
			photo_actor_2 = Label(fenetre_actors, image=photo2)
			photo_actor_2.grid(row=0, column=1)
			actor_2 = Button(fenetre_actors, text=images[1][:-4], font=("Times", 15), command=lambda: movies_actor(1))
			actor_2.grid(row=1, column=1)
			photo_actor_2.bind("<Double-Button-1>", lambda _: movies_actor(1))

		if len(images) >= 3:
			photo3 = load_photo(images[2])
			Profile_actors[3] = photo3
			photo_actor_3 = Label(fenetre_actors, image=photo3)
			photo_actor_3.grid(row=0, column=2)
			actor_3 = Button(fenetre_actors, text=images[2][:-4], font=("Times", 15), command=lambda: movies_actor(2))
			actor_3.grid(row=1, column=2)
			photo_actor_3.bind("<Double-Button-1>", lambda _: movies_actor(2))

		if len(images) >= 4:
			photo4 = load_photo(images[3])
			Profile_actors[4] = photo4
			photo_actor_4 = Label(fenetre_actors, image=photo4)
			photo_actor_4.grid(row=2, column=0)
			actor_4 = Button(fenetre_actors, text=images[3][:-4], font=("Times", 15), command=lambda: movies_actor(3))
			actor_4.grid(row=3, column=0)
			photo_actor_4.bind("<Double-Button-1>", lambda _: movies_actor(3))

		if len(images) >= 5:
			photo5 = load_photo(images[4])
			Profile_actors[5] = photo5
			photo_actor_5 = Label(fenetre_actors, image=photo5)
			photo_actor_5.grid(row=2, column=1)
			actor_5 = Button(fenetre_actors, text=images[4][:-4], font=("Times", 15), command=lambda: movies_actor(4))
			actor_5.grid(row=3, column=1)
			photo_actor_5.bind("<Double-Button-1>", lambda _: movies_actor(4))

		if len(images) >= 6:
			photo6 = load_photo(images[5])
			Profile_actors[6] = photo6
			photo_actor_6 = Label(fenetre_actors, image=photo6)
			photo_actor_6.grid(row=2, column=2)
			actor_6 = Button(fenetre_actors, text=images[5][:-4], font=("Times", 15), command=lambda: movies_actor(5))
			actor_6.grid(row=3, column=2)
			photo_actor_6.bind("<Double-Button-1>", lambda _: movies_actor(5))

		fenetre_actors.bind("<Escape>", lambda _: fenetre_actors.destroy())
		fenetre_actors.mainloop()
		# ****************************************************************************
	button_view_subtitles = Button(fenetre2, text="Subtitles", command=view_subtitles, font=("Arial", 15))
	button_view_subtitles.place(x=360, y=360)
	button_view_actors = Button(fenetre2, text="Actors", command=view_actors, font=("Arial", 15))
	button_view_actors.place(x=480, y=360)
	fenetre2.bind("<Escape>", theExit)
	fenetre2.mainloop()
############################################################################################

def replace_movies(event):
	global etat_replace_movies, id_Select1, name_Select1, year_Select1, rating_Select1, language_Select1, movie_other_name_Select1, picture_Select1, story_Select1, trailer_Select1, the_type_Select1, watched_Select1, linkEgybest_Select1, linkYTS_Select1, actors_Select1, id_Select2, name_Select2, year_Select2, rating_Select2, language_Select2, movie_other_name_Select2, picture_Select2, story_Select2, trailer_Select2, the_type_Select2, watched_Select2, linkEgybest_Select2, linkYTS_Select2, actors_Select2
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	movies_res = cursor.execute("SELECT * FROM Movies")
	for row in movies_res:
			tree.insert("", END, value=row, tags=(str(row[1]) + " " + str(row[2]),))
			if row[10] == "True":
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="green", foreground="black")
			elif row[10] == "False":
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="red", foreground="black")
			else:
				tree.tag_configure(str(row[1]) + " " + str(row[2]), background="blue", foreground="black")
	conn.close()
	if not etat_replace_movies:
		id_Select1 = name_Select1 = year_Select1 = rating_Select1 = language_Select1 = movie_other_name_Select1 = picture_Select1 = story_Select1 = trailer_Select1 = the_type_Select1 = watched_Select1 = linkEgybest_Select1 = linkYTS_Select1 = actors_Select1 = id_Select2 = name_Select2 = year_Select2 = rating_Select2 = language_Select2 = movie_other_name_Select2 = picture_Select2 = story_Select2 = trailer_Select2 = the_type_Select2 = watched_Select2 = linkEgybest_Select2 = linkYTS_Select2 = actors_Select2 = ""
		id_Select1 = int(tree.item(tree.selection())["values"][0])
		name_Select1 = str(tree.item(tree.selection())["values"][1])
		year_Select1 = int(tree.item(tree.selection())["values"][2])
		rating_Select1 = str(tree.item(tree.selection())["values"][3])
		language_Select1 = str(tree.item(tree.selection())["values"][4])
		movie_other_name_Select1 = str(tree.item(tree.selection())["values"][5])
		picture_Select1 = str(tree.item(tree.selection())["values"][6])
		story_Select1 = str(tree.item(tree.selection())["values"][7])
		trailer_Select1 = str(tree.item(tree.selection())["values"][8])
		the_type_Select1 = str(tree.item(tree.selection())["values"][9])
		watched_Select1 = str(tree.item(tree.selection())["values"][10])
		linkEgybest_Select1 = str(tree.item(tree.selection())["values"][11])
		linkYTS_Select1 = str(tree.item(tree.selection())["values"][12])
		actors_Select1 = str(tree.item(tree.selection())["values"][13])
		tree.tag_configure(str(name_Select1) + " " + str(year_Select1), background="gray")
		etat_replace_movies = True
		print('You have selected "{}", Please select the second movie to switch'.format(name_Select1))
	else:
		id_Select2 = int(tree.item(tree.selection())["values"][0])
		name_Select2 = str(tree.item(tree.selection())["values"][1])
		year_Select2 = int(tree.item(tree.selection())["values"][2])
		rating_Select2 = str(tree.item(tree.selection())["values"][3])
		language_Select2 = str(tree.item(tree.selection())["values"][4])
		movie_other_name_Select2 = str(tree.item(tree.selection())["values"][5])
		picture_Select2 = str(tree.item(tree.selection())["values"][6])
		story_Select2 = str(tree.item(tree.selection())["values"][7])
		trailer_Select2 = str(tree.item(tree.selection())["values"][8])
		the_type_Select2 = str(tree.item(tree.selection())["values"][9])
		watched_Select2 = str(tree.item(tree.selection())["values"][10])
		linkEgybest_Select2 = str(tree.item(tree.selection())["values"][11])
		linkYTS_Select2 = str(tree.item(tree.selection())["values"][12])
		actors_Select2 = str(tree.item(tree.selection())["values"][13])
		if not id_Select1 == id_Select2:
			conn = sqlite3.connect("MOVIES.db")
			cursor = conn.cursor()
			cursor.execute("UPDATE Movies SET name=?, year=?, rating=?, language=?, movie_other_name=?, picture=?, story=?, trailer=?, the_type=?, watched=?, linkEgybest=?, linkYTS=?, actors=? WHERE id=?", (name_Select1, year_Select1, rating_Select1, language_Select1, movie_other_name_Select1, picture_Select1, story_Select1, trailer_Select1, the_type_Select1, watched_Select1, linkEgybest_Select1, linkYTS_Select1, actors_Select1, id_Select2))
			conn.commit()
			conn.close()
			conn = sqlite3.connect("MOVIES.db")
			cursor = conn.cursor()
			cursor.execute("UPDATE Movies SET name=?, year=?, rating=?, language=?, movie_other_name=?, picture=?, story=?, trailer=?, the_type=?, watched=?, linkEgybest=?, linkYTS=?, actors=? WHERE id=?", (name_Select2, year_Select2, rating_Select2, language_Select2, movie_other_name_Select2, picture_Select2, story_Select2, trailer_Select2, the_type_Select2, watched_Select2, linkEgybest_Select2, linkYTS_Select2, actors_Select2, id_Select1))
			conn.commit()
			conn.close()
			print("{} <---> {}".format(name_Select1, name_Select2))
			tree.tag_configure(str(name_Select1) + " " + str(year_Select1), foreground="white")
			tree.tag_configure(str(name_Select2) + " " + str(year_Select2), foreground="white")
			etat_replace_movies = False
			display_movies()
			return messagebox.showinfo(title="Success", message="{} and {} are switched successfuly".format(name_Select1, name_Select2))
def check_etat_replace_movies(event):
	if etat_replace_movies:
		replace_movies("event")
	else:
		openTop("event")

checkbutton_search_by_name.bind("<ButtonRelease>", func_checkbutton_search_by_name)
checkbutton_search_by_year.bind("<ButtonRelease>", func_checkbutton_search_by_year)
checkbutton_search_by_rating.bind("<ButtonRelease>", func_checkbutton_search_by_rating)
checkbutton_search_by_language.bind("<ButtonRelease>", func_checkbutton_search_by_language)
entry_search.bind("<Key>", search_by)
entry_search.bind("<Return>", search_by)

################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
s = ttk.Style()
if fenetre.getvar('tk_patchLevel')=='8.6.9': #and OS_Name=='nt':
	def fixed_map(option):
		# Fix for setting text colour for Tkinter 8.6.9
		# From: https://core.tcl.tk/tk/info/509cafafae
		#
		# Returns the style map for 'option' with any styles starting with
		# ('!disabled', '!selected', ...) filtered out.
		#
		# style.map() returns an empty list for missing options, so this
		# should be future-safe.
		return [elm for elm in s.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
	s.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# fenetre.bind("<F5>", refresh)
fenetre.bind("<F2>", new_movie)
fenetre.bind("<F5>", update_infos)
fenetre.bind("<Control-u>", update_the_movie)
fenetre.bind("<Control-U>", update_the_movie)
fenetre.bind("<Control-f>", lambda _: entry_search.focus())
fenetre.bind("<Control-F>", lambda _: entry_search.focus())
fenetre.bind("<Control-r>", refresh)
fenetre.bind("<Control-R>", refresh)
tree.bind("<<TreeviewSelect>>", treeActionSelect)
tree.bind("<Delete>", event_button_delete)
tree.bind("<r>", replace_movies)
tree.bind("<R>", replace_movies)
tree.bind("<d>", open_google_drive)
tree.bind("<D>", open_google_drive)
tree.bind("<e>", EgyBest)
tree.bind("<E>", EgyBest)
tree.bind("<t>", Torrent)
tree.bind("<T>", Torrent)
tree.bind("<y>", open_youtube)
tree.bind("<Y>", open_youtube)
tree.bind("<w>", watched_already)
tree.bind("<W>", watched_already)

tree.bind('<Control-a>', lambda *args: tree.selection_add(tree.get_children())) #selected all row treeview
tree.bind('<Control-A>', lambda *args: tree.selection_add(tree.get_children())) #selected all row treeview

########################################################################################################
# SHOW IN FILE
def get_name_file(event):
	os.makedirs("SHOW IN FILE/", exist_ok=True)
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	movies_name = list(cursor.execute("SELECT * FROM Movies ORDER BY name ASC"))
	if os.path.isfile(os.path.join(os.getcwd(), "SHOW IN FILE/", "movies_name.txt")):
		os.remove(os.path.join(os.getcwd(), "SHOW IN FILE/", "movies_name.txt"))
		print("File Deleted")
	for row in movies_name:
		file_name = open("SHOW IN FILE/Name.txt", "a")
		file_name.write(str(int(movies_name.index(row)) + 1) + "- " + str(row[1]) + " (" + str(row[2]) + ") " + str(row[3]) + " " + str(row[4]) + "\n")
		file_name.close()
	conn.close()
	print("NAME SHOW IN FILE")

def get_year_file(event):
	os.makedirs("SHOW IN FILE/", exist_ok=True)
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	movies_year = list(cursor.execute("SELECT * FROM Movies ORDER BY year DESC"))
	if os.path.isfile(os.path.join(os.getcwd(), "SHOW IN FILE/", "movies_year.txt")):
		os.remove(os.path.join(os.getcwd(), "SHOW IN FILE/", "movies_year.txt"))
		print("File Deleted")
	for row in movies_year:
		file_year = open("SHOW IN FILE/Year.txt", "a")
		file_year.write(str(int(movies_year.index(row)) + 1) + "- " + str(row[1]) + " (" + str(row[2]) + ") " + str(row[3]) + " " + str(row[4]) + "\n")
		file_year.close()
	conn.close()
	print("YEAR SHOW IN FILE")

def get_rating_file(event):
	os.makedirs("SHOW IN FILE/", exist_ok=True)
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	movies_rating = list(cursor.execute("SELECT * FROM Movies ORDER BY rating DESC"))
	if os.path.isfile(os.path.join(os.getcwd(), "SHOW IN FILE/", "movies_rating.txt")):
		os.remove(os.path.join(os.getcwd(), "SHOW IN FILE/", "movies_rating.txt"))
		print("File Deleted")
	for row in movies_rating:
		file_rating = open("SHOW IN FILE/Rating.txt", "a")
		file_rating.write(str(int(movies_rating.index(row)) + 1) + "- " + str(row[1]) + " (" + str(row[2]) + ") " + str(row[3]) + " " + str(row[4]) + "\n")
		file_rating.close()
	conn.close()
	print("RATING SHOW IN FILE")

def get_language_file(event):
	os.makedirs("SHOW IN FILE/", exist_ok=True)
	conn = sqlite3.connect("MOVIES.db")
	cursor = conn.cursor()
	movies_language = list(cursor.execute("SELECT * FROM Movies ORDER BY language ASC"))
	if os.path.isfile(os.path.join(os.getcwd(), "SHOW IN FILE/", "movies_language.txt")):
		os.remove(os.path.join(os.getcwd(), "SHOW IN FILE/", "movies_language.txt"))
		print("File Deleted")
	for row in movies_language:
		file_language = open("SHOW IN FILE/Language.txt", "a")
		file_language.write(str(int(movies_language.index(row)) + 1) + "- " + str(row[1]) + " (" + str(row[2]) + ") " + str(row[3]) + " " + str(row[4]) + "\n")
		file_language.close()
	conn.close()
	print("LANGUAGE SHOW IN FILE")

fenetre.bind('<Control-y>', get_year_file)
fenetre.bind('<Control-Y>', get_year_file)

fenetre.bind('<Control-n>', get_name_file)
fenetre.bind('<Control-N>', get_name_file)

fenetre.bind('<Control-l>', get_language_file)
fenetre.bind('<Control-L>', get_language_file)

fenetre.bind('<Control-p>', get_rating_file)
fenetre.bind('<Control-P>', get_rating_file)
########################################################################################################

def sortir(event):
	exit()

tree.bind('<Double-Button-1>', openTop)
tree.bind('<Return>', check_etat_replace_movies)

fenetre.bind("<Escape>", sortir)

fenetre.mainloop()


# Movies : https://teer.egybest.com/movie/{"movie-name"}-{"year"}/
# Series : https://teer.egybest.com/series/{"serie-name"}-{"year"}/
# Seasons : https://teer.egybest.com/season/{"serie-name"}-{"year"}-{season-"numberOfTheSeason"}/
# Episodes : https://teer.egybest.com/episode/{"serie-name"}-{"year"}-{season-"numerOfTheSeason"}-{ep-"numberOfTheEpisode"}/

# row[0] : "id"
# row[1] : "name"
# row[2] : "year"
# row[3] : "rating"
# row[4] : "language"
# row[5] : "other name"
# row[6] : "picture"
# row[7] : "story"
# row[8] : "trailer"
# row[9] : "type"
# row[10] : "watched"

# row[11] : "linkEgybest"
# row[12] : "linkYTS"
# row[13] : "actors"


# id_Select = tree.item(tree.selection())["values"][0]
# name_Select = tree.item(tree.selection())["values"][1]
# year_Select = tree.item(tree.selection())["values"][2]
# rating_Select = tree.item(tree.selection())["values"][3]
# language_Select = tree.item(tree.selection())["values"][4]
# movie_other_name_Select = tree.item(tree.selection())["values"][5]
# picture_Select = tree.item(tree.selection())["values"][6]
# story_Select = tree.item(tree.selection())["values"][7]
# trailer_Select = tree.item(tree.selection())["values"][8]
# the_type_Select = tree.item(tree.selection())["values"][9]
# watched_Select = tree.item(tree.selection())["values"][10]
# linkEgybest = tree.item(tree.selection())["values"][11]
# linkYTS = tree.item(tree.selection())["values"][12]
# actors = tree.item(tree.selection())["values"][13]


# copy function :
# def copier(event):
# 	root.clipboard_clear()
# 	root.clipboard_append("HASSAN")

# root.bind("<Control-c>", copier)
# root.bind("<Control-a>", lambda e: print("Hassan"))

# fenetre.bind("<Control-Shift-u>", replace_movies)


# <Control-Button-1> for pressing Control and mouse button 1 (left button)
# <Control-Button-3> for pressing Control and mouse button 3 (right button)














# awake
# coda
# the unforgivable
# soldier boy
# the garden of words
# case 39
# panic room
# till death
# dont look up
# erna i krig
# awake,coda,the unforgivable,soldier boy,the garden of words,case 39,panic room,till death,dont look up,erna i krig


# WIFI : inwi Home 4G65039A
# PASSWORD : 49591829

# remove folder :
# import shutil
# shutil.rmtree('Movies notebook')

# answer = messagebox.askyesno("Question","Do you like Python?")
# answer = messagebox.askyesnocancel("Question", "Continue playing?")

# heart of champions 2021























# import tkinter as tk
# from tkinter import ttk, messagebox
# import sqlite3

# class MovieDatabase:
#     def __init__(self, db_name="MOVIES.db"):
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#         self.create_table()

#     def create_table(self):
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS Movies (
#                 id INTEGER PRIMARY KEY,
#                 name TEXT,
#                 year INTEGER,
#                 rating TEXT,
#                 language TEXT,
#                 movie_other_name TEXT,
#                 picture TEXT,
#                 story TEXT,
#                 trailer TEXT,
#                 the_type TEXT,
#                 watched TEXT,
#                 linkEgybest TEXT,
#                 linkYTS TEXT,
#                 actors TEXT
#             )
#         """)
#         self.conn.commit()

#     def add_movie(self, movie_data):
#         self.cursor.execute("""
#             INSERT INTO Movies (name, year, rating, language, movie_other_name, picture, story, trailer, the_type, watched, linkEgybest, linkYTS, actors)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, movie_data)
#         self.conn.commit()

#     def get_movies(self):
#         self.cursor.execute("SELECT * FROM Movies")
#         return self.cursor.fetchall()

#     def close(self):
#         self.conn.close()

# class MovieGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Movie Manager")
#         self.root.geometry("800x600")
#         self.db = MovieDatabase()

#         self.create_widgets()
#         self.load_movies()

#     def create_widgets(self):
#         self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Year", "Rating", "Language"), show="headings")
#         self.tree.heading("ID", text="ID")
#         self.tree.heading("Name", text="Name")
#         self.tree.heading("Year", text="Year")
#         self.tree.heading("Rating", text="Rating")
#         self.tree.heading("Language", text="Language")
#         self.tree.pack(fill=tk.BOTH, expand=True)

#         self.add_button = ttk.Button(self.root, text="Add Movie", command=self.add_movie)
#         self.add_button.pack()

#     def load_movies(self):
#         for row in self.tree.get_children():
#             self.tree.delete(row)
#         for movie in self.db.get_movies():
#             self.tree.insert("", tk.END, values=movie)

#     def add_movie(self):
#         # Example: Add a new movie with some dummy data
#         movie_data = ("Inception", 2010, "8.8", "English", "", "inception.jpg", "A thief who steals corporate secrets...", "https://youtube.com", "Action", "False", "https://egybest.com", "https://yts.mx", "Leonardo DiCaprio")
#         self.db.add_movie(movie_data)
#         self.load_movies()
#         messagebox.showinfo("Success", "Movie added successfully!")

#     def on_closing(self):
#         self.db.close()
#         self.root.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MovieGUI(root)
#     root.protocol("WM_DELETE_WINDOW", app.on_closing)
#     root.mainloop()