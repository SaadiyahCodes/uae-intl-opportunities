#!/usr/bin/env python3
import json
from typing import TypedDict, Optional, Dict, List

class Opportunity(TypedDict, total=False):
    name:        str
    url:         str
    field:       str
    location:    str
    ageCategory: str
    deadline:    str


class Certificate(TypedDict):
    name:  str
    url:   str
    field: str


class EducationResource(TypedDict):
    name:        str
    url:         str
    description: str


class PeopleCommunity(TypedDict):
    name:        str
    url:         str
    description: str


class OpportunitiesSchema(TypedDict):
    closingSoon:        List[Opportunity]
    categories:         Dict[str, List[Opportunity]]
    certificates:       List[Certificate]
    educationResources: List[EducationResource]
    peopleCommunities:  List[PeopleCommunity]


def main():
    with open('data.json', 'r', encoding='utf-8') as f:
        data: OpportunitiesSchema = json.load(f)

    with open('README_template.md', 'r', encoding='utf-8') as f:
        template = f.read()

    tables_content = generate_tables_section(data)

    final_readme = insert_generated_content(template, tables_content)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(final_readme)

    print("README.md generated successfully!")

def insert_generated_content(template, tables_content):
    start_marker = "<!-- AUTO-GENERATED-TABLES-START -->"
    end_marker = "<!-- AUTO-GENERATED-TABLES-END -->"

    start_index = template.index(start_marker) + len(start_marker)
    end_index = template.index(end_marker)

    return (
        template[:start_index]
        + "\n\n"
        + tables_content.strip()
        + "\n\n"
        + template[end_index:]
    )

def generate_tables_section(data):
    content = ""

    # Closing Soon
    closing_soon = data.get('closingSoon', [])
    if closing_soon:
        content += "## ❗ Closing Soon\n\n"
        content += generate_table(
            ['Name', 'Description', 'Deadline'],
            closing_soon,
            ['name', 'description', 'deadline']
        )
        content += "\n---\n\n"

    # Categories
    for category, opportunities in data.get('categories', {}).items():
        if not opportunities:
            continue

        content += f"## {category}\n\n"

        if category == "Certificates":
            content += generate_table(
                ['Name', 'Field'],
                opportunities,
                ['name', 'field']
            )
        else:
            content += generate_table(
                ['Name', 'Field', 'Location', 'Age Category', 'Deadline'],
                opportunities,
                ['name', 'field', 'location', 'ageCategory', 'deadline']
            )

        content += "\n---\n\n"

    # Education Resources
    resources = data.get('educationResources', [])
    if resources:
        content += "## Education Resources\n\n"
        for resource in resources:
            content += f"- [{resource['name']}]({resource['url']}): {resource['description']}  \n"
        content += "\n---\n\n"

    # People/Communities
    people = data.get('peopleCommunities', [])
    if people:
        content += "## People/Communities/Job Boards\n\n"
        for item in people:
            description = item.get('description', '')
            content += f"- [{item['name']}]({item['url']}): {description}  \n"
        content += "\n---\n\n"

    return content

def generate_table(headers: list[str], items: list[Opportunity], fields: list[str]) -> str:
    """Generate a markdown table with given headers and items"""
    if not items:
        return ""

    #Table header
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["-------"] * len(headers)) + " |\n"

    #Table rows
    for item in items:
        row = []
        for field_index, field in enumerate(fields):
            value = str(item.get(field, "")).replace("|", "\\|")

            #Create hyperlink for name field
            if field_index == 0:
                url = item.get('url', '')
                if url and url != 'NA':
                    value = f"[{value}]({url})"

            row.append(value)
        table += "| " + " | ".join(row) + " |  \n"

    return table

if __name__ == "__main__":
    main()
