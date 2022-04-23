from audioop import mul
from email.utils import decode_rfc2231
from enum import unique
from fileinput import filename
from pipes import Template
from re import T
from signal import pause
import string
from unicodedata import name
# from tkinter import TOP
from xmlrpc.client import APPLICATION_ERROR

from jinja2 import Template 

from app import app 

from flask import flash, render_template, request, redirect, jsonify, make_response, json, send_from_directory, url_for, session

from werkzeug.utils import secure_filename

from PyPDF2 import PdfFileReader, PdfFileMerger

from fpdf import FPDF 

from flask_sqlalchemy import SQLAlchemy

import os 

# -*- coding: utf-8 -*- 

@app.route("/admin/dashboard")
def log_out():

    

    return redirect(url_for('index'))
    
@app.route("/", methods = ["GET", "POST"])
def index():

    session.pop("USERNAME", None)

    if request.method == "POST":

        if request.form['password'] == 'user1':
            session["USERNAME"] = "user1"
            return redirect(url_for("upload_pdf"))
        elif (request.form['password'] != ''):
            flash("Nieprawidłowe dane logowania!")
        

    return render_template("/public/index.html")

@app.route("/about")
def about():

    try:
        return send_from_directory(app.config["PDF_DOWNLOADS"], "merged.pdf", as_attachment=True)
    except FileNotFoundError:
        os.abort(404)


app.config["PDF_UPLOADS"] = "/home/manajpatryk/app/app/static/pdf/uploads"
app.config["PDF_DOWNLOADS"] = "/home/manajpatryk/app/app/static/pdf/downloads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PDF"]
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///directive.db'
app.config["MAX_IMAGE_FILESIZE"] = 10485760 
app.config['SECRET_KEY'] = '000d88cd9d90036ebdd237eb6b0db000'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

#Initialize the database
db = SQLAlchemy(app)


#Create a db model 
class Direcive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    dyrect = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        template = '{0.id} {0.name} {0.dyrect}'
        return template.format(self)
        

