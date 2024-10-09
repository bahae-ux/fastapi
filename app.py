from flask import Flask, render_template, request, send_file
import pandas as pd
import comtradeapicall
import io

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
        output = io.BytesIO()
        mydf.to_excel(output, index=False)
        output.seek(0)

        # Envoyer le fichier Excel en réponse
        return  mydf.to_html(classes='table table-bordered table-striped', index=False)# return send_file(output, attachment_filename='data.xlsx', as_attachment=True)

    return render_template('index.html')
 except Exception as me:
     return str(me)
if __name__ == '__main__':
    app.run(debug=True)
