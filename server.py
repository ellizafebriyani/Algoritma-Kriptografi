import math
from flask import Flask, render_template, request, send_file
import classic.vigenere
import classic.fullvigenere
import classic.extvigenere
import classic.playfair
import classic.util
import classic.affine
import classic.hill
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './processed-files'


'''
Notes:
1. Untuk semua module, import classic.<nama>
2. Sebelum olah akses input dari user, jangan lupa olah menggunakan classic.util
3. Akses input teks dari user di request.form["message"]
'''


# Routes
@app.route('/')
def landing():
    return render_template("index.html", message="Henlo!")


@app.route('/<cipher>')
def view_cipher_page(cipher):
    return render_template(cipher+".html", message=cipher)


# Post routes fill here
@app.route('/vigenere', methods=['POST'])
def view_vigenere_result():
    msg = classic.util.alphabetify(request.form["message"])
    key = classic.util.alphabetify(request.form["key"])

    if request.form["act"] == "enc":
        result = classic.vigenere.encrypt(msg, key)
    else:
        result = classic.vigenere.decrypt(msg, key)

    if request.form["format"] == "block":
        result = classic.util.blockify(result)

    if request.form["type-out"] == "file":
        f_path = app.config['UPLOAD_FOLDER'] + \
            "/" + request.form["act"] + ".txt"
        f = open(f_path, "w")
        f.write(result)
        f.close()
        return send_file(f_path, as_attachment=True)

    return render_template("vigenere.html", result=result, inputtext=msg, key=key)


'''  @app.route('/fullvigenere', methods=['POST'])
def view_fullvigenere_result():
    msg = classic.util.alphabetify(request.form["message"])
    key = classic.util.alphabetify(request.form["key"])

    if request.form["act"] == "enc":
        result = classic.fullvigenere.encrypt(msg, key)
    else:
        result = classic.fullvigenere.decrypt(msg, key)
    
    if request.form["format"] == "block":
            result = classic.util.blockify(result)
    
    if request.form["type-out"] == "file":
        f_path = app.config['UPLOAD_FOLDER'] + "/" + request.form["act"] + ".txt"
        f = open(f_path, "w")
        f.write(result)
        f.close()
        return send_file(f_path, as_attachment=True)
    
    return render_template("fullvigenere.html", result=result, inputtext=msg, key=key) '''


@app.route('/fullvigenere', methods=['POST'])
def view_fullvigenere_result():
    msg = classic.util.alphabetify(
        request.form["message"])  # Memastikan input valid
    key = classic.util.alphabetify(request.form["key"])
    # Mendapatkan jenis cipher dari HTML
    cipher_type = request.form["cipher_type"]
    act = request.form["act"]
    output_format = request.form["format"]
    output_type = request.form["type-out"]

    # Pemrosesan enkripsi atau dekripsi
    if act == "enc":
        if cipher_type == "fullvigenere":
            result = classic.fullvigenere.encrypt(msg, key)
        elif cipher_type == "autokey":
            result = classic.fullvigenere.auto_key_encrypt(msg, key)
        else:
            result = "Invalid Cipher Type!"
    else:
        if cipher_type == "fullvigenere":
            result = classic.fullvigenere.decrypt(msg, key)
        elif cipher_type == "autokey":
            result = classic.fullvigenere.auto_key_decrypt(msg, key)
        else:
            result = "Invalid Cipher Type!"

    # Format hasil
    if output_format == "block":
        result = ' '.join([result[i:i+5] for i in range(0, len(result), 5)])

    # Output file atau teks
    if output_type == "file":
        f_path = f"{app.config['UPLOAD_FOLDER']}/{act}_result.txt"
        with open(f_path, "w") as f:
            f.write(result)
        return send_file(f_path, as_attachment=True)

    # Tampilkan hasil dalam HTML
    return render_template("fullvigenere.html", result=result, inputtext=msg, key=key)


@app.route('/extvigenere', methods=['POST'])
def view_extvigenere_result():
    key = request.form["key"]

    if request.form["type-inp"] == "txt":
        msg = request.form["message"]

        if request.form["act"] == "enc":
            result = classic.extvigenere.encrypt(msg, key)
        else:
            result = classic.extvigenere.decrypt(msg, key)

        if request.form["format"] == "block":
            result = classic.util.blockify(result)

        if request.form["type-out"] == "file":
            f_path = app.config['UPLOAD_FOLDER'] + \
                "/" + request.form["act"] + ".txt"
            f = open(f_path, "w")
            f.write(result)
            f.close()
            return send_file(f_path, as_attachment=True)

        return render_template("extvigenere.html", result=result, inputtext=msg, key=key)

    else:
        # Save File
        f = request.files["file"]
        f_loc = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(f_loc)

        if request.form["act"] == "enc":
            res_loc = classic.extvigenere.encrypt(f_loc, key, True)
        else:
            res_loc = classic.extvigenere.decrypt(f_loc, key, True)

        return send_file(res_loc, as_attachment=True)


@app.route('/playfair', methods=['POST'])
def view_playfair_result():
    msg = classic.util.alphabetify(request.form["message"])
    key = classic.util.alphabetify(request.form["key"])

    if request.form["act"] == "enc":
        result = classic.playfair.encrypt(msg, key)
    else:
        result = classic.playfair.decrypt(msg, key)

    if request.form["format"] == "block":
        result = classic.util.blockify(result)

    if request.form["type-out"] == "file":
        f_path = app.config['UPLOAD_FOLDER'] + \
            "/" + request.form["act"] + ".txt"
        f = open(f_path, "w")
        f.write(result)
        f.close()
        return send_file(f_path, as_attachment=True)

    return render_template("playfair.html", result=result, inputtext=msg, key=key)

