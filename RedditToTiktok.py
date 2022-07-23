
from turtle import back, down, width
from gtts import gTTS
from pytube import YouTube
from moviepy.editor import *
import configparser
import os
import praw

savePath = "C:/" #insert save path here 
link = "https://www.youtube.com" #insert youtube video link
subredditName = "AmItheAsshole" #insert subreddit name
language = "en" #insert language here en for englishb
slowRead = False #True or False to have it read slowly or fast
prawClientID = "whoopsie" #insert ClientID here
prawClientSecret = "daysies" #insert Client Secret here
prawUserAgent = "Python:read-only:xyz" #insert User Agent here
finalWidth = 1080 #inser final video width
finalHeight = 1920  #insert final video height

#initilizing pytube download through link
try:
    yt = YouTube(link)
except:
    print("Invalid Link")

mp4File = yt.streams.filter(file_extension="mp4")
mp4File720p = mp4File.get_by_resolution("720p")
mp4File720p.download(savePath, "video.mp4")

#starting video editing and resizing

background =VideoFileClip("video.mp4")
noAudio = background.without_audio()
resized = noAudio.resize((finalWidth, finalHeight))

#retrieving subreddit and hottest post

#initilizing praw read-only

reddit = praw.Reddit(
    client_id= prawClientID,
    client_secret= prawClientSecret,
    user_agent= prawUserAgent
)

subreddit = reddit.subreddit(subredditName)

for submission in subreddit.hot(limit=2):
    if not submission.stickied:
        submissionID = submission.id
        SubmissionText = submission.title + submission.selftext
        textToSpeechObj = gTTS(text=SubmissionText, lang=language, slow=slowRead)
        textToSpeechObj.save("submission.mp3")

#compiling everything together

finalVid = resized.set_audio(AudioFileClip("submission.mp3"))
finalVid.write_videofile("final.mp4", preset='ultrafast', audio=True, codec = "mpeg4")
os.remove("submission.mp3") 