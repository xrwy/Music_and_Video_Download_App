from flask import Flask, render_template, request
from pytube import YouTube
import os

app = Flask(__name__)

video_Link = ''
video_Save_Path = ''
resolution = 0
path__ = ''


@app.route('/', methods=['GET'])
def main():
	return render_template('main.html')

@app.route('/download_video', methods=['GET'])
def successDownloadingVideo():
	return render_template('downloading_video.html')

@app.route('/download_song', methods=['GET'])
def successDownloadingSong():
	return render_template('downloading_song.html')

@app.route('/download_video_result', methods=['GET','POST'])
def downloadVideoResult():
	video_Links = []
	video_Paths = []
	true_or_False = []

	if request.method == 'POST':
		video_Link = request.form['videoLink']
		video_Save_Path = request.form['videoSavePath']
		resolution = request.form['resolution']

		if video_Link == '' or video_Save_Path == '' or resolution == '' or resolution == 'Resolution':
			return 'Do Not Leave The Fields Blank / Fill in the Fields Properly!!!'
		else:
			video_Links = video_Link.split(',')
			for video_Link in video_Links:
				if(video_Link.startswith('https://')) == False:
					return 'Please Enter Youtube Link.'
				else:
					continue


			for link in video_Links:
				resolutionP = int(resolution)
				try:
					yt = YouTube(link)
					
					video_Save_Path_ = video_Save_Path.replace('\\','/')
					video_Save_Path__ =  video_Save_Path_.split('/')
					d = video_Save_Path__[1:]
					c = video_Save_Path__[0][1:]
					slashExtended = '\\'.join(d)
					way = c + "\\" + str(slashExtended)

					videoStreams = yt.streams.filter(file_extension='mp4').get_by_itag(resolutionP)

					video_Paths.append([str(way), "\\", str(yt.title).lower(), '.mp4', str(link)])
					#video_Paths.append([str(way), "\\", str(yt.title) + "error_example",".mp4", str(link)])
					
					videoStreams.download(way)
					
				except Exception as e:
					for video_Path__ in video_Paths:
						fileControl = str(video_Path__[0]) + str(video_Path__[1]) + str(video_Path__[2]) + str(video_Path__[3])
						if os.path.exists(fileControl):
							true_or_False.append([False, video_Path__[0], video_Path__[1], video_Path__[2], video_Path__[3], video_Path__[4]])
						else:
							true_or_False.append([True, video_Path__[0], video_Path__[1], video_Path__[2], video_Path__[3], video_Path__[4]])
			
			for video_Path__ in video_Paths:
				fileControl = str(video_Path__[0]) + str(video_Path__[1]) + str(video_Path__[2]) + str(video_Path__[3])
				if os.path.exists(fileControl):
					true_or_False.append([False, video_Path__[0], video_Path__[1], video_Path__[2], video_Path__[3], video_Path__[4]])
				else:
					true_or_False.append([True, video_Path__[0], video_Path__[1], video_Path__[2], video_Path__[3], video_Path__[4]])
			
			return render_template('downloading_video_success.html', true_or_false_ = true_or_False)
	else:
		return 'For post requests only.'

@app.route('/download_song_result', methods=['GET','POST'])
def downloadSongResult():
	songs_Links = []
	song_Paths_control = []
	true_or_False = []

	if request.method == 'POST':
		song_Link = request.form['songLink']
		song_Save_Path = request.form['songSavePath']

		if song_Link == '' or song_Save_Path == '':
			return 'Do Not Leave The Fields Blank !!!'
		else:
			songs_Links = song_Link.split(',')
			for songs_Link in songs_Links:
				if(songs_Link.startswith('https://')) == False:
					return 'Please Enter Youtube Link.'
				else:
					continue

			#song_Save_Path_ = song_Save_Path.replace('\\','\\')
			for link in songs_Links:
				try:
					yt = YouTube(link)
					songStreams = yt.streams.filter(only_audio=True).first()

					try:
						outFile = songStreams.download(output_path=song_Save_Path)
						base, ext = os.path.splitext(outFile)
						newFile = base + '.mp3'
						os.rename(outFile, newFile)
						song_Paths_control.append([True, str(song_Save_Path), str(yt.title), str(link)])
					except Exception as e:
						song_Paths_control.append([False, str(song_Save_Path), str(yt.title), str(link)])
						os.remove(outFile)
				except Exception as e:
					return 'Error : Connection Error !!! or ' + str(e) 

			for song_Paths in song_Paths_control:
				fileControl = str(song_Paths[0]) + str(song_Paths[1]) + str(song_Paths[2]) + str(song_Paths[3])
				if os.path.exists(fileControl):
					true_or_False.append([song_Paths[0], song_Paths[1], song_Paths[2], song_Paths[3]])
				else:
					true_or_False.append([song_Paths[0], song_Paths[1], song_Paths[2], song_Paths[3]])

			return render_template('downloading_song_success.html', true_or_false_ = true_or_False)
	else:
		return 'For post requests only.'


if __name__ == '__main__':
	app.run(debug=True)
