from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup , SoupStrainer

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/vehicle_details',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            home_url = 'https://parivahan.gov.in/rcdlstatus'
            post_url = 'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml'
            first = request.form['first'].replace(" ","")
            second = request.form['second'].replace(" ","")

            r = requests.get(url=home_url)
            cookies = r.cookies
            soup = BeautifulSoup(r.text, 'html.parser')
            viewstate = soup.select('input[name="javax.faces.ViewState"]')[0]['value']

            data = {
                    'javax.faces.partial.ajax':'true',
                    'javax.faces.source': 'form_rcdl:j_idt43',
                    'javax.faces.partial.execute':'@all',
                    'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
                    'form_rcdl:j_idt43':'form_rcdl:j_idt43',
                    'form_rcdl':'form_rcdl',
                    'form_rcdl:tf_reg_no1': first,
                    'form_rcdl:tf_reg_no2': second,
                    'javax.faces.ViewState': viewstate,
            }

            r = requests.post(url=post_url, data=data, cookies=cookies)
            soup = BeautifulSoup(r.text, 'html.parser')
            table = SoupStrainer('tr')
            soup = BeautifulSoup(soup.get_text(),'html.parser',parse_only=table)
            print(soup.get_text())
            reviews = []
            Reg_No = soup.get_text().split("\n")[2]
            reg_date = soup.get_text().split("\n")[4]
            chassis_no = soup.get_text().split("\n")[7]
            engin_no = soup.get_text().split("\n")[9]
            owner_name = soup.get_text().split("\n")[12]
            fuel_type = soup.get_text().split("\n")[17]
            fitness_upto = soup.get_text().split("\n")[23]
            insurance_upto = soup.get_text().split("\n")[25]
            fuel_norms = soup.get_text().split("\n")[28]
            roadtaxpaid_upto = soup.get_text().split("\n")[30]
            vehicle_class = soup.get_text().split("\n")[15]
            marker_model = soup.get_text().split("\n")[20]


            mydict={"Registration No": Reg_No, "Reg date": reg_date, "chassis No": chassis_no, "Engin No": engin_no, "Owner Name": owner_name, "Fuel Type": fuel_type, "Fitness Upto": fitness_upto,
                    "Insurance Upto": insurance_upto, "Fuel Norms": fuel_norms, "Road tax paid upto": roadtaxpaid_upto, "Vehicle Class": vehicle_class, "Maker/Model": marker_model}
            reviews.append(mydict)
            return render_template('results.html',reviews=reviews[0:(len(reviews))])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'Details Not Found'
            # return render_template('results.html')

    else:
        return render_template('index.html')
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)