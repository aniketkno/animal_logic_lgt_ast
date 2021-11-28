import sqlite3
import io
import csv

import person_service
from flask import (
    Flask,
    render_template,
    Blueprint,
    jsonify,
    make_response,
    request,
    flash,
    url_for,
    redirect,
)


person_page = Blueprint("person_page", __name__, template_folder="templates")


def create_connection(db_name):
    conn = sqlite3.connect(f"{db_name}.db")
    cur = conn.cursor()
    return conn, cur


@person_page.route("/")
def show_persons():
    return render_template("index.html", persons=get_all_person_data())


@person_page.route("/api/create_person_data", methods=["POST"])
def create_person_data():

    db_name = "person"
    conn, cur = create_connection(db_name)
    # Read Values
    person = (
        request.form["person-name"],
        request.form["person-address"],
        request.form["person-phone-number"],
    )

    if not request.form["person-name"]:
        flash("Enter Name", "red")
    if not request.form["person-address"]:
        flash("Enter Address", "red")
    if not request.form["person-phone-number"]:
        flash("Enter Phone Number", "red")
    if (
        request.form["person-name"]
        and request.form["person-address"]
        and request.form["person-phone-number"]
    ):
        person_service.set_person_data(person, conn, cur)
        flash("person added successfully", "green")
    return redirect(url_for("person_page.show_persons"))


@person_page.route("/api/delete_person_data/<person_id>", methods=["POST", "GET"])
def delete_person_data(person_id):

    db_name = "person"
    conn, cur = create_connection(db_name)

    person_service.delete_person_data(person_id, conn, cur)
    flash("person deleted successfully", "yellow")
    return redirect(url_for("person_page.show_persons"))


@person_page.route("/api/get_all_person_data", methods=["GET"])
def get_all_person_data():

    db_name = "person"
    conn, cur = create_connection(db_name)

    # Read Values
    list_basic_person_dto = person_service.get_all_person_data(cur)
    print(list_basic_person_dto)
    return list_basic_person_dto


@person_page.route("/api/get_all_person_data_json", methods=["GET"])
def get_all_person_data_json():

    db_name = "person"
    conn, cur = create_connection(db_name)

    # Read Values
    list_basic_person_dto = person_service.get_all_person_data(cur)
    print(list_basic_person_dto)
    return jsonify(list_basic_person_dto)


@person_page.route("/api/get_all_person_data_csv", methods=["GET"])
def get_all_person_data_csv():

    db_name = "person"
    conn, cur = create_connection(db_name)

    list_basic_person_dto = person_service.get_all_person_data(cur)
    # print(list_basic_person_dto)
    si = io.StringIO()

    cw = csv.writer(si)
    for basic_person_dto in list_basic_person_dto:
        cw.writerow(
            (
                basic_person_dto.name,
                basic_person_dto.address,
                str(basic_person_dto.phone),
            )
        )
    output = make_response(si.getvalue())
    output.headers["Content-type"] = "text/csv"
    return output
