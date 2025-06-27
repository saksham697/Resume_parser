# def export_to_csv(info, filename="parsed_resumes.csv"):
#     file_exists = os.path.isfile(filename)

#     with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=["name", "email", "phone", "skills", "education" ,"experience","file_name"])

#         if not file_exists:
#             writer.writeheader()  # Write header only once

#         # Convert list fields to comma-separated strings
#         row = {
#             "name": info.get("name"),
#             "email": info.get("email"),
#             "phone": info.get("phone"),
#             "skills": ", ".join(info.get("skills", [])),
#             "education": ", ".join(info.get("education", [])),
#             "experience": info.get("experience"),
#             "file_name": info.get("file_name")
#         }

#         writer.writerow(row)
#         print(f"Data exported to {filename}")



# if __name__ == "__main__":
#     folder_path = "resumes" 
#     files = [f for f in os.listdir(folder_path) if f.endswith(('pdf', 'docx'))]

#     if not files:
#         print("no resume files foun in the folder")

#     else:
#         for filename in files:
#             full_path = os.path.join(folder_path, filename)
#             print(f"Parsing: {filename}")
#             try:
#                 text = parser(full_path)
#                 info = extract_info(text)
#                 info["file_name"] = filename 
#                 export_to_csv(info, "parsed_resumes.csv")
#             except Exception as e:
#                 print(f" Failed to parse {filename}: {e}")