def allowed_pdf(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config ["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_pdf_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True 
    else:
        return False


@app.route("/upload-pdf", methods = ["GET", "POST"])
def upload_pdf():

    if request.method == "POST":

        if request.files:

            if not allowed_pdf_filesize(request.cookies.get("filesize")):
                flash("Plik jest za duży!")
                print("File exceeded maximum size")
                return redirect(request.url)
            
            pdf = request.files["pdf"]

            if pdf.filename == "":
                flash("Nie wybrano pliku!")
                print(".pdf must have a filename")
                return redirect(request.url)

            if not allowed_pdf(pdf.filename):
                flash("Niedozwolone rozszerzenie pliku!")
                print("Than extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(pdf.filename)
                pdf.save(os.path.join(app.config["PDF_UPLOADS"], pdf.filename))

            print(".pdf saved")

            translate_declaration(pdf.filename)


            try:
                return send_from_directory(app.config["PDF_DOWNLOADS"], "merged.pdf", as_attachment=True)
            except FileNotFoundError:
                os.abort(404)
            # return redirect(request.url)
        
        else:

            req = request.get_json()
            FormName_1 = req["dyr_name_1"]
            FormDyrec_1 = req["dyrect_1"]
            FormName_2 = req["dyr_name_2"]
            FormDyrec_2 = req["dyrect_2"]
            FormName_3 = req["dyr_name_3"]
            FormDyrec_3 = req["dyrect_3"]
            FormName_4 = req["dyr_name_4"]
            FormDyrec_4 = req["dyrect_4"]
            FormName_5 = req["dyr_name_5"]
            FormDyrec_5 = req["dyrect_5"]
            flag = req['flag']

            bb=[]

            if (FormName_1 != '' and FormDyrec_1 == '') or (FormName_2 != '' and FormDyrec_2 == '') or (FormName_3 != '' and FormDyrec_3 == '') or (FormName_4 != '' and FormDyrec_4 == '') or (FormName_5 != '' and FormDyrec_5 == ''):
                
                    if (FormName_1 != '' and FormDyrec_1 == ''):
                        if flag == "0":
                            bb.append(str(Direcive.query.filter_by(name=FormName_1).first().dyrect))
                        elif flag == "1":
                            Direcive.query.filter_by(name=FormName_1).delete() 
                            db.session.commit()
                    
                    if FormName_2 != '' and FormDyrec_2 == '':
                        if flag == "0":
                            bb.append(str(Direcive.query.filter_by(name=FormName_2).first().dyrect))
                        elif flag == "1":
                            Direcive.query.filter_by(name=FormName_2).delete()
                            db.session.commit()

                    if FormName_3 != '' and FormDyrec_3 == '':
                        if flag == "0":
                            bb.append(str(Direcive.query.filter_by(name=FormName_3).first().dyrect))
                        elif flag == "1":
                            Direcive.query.filter_by(name=FormName_3).delete()
                            db.session.commit()

                    if FormName_4 != '' and FormDyrec_4 == '':
                        if flag == "0":
                            bb.append(str(Direcive.query.filter_by(name=FormName_4).first().dyrect))
                        elif flag == "1":
                            Direcive.query.filter_by(name=FormName_4).delete()
                            db.session.commit()

                    if FormName_5 != '' and FormDyrec_5 == '':
                        if flag == "0":
                            bb.append(str(Direcive.query.filter_by(name=FormName_5).first().dyrect))
                        elif flag == "1":
                            Direcive.query.filter_by(name=FormName_5).delete()
                            db.session.commit()

                    res = make_response(jsonify(bb), 200)
                    return res
                
            elif (FormName_1 !='' and FormDyrec_1 !='') or (FormName_2 !='' and FormDyrec_2 !='') or (FormName_3 !='' and FormDyrec_3 !='') or (FormName_4 !='' and FormDyrec_4 !='') or (FormName_5 !='' and FormDyrec_5 !=''):
                
                if FormName_1 !='' and FormDyrec_1 !='': 
                    if Direcive.query.filter_by(name=FormName_1) != '':
                        Direcive.query.filter_by(name=FormName_1).delete() 
                        db.session.commit()
                    db.session.add(Direcive(name = FormName_1, dyrect = FormDyrec_1))

                if FormName_2 !='' and FormDyrec_2 !='':
                    if Direcive.query.filter_by(name=FormName_2) != '':
                        Direcive.query.filter_by(name=FormName_2).delete() 
                        db.session.commit()
                    db.session.add(Direcive(name = FormName_2, dyrect = FormDyrec_2))

                if FormName_3 !='' and FormDyrec_3 !='':
                    if Direcive.query.filter_by(name=FormName_3) != '':
                        Direcive.query.filter_by(name=FormName_3).delete() 
                        db.session.commit()
                    db.session.add(Direcive(name = FormName_3, dyrect = FormDyrec_3))

                if FormName_4 !='' and FormDyrec_4 !='':
                    if Direcive.query.filter_by(name=FormName_4) != '':
                        Direcive.query.filter_by(name=FormName_4).delete() 
                        db.session.commit()
                    db.session.add(Direcive(name = FormName_4, dyrect = FormDyrec_4))
                    
                if FormName_5 !='' and FormDyrec_5 !='':
                    if Direcive.query.filter_by(name=FormName_5) != '':
                        Direcive.query.filter_by(name=FormName_5).delete() 
                        db.session.commit()
                    db.session.add(Direcive(name = FormName_5, dyrect = FormDyrec_5))

                db.session.commit() 


                # else: 
                #     flash("Sprawdź czy podanego numemru dyrektywy nie ma już w bazie. Jeśli próbujesz napisać istniejącą dyrektywę, to najpierw musisz usunąć starą!")
                
    dyrectives = Direcive.query.all()

    if session.get("USERNAME", None) is not None:
        return render_template("public/upload_pdf.html", dyrectives=dyrectives)
    else:
        print("Nieznaleziono w sesji")
        return redirect(url_for("index"))


    # return render_template("public/upload_pdf.html", dyrectives=dyrectives)


def translate_declaration(filename):

    path = os.path.join(app.config['PDF_UPLOADS'], filename)
    input_file = PdfFileReader(open(path,'rb'))
   
    pdf = FPDF('P', 'mm', 'A4')

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    pdf.add_font('Siemens', '', r'/home/manajpatryk/app/app/fonts/Dialog-Bold.ttf', uni=True)
    pdf.add_font('Open_Sans', '', r'/home/manajpatryk/app/app/fonts/OpenSans-Italic-VariableFont_wdt.ttf', uni=True)
    pdf.add_font('Robo', '',r'/home/manajpatryk/app/app/fonts/Roboto-Regularr.ttf', uni=True)

    pdf.set_font('Siemens', '', 28)

    pdf.set_text_color(0,153,153)

    pdf.cell(115, 10, "SIEMENS", border=False)
    
    pdf.set_text_color(0,0,0)
    pdf.set_font('Robo', '', 16)
    req = request.form
    first_cell = req.get("decnum")
    pdf.cell(75, 15, "Nr "+first_cell, ln=True, border=False, align='R')
    pdf.set_font('Robo', '', 20)
    pdf.cell(190, 15, 'Tłumaczenie deklaracji zgodności', ln=True, border=False, align='C')
    pdf.set_font('Robo', '', 10)

    
    pdf.cell(40,10, 'Opis produktu', border=False)
    product_identyf = req.get("prodident")
    pdf.multi_cell(130, 10, product_identyf, border=False)
    pdf.cell(40,10, 'Producent', border=False)
    manufacturer = req.get("manufac")
    pdf.multi_cell(130, 10, manufacturer, border=False)
    pdf.cell(40,10, 'Adres', border=False)
    adr = req.get("adresss")
    pdf.multi_cell(130, 10, adr, border=False)

    pdf.multi_cell(190, 3, '')
    pdf.multi_cell(190, 5, 'Deklarujemy z całą odpowiedzialnością, że określone wyżej produkty są zgodne z następującymi europejskimi dyrektywami:')
    pdf.multi_cell(190, 3, '')

    if request.form['directive_number_1'] != "" and request.form['directive_1']:
        pdf.cell(30, 5, request.form['directive_number_1'], border=False)
        pdf.multi_cell(160, 5, request.form['directive_1'], border=False)

    if request.form['directive_number_2'] != "" and request.form['directive_2']:
        pdf.cell(30, 5, request.form['directive_number_2'], border=False)
        pdf.multi_cell(160, 5, request.form['directive_2'], border=False)

    if request.form['directive_number_3'] != "" and request.form['directive_3']:
        pdf.cell(30, 5, request.form['directive_number_3'], border=False)
        pdf.multi_cell(160, 5, request.form['directive_3'], border=False)
    
    if request.form['directive_number_4'] != "" and request.form['directive_4']:
        pdf.cell(30, 5, request.form['directive_number_4'], border=False)
        pdf.multi_cell(160, 5, request.form['directive_4'], border=False)

    if request.form['directive_number_5'] != "" and request.form['directive_5']:
        pdf.cell(30, 5, request.form['directive_number_5'], border=False)
        pdf.multi_cell(160, 5, request.form['directive_5'], border=False) 
    
    
    pdf.multi_cell(195, 10, 'Zgodność z dyrektywami została potwierdzona przez spełnienie następujących norm:')

    pdf.cell(47.5, 10, 'Norma', ln=0)
    pdf.cell(47.5, 10, 'Rok', ln=0)
    pdf.cell(47.5, 10, 'Rok', ln=0)
    pdf.cell(47.5, 10, 'Norma', ln=1)


    if request.form['norma_1'] != "": 
        pdf.cell(47.5, 7, request.form['norma_1'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_1'], border=False, ln=0)

    if request.form['norma_2'] !="":
        pdf.cell(47.5, 7, request.form['norma_2'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_2'], border=False, ln=1)

    if request.form['norma_3'] != "": 
        pdf.cell(47.5, 7, request.form['norma_3'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_3'], border=False, ln=0)

    if request.form['norma_4'] !="":
        pdf.cell(47.5, 7, request.form['norma_4'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_4'], border=False, ln=1)

    if request.form['norma_5'] != "": 
        pdf.cell(47.5, 7, request.form['norma_5'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_5'], border=False, ln=0)

    if request.form['norma_6'] !="":
        pdf.cell(47.5, 7, request.form['norma_6'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_6'], border=False, ln=1) 
    
    if request.form['norma_7'] != "": 
        pdf.cell(47.5, 7, request.form['norma_7'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_7'], border=False, ln=0)

    if request.form['norma_8'] !="":
        pdf.cell(47.5, 7, request.form['norma_8'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_8'], border=False, ln=1)

    if request.form['norma_9'] != "": 
        pdf.cell(47.5, 7, request.form['norma_9'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_9'], border=False, ln=0)

    if request.form['norma_10'] !="":
        pdf.cell(47.5, 7, request.form['norma_10'], border=False, ln=0)
        pdf.cell(47.5, 7, request.form['rok_10'], border=False, ln=1)

    pdf.set_xy(10, 210)
    pdf.set_font('Robo', '', 11)
    pdf.cell(60, 7, request.form['date_place'], border = 'B', align = 'C', ln=2)
    pdf.set_font('Robo', '', 8)
    pdf.cell(60, 7, 'Miejsce i data sporządzenia oryginału', border = '', align = 'C', ln=2)

    pdf.set_xy(10, 230)
    pdf.set_font('Robo', 'U', 8)
    pdf.cell(190, 3, "Niniejsza deklaracja poświadcza zgodność ze wskazanymi dyrektywami, lecz nie oznacza gwarancji jakości lub trwałości.", align = 'C', ln=2)

    pdf.set_xy(10, 240)
    pdf.cell(190, 3, "" , border = 'T', ln=2)
    pdf.set_font('Robo', '', 7)
    pdf.cell(47.5, 5, "Przetłumaczył: ", ln=2)
    pdf.cell(60, 15, "", border=True)
    pdf.set_font('Robo', '', 10)
    pdf.set_xy(10, 270)
    pdf.cell(190, 10, "W załączniku dołączono oryginalną deklarację zgodności w językach angielskim i niemieckim.")

    pdf.output('pdf_1.pdf')

    merger = PdfFileMerger()

    merger.append(open('pdf_1.pdf', 'rb'))
    merger.append(input_file)
    

    merger.write("/home/manajpatryk/app/app/static/pdf/downloads/merged.pdf")
    merger.close()

    rm_path = "/home/manajpatryk/app/app/static/pdf/uploads/" + filename

    os.remove(rm_path)

