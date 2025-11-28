from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/button', methods=['POST'])
def button():
    if request.method == 'POST':
        button_value = request.form.get('button')
        if button_value == 'pressed':
            with open("Bookinglogs.txt", "r+") as file: #AI assisted, i was confused dont know everything about file handling
                lines = file.readlines()  

                file.seek(0) 
                for line in lines:
                    if "Reservert sete: " in line and "Navn" not in line:
                        file.write(" " * (len(line)-1) + "\n")
                    else:
                        file.write(line)             
            return render_template('kjøpside.html', order=ordernr, username=username, pas=passs, telefon=telefon, email=email, addresse=addresse)
        button_value = request.form.get('home')
        if button_value == 'pressed':
            return render_template('index.html', order=ordernr, username=username, pas=passs, telefon=telefon, email=email, addresse=addresse)
        button_value = request.form.get('seats')
        if button_value == 'pressed':        
            setter = reservedseats()
            return render_template('sjekkside.html', order=ordernr, username=username, pas=passs, telefon=telefon, email=email, addresse=addresse, setter=setter)
        

@app.route('/')
def sjekkside():
    return render_template('sjekkside.html')


@app.route('/')
def kjøpside():
    items=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ,14 ,15 ,16 ,17, 18, 19, 20, 21 ,22, 23, 24]
    return render_template('kjøpside.html', items=items)

with open("Bookinglogs.txt", "a") as g:
    g.truncate(0)

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    item_name = data.get("seat")

    with open("Bookinglogs.txt", "a") as g:
        g.write(f"Reservert sete: {item_name} " )
    
    return jsonify({"status": "success", "item": item_name})

@app.route("/unsave", methods=["POST"])
def unsave():
    data = request.get_json()
    item_name = data.get("seat")

    target=f"Reservert sete: {item_name} "
    with open("Bookinglogs.txt", "r") as f:
        content = f.read()

    content = content.replace(target, "")

    with open("Bookinglogs.txt", "w") as f:
        f.write(content)
    
    return jsonify({"status": "success", "item": item_name})

setter=""
ordernr=0
username=""
email=""
addresse = ""
telefon = ""
passs = ""


@app.route('/submit_form', methods=['POST'])
def submitform():
    global ordernr, username, passs, telefon, email, addresse
    ordernr = ordernr+1
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('mail')
        addresse = request.form.get('address')
        telefon = request.form.get('pnumber')
        passs = request.form.get('passes')
        with open("Bookinglogs.txt", "a") as g:
            g.write(f"Ordrenummer: {ordernr}, Passtype: {passs}, Navn: {username}, Telefon: {telefon}, Mail: {email}, Addresse: {addresse}\n")
        return render_template('takkside.html', order=ordernr, username=username, pas=passs, telefon=telefon, email=email, addresse=addresse)

def read_seats():
    seats=[]
    with open("Bookinglogs.txt", "r") as r:
        for _ in open("Bookinglogs.txt"):
            line = r.readline()
            if "Reservert sete: " in line:
                found = re.findall(r"Reservert sete:\s*(\d+)", line)
                for s in found:
                    seat_num = int(s)
                    if seat_num <= 25:  
                        seats.append(seat_num)
        #with open("test.txt", "a") as t:    For testing
        #    t.truncate(0)
        #    s=str(seats)
        #    t.write(s)

    return seats
            
@app.route("/get_seats", methods=["POST"])
def get_seats():
    seats = read_seats()
    return jsonify(seats)

#read_seats() For testing

def reservedseats():
    global username
    found=[]
    with open("Bookinglogs.txt", "r") as r:
        for _ in ("Bookinglogs.txt"):
            linjen = r.readline()
            if username in linjen:
                found = re.findall(r"Reservert sete:\s*(\d+)", linjen)   
                return found


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')