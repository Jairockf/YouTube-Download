from pytube import YouTube

def get_video(url, progress_callback, ruta): # Funcion para descargar videos
    yt = YouTube(url, on_progress_callback=progress_callback)
    stream = yt.streams.get_highest_resolution()
    stream.download(ruta)
    print("Video descargado con exito")

def get_audio(url, progress_callback, ruta): # Funcion para descargar musica
    yt = YouTube(url, on_progress_callback=progress_callback)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(ruta)
    print("Canción descargado con exito")

def run(stream,chunk,file_handle=None,remaining=None):
    size = 0
    total = stream.filesize
    size += len(chunk)
    progress = float(size/total*100)
    print(progress)
    print("Señan emitida")
    return progress
        
if __name__ == '__main__':
    video = input("Ingresa la URL: ")
    get_video(video)