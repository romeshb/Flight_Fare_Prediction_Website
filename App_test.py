from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", method = ["Get"]) #app.route(rule, options)
def HomePage():
    return render_template("index.html")

@app.route("/price", method = ["Post"]) # will be called when 'Get Price' is clicked
def prediction():
    if request.method == "Post" :

        # We'll do the data transformation here same as it was feed to the model while training
        pred = model.predict()

        output = pred
        range = [pred Interval()] # refer this https://towardsdatascience.com/prediction-intervals-in-linear-regression-2ea14d419981

        return render_template('index.html', text1 ="Your Flight Prices will be Rs.{}".format(output),
                               text2 = 'Most likely in the range of Rs. {}'.format(output),



                               )

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