@app.route('/affine', methods=['POST'])
def view_affine_result():
    msg = classic.util.alphabetify(request.form["message"])
    key_m = int(request.form["key_m"])
    key_b = int(request.form["key_b"])
    validation_msg = ""

    key_m_all = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    if key_m not in key_m_all:
        validation_msg = "Invalid value for m. Try another!"
        return render_template("affine.html", inputtext=msg, key_m=key_m, key_b=key_b, validate=validation_msg)

    if request.form["act"] == "enc":
        result = classic.affine.encrypt(msg, key_m, key_b)
    else:
        result = classic.affine.decrypt(msg, key_m, key_b)

    if request.form["format"] == "block":
        result = classic.util.blockify(result)

    if request.form["type-out"] == "file":
        f_path = app.config['UPLOAD_FOLDER'] + \
            "/" + request.form["act"] + ".txt"
        f = open(f_path, "w")
        f.write(result)
        f.close()
        return send_file(f_path, as_attachment=True)

    return render_template("affine.html", result=result, inputtext=msg, key_m=key_m, key_b=key_b, validation=validation_msg)


@app.route('/hill', methods=['POST'])
def view_hill_result():
    msg = classic.util.alphabetify(request.form["message"])

    # Get matrix size
    matrix_size = int(request.form.get("matrix-size", "3"))

    # Get key values based on matrix size
    key_values = []
    for i in range(matrix_size):
        key_name = f"key_{i}"
        if key_name in request.form:
            key_values.append(request.form[key_name])
        else:
            # Missing key input
            error_message = f"Input matriks tidak lengkap. Diperlukan {matrix_size} baris."
            return render_template("hill.html",
                                inputtext=msg,
                                error_message=error_message,
                                matrix_size=str(matrix_size))

    # Validate key matrix format and parse into a matrix
    try:
        key_matrix = []
        for i in range(matrix_size):
            row_values = key_values[i].split(',')

            # Check if row has correct number of elements
            if len(row_values) != matrix_size:
                error_message = f"Baris {i+1} harus memiliki tepat {matrix_size} angka yang dipisahkan koma."
                return render_template("hill.html",
                                    inputtext=msg,
                                    error_message=error_message,
                                    matrix_size=str(matrix_size),
                                       **{f"key_{j}": key_values[j] for j in range(len(key_values))})

            # Convert to integers
            try:
                row = list(map(int, row_values))
                key_matrix.append(row)
            except ValueError:
                error_message = f"Format input tidak valid pada baris {i+1}. Masukkan angka yang dipisahkan koma."
                return render_template("hill.html",
                                    inputtext=msg,
                                    error_message=error_message,
                                    matrix_size=str(matrix_size),
                                       **{f"key_{j}": key_values[j] for j in range(len(key_values))})

    except Exception as e:
        # General format error
        error_message = f"Format matriks tidak valid: {str(e)}"
        return render_template("hill.html",
                            inputtext=msg,
                            error_message=error_message,
                            matrix_size=str(matrix_size),
                               **{f"key_{j}": key_values[j] for j in range(len(key_values))})

    # Check if matrix is invertible
    check_determinant = classic.hill.determinant_matrix(
        key_matrix, matrix_size)
    if math.gcd(check_determinant % 26, 26) != 1:
        error_message = f"Matriks {matrix_size}x{matrix_size} ini tidak dapat digunakan sebagai kunci karena tidak memiliki invers dalam modulo 26!"
        return render_template("hill.html",
                            inputtext=msg,
                            error_message=error_message,
                            matrix_size=str(matrix_size),
                               **{f"key_{j}": key_values[j] for j in range(len(key_values))})

    # Process encryption/decryption
    try:
        if request.form["act"] == "enc":
            result = classic.hill.encrypt(msg, key_matrix, size=matrix_size)
        else:
            result = classic.hill.decrypt(msg, key_matrix, matrix_size)

            # Check if there was an error in decryption
            if result.startswith("ERROR:"):
                error_message = result[6:]  # Remove "ERROR:" prefix
                return render_template("hill.html",
                                    inputtext=msg,
                                    error_message=error_message,
                                    matrix_size=str(matrix_size),
                                       **{f"key_{j}": key_values[j] for j in range(len(key_values))})

        if request.form["format"] == "block":
            result = classic.util.blockify(result)

        if request.form["type-out"] == "file":
            f_path = app.config['UPLOAD_FOLDER'] + \
                "/" + request.form["act"] + ".txt"
            f = open(f_path, "w")
            f.write(result)
            f.close()
            return send_file(f_path, as_attachment=True)

        return render_template("hill.html",
                            result=result,
                            inputtext=msg,
                            matrix_size=str(matrix_size),
                               **{f"key_{j}": key_values[j] for j in range(len(key_values))})

    except Exception as e:
        # Handle any other errors during processing
        error_message = f"Terjadi kesalahan: {str(e)}"
        return render_template("hill.html",
                            inputtext=msg,
                            error_message=error_message,
                            matrix_size=str(matrix_size),
                               **{f"key_{j}": key_values[j] for j in range(len(key_values))})


# Entry point
if __name__ == '__main__':
    app.run()
