from os import listdir
from os.path import isfile, join, abspath
from getdata import generate_md_list, read_template, process_json_file, write_output_file

if __name__ == "__main__":
    TEMPLATE_README = "../template.md"
    DATA_DIR = abspath("../verbs")
    raw_template_content = read_template(TEMPLATE_README)
    generate_md_list(abspath("../verbs-md"), '../README.md')
    for f in listdir(DATA_DIR):
        if isfile(join(DATA_DIR, f)) and f.endswith(".json"):
            json_path = join(DATA_DIR, f)
            verb, raw_template = process_json_file(json_path, raw_template_content)
            write_output_file(verb, raw_template)
