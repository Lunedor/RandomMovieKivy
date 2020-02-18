#-*-coding:utf-8-*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from trakt.users import User
import random
import imdb
from kivy.properties import StringProperty, ObjectProperty


Builder.load_string("""
<GirisEkrani>:
    GridLayout:
        rows:4
        cols: 1
        Label:
            text: "Kullanıcı adı:"
            font_size: "20sp"
        TextInput:
            id: username
            multiline: False
            halign: 'center'
            size_hint_max_y: 40
        Button:
            text: "Oturum Aç"
            on_press: root.login()
            size_hint_max_y: 40
        Label:
            text: " "
            font_size: "20sp"

<GirisOnayEkrani>:
    GridLayout:
        cols: 2
        rows: 1
        orientation: 'horizontal'
        spacing: 10
        GridLayout:
            cols: 1
            rows: 1
            orientation: 'horizontal'
            AsyncImage:
                id: poster
                source: root.posterurl
                nocache: True
        GridLayout:
            cols: 1
            rows: 5
            orientation: 'vertical'
            spacing: 10
            Label:
                text: root.showline1
                markup: True
                bold: True
                size: self.texture_size
                halign: 'center'
                valign: 'middle'
                id: self.lbl
                size_hint_max_y: 80
            TextInput:
                text: root.showline2
                id: self.lbl2
                size_hint_max_y: 90
            TextInput:
                text: root.showline3
                id: self.lbl3
                multiline: True
            TextInput:
                text: root.showline4
                id: self.lbl4
                multiline: True
            BoxLayout:
                cols: 2
                rows: 1
                spacing: 1
                padding: 50, 10, 10, 10
                halign: 'center'
                valign: 'middle'
                size_hint_max_y: 50
                orientation: 'horizontal'
                Button:
                    text: "Good Luck!"
                    font_size: 14
                    size_hint_max_y: 40
                    on_press: root.clk()
                Button:
                    text: "Exit"
                    font_size: 14
                    size_hint_max_y: 40
                    on_press: root.clk2()

<GirisRedEkrani>:
    BoxLayout:
        orientation: "vertical"
        Label:
            text: "Hatalı Giriş"
        Button:
            text: "Tekrar Dene"
            on_press: root.anaEkranaDon()

<RootWidget>:
    id: kok
    GirisEkrani:
        id: giris
        name: "giris_ekrani"
    GirisOnayEkrani:
        id: onay
        name: "giris_basarili"
    GirisRedEkrani:
        id: red
        name: "giris_hatali"
""")


def dataget():
    myline = str(random.choice(watchlist))[9:1000]
    movies = moviesDB.search_movie(str(myline))
    id = movies[0].getID()
    global movie
    movie = moviesDB.get_movie(id)
    global posterurl
    posterurl = movie["full-size cover url"]
    global title
    title = movie['title']
    global year
    year = movie["year"]
    global rating
    rating = movie["rating"]
    global runtime
    runtimes = movie["runtimes"]
    runtime = ' '.join(map(str, runtimes))
    global directStr
    directors = movie["directors"]
    directStr = ' '.join(map(str, directors))
    global writerStr
    writers = movie["writers"]
    writerStr = ', '.join(map(str, writers))
    global casting
    casting = movie["cast"]
    global actors
    actors = ', '.join(map(str, casting))
    global summary
    summary = movie["plot outline"]
    genres = movie["genres"]
    global genre
    genre = ', '.join(map(str, genres))
    print(movie)
    print(id)

class GirisEkrani(Screen):
    def login(self):
        try:
            username = self.ids.username.text
            global moviesDB
            moviesDB = imdb.IMDb()
            myuser = User(str(username))
            global watchlist
            watchlist = myuser.watchlist_movies
            global myline
            try:
                dataget()
                # after you get new values update the variables connected to widgets
            except:
                print('Error')
                dataget()
            self.manager.current = "giris_basarili"


        except:
            self.manager.current = "giris_hatali"


class GirisOnayEkrani(Screen):

    posterurl = ObjectProperty("https://previews.123rf.com/images/fabiopagani/fabiopagani1506/fabiopagani150600017/40976008-movie-clapper-with-vintage-empty-film-reels-on-white-background-vertical-frame.jpg")
    showline1 = StringProperty("Pick")
    showline2 = StringProperty("A Movie")
    showline3 = StringProperty("For")
    showline4 = StringProperty("Me")

    def update_values(self):
        self.posterurl = movie["full-size cover url"]
        self.showline1 = title + "\n" + str(year) + " - " + str(rating) + "\n" + str(
            runtime) + " minutes" + " - " + genre
        self.showline2 = "Director: " + directStr + "\n" + "\n" + "Writers: " + writerStr
        self.showline3 = "Cast: " + actors
        self.showline4 = "Summary: " + "\n" + str(summary)


    def clk(self):
        try:
            dataget()
            # after you get new values update the variables connected to widgets
            self.update_values()
        except:
            print('Error')
            dataget()
            self.update_values()

    def clk2(self):
        exit()

class GirisRedEkrani(Screen):
    def anaEkranaDon(self):
        self.manager.current = "giris_ekrani"

class RootWidget(ScreenManager):
    pass

class RandomMovieApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    RandomMovieApp().run()