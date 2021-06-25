import requests
from flask import Flask,render_template,request
from twilio.rest import Client
import requests

account_sid='ACa3be81cadae79a9b096c24b55a34327d'
auth_token='13128a008fcb5a632d1225eb643cefa0'

client=Client(account_sid,auth_token)
app=Flask(__name__,static_url_path='/static')

@app.route('/')
def registration_form():
    return render_template('user_login.html')

@app.route('/login',methods=['POST','GET'])
def login_registration_dtls():
    first_name=request.form['fname']
    last_name=request.form['lname']
    email_id=request.form['mail']
    source_st=request.form['state']
    source_dt=request.form['source']
    destination_st=request.form['dstate']
    destination_dt=request.form['destination']
    phoneNumber=request.form['phoneNumber']
    id_proof=request.form['aadhar']
    date=request.form['date']
    full_name=first_name+"."+last_name
    r=requests.get('https://api.covid19india.org/v4/data.json')
    json_data=r.json()
    cnt=json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop=json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass=((cnt/pop)*100)
    if travel_pass<30 and request.method=='POST':
        status='CONFIRMED'
        client.messages.create(to="whatsapp:+917901527150",
                               from_="whatsapp:+14155238886",
                               body="Hello"+" "+full_name+" "+"Your travel from"+" "+source_dt+" "+"to"+" "+destination_dt+" "+"Has"+" "+status+"on"+" "+date+" "+",Apply later")
        return render_template('user_registration_dtls.html',var=full_name,var1=email_id,var2=id_proof,
                               var3=source_st,var4=source_dt,var5=destination_st,var6=destination_dt,
                               var7=phoneNumber,var8=date,var9=status)
    else:
        status='Not Confirmed'
        client.messages.create(to="whatsapp:+917901527150",
                               from_="whatsapp:+14155238886",
                                body="Hello " + " " + full_name + "  " + "your travel from" + source_dt + " " + "To" + " " + destination_dt + " "
                                    + "Has" + " " + status + " On" + " " + date + " " + ", Apply later")
        return render_template('user_registration_dtls.html',var=full_name,var1=email_id,var2=id_proof,
                               var3=source_st,var4=source_dt,var5=destination_st,var6=destination_dt,
                               var7=phoneNumber,var8=date,var9=status)
if __name__=="__main__":
        app.run(port=9001,debug=True)