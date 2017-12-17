"""
Basic rundown:
    Grab top image of the week from /r/abandonedporn
    Grab top story from /r/twosentencehorror
    Determine dimensions of the image
    Determine layout of text
    Overlay text on image
    Output new image

    PRAW::
    secret: 
    client ID: 

    Imgur::
    secret: 
    client ID: 
"""

import praw
import os
import datetime

# API credentials
praw_id =  # Enter Praw client ID
praw_secret =  # Enter Praw secret
imgur_id =  # Enter imgur client ID
imgur_secret =  # Enter imgur secret

current_date = datetime.datetime.now()
file_location = os.path.expanduser(#PATH WHERE IMAGES ARE TO BE SAVED)
tmp_file = file_location + "tmp.jpg"
saved_file = file_location + "autoDemote_%s-%s-%s.jpg".format(current_date.year,
							      current_date.month, 
							      current_date.day)

story_source = 'twosentencehorror'
image_source = 'abandonedporn'

font_path = "C:\\Windows\\Fonts\\ARJULIAN.ttf"  # Text path - may want to update this
current_date = datetime.datetime.now()

r = praw.Reddit(client_id=praw_id,
                client_secret=  # praw_secret,
                password=  # Reddit password,
                user_agent='autoDemote by /u/koberg',  # You don't have to keep this
                username=  # Reddit ID)


def get_image():
    import urllib

    # Obtain top rated post from the week and assign the url to image_url
    # Return default 25 and give us first one that doesn't come with www.flickr.com
	# Could add in flicker functionality later
    for submission in r.subreddit(image_source).top('week'):
        if 'www.flickr.com' not in str(submission.url):
            urllib.urlretrieve(submission.url, tmp_file)

            return tmp_file


def get_story():
    # Obtain top rated post from the week, title and selftext
    raw_story = []
    format_story = []
    for submission in r.subreddit(story_source).top('week', limit=1):
        for word in submission.title.split():
            raw_story.append(word)
        for word in str(submission.selftext).split():
            raw_story.append(word)

        # Break story into blocks of 4 words per line
        for word in xrange(0, len(raw_story), 4):
            format_story.append(raw_story[word:word + 4])

        return format_story


def auto_demote(image, text):
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw

    # Combine the image from get_image() with the text from get_story()
    img = Image.open(image)
    img_width, img_height = img.size
    font_size = int(img_height/len(text)/2)
    y_coord = 50
    font = ImageFont.truetype(font_path, int(font_size), encoding='unic')
    draw = ImageDraw.Draw(img)
    for line in text:
        # create border behind text
        draw.text((50-1, y_coord-1), ' '.join(line), font=font, fill='white')
        draw.text((50+1, y_coord-1), ' '.join(line), font=font, fill='white')
        draw.text((50+1, y_coord+1), ' '.join(line), font=font, fill='white')
        draw.text((50-1, y_coord+1), ' '.join(line), font=font, fill='white')
        # draw text
        draw.text((50, y_coord), ' '.join(line), font=font, fill='black')
        y_coord = y_coord + font_size + 10
    img.save(saved_file)


if __name__ == '__main__':
    
    my_image = get_image()
    my_story = get_story()

    auto_demote(my_image, my_story)

    os.remove(tmp_file)
