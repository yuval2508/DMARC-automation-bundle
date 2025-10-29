from flask import Flask, request, render_template_string, send_file
import os
import tempfile
from parse_dmarc import parse_dmarc_xml

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            temp_dir = tempfile.mkdtemp()
            xml_path = os.path.join(temp_dir, 'report.xml')
            file.save(xml_path)
            html_output = os.path.join(temp_dir, 'report.html')
            excel_output = os.path.join(temp_dir, 'report.xlsx')
            parse_dmarc_xml(xml_path, html_output, excel_output)
            with open(html_output, 'r') as f:
                html_content = f.read()
            return html_content
    return '''
    <!doctype html>
    <title>DMARC Report Parser</title>
    <h1>Upload DMARC XML report</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
