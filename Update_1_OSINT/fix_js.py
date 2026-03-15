import os, glob

os.chdir('dashboard/templates')
files = [f for f in glob.glob('*-new.html') if f != 'base-new.html']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '{% block page_script %}' in content:
        start = content.find('{% block page_script %}') + len('{% block page_script %}')
        end = content.find('{% endblock %}', start)
        inner = content[start:end]
        
        if '<script>' not in inner:
            new_content = content[:start] + '\n<script>\n' + inner.strip() + '\n</script>\n' + content[end:]
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print('Fixed ' + f)
