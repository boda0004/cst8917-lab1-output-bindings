# Azure Function with Storage Queue Output Binding

This project demonstrates how to create and deploy an Azure Function App that sends messages to an Azure Storage Queue using Output Binding.

---

## Prerequisites

Make sure you have the following tools installed:

- Python 3.11
- Azure CLI
- Azure Functions Core Tools
- Visual Studio Code
- An active Azure Subscription

---

## Steps to Complete the Lab (Chronological Order)

### 1. Create a Resource Group (if not already created)

	az group create --name CST8917Lab01 --location "canadacentral"


### 2. Create a Storage Account

	az storage account create --name cst8917lab01 --location canadacentral --resource-group CST8917Lab01 --sku Standard_LRS


### 3. Create a Local Azure Function App

	az functionapp create --resource-group CST8917Lab01 --consumption-plan-location canadacentral --runtime python --runtime-version 3.11 --functions-version 4 --name cst8917-func-queueapp --storage-account cst8917lab01 --os-type Linux


### 4. Create a New Function inside a folder

	func init storagequeueapp --python


### 5. Create a New Function

	cd storagequeueapp
	func new --name SendMessageFunction --template "HTTP trigger" --authlevel "anonymous"

	
### 6. Modify `function_app.py`

	python
		import azure.functions as func
		import logging
		
		app = func.FunctionApp()
		
		@app.function_name(name="SendMessageFunction")
		@app.route(route="SendMessageFunction")  # You can change 'SendMessageFunction' to anything like 'send'
		@app.queue_output(arg_name="msg", queue_name="myqueue-items", connection="AzureWebJobsStorage")
		def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
		    name = req.params.get('name')
		
		    if not name:
		        return func.HttpResponse(
		            "Please pass a name in the query string.",
		            status_code=400
		        )
		
		    message = f"Hello {name}, welcome to Azure Functions Queue!"
		    msg.set(message)
		
		    return func.HttpResponse(f"Message sent to queue: {message}")


### 7. Test Locally

	func start

	Open browser or use Postman to call:

	http://localhost:7071/api/SendMessageFunction


### 8. Deploy the Function to Azure

	func azure functionapp publish cst8917-func-queueapp


---

## Final Result
Your function app is deployed and can be triggered via:

	https://cst8917-func-queueapp.azurewebsites.net/api/sendmessagefunction


Sending a POST request with JSON will add a message to your Azure Storage Queue `student-queue`.

---

## Notes
- Always verify the storage queue exists in the Azure Portal.
- You can view the queue messages using Azure Storage Explorer.
- Monitor logs and usage from the Azure Portal under **Function App > Monitoring**.

---




# Azure Function with SQL Output Binding

In this Task we'll see how to create and deploy an Azure Function App that inserts data into an Azure SQL Database using SQL Output Binding.

---

## Steps to Complete the Lab (Chronological Order)

### 1. Create an Azure SQL Server

	az sql server create --name cst8917sqlserver --resource-group CST8917Lab01 --location canadacentral --admin-user yourusername --admin-password yourpassword


### 2. Create an Azure SQL Database

	az sql db create --resource-group CST8917Lab01 --server cst8917sqlserver --name cst8917db --service-objective S0


### 3. Set Server Firewall Rule to Allow Azure Services

	az sql server firewall-rule create --resource-group CST8917Lab01 --server cst8917sqlserver --name AllowAzureServices --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0


### 4. Create the Students Table

	Use Azure Data Studio or SQL query tool:
	sql
	CREATE TABLE Students (
	    name NVARCHAR(50),
	    grade INT
	);


### 5. Create a Local Azure Function App
	
func init sqlbindingapp --python


### 6. Create a New Function

	cd sqlbindingapp
	func new --name AddStudentFunction --template "HTTP trigger" --authlevel "anonymous"


### 7. Modify `function_app.py`

	python
		import azure.functions as func
		import logging
		
		app = func.FunctionApp()
		
		@app.function_name(name="AddStudentFunction")
		@app.route(route="addstudent", methods=["POST"])
		@app.sql_output(
		    arg_name="output",                      # This MUST match the function parameter name below
		    command_text="dbo.Students",            # Your table name
		    connection_string_setting="SqlConnectionString"  # This is just a key name
		  # This must point to your key in local.settings.json
		)
		def AddStudentFunction(req: func.HttpRequest, output: func.Out[func.SqlRow]) -> func.HttpResponse:
		    logging.info('Processing request to add student to SQL DB.')
		
		    try:
		        req_body = req.get_json()
		        name = req_body.get("name")
		        grade = int(req_body.get("grade"))
		    except Exception as e:
		        logging.error(f"Invalid input or missing fields: {e}")
		        return func.HttpResponse("Invalid input", status_code=400)
		
		    # Create the SQL row
		    row = func.SqlRow.from_dict({
		        "name": name,
		        "grade": grade
		    })
		    output.set(row)
		
		    return func.HttpResponse("Student inserted successfully.")

### 8. Add SQL Connection String to `local.settings.json`

	json
	{
	  "IsEncrypted": false,
	  "Values": {
	    "FUNCTIONS_WORKER_RUNTIME": "python",
	    "SqlConnectionString": "Enter Your connection string"
	  }
	}



### 9. Test Locally

	func start

	Test using curl or Postman:

	curl -X POST http://localhost:7071/api/addstudent -H "Content-Type: application/json" -d "{"name": "Alice", "grade": 90}"


### 10. Create Azure Function App

	az functionapp create --resource-group CST8917Lab01 --consumption-plan-location canadacentral --runtime python --runtime-version 3.11 --functions-version 4 --name cst8917-func-sqlapp --storage-account cst8917lab01 --os-type Linux


### 12. Publish to Azure

	func azure functionapp publish cst8917-func-sqlapp


---

## ✅ Final Result
	Function app is live at:

	https://cst8917-func-sqlapp.azurewebsites.net/api/addstudent


---

## Notes
- Ensure the Azure SQL DB firewall allows your IP or Azure Services.
- Always use secure passwords and store them using Key Vault in production.

---

✅ Lab Completed Successfully!

# Demo Video
https://youtu.be/pX4oZxZoO2w
