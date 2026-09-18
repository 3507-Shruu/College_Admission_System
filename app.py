from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Secret key for sessions and flash messages
app.secret_key = os.getenv("SECRET_KEY", "college-admission-secret-key")


# MySQL Database Connection
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

print("MySQL Database Connected Successfully!")


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Student Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        student_id = request.form["student_id"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Check password
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        # Hash password
        hashed_password = generate_password_hash(password)

        cursor = None

        try:
            cursor = db.cursor()

            query = """
                INSERT INTO students
                (student_id, full_name, email, phone, password)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                student_id,
                full_name,
                email,
                phone,
                hashed_password
            )

            cursor.execute(query, values)
            db.commit()

            cursor.close()

            flash("Registration successful! You can now login.")
            return redirect(url_for("login"))

        except mysql.connector.Error as err:

            print("Database Error:", err)

            if cursor:
                cursor.close()

            flash("Student ID or Email already exists.")
            return redirect(url_for("register"))

    return render_template("register.html")


# Student Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        login_id = request.form["login_id"]
        password = request.form["password"]

        cursor = None

        try:
            cursor = db.cursor(dictionary=True)

            query = """
                SELECT id, student_id, full_name, email, password
                FROM students
                WHERE student_id = %s OR email = %s
            """

            cursor.execute(query, (login_id, login_id))
            student = cursor.fetchone()

            cursor.close()

            # Check student and password
            if student and check_password_hash(student["password"], password):

                session["student_id"] = student["student_id"]
                session["full_name"] = student["full_name"]

                return redirect(url_for("dashboard"))

            else:
                flash("Invalid Student ID/Email or Password.")
                return redirect(url_for("login"))

        except mysql.connector.Error as err:

            print("Database Error:", err)

            if cursor:
                cursor.close()

            flash("Database error. Please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")


# Student Dashboard
@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")

# Admission Application
@app.route("/admission-application", methods=["GET", "POST"])
def admission_application():

    if "student_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        student_id = session["student_id"]

        admission_year = request.form["admission_year"]
        student_year = request.form["student_year"]
        hostel_admission = request.form["hostel_admission"]
        course = request.form["course"]
        admission_type = request.form["admission_type"]
        admission_card_no = request.form.get("admission_card_no")

        full_name = request.form["full_name"]
        father_name = request.form["father_name"]
        mother_name = request.form["mother_name"]
        date_of_birth = request.form["date_of_birth"]

        fe_admission_year = request.form.get("fe_admission_year")
        se_admission_year = request.form.get("se_admission_year")
        te_admission_year = request.form.get("te_admission_year")

        eligibility_no = request.form.get("eligibility_no")
        pr_no = request.form.get("pr_no")

        religion = request.form.get("religion")
        caste = request.form.get("caste")
        caste_category = request.form.get("caste_category")

        scholarship = request.form["scholarship"]
        scholarship_type = request.form.get("scholarship_type")

        bank_name = request.form.get("bank_name")
        account_no = request.form.get("account_no")
        ifsc_code = request.form.get("ifsc_code")
        bsr_code = request.form.get("bsr_code")

        aadhaar_no = request.form.get("aadhaar_no")

        email = request.form["email"]
        phone = request.form["phone"]

        permanent_address = request.form.get("permanent_address")
        permanent_district = request.form.get("permanent_district")
        permanent_pincode = request.form.get("permanent_pincode")

        local_address = request.form.get("local_address")
        local_district = request.form.get("local_district")
        local_pincode = request.form.get("local_pincode")
        local_phone = request.form.get("local_phone")

        cursor = None

        try:

            cursor = db.cursor()

            query = """
                INSERT INTO applications (
                    student_id,
                    admission_year,
                    student_year,
                    hostel_admission,
                    course,
                    admission_type,
                    admission_card_no,
                    full_name,
                    father_name,
                    mother_name,
                    date_of_birth,
                    fe_admission_year,
                    se_admission_year,
                    te_admission_year,
                    eligibility_no,
                    pr_no,
                    religion,
                    caste,
                    caste_category,
                    scholarship,
                    scholarship_type,
                    bank_name,
                    account_no,
                    ifsc_code,
                    bsr_code,
                    aadhaar_no,
                    email,
                    phone,
                    permanent_address,
                    permanent_district,
                    permanent_pincode,
                    local_address,
                    local_district,
                    local_pincode,
                    local_phone
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """

            values = (
                student_id,
                admission_year,
                student_year,
                hostel_admission,
                course,
                admission_type,
                admission_card_no,
                full_name,
                father_name,
                mother_name,
                date_of_birth,
                fe_admission_year,
                se_admission_year,
                te_admission_year,
                eligibility_no,
                pr_no,
                religion,
                caste,
                caste_category,
                scholarship,
                scholarship_type,
                bank_name,
                account_no,
                ifsc_code,
                bsr_code,
                aadhaar_no,
                email,
                phone,
                permanent_address,
                permanent_district,
                permanent_pincode,
                local_address,
                local_district,
                local_pincode,
                local_phone
            )

            cursor.execute(query, values)
            db.commit()

            cursor.close()

            flash("Application submitted successfully!")

            return redirect(url_for("dashboard"))

        except mysql.connector.Error as err:

            print("Application Database Error:", err)

            if cursor:
                cursor.close()

            flash("Unable to submit application. Please try again.")

            return redirect(url_for("admission_application"))

    return render_template("admission_application.html")

# Application Status
@app.route("/application-status")
def application_status():

    if "student_id" not in session:
        return redirect(url_for("login"))

    cursor = None

    try:
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT application_id,
                   application_status,
                   created_at
            FROM applications
            WHERE student_id = %s
            ORDER BY application_id DESC
            LIMIT 1
        """

        cursor.execute(query, (session["student_id"],))
        application = cursor.fetchone()

        cursor.close()

        return render_template(
            "application_status.html",
            application=application
        )

    except mysql.connector.Error as err:

        print("Status Database Error:", err)

        if cursor:
            cursor.close()

        flash("Unable to load application status.")
        return redirect(url_for("dashboard"))

# Document Verification
@app.route("/document-verification", methods=["GET", "POST"])
def document_verification():

    if "student_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        student_id = session["student_id"]

        documents = [
            ("first_year_marksheet", "1st Year Marksheet / Result", True),
            ("first_year_passing_certificate", "1st Year Passing Certificate", False),
            ("lc_tc", "Leaving / Transfer Certificate (LC/TC)", True),
            ("migration_certificate", "Migration Certificate", False),
            ("tenth_certificate", "10th Standard Marksheet", True),
            ("twelfth_certificate", "12th Standard Marksheet", True),
            ("diploma_certificate", "Diploma Marksheet", True),
            ("identity_proof", "Aadhaar Card / Identity Proof", True),
            ("passport_photo", "Passport-size Photograph", True),
            ("caste_certificate", "Caste Certificate", True),
            ("caste_validity", "Caste Validity Certificate", True),
            ("non_creamy_layer", "Non-Creamy Layer Certificate", True),
            ("ews_certificate", "EWS Certificate", True),
            ("domicile_certificate", "Domicile Certificate", True),
            ("gap_certificate", "Gap Certificate / Affidavit", True),
            ("bank_passbook", "Bank Details / Bank Passbook", True)
        ]

        allowed_extensions = {
            "pdf",
            "jpg",
            "jpeg",
            "png"
        }

        MAX_DOCUMENT_SIZE = 600 * 1024 * 1024
        MAX_PHOTO_SIZE = 100 * 1024 * 1024

        # Check mandatory documents
        for field_name, document_type, mandatory in documents:

            file = request.files.get(field_name)

            if mandatory and (file is None or file.filename == ""):

                flash(document_type + " is required.")
                return redirect(url_for("document_verification"))

        cursor = None

        try:

            cursor = db.cursor()

            for field_name, document_type, mandatory in documents:

                file = request.files.get(field_name)

                # Skip optional document if not uploaded
                if file is None or file.filename == "":
                    continue

                filename = secure_filename(file.filename)

                # Check filename
                if "." not in filename:

                    flash("Invalid file for " + document_type)
                    cursor.close()

                    return redirect(
                        url_for("document_verification")
                    )

                # Check file extension
                extension = filename.rsplit(".", 1)[-1].lower()

                if extension not in allowed_extensions:

                    flash(
                        "Invalid file format for "
                        + document_type
                        + ". Use PDF, JPG, JPEG or PNG."
                    )

                    cursor.close()

                    return redirect(
                        url_for("document_verification")
                    )

                # Check file size
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)

                if field_name == "passport_photo":

                    max_size = MAX_PHOTO_SIZE

                else:

                    max_size = MAX_DOCUMENT_SIZE

                if file_size > max_size:

                    if field_name == "passport_photo":

                        flash(
                            "Passport photo must be 2 MB or less."
                        )

                    else:

                        flash(
                            document_type
                            + " must be 5 MB or less."
                        )

                    cursor.close()

                    return redirect(
                        url_for("document_verification")
                    )

                # Create unique filename
                unique_filename = (
                    str(uuid.uuid4())
                    + "_"
                    + filename
                )

                file_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    unique_filename
                )

                # Save file
                file.save(file_path)

                # Save document information in MySQL
                query = """
                    INSERT INTO documents
                    (
                        student_id,
                        document_type,
                        file_name,
                        file_path,
                        verification_status
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """

                values = (
                    student_id,
                    document_type,
                    filename,
                    file_path,
                    "Pending"
                )

                cursor.execute(query, values)

            db.commit()
            cursor.close()

            flash("Documents uploaded successfully!")

            return redirect(url_for("dashboard"))

        except mysql.connector.Error as err:

            print("Document Database Error:", err)

            if cursor:
                cursor.close()

            flash(
                "Unable to upload documents. Please try again."
            )

            return redirect(
                url_for("document_verification")
            )

    return render_template("document_verification.html")


# Logout
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)