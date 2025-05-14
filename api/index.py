from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder='../templates')

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_primes_up_to(n):
    return [num for num in range(2, n + 1) if is_prime(num)]

@app.route('/')
def home():
    limit = request.args.get('limit', type=int)
    primes = None
    if limit:
        if limit < 2:
            return "Please enter a number greater than or equal to 2"
        primes = get_primes_up_to(limit)
    return render_template('index.html', primes=primes, limit=limit)

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