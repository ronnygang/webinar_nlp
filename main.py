from extract import main as extract
from analyze import main as analyze
import gc

def main(request):
    gc.collect()
    request_json = request.get_json()
    if not request_json or 'process' not in request_json:
        return 'Please, insert parameters'

    function = request_json['process']

    options = {
        'extract': extract,
        'analize': analyze      
    }

    process = options.get(function)
    if process:
        return process()
    return f"No valid process for {function}"

if __name__ == "__main__":
    response = main()
    print(response)
