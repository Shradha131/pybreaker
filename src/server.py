from flask import Flask
import requests
import pybreaker
import logging


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
db_breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=5,
                                      listeners=[Glistener()]
                                      )


@db_breaker
@app.route('/')
def hello_word():
    print db_breaker.current_state
    return 'hello from server 1'


@app.route('/err')
@db_breaker
def test():
    print db_breaker.current_state
    raise NotImplementedError()


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8082)

