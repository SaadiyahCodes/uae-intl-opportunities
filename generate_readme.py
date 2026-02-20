#!/usr/bin/env python3
import json
import os
from datetime import datetime

def main():
    #Load data from JSON file
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    #Generate README content
    readme_content = generate_readme_content(data)
    
    #Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("README.md generated successfully!")

def generate_readme_content(data):
    #Header section
    content = """# uae-intl-opportunities

A comprehensive list of opportunities for students/professionals in UAE as well as global/international programs. Includes fellowships, volunteer programs, certificates and more! Most of these opportunities are free and/or global <3

<sub>P.S Not all opportunities are publicly declared with application forms.</br>
If you're really interested or passionate about working with someone/or on some topic, all you need is an email! 
Create your own opportunities ✨</sub>

<sub>**Note:❗Always verify if there are any fees to enroll/participate**</sub>


---


### Browse Opportunities by Category

"""
    
    #Add navigation links for all categories
    content += "🤝 **[Volunteer](https://github.com/SaadiyahCodes/uae-intl-opportunities?tab=readme-ov-file#volunteer)**  \n"
    content += "💼 **[Jobs / Internships / Fellowships](https://github.com/SaadiyahCodes/uae-intl-opportunities?tab=readme-ov-file#jobs--internships--fellowships)**  \n"
    content += "🎓 **[Certificates](https://github.com/SaadiyahCodes/uae-intl-opportunities?tab=readme-ov-file#certificates)**  \n"
    content += "🔎 **[Research](https://github.com/SaadiyahCodes/uae-intl-opportunities?tab=readme-ov-file#research)**  \n"
    content += "🧩 **[Competitions](https://github.com/SaadiyahCodes/uae-intl-opportunities?tab=readme-ov-file#competitions)**  \n"
    content += "💎 **[Education Resources](https://github.com/SaadiyahCodes/uae-intl-opportunities?tab=readme-ov-file#education-resources)**  \n"
    content += "🌐 **[People/Communities/Job Boards](https://github.com/SaadiyahCodes/uae-intl-opportunities?tab=readme-ov-file#peoplecommunitiesjob-boards)**  \n\n"
    
    #Closing Soon section
    content += "## ❗Closing Soon  \n"
    content += generate_table(
        ['Name', 'Description', 'Deadline'],
        data['closingSoon'],
        ['name', 'description', 'deadline']
    )
    content += "\n---\n\n"
    
    #Generate content for each category
    for category, opportunities in data['categories'].items():
        if not opportunities:
            continue
            
        content += f"## {category}  \n\n"
        
        #Determine columns based on category
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
    
    #Education Resources section
    content += "## Education Resources  \n\n"
    for resource in data['educationResources']:
        content += f"- [{resource['name']}]({resource['url']}): {resource['description']}  \n"
    content += "\n---\n\n"
    
    #People/Communities/Job Boards section
    content += "## People/Communities/Job Boards  \n"
    for item in data['peopleCommunities']:
        description = item['description'] if item['description'] else ""
        content += f"- [{item['name']}]({item['url']}): {description}  \n"
    content += "\n---\n\n"
    
    #Notes section
    content += """### Notes

- "Rolling" = No fixed deadline, apply anytime  
- Always verify deadlines and eligibility requirements on official websites
- If a link no longer works, the opportunity may have been closed"""
    
    return content

def generate_table(headers, items, fields):
    """Generate a markdown table with given headers and items"""
    if not items:
        return ""
    
    #Table header
    table = "| " + " | ".join(headers) + " |  \n"
    table += "| " + " | ".join(["-------"] * len(headers)) + " |  \n"
    
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
