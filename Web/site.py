from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    #if request.method == "POST":
        # cmd = request.POST.get('submit')
        # cmd = request.form['submit']
        # как передать команду orangepi?
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
