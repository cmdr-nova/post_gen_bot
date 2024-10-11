import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
from mastodon import Mastodon
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

# Ensure you have the necessary NLTK data files, you'll need these to make the statuses a little more logical and structured.
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('stopwords')

# Function to remove HTML tags, just in case your Sheets have a bunch of HTML from imported toots hanging around everywhere.
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Function to filter out specific phrases, because maybe there's some stuff you don't want your bot to post, or maybe you need to filter out strange phrases.
def filter_phrases(text, phrases):
    for phrase in phrases:
        text = text.replace(phrase, '')
    return text

# Set us up the Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds/name_of_your_credentials_file.json', scope)
client = gspread.authorize(creds)

# Input your Google Sheets id codes found in the URL to them, and make sure to share them with the API e-mail provided in the credentials.
spreadsheet_ids = ['google_sheet_id_1', 'google_sheet_id_2', 'google_sheet_id_3']  # You can have as many as you want
data = []

for spreadsheet_id in spreadsheet_ids:
    sheet = client.open_by_key(spreadsheet_id).sheet1
    # Extract only column C (index 2, since it's zero-based). I've done this specifically for mine, because all of my old Mastodon posts are in column C.
    column_c = sheet.col_values(3)  # col_values uses 1-based indexing
    # Remove HTML tags and filter out specific phrases from each entry. Feel free to add whatever you want!
    column_c = [filter_phrases(remove_html_tags(entry), ["quot"]) for entry in column_c]
    data.extend(column_c)

# Here's the part where random statuses are generated.
def generate_random_status(data):
    # Split each entry into words or phrases and tag parts of speech.
    words = []
    for entry in data:
        words.extend(word_tokenize(entry))

    # Filter out stopwords and punctuation.
    words = [word for word in words if word.isalnum() and word.lower() not in stopwords.words('english')]

    # Tag parts of speech.
    tagged_words = pos_tag(words)

    # Separate words into verbs, adjectives, nouns, and others.
    verbs = [word for word, pos in tagged_words if pos.startswith('VB')]
    adjectives = [word for word, pos in tagged_words if pos.startswith('JJ')]
    nouns = [word for word, pos in tagged_words if pos.startswith('NN')]
    others = [word for word, pos in tagged_words if not pos.startswith('VB') and not pos.startswith('JJ') and not pos.startswith('NN')]

    # Define sentence templates (this can be modified).
    templates = [
        "The {adj} {noun} {verb} {adv}.",
        "{noun} {verb} {adj} {noun}.",
        "A {adj} {noun} {verb} {adv}.",
        "{noun} {verb} the {adj} {noun}."
    ]

    # Randomly select a template and fill in the blanks.
    template = random.choice(templates)
    status = template.format(
        adj=random.choice(adjectives) if adjectives else '',
        noun=random.choice(nouns) if nouns else '',
        verb=random.choice(verbs) if verbs else '',
        adv=random.choice(others) if others else ''
    )

    return status

# Here's where we post to Mastodon!
mastodon = Mastodon(
    access_token='mastodon_app_access_key',
    api_base_url='https://yourmastodoninstance.url'
)

status = generate_random_status(data)
if status.strip():  # Ensure the status is not blank
    mastodon.toot(status)
else:
    print("Generated status is blank, skipping toot.")
