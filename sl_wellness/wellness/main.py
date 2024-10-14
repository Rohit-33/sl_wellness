from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import WellnessProgram
from datetime import datetime, timezone

main = Blueprint('main', __name__)

@main.route("/adminpview")
def display_admin_wp():
    wplist = WellnessProgram.query.all()
    return render_template("adminprogramlist.html", programs=wplist)

@main.route('/addwp')
def create_wellness_program():
    return render_template("addprogram.html")

@main.route("/addwp", methods=['POST'])
def create_wp_post():
    pname = request.form["pname"]
    pstart = request.form["pstart"]
    pend = request.form["pend"]
    pvenue = request.form["pvenue"]
    porganizer = request.form['porganizer']
    pdesc = request.form['pdesc']
    pcontact = request.form['pcontact']

    print(pname, pstart, pend)

    pstart = datetime.strptime(pstart, '%Y-%m-%dT%H:%M')
    pstart = pstart.replace(tzinfo=timezone.utc)

    pend = datetime.strptime(pend, '%Y-%m-%dT%H:%M')
    pend = pend.replace(tzinfo=timezone.utc)

    wp = WellnessProgram(pname=pname, pstart=pstart, pend=pend,
                         pvenue=pvenue, porganizer=porganizer, 
                         pdesc=pdesc, pcontact=pcontact
                         )
    db.session.add(wp)
    db.session.commit()

    flash("new wellness program is added")

    return redirect(url_for("main.display_admin_wp"))

@main.route("/updatewp/<int:wpid>", methods=['GET', 'POST'])
def update_wp(wpid):
    wp = WellnessProgram.query.get_or_404(wpid)
    print(wp.pid, wp.pname, wp.pdesc)

    if request.method == "POST":
        wp.pname = request.form["pname"]
        wp.pvenue = request.form["pvenue"]
        wp.porganizer = request.form['porganizer']
        wp.pdesc = request.form['pdesc']
        wp.pcontact = request.form['pcontact']
        pstart = request.form['pstart']
        pend =request.form['pend']

        pstart = datetime.strptime(pstart, '%Y-%m-%dT%H:%M')
        pstart = pstart.replace(tzinfo=timezone.utc)

        pend = datetime.strptime(pend, '%Y-%m-%dT%H:%M')
        pend = pend.replace(tzinfo=timezone.utc)

        wp.pstart = pstart
        wp.pend = pend

        db.session.commit()
        flash("Program details updated successfully")

        return redirect(url_for("main.display_admin_wp"))

    print("hello")
    return render_template("updateprogram.html", program=wp)

@main.route("/deletewp/<int:wpid>", methods=['GET', 'POST'])
def delete_wp(wpid):
    wp = WellnessProgram.query.get_or_404(wpid)
    db.session.delete(wp)
    db.session.commit()
    return redirect(url_for("main.display_admin_wp"))



