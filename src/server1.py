from flask import Flask
import requests
import pybreaker
import logging
from datetime import datetime, timedelta

class Glistener(pybreaker.CircuitBreakerListener):
    "Listener used by circuit breakers that execute database operations."

    def state_change(self, cb, old_state, new_state):
        msg = "State Change: CB: {0}, New State: {1}".format(cb.name, new_state)
        logging.basicConfig(level=logging.INFO)
        logging.info(msg)

    def failure(self, cb, exc):
        "Called when a function invocation raises a system error."
        pass

    def success(self, cb):
        "Called when a function invocation succeeds."
        pass


app = Flask(__name__)
db_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=5, err_threshold=0.6)
opened_at = datetime.utcnow()
timeout = timedelta(seconds=5)
@db_breaker
@app.route('/')
def hello_word():
    return "Total : {0}\nFail : {1}\nSuccess : {2}\nState : {3}"\
        .format(db_breaker._state_storage._total_calls_counter, db_breaker._state_storage.fail_counter,
                    db_breaker._state_storage.success_counter, db_breaker.current_state)

@db_breaker
@app.route('/err')
def err():
    raise NotImplementedError()

@db_breaker
def test():
    # err()
    response = requests.get('http://127.0.0.1:5001')
    data = response.json()
    print data


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8082)

