"""
++ In this application we shall define a bank.

++ The Application will simply work by accepting (POST) a call with name + ID parameters that shall update a dictionary (list_of_names)(in memory, not doing sqlite etc).

++ The Application can also be called (GET) with the ID & if ID exists in the DB (list_of_names) name etc info is returned.
"""

#Importing Flask & Flask Restplus
from flask import Flask, request
from flask_restplus import Api, Resource, fields

flask_app = Flask(__name__)
app = Api(app = flask_app, version = "1.0", title = "Bank Account Recorder", description = "Manage names of bank Accounts")

# Note the below will be the root of the URL http://localhost:5000/bank/{id} (GET, POST etc)
bank_space = app.namespace("bank", description="Bank Namespace")

#In the MVC, the below is defining our Model aka the database.
bank_model_dict = {"name": fields.String(required = True, description="Name of the Account", help="Name cannot be blank" ) }
model = app.model("Bank Model", bank_model_dict)

#Dictionary which will act as in-memory DB
list_of_names = {}

#The root expects that a id (Integer) is sent.
@bank_space.route("/<int:id>")
class BankClass(Resource):
    #--------------------------------------------------------------------------------------------------
    #Using app.doc for documenting Swagger.
    #response key shows what status codes are sent back.
    #params defines the expected input.
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },params={'id': 'Please specify the Bank Account ID' })
    def get(self, id):
        try:
            name = list_of_names[id]
            return {"status": "Person info located", "name": list_of_names[id]}
        except KeyError as e:
            bank_space.abort(500, e.__doc__, status = "Could not retrieve Account (ID) information", statusCode = "500")
        except Exception as e:
            bank_space.abort(400, e.__doc__, status = "Invalid Argument. Could not retrieve Account information", statusCode = "400")
        """
        Test # 1
        -----------------
        curl -X GET "http://127.0.0.1:5000/bank/1111" -H  "accept: application/json"

        Response for a call that exists (200)
            {
            "status": "Person info located",
            "name": "Upi"
            }
        Test # 2
        ----------------
        curl -X GET "http://127.0.0.1:5000/bank/2222" -H  "accept: application/json"

        Response for a call that does not exists yet (500)
            {
            "status": "Could not retrieve Account (ID) information",
            "statusCode": "500",
            "message": "Mapping key not found."
            }
        """

    #--------------------------------------------------------------------------------------------------
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },params={ 'id': 'Specify the Name of the person' })
    @app.expect(model)#think of this as the body/Database what columns you want to update. Model was defined previously.
    def post(self, id):
        try:
            if not request.json["name"]:
                raise Exception("Passed Name string is empty.")
            else:
                list_of_names[id] = request.json["name"]
                return {"status": "Person info Added", "name": list_of_names[id]}
        except KeyError as e:
            bank_space.abort(500, e.__doc__, status = "Could not Save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not Save information", statusCode = "400")
    """
    Test # 1
    -------------------
    curl -X POST "http://127.0.0.1:5000/bank/1111" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"name\": \"Upi\"}"

    Response 200:
        {
        "status": "Person info Added",
        "name": "Upi"
        }

    """
#----------------------------------------------------------------------------------------------------------------------------
"""
Running the steps in a virtual environment
--------------------------------------------
cisco@USUJLANA-41PCQ:/mnt/c/Users/usujlana/Desktop/TFTP/FLASK$ python -m venv flask_restplus

cisco@USUJLANA-41PCQ:/mnt/c/Users/usujlana/Desktop/TFTP/FLASK$ cd flask_restplus/

cisco@USUJLANA-41PCQ:/mnt/c/Users/usujlana/Desktop/TFTP/FLASK/flask_restplus$ source bin/activate

(flask_restplus) cisco@USUJLANA-41PCQ:/mnt/c/Users/usujlana/Desktop/TFTP/FLASK/flask_restplus$ pip install flask

(flask_restplus) cisco@USUJLANA-41PCQ:/mnt/c/Users/usujlana/Desktop/TFTP/FLASK/flask_restplus$ pip install flask-restplus


(flask_restplus) cisco@USUJLANA-41PCQ:/mnt/c/Users/usujlana/Desktop/TFTP/FLASK/flask_restplus$ FLASK_APP=Flask_RestPlus_2.py flask run
 * Serving Flask app "Flask_RestPlus_2.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

"""