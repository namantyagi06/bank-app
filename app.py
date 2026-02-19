from flask import Flask, render_template, request

app = Flask(__name__)

accounts = {}

class Account:
    def __init__(self, acc, name, balance, kyc):
        self.accountNo = acc
        self.holderName = name
        self.balance = balance
        self.kycVerified = kyc

@app.route("/")
def home():
    return render_template("index.html", accounts=accounts)

@app.route("/create", methods=["POST"])
def create():
    acc = request.form["acc"]
    name = request.form["name"]
    bal = float(request.form["bal"])
    kyc = request.form.get("kyc")

    accounts[acc] = Account(acc,name,bal,True if kyc else False)
    return "Account Created"

@app.route("/transfer", methods=["POST"])
def transfer():
    sender = request.form["sender"]
    receiver = request.form["receiver"]
    amount = float(request.form["amount"])

    if not accounts[sender].kycVerified:
        return "Sender KYC not verified"

    if accounts[sender].balance < amount:
        return "Insufficient Balance"

    accounts[sender].balance -= amount
    accounts[receiver].balance += amount

    return "Transfer Successful"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


