#!/usr/bin/env python3

import pandas as pd
import os
import textwrap

filename = "quotes.csv"

os.system("cls" if os.name == "nt" else "clear")

if not os.path.exists(filename):
    print(f"{filename} not found.")
    exit()

df = pd.read_csv(filename)

#sanity check
#print(df.head())
#print(df.info())

df["tag_list"] = df["tags"].apply(
    lambda tags: tags.split(", ") if isinstance(tags, str) else []
)

#sanity check
#print(df[["author","tag_list"]].head())
#print(type(df.loc[0, "tag_list"]))

all_tags = []

for tags in df["tag_list"]:
    for tag in tags:
        if "misattributed" not in tag and "attributed" not in tag:
            all_tags.append(tag)

unique_tags = sorted(set(all_tags))

# Set layout of tag listing
column_width = 35
columns = 5
line_width = column_width * columns

app_title = " Ryan's Quote Tag Selector "
app_description = "Sometimes you need a great quote in your life, but just can't find one that is appropriate for the situation. This application helps you find a quote from the great list of quotes at 'quotes.toscrape.com'. Enter a number to select a tag and receive all applicable quotes from the site."
wrapped_app_description = textwrap.fill(app_description, width=line_width)

print()
print(app_title.center(line_width, "="))
print()
print(wrapped_app_description)
print()
print("=" * line_width)
print()
for number, tag in enumerate(unique_tags, start=1):
    label = f"{number}. {tag}"
    print(f"{label:<{column_width}}", end="")
    if number % columns == 0:
        print()

print()
print()
print("=" * line_width)

choice = input("\nEnter a tag number: ").strip()

if not choice.isdigit():
    print("Please enter a number.")
    exit()

choice = int(choice)
selected_tag = unique_tags[choice - 1]

matching_quotes = df[df["tag_list"].apply(lambda tags: selected_tag in tags)]
for _, row in matching_quotes.iterrows():
    print(f'\n{row["quote"]} -{row["author"]}\n')