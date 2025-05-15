from flask import Flask, jsonify, request, render_template
import time
import json
import os

app = Flask(__name__, template_folder='../templates')

CHUNK_TIME_LIMIT = 2  # seconds
PRIMES_FILE = 'primes.json'

def load_primes():
    if os.path.exists(PRIMES_FILE):
        with open(PRIMES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_primes(limit, primes):
    stored_primes = load_primes()
    stored_primes[str(limit)] = primes
    with open(PRIMES_FILE, 'w') as f:
        json.dump(stored_primes, f)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_primes_up_to(n, start_from=2):
    primes = []
    start_time = time.time()
    
    stored_primes = load_primes()
    str_n = str(n)
    
    # Check if we already have the full result
    if str_n in stored_primes:
        return stored_primes[str_n], False, n
    
    # Find the largest precomputed result we can use
    largest_precomputed = 0
    precomputed_primes = []
    for limit in stored_primes:
        limit_n = int(limit)
        if limit_n < n and limit_n > largest_precomputed:
            largest_precomputed = limit_n
            precomputed_primes = stored_primes[limit]
    
    if largest_precomputed > start_from:
        primes = [p for p in precomputed_primes if p >= start_from]
        start_from = max(precomputed_primes) + 1
    
    current = start_from
    while current <= n:
        if time.time() - start_time > CHUNK_TIME_LIMIT:
            # Time limit reached, save partial results
            all_primes = primes.copy()
            save_primes(current - 1, all_primes)
            return all_primes, True, current
        
        if is_prime(current):
            primes.append(current)
        current += 1
    
    # Calculation completed
    save_primes(n, primes)
    return primes, False, n

@app.route('/')
def home():
    limit = request.args.get('limit', type=int)
    start_from = request.args.get('start_from', type=int, default=2)
    primes = None
    next_start = None
    
    if limit:
        if limit < 2:
            return "Please enter a number greater than or equal to 2"
        primes, has_more, next_start = get_primes_up_to(limit, start_from)
    
    return render_template('index.html', 
                         primes=primes, 
                         limit=limit, 
                         has_more=has_more if primes else False,
                         next_start=next_start if primes else None)

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