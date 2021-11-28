import sqlite3
import io
import csv
import glob
import fnmatch
import person_service
from flask import (
    Flask,
    flash,
    jsonify,
    request,
    url_for,
    redirect,
    Blueprint,
    make_response,
    render_template,
)


person_page = Blueprint("person_page", __name__, template_folder="templates")


def create_connection(db_name):
    conn = sqlite3.connect(f"{db_name}.db")
    cur = conn.cursor()
    return conn, cur


@person_page.route("/")
def show_persons():
    return render_template("index.html", persons=get_all_person_data())


@person_page.route("/api/filter_names", methods=["GET", "POST"])
def filter_names():
    filter_pattern = request.form["filter-names"]
    db_name = "person"
    conn, cur = create_connection(db_name)
    
    list_basic_person_dto = person_service.get_all_person_data(cur)
    list_ids = [
        basic_person_dto.id
        for basic_person_dto in list_basic_person_dto
        if fnmatch.fnmatch(basic_person_dto.name, filter_pattern)
    ]
    return render_template("index.html", persons=get_person_by_ids(list_ids))


@person_page.route("/api/create_person_data", methods=["POST"])
def create_person_data():

    db_name = "person"
    conn, cur = create_connection(db_name)
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


@person_page.route("/api/get_person_by_ids", methods=["GET"])
def get_person_by_ids(ids):

    db_name = "person"
    conn, cur = create_connection(db_name)

    list_basic_person_dto = person_service.get_person_by_ids(ids, cur)
    return list_basic_person_dto


@person_page.route("/api/get_all_person_data", methods=["GET"])
def get_all_person_data():

    db_name = "person"
    conn, cur = create_connection(db_name)

    list_basic_person_dto = person_service.get_all_person_data(cur)
    return list_basic_person_dto


@person_page.route("/api/get_all_person_data_json", methods=["GET"])
def get_all_person_data_json():

    db_name = "person"
    conn, cur = create_connection(db_name)

    list_basic_person_dto = person_service.get_all_person_data(cur)
    return jsonify(list_basic_person_dto)


@person_page.route("/api/get_all_person_data_csv", methods=["GET"])
def get_all_person_data_csv():

    db_name = "person"
    conn, cur = create_connection(db_name)

    list_basic_person_dto = person_service.get_all_person_data(cur)
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
