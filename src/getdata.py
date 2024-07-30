import os
import json
from os.path import abspath


def generate_md_list(directory, output_file):
    try:
        md_files = [f for f in os.listdir(directory) if f.endswith('.md')]
        with open(output_file, 'w') as file:
            file.write('# List of verbs \n\n')
            for md_file in md_files:
                file.write(f'- [{md_file}]({directory}/{md_file})\n')

    except FileNotFoundError:
        print(f'The directory {directory} was not found.')

def read_template(template_path):
    with open(template_path) as template:
        return template.read()

def process_json_file(json_path, template_content):
    with open(json_path) as json_file:
        data = json.load(json_file)
    verb = os.path.basename(json_file.name.split(".")[0])

    tenses_dict = {
        'simple': data.get('simple', {}),
        'perfect': data.get('perfect', {}),
        'continuous': data.get('continuous', {}),
        'perfectcontinuous': data.get('perfectcontinuous', {})
    }

    raw_template = template_content.replace("@VERB", verb)

    for tense_type, tense_data in tenses_dict.items():
        for tense in ['past', 'present', 'future']:
            for form in ['affirmative', 'negative', 'interrogative']:
                marker = f"@{tense.upper()}{tense_type.upper()}{form.upper()}"
                replacement = tense_data.get(tense, {}).get(form, "")
                raw_template = raw_template.replace(marker, replacement)
    return verb, raw_template

def write_output_file(verb, content):
    output_path = abspath(f"../verbs-md/{verb}.md")
    with open(output_path, "w") as out_file:
        out_file.write(content)

