from flask import Flask, render_template, request, send_file, render_template_string
import pandas as pd
import comtradeapicall
import io
import random
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
 try:    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        type_code = request.form['type_code']
        freq_code = request.form['freq_code']
        cl_code = request.form['cl_code']
        period = request.form['period']
        reporter_code = request.form['reporter_code']
        cmd_code = request.form['cmd_code']
        flow_code = request.form['flow_code']

        # Appeler l'API
        mydf = comtradeapicall.previewTarifflineData(typeCode='C', freqCode='M', clCode='HS', period='202205',
                                             reporterCode='36', cmdCode='91,90', flowCode='M', partnerCode=36,
                                             partner2Code=None,
                                             customsCode=None, motCode=None, maxRecords=500, format_output='JSON',
                                             countOnly=None, includeDesc=True)

        # Convertir le DataFrame en fichier Excel
        excel_file_path = f'static/output{random.randint(500, 1000)}.xlsx'
        mydf.to_excel(excel_file_path, index=False)
        download_link = f'/download/{os.path.basename(excel_file_path)}'

          # Render HTML with table and download button
        html = f'''
    <h1>Data Table</h1>
    {mydf.to_html(classes='table table-bordered table-striped', index=False)}
    <br>
    <a href="{download_link}" class="btn btn-primary">Download Excel</a>
    '''

        return render_template_string(html)
 except Exception as me:
     return str(me)
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join('static', filename)
    return send_file(file_path, as_attachment=True)  
if __name__ == '__main__':
    app.run(debug=True)
