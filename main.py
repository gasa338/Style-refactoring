from bs4 import BeautifulSoup
import pandas as pd
import dicttoxml
import re

# Putanja do fajla
file_path = r"C:\laragon\www\maxwell\wp-content\themes\maxxwell\blocks\about\about-agency-1\about-agency-1.php"

import glob
import os

# Definiši putanju sa zvezdicama za rekurzivnu pretragu
search_path = r"C:\laragon\www\maxwell\wp-content\themes\maxxwell\blocks\*\*\*.php"

# Pronađi sve .php fajlove u strukturi foldera
php_files = glob.glob(search_path)

# Sortiraj fajlove prema imenu
php_files_sorted = sorted(php_files, key=lambda x: os.path.basename(x))



# Tailwind config classes (primer)
tailwind_classes_full = [
    'accent-',
    'animate-',
    'aria-',
    'aspect-',
    'backdrop-blur-',
    'backdrop-brightness-',
    'backdrop-contrast-',
    'backdrop-grayscale-',
    'backdrop-hue-rotate-',
    'backdrop-invert-',
    'backdrop-opacity-',
    'backdrop-saturate-',
    'backdrop-sepia-',
    'bg-',
    'bg-opacity-',
    'bg-center',
    'bg-cover',
    'bg-contain',
    'blur-',
    'border-',
    'border-opacity-',
    'rounded-',
    'border-spacing-',
    'border-',
    'shadow-',
    'brightness-',
    'caret-',
    'text-',
    'columns-',
    'container',
    'content-',
    'contrast-',
    'cursor-',
    'divide-',
    'divide-opacity-',
    'divide-',
    'drop-shadow-',
    'fill-',
    'flex-',
    'basis-',
    'grow-',
    'shrink-',
    'font-',
    'text-',
    'font-',
    'gap-',
    'from-',
    'via-',
    'to-',
    'grayscale-',
    'auto-cols-',
    'auto-rows-',
    'col-',
    'col-end-',
    'col-start-',
    'row-',
    'row-end-',
    'row-start-',
    'grid-cols-'
]
tailwind_classes_tipografija = [
    'bg-',
    'border-',
    'border-opacity-',
    'rounded-',
    'text-',
    'font-',
]

# Ispis sortiranih fajlova
print("Sortirani PHP fajlovi:")
file_names = []
classes_in_html_list = []
for file_path in php_files_sorted:
    # print(file_path)
    file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
    # print(file_name_without_ext)

    # Učitaj HTML sadržaj iz fajla
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parsiraj HTML sadržaj
    soup = BeautifulSoup(html_content, 'html.parser')

    # Izvuci sve klase koje se koriste u HTML-u
    classes_in_html = set()
    for tag in soup.find_all(True, {"class": True}):
        classes_in_html.update(tag.get("class"))

    # Poravnaj listu klasa
    classes_in_html = [item for sublist in classes_in_html for item in sublist.split()]

    file_names.append(file_name_without_ext)

    # Ukoliko trazimo specijalnu klasu
    matched_classes = []
    for cls in tailwind_classes_tipografija:
        pattern = re.compile(re.escape(cls))  # Kreiraj regex šablon za delimično poklapanje
        for html_class in classes_in_html:
            if pattern.search(html_class):
                matched_classes.append(html_class)


    classes_in_html_list.append(matched_classes)
    # Ispis pronađenih klasa
    # for cls in matched_classes:
    #     print(cls)



# Podaci
data = {
    'Blocks': file_names,
    'Classes': classes_in_html_list
}
# Kreiranje DataFrame
df = pd.DataFrame(data)

#############################################################################################
###################                   JSON                          #########################
#############################################################################################
json_result = df.to_json(orient='records', indent=4)

# Sačuvaj JSON objekat u fajl
with open('output.json', 'w') as json_file:
    json_file.write(json_result)


#############################################################################################
###################                   Excel                          #########################
#############################################################################################
# Export u Excel
excel_file = 'podaci.xlsx'
df.to_excel(excel_file, index=False)



#############################################################################################
###################                   XML                          #########################
#############################################################################################
# Konverzija JSON objekta u XML format
xml_result = dicttoxml.dicttoxml(json_result, custom_root='data', attr_type=False)

# Sačuvaj XML objekat u fajl
with open('output.xml', 'wb') as xml_file:
    xml_file.write(xml_result)