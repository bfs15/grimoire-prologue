#! python

import argparse
import subprocess
import os
import sys
import urllib.request
import shutil

import Grimoire

if __name__ == "__main__":
	## Instantiate the parser
	parser = argparse.ArgumentParser(
				description='Downloads a video link into mp3 or video if --video is passed (auto-updates)\n'
            'py ' + __file__ + ' <link>',
						formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('link',
							help='link to the video')
	parser.add_argument('pathOutDir', nargs='?',
							help='path to the output directory')
	parser.add_argument('-v', action='store_true',
							help='verbose')
	parser.add_argument('--video', action='store_true',
							help='download video, not only mp3')
	parser.add_argument('--help_dl', action='store_true',
							help='downloader help.')
	parser.add_argument('remainder_args', nargs=argparse.REMAINDER)

	## Parse arguments
	args = parser.parse_args()

	if not args.pathOutDir:
		args.pathOutDir = './output/'
		print(f'output in {args.pathOutDir}', flush=True)

	pathYoutubeDl = ''
	if shutil.which('youtube-dl'):
		# youtube-dl is installed
		pathYoutubeDl = 'youtube-dl'
	else:
		# youtube-dl is on same directory as script
		pathScriptDir = Grimoire.getDirLocation(__file__)
		pathYoutubeDl = os.path.join(pathScriptDir, 'youtube-dl')

		if not os.path.isfile(pathYoutubeDl):
			# if youtube-dl doesn't exist, download it on the script's dir
			print('youtube-dl not detected, downloading...', flush=True)
			# select os
			if os.name == 'nt':
				url = 'https://yt-dl.org/latest/youtube-dl.exe'
			elif os.name == 'posix':
				url = 'https://yt-dl.org/downloads/latest/youtube-dl'
			else:
				raise OSError('OS not supported. Install youtube-dl on your machine.')

			# Download the file from 'url' and save it locally under 'file_name':
			Grimoire.downloadFile(url, pathYoutubeDl)
		else:
			# update
			bashCommand = pathYoutubeDl + ' -U '
			print(bashCommand, flush=True)
			process = subprocess.call(bashCommand)

	Grimoire.ensure_dir(args.pathOutDir)

	bashCommand = pathYoutubeDl + ' '
	if not args.video:
		bashCommand = bashCommand + ' -x --audio-format "mp3" --audio-quality 320K --embed-thumbnail '
	if args.help_dl:
		bashCommand = bashCommand + ' --help '
	else:
		outputCom = f' --output "{args.pathOutDir}%(title)s - %(id)s.%(ext)s" '
		# https://github.com/ytdl-org/youtube-dl/issues/698
		defaultArgs = " -i "

		bashCommand += args.link + defaultArgs + outputCom
		bashCommand += ' ' + ' '.join(args.remainder_args)

	print(bashCommand, flush=True)
	try:
		process = subprocess.call(bashCommand)
	except Exception as err:
		print(err)
		exit(1)
	else:
		if process != 0:
			print("Try updating youtube-dl:")
			print("conda upgrade youtube-dl")
			print("pip install -U youtube-dl")
			print("if you don't know conda use the pip command")
		exit(process)
