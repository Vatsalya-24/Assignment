from flask import Flask, jsonify
import requests

app = Flask(__name__)

def get_latest_stories():
  """
  Extracts the titles and links of the latest 6 stories from Time.com using basic HTML parsing.

  Returns:
      list: A list of dictionaries containing title and link for each story.
  """
  url = "https://time.com/"
  response = requests.get(url)
  content = response.text

  # Define starting and ending tags for the story elements
  start_tag = '<h3 class="title-text">'
  end_tag = '</h3>'

  # Initialize variables
  stories = []
  current_story = {}
  in_story = False

  # Loop through the content
  for line in content.splitlines():
    if start_tag in line:
      # Start of a new story
      in_story = True
      current_story = {"title": "", "link": ""}
    elif end_tag in line:
      # End of a story
      in_story = False
      stories.append(current_story)
      if len(stories) == 6:
        break  # Reached the target number of stories
    elif in_story:
      # Extract title and link within the story element
      if 'href="' in line:
        # Extract link
        link_start = line.find('href="') + 6
        link_end = line.find('"', link_start)
        current_story["link"] = line[link_start:link_end]
      else:
        # Extract title (assuming title is the remaining text)
        current_story["title"] += line.strip()

  return stories

@app.route("/getTimeStories")
def get_time_stories():
  """
  API endpoint to retrieve the latest stories.
  """
  stories = get_latest_stories()
  return jsonify(stories)

if __name__ == "__main__":
  app.run(debug=True)
