#!/usr/bin/env python3
import json
from typing import TypedDict
from datetime import datetime

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
    closingSoon:        list[Opportunity]
    categories:         dict[str, list[Opportunity]]
    certificates:       list[Certificate]
    educationResources: list[EducationResource]
    peopleCommunities:  list[PeopleCommunity]


class ClosedOpportunity(TypedDict, total=False):
    name:        str
    url:         str
    field:       str
    location:    str
    ageCategory: str
    deadline:    str
    closedDate:  str
    category:    str


def main():
    # Load active opportunities
    with open('data.json', 'r', encoding='utf-8') as f:
        data: OpportunitiesSchema = json.load(f)

    # Load closed opportunities (create if doesn't exist)
    try:
        with open('closed_opportunities.json', 'r', encoding='utf-8') as f:
            closed_data = json.load(f)
    except FileNotFoundError:
        closed_data = []
        with open('closed_opportunities.json', 'w', encoding='utf-8') as f:
            json.dump(closed_data, f, indent=2)

    # Generate main README
    with open('README_template.md', 'r', encoding='utf-8') as f:
        template = f.read()

    tables_content = generate_tables_section(data)
    final_readme = insert_generated_content(template, tables_content)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(final_readme)

    # Generate CLOSED.md
    generate_closed_opportunities_page(closed_data)

    print("README.md and CLOSED.md generated successfully!")


def insert_generated_content(template, tables_content):
    """Insert content while preserving front matter"""
    start_marker = "<!-- AUTO-GENERATED-TABLES-START -->"
    end_marker = "<!-- AUTO-GENERATED-TABLES-END -->"

    if start_marker not in template or end_marker not in template:
        # Fallback - append content
        return template + "\n\n" + tables_content
    
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
            ['Name', 'Field', 'Deadline'],
            closing_soon,
            ['name', 'field', 'deadline']
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

    # Table header
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["-------"] * len(headers)) + " |\n"

    # Table rows
    for item in items:
        row = []
        for field_index, field in enumerate(fields):
            value = str(item.get(field, "")).replace("|", "\\|")

            # Create hyperlink for name field
            if field_index == 0:
                url = item.get('url', '')
                if url and url != 'NA':
                    value = f"[{value}]({url})"

            row.append(value)
        table += "| " + " | ".join(row) + " |  \n"

    return table


def generate_closed_opportunities_page(closed_opportunities):
    """Generate CLOSED.md using template"""
    
    # Try to load template with front matter
    try:
        with open('CLOSED_template.md', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        # Fallback template if file doesn't exist
        template = """---
layout: default
title: Closed Opportunities Archive
---
# 🗄️ Closed Opportunities Archive

This page contains opportunities that have closed or expired. We keep them here for reference and to help you discover similar opportunities that may reopen in the future.

> [!TIP]
> Many of these opportunities run annually! Bookmark this page and check back next year.

**[← Back to Active Opportunities](README.md)**

---

<!-- AUTO-GENERATED-CONTENT-START -->
<!-- AUTO-GENERATED-CONTENT-END -->

### Notes

- These opportunities have passed their deadline or are no longer accepting applications
- Check if similar opportunities will be offered in the future
- Many programs run annually - set a reminder to apply next year!

**[← Back to Active Opportunities](README.md)**
"""
    
    content = ""
    
    if not closed_opportunities:
        content = "_No closed opportunities yet._\n"
    else:
        # Group by category
        by_category = {}
        for opp in closed_opportunities:
            category = opp.get('category', 'Other')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(opp)
        
        # Sort by closed date (most recent first)
        for category in by_category:
            by_category[category].sort(
                key=lambda x: x.get('closedDate', ''), 
                reverse=True
            )
        
        # Generate tables by category
        for category in sorted(by_category.keys()):
            opportunities = by_category[category]
            content += f"## {category}\n\n"
            
            headers = ['Name', 'Field', 'Location', 'Deadline', 'Closed']
            fields = ['name', 'field', 'location', 'deadline', 'closedDate']
            
            content += generate_table(headers, opportunities, fields)
            content += "\n---\n\n"
    
    final_closed = insert_generated_content(template, content)
    
    with open('CLOSED.md', 'w', encoding='utf-8') as f:
        f.write(final_closed)


if __name__ == "__main__":
    main()
