from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup
import csv


app = Flask(__name__)

@app.route("/", methods = ['GET'])  
def homepage():
    return render_template("index.html")

url = 'https://www.youtube.com/@PW-Foundation/videos'

@app.route("/thumbnails", methods = ['GET','POST'])
def f1():

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url, headers=headers)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all video thumbnails
    video_thumbnails = soup.find_all('img', {'class': 'style-scope yt-img-shadow'})

    # Extract the URLs of the thumbnails of the first five videos
    thumbnail_urls = []
    for thumbnail in video_thumbnails[:5]:
        thumbnail_urls.append(thumbnail['src'])

    # Save the thumbnail URLs to a CSV file
    with open('thumbnail_urls.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Thumbnail URL'])
        for url in thumbnail_urls:
            writer.writerow([url])


@app.route("/time", methods = ['GET','POST'])
def f():


    # Set user-agent header to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Send an HTTP GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # Create a BeautifulSoup object with the response HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the time of posting for the first five videos
    time_posted_list = []
    for video in soup.find_all('div', {'id': 'dismissible'}):
        time_posted = video.find('span', {'class': 'style-scope ytd-grid-video-renderer'}).text.strip()
        time_posted_list.append(time_posted)
        if len(time_posted_list) == 5:
            break

    # Save the results in a CSV file
    with open('time_posted.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time of Posting'])
        for time in time_posted_list:
            writer.writerow([time])
    


@app.route("/title", methods = ['GET','POST'])
def f3():
    # Set the URL and headers
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url, headers=headers)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all video titles
    video_titles = soup.find_all('a', {'class': 'yt-simple-endpoint style-scope ytd-grid-video-renderer'})

    # Extract the titles of the first five videos
    video_titles_list = []
    for title in video_titles[:5]:
        video_titles_list.append(title.text.strip())

    # Save the video titles to a CSV file
    with open('video_titles.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Video Title'])
        for title in video_titles_list:
            writer.writerow([title])


@app.route("/videourl", methods = ['GET','POST'])
def f4():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url, headers=headers)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all video links
    video_links = soup.find_all('a', {'class': 'yt-simple-endpoint style-scope ytd-grid-video-renderer'})

    # Extract the URLs of the first five videos
    video_urls = []
    for link in video_links[:5]:
        video_urls.append('https://www.youtube.com' + link['href'])

    # Save the video URLs to a CSV file
    with open('video_urls.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Video URL'])
        for url in video_urls:
            writer.writerow([url])


@app.route("/views", methods = ['GET','POST'])
def f5():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url, headers=headers)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all video views
    video_views = soup.find_all('span', {'class': 'style-scope ytd-grid-video-renderer'})

    # Extract the number of views of the first five videos
    video_views_list = []
    for view in video_views:
        if 'views' in view.text.strip():
            video_views_list.append(view.text.strip())

            if len(video_views_list) == 5:
                break

    # Save the video views to a CSV file
    with open('video_views.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Number of Views'])
        for view in video_views_list:
            writer.writerow([view])



if __name__=="__main__":
    app.run(host="0.0.0.0")
