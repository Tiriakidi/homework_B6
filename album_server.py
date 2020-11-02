from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

class ValidationError(Exception):
    def __init__(self, msg):
        self.msg = msg


@route("/albums/<artist>")
def albums(artist):
    try:
        albums_list = album.find(artist)
        album_names = [album.album for album in albums_list]
        album_size = len(album_names)
        result = "Найдено {} альбомов {}:\n".format(album_size, artist)
        result += "\n".join(album_names)
        return result
    except album.DataError as err:
        return HTTPError(err.code, "Альбомов {} не найдено".format(artist))
        

@route("/albums", method="POST")
def add_album():
    new_album = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    try:
        validate(new_album)
        album.add(new_album)
    except ValidationError as err:
        return HTTPError(400, err.msg)
    except album.DataError as err:
        return HTTPError(err.code, "Альбом {} у артиста {} уже существует".format(new_album["album"], new_album["artist"]))

def validate(album):
    if not album["artist"]:
        raise ValidationError("Имя артиста необходимо ввести")
    if not album["album"]:
        raise ValidationError("Название альбома необходимо ввести")
    max_year = 2020
    min_year = 1900
    if not album["year"].isdigit() or int(album["year"]) > max_year or int(album["year"]) < min_year:
        raise ValidationError("Вы ввели неправильный год")

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)