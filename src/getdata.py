import os
import json
from os import listdir
from os.path import isfile, join, abspath

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
    output_path = abspath(f"../{verb}.md")
    with open(output_path, "w") as out_file:
        out_file.write(content)

if __name__ == "__main__":
    TEMPLATE_README = "../template.md"
    DATA_DIR = abspath("../verbs")
    raw_template_content = read_template(TEMPLATE_README)

    for f in listdir(DATA_DIR):
        if isfile(join(DATA_DIR, f)) and f.endswith(".json"):
            json_path = join(DATA_DIR, f)
            verb, raw_template = process_json_file(json_path, raw_template_content)
            write_output_file(verb, raw_template)

