import os
import glob
print('Starting Python Script')
# Change to the templates directory
target_dir = r"C:\Users\User\OneDrive\Desktop\Final OSINT\Update_1_OSINT\dashboard\templates"
os.chdir(target_dir)

files = glob.glob('*.html')

for fl in files: # Use 'fl' to avoid reserved word conflicts in shell blocks just in cases!
    if "base" in fl:
        continue
    with open(fl, "r", encoding="utf-8") as file:
        content = file.read()
    
    start_tag = "{% block page_script %}\n"
    if start_tag in content:
        start_idx = content.find(start_tag) + len(start_tag)
        end_idx = content.find("{% endblock %}", start_idx)
        
        inner = content[start_idx:end_idx]
        
        if "<script>" not in inner:
            new_content = content[:start_idx] + "<script>\n" + inner.strip() + "\n</script>\n" + content[end_idx:]
            with open(fl, "w", encoding="utf-8") as file:
                file.write(new_content)
            print("Fixed " + fl)
    else:
        # Check without newline
        start_tag = "{% block page_script %}"
        start_idx = content.find(start_tag) + len(start_tag)
        if start_idx >= len(start_tag):
             end_idx = content.find("{% endblock %}", start_idx)
             if end_idx != -1:
                 inner = content[start_idx:end_idx]
                 if "<script>" not in inner:
                     new_content = content[:start_idx] + "\n<script>\n" + inner.strip() + "\n</script>\n" + content[end_idx:]
                     with open(fl, "w", encoding="utf-8") as file:
                         file.write(new_content)
                     print("Fixed " + fl)

print('End of Python Script')
