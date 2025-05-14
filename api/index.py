from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_primes_up_to(n):
    return [num for num in range(2, n + 1) if is_prime(num)]

# HTML template for the form
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Prime Numbers Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        .result { margin-top: 20px; }
        input[type="number"] { padding: 5px; font-size: 16px; }
        button { padding: 5px 15px; font-size: 16px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Prime Numbers Generator</h1>
        <form method="GET">
            <label for="limit">Enter a number:</label>
            <input type="number" id="limit" name="limit" min="2" required>
            <button type="submit">Generate Primes</button>
        </form>
        {% if primes %}
        <div class="result">
            <h3>Prime numbers up to {{ limit }}:</h3>
            <p>{{ primes }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    limit = request.args.get('limit', type=int)
    primes = None
    if limit:
        if limit < 2:
            return "Please enter a number greater than or equal to 2"
        primes = get_primes_up_to(limit)
    return render_template_string(HTML_TEMPLATE, primes=primes, limit=limit)

@app.route('/about')
def about():
    return 'About'

@app.route('/primes')
def primes():
    try:
        limit = request.args.get('limit', type=int)
        if limit is None:
            return jsonify({'error': 'Please provide a limit parameter'}), 400
        if limit < 2:
            return jsonify({'error': 'Limit must be greater than or equal to 2'}), 400
        
        prime_numbers = get_primes_up_to(limit)
        return jsonify({
            'limit': limit,
            'primes': prime_numbers
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)