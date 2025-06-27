from pydoc import doc
import streamlit as st
import re   #regular expressions regex 
import spacy  #for nlp tokenization etc 
import csv    #generate output in structured way 
import os 
import pandas as pd 
import spacy.cli
spacy.cli.download("en_core_web_sm")
import en_core_web_sm
nlp = en_core_web_sm.load()




DEGREES = [
    "b.tech", "bachelor of technology",
    "b.sc", "bachelor of science",
    "m.tech", "m.sc", "master", "master of science", "mba",
    "phd", "bca", "mca"
]



def extract_name(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()][:10]

    for line in lines:
        if '@' in line or any(char.isdigit() for char in line):
            continue
        if any(word.lower() in line.lower() for word in ['resume', 'curriculum', 'cv']):
            continue

        words = line.split()
        if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
            return line

    return None


def extract_info(text):
    info = {}

    #extract emails
    emails = re.findall(r'\b\S+@\S+\.\S+\b', text)
    info['email'] = emails[0] if emails else None

    # Extract phone number (basic version)
    phones = re.findall(r'\+?\d[\d\s\-]{8,}\d', text)
    info['phone'] = phones[0] if phones else None

    info['name'] = extract_name(text)
    info['skills'] = extract_skills(text)
    info['education'] = extract_education(text)
    # Extract experience (look for patterns like "3 years", "5+ years")
    experience_matches = re.findall(r'(\d{1,2}\+?)\s*(?:years?|yrs?)', text.lower())

    info['experience'] = experience_matches[0] + " years" if experience_matches else None
    info['cgpa'] = extract_gpa(text)

    # Extract job titles (very basic version using spaCy's NER)
    # doc = nlp(text)
    # job_titles = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    # info['file_name'] = job_titles[0] if job_titles else None

    return info


def parser(path):
    import pdfplumber , docx2txt 

    if path.endswith(".pdf"):
        all_text = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)
            return "\n".join(all_text)
                    
        #pdf.pages: list of all pages in the pdf file  , page is an obj representing one page
        #page.extract_text(): extracts all readable text and \n joins all the page content into one giant string as page1,page2 text 
    
    elif path.endswith(".docx"):
        return docx2txt.process(path)  #no object just full document string no loops needed
    
    else:
        raise ValueError("Unsupported file format")
    


SKILLS_DB = [
    # Programming Languages
    'python', 'java', 'c++', 'c', 'c#', 'go', 'rust', 'javascript', 'typescript',
    'ruby', 'kotlin', 'swift', 'php', 'matlab', 'r',

    # Web Development
    'html', 'css', 'bootstrap', 'tailwind', 'react', 'angular', 'vue',
    'node', 'express', 'next.js', 'django', 'flask', 'fastapi',

    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'firebase',

    # Data Science & Machine Learning
    'pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn',
    'tensorflow', 'keras', 'pytorch', 'xgboost', 'statsmodels',

    # DevOps & Cloud
    'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'linux',
    'ci/cd', 'jenkins', 'terraform', 'ansible',

    # Tools & Platforms
    'git', 'github', 'gitlab', 'jupyter', 'vscode', 'notion', 'jira',

    # Soft Skills / Others
    'communication', 'leadership', 'teamwork', 'problem solving',
    'adaptability', 'critical thinking', 'time management', 'creativity',

    # Design & Product
    'figma', 'canva', 'adobe xd', 'photoshop', 'illustrator',
    'wireframing', 'ux research', 'product management',

    # Extras
    'excel', 'powerpoint', 'word', 'chatgpt', 'api integration',
    'graphql', 'rest api', 'sqlalchemy'
]


def extract_skills(text):
    found = []
    text_lower = text.lower()
    for skill in SKILLS_DB:
        if skill in text_lower:
            found.append(skill)
    return list(set(found))

def extract_gpa(text):
    cgpa_match = re.findall(r'(?:CGPA|GPA|cgpa)[:\s]*([\d\.]{1,4})\s*(?:/10)?' , text , flags=re.IGNORECASE)
    if cgpa_match:
        return f"{cgpa_match[0]}(CGPA)"
    else:
        return None
    
def extract_education(text):
    edu = []
    text_lower = text.lower()
    for degree in DEGREES:
        if degree in text_lower:
            edu.append(degree)
    return list(set(edu))



st.set_page_config(page_title="RESUME PARSER" , layout='wide')
st.title("RESUME PARSER WEB APP")
st.write("upload multiple resumes(pdf/docx) and get structured info out of it")
uploaded_files = st.file_uploader("upload you resume", type=["pdf","docx"] , accept_multiple_files=True)
all_data = []
if uploaded_files:
    with st.spinner("reading and analyzing. . . ."):
        for file in uploaded_files:
            file_ext = file.name.split('.')[-1]
            temp_file_path = f"temp_resume.{file_ext}"
       

       
            with open(temp_file_path , "wb") as f:
                f.write(file.read())

            text = parser(temp_file_path)

            if not text.strip():
                st.error("Could not extract text from this file.")
                continue

            info = extract_info(text)
            info["cgpa"] = extract_gpa(text)
            info["file_name"] = file.name
            all_data.append(info)

    if all_data:
        st.success("All files parsed successfully!")
        st.subheader("Extracted Information Table")
        df = pd.DataFrame(all_data)
        st.dataframe(df)
            
os.remove(temp_file_path)


    

    
    




