import os
import json
from bs4 import BeautifulSoup

input_file = os.path.join("data-json", "trip-time-use.json")
output_file = os.path.join("data-json", "trip-time-use-ok-removed.json")

with open(input_file, "r") as f:
    data = json.load(f)

form = data["form"]

# Parse the Form HTML
soup = BeautifulSoup(form, "html.parser")

# Find all fieldsets with the specific class
fieldsets = soup.find_all("fieldset", class_="question simple-select trigger")

# Loop through each fieldset and modify it
for fieldset in fieldsets:
    legend = fieldset.find("legend")
    if legend:
        question_label = legend.find("span", class_="question-label active")
        input_tag = fieldset.find("input", {"type": "radio"})
        option_wrapper = fieldset.find("div", class_="option-wrapper")

        if question_label and input_tag and option_wrapper:
            # Modify the structure
            option_wrapper.clear()
            new_label = soup.new_tag("label")
            new_input = input_tag.extract()
            new_span = question_label.extract()

            new_label.append(new_input)
            new_label.append(new_span)

            option_wrapper.append(new_label)
            legend.clear()
            legend.append(option_wrapper)

# Update the form in the data structure
data["form"] = str(soup)

# Write the modified data back to the file
with open(output_file, "w") as f:
    json.dump(data, f, indent=4)


with open(output_file, "r") as f:
    data = json.load(f)
    print(data["form"])
