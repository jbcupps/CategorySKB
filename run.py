from skb.app import app
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Flask application.")
    parser.add_argument('--host', default='127.0.0.1', help='The host to bind to.')
    args = parser.parse_args()

    app.run(debug=True, host=args.host) 