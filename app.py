import os
from flask import Flask, jsonify, render_template, request, send_file
import secrets
import string
import math

app = Flask(__name__)

word_list = []
with open('wordlist.txt', 'r') as file:
    word_list = [line.strip() for line in file if len(line.strip()) <= 12]  # Oletusarvo max pituudelle

special_characters = "!@#$%^&*()"

def calculate_entropy(password):
    pool_size = len(set(password))
    entropy = len(password) * math.log2(pool_size)
    return entropy

def get_random_separator(separator_type, user_defined_separator=''):
    if separator_type == "number":
        return str(secrets.choice(string.digits))
    elif separator_type == "special":
        return secrets.choice(special_characters)
    elif separator_type == "single_character":
        return user_defined_separator
    return '-' 


def generate_passphrase(word_count=4, capitalize=False, separator_type='space', max_word_length=12, user_defined_separator=''):
    filtered_word_list = [word for word in word_list if len(word) <= max_word_length]
    passphrase_words = [secrets.choice(filtered_word_list) for _ in range(word_count)]
    if capitalize:
        passphrase_words = [word.capitalize() for word in passphrase_words]
    
    separator = get_random_separator(separator_type, user_defined_separator)
    passphrase = separator.join(passphrase_words)
    return passphrase

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-password', methods=['POST'])
def generate_password_route():
    length = request.form.get('length', type=int, default=12)
    include_uppercase = request.form.get('include_uppercase', 'false') == 'true'
    include_digits = request.form.get('include_digits', 'false') == 'true'
    include_special = request.form.get('include_special', 'false') == 'true'
    generate_type = request.form.get('type', 'password')
    capitalize = request.form.get('capitalize', 'false') == 'true'
    separator_type = request.form.get('separator_type', 'space')
    max_word_length = request.form.get('max_word_length', type=int, default=12)
    user_defined_separator = request.form.get('user_defined_separator', '')
    
    if generate_type == 'passphrase':
        word_count = request.form.get('word_count', type=int, default=4)
        password = generate_passphrase(word_count, capitalize, separator_type, max_word_length, user_defined_separator)
    else:
        characters = string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_digits:
            characters += string.digits
        if include_special:
            characters += special_characters
        password = ''.join(secrets.choice(characters) for _ in range(length))
    
    entropy = calculate_entropy(password)
    return jsonify(password=password, entropy=entropy)

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/service-worker.js')
def serve_sw():
    return send_file('service-worker.js', mimetype='application/javascript')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5069)))
