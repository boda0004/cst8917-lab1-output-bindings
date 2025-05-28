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
