from flask import Flask, render_template, request
import chat_bot_functions as cbf
import variables as v
v.i = 0
v.intent = ""
v.output_type = -2
v.cust_id = None
v.check = False
v.c = 0
app = Flask(__name__)






@app.route("/")
def index():
    return render_template("index.html")

@app.before_request
def ini():
    if v.i == -1:
        v.i = 0
        return cbf.initial()

@app.route("/get")
def get_bot_response():

    if v.i == 0:
        userText = request.args.get('msg')
        intent = cbf.initial(userText)
        if intent is not None:
            v.intent=intent
    if v.check is False:
        if v.c == 0:
            output, v.c = cbf.check_veification()
            v.c=1
            return output
        else:
            v.cust_id, password = request.args.get('msg').split()
            v.cust_id = int(v.cust_id)
            v.check = cbf.check_veification(v.cust_id, password)
    if v.check:
        if v.intent == "accountbalance":
            if v.output_type == -2:
                output, v.output_type = cbf.account_balance()
                return output
            elif v.output_type == 0:
                account_type = request.args.get('msg')
                output, v.output_type = cbf.account_balance(v.cust_id, account_type)
                if v.output_type == 1:
                    v.i = -1
                    v.output_type = -2
                return output
        elif v.intent == "register":
            v.i = -1
            output=cbf.register()
            return output
        elif v.intent == "nonsesne":
            v.i = -1
            return cbf.nonsense()
        elif v.intent == "OK":
            v.i = -1
            v.intent = ""
            v.output_type = -2
            v.cust_id = None
            v.check = False
            return cbf.OK()
        elif v.intent == "Forgortpassword":
            v.i = -1
            return cbf.Forgortpassword()
        elif v.intent == "discoterms":
            v.i = -1
            return cbf.disco_terms()
        elif v.intent == "representative":
            v.i = -1
            return cbf.representative()
        elif v.intent == "FundTransfer":
            if v.output_type == -2:
                output, v.output_type = cbf.fund_transfer()
                return output
            else:
                bef_id, amount = request.args.get('msg')
                bef_id = int(bef_id)
                amount = int(amount)
                o = cbf.fund_transfer(v.cust_id, bef_id, amount)
                if o == -1:
                    return "Fund Transfer Sucesfull"
                elif o == 0:
                    v.i = -1
                    return "Insuffiecient Balance"
                elif o == 1:
                    v.output_type = -2
                    return "Benificiary doesn't exist"
    else:
        return "Invalid Credentials"



if __name__ == "__main__":
    app.run(debug=True)
