from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['https://www.youtube.com/@PW-Foundation/videos']
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    video_links = soup.find_all("a", {"class": "yt-simple-endpoint style-scope ytd-grid-video-renderer"})
    video_urls = [f'https://www.youtube.com{link["href"]}' for link in video_links[:5]]
    video_titles = [link["title"] for link in video_links[:5]]
    video_thumbnails = [link.find("img")["src"] for link in video_links[:5]]
    video_views = [link.find("span", {"class": "style-scope ytd-grid-video-renderer"}) for link in video_links[:5]]
    data = {
        "URL": video_urls,
        "Title": video_titles,
        "Thumbnail": video_thumbnails,
        "Views": video_views
    }
    df = pd.DataFrame(data)
    df.to_csv('video_data.csv', index=False)
    return render_template('index.html', success=True)


@app.route('/videos')
def get_video_urls():
    channel_url = request.args.get('https://www.youtube.com/@PW-Foundation/videos')
    if not channel_url:
        return jsonify({'error': 'Please provide a channel URL'})
    
    response = requests.get(channel_url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    video_links = soup.find_all("a", {"class": "yt-simple-endpoint style-scope ytd-grid-video-renderer"})
    video_urls = [f'https://www.youtube.com{link["href"]}' for link in video_links[:5]]
    
    return jsonify({'video_urls': video_urls})


@app.route('/thumbnails')
def get_video_thumbnails():
    channel_url = request.args.get('https://www.youtube.com/@PW-Foundation/videos')
    if not channel_url:
        return jsonify({'error': 'Please provide a channel URL'})
    
    response = requests.get(channel_url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    thumbnail_links = soup.find_all("a", {"class": "yt-simple-endpoint inline-block style-scope ytd-thumbnail"})
    thumbnail_urls = [link.find('img')['src'] for link in thumbnail_links[:5]]
    
    return jsonify({'thumbnail_urls': thumbnail_urls})


@app.route('/titles')
def get_video_titles():
    channel_url = request.args.get('https://www.youtube.com/@PW-Foundation/videos')
    if not channel_url:
        return jsonify({'error': 'Please provide a channel URL'})
    
    response = requests.get(channel_url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    title_links = soup.find_all("a", {"class": "yt-simple-endpoint style-scope ytd-grid-video-renderer"})
    titles = [link.find('span', {"class": "style-scope ytd-grid-video-renderer"}).text for link in title_links[:5]]
    
    return jsonify({'titles': titles})    


@app.route('/views')
def get_video_views():
    channel_url = request.args.get('https://www.youtube.com/@PW-Foundation/videos')
    if not channel_url:
        return jsonify({'error': 'Please provide a channel URL'})
    
    response = requests.get(channel_url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    view_counts = soup.find_all("span", {"class": "style-scope ytd-grid-video-renderer"})
    views = [count.text for count in view_counts if 'views' in count.text][:5]
    
    return jsonify({'views': views})



@app.route('/times')
def get_video_times():
    channel_url = request.args.get('https://www.youtube.com/@PW-Foundation/videos')
    if not channel_url:
        return jsonify({'error': 'Please provide a channel URL'})
    
    response = requests.get(channel_url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    time_spans = soup.find_all("span", {"class": "style-scope ytd-grid-video-renderer"})
    times = [time.text for time in time_spans if 'ago' in time.text][:5]
    
    return jsonify({'times': times})




if __name__=="__main__":
    app.run(host="0.0.0.0")
