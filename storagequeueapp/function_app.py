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
