import json
import datetime
import os
from slugify import slugify

def create_markdown_from_conversations(file_path):
    with open(file_path, 'r') as f:
        conversations = json.load(f)

    # create a new directory if it does not exist
    if not os.path.exists("conversations"):
        os.makedirs("conversations")

    for conversation in conversations:
        # slugify the title to use as filename
        md_file_name = slugify(conversation['title']) + '.md'
        md_file_path = os.path.join("conversations", md_file_name)

        with open(md_file_path, 'w') as f:
            # Write title and creation time to markdown file
            f.write(f"# {conversation['title']}  \n")
            f.write("\n")

            # Loop through each message
            for key, value in conversation['mapping'].items():
                if value['message']:
                    # Write role, timestamp, and message to markdown file
                    role = value['message']['author']['role']
                    # create_time = datetime.datetime.fromtimestamp(value['message']['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                    # Check if 'parts' key exists in 'content' before accessing it
                    content = " ".join(value['message']['content']['parts']) if 'parts' in value['message']['content'] else ''
                    f.write(f"**{role.capitalize()}** : {content}  \n")
            f.write("\n\n")

        print(f"Markdown file created: {md_file_path}")

# Usage
create_markdown_from_conversations('conversations.json')
