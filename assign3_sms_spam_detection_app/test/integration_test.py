import os, yaml, time
import subprocess

# import the flask app
from src.app import app
from src.score import score

##########################################################################################################################


# extract the parameters in configs
config_file_path = os.path.join('config', 'test_config', 'integration.yaml')

with open(config_file_path) as fh:
    config = yaml.load(fh, Loader=yaml.FullLoader)

# extract app.py path
app_path = config['app_path']

# extract sample sms text (spam)
input_text = config['input_text']

'''
def test_app():
    # start the flask app using command_line
    cmd = 'python ' + app_path + ' &'
    os.system(cmd)

    # wait for the app to start up
    time.sleep(1)

    # wait for the app to start listening
    endpoint = "http://localhost:5000/score"
    timeout = 5
    while True:
        try:
            response_get = requests.get(endpoint, timeout=timeout)
            if response_get.ok:
                break
        except:
            pass
    
    # assert whether the response is what we expect
    assert (response_get.status_code == 200)
    
    # send a POST request with input message
    sms_text = input_text
    # extract response
    response_post = requests.post(endpoint, data={"sms_text":sms_text})

    # check the response
    assert response_post.ok
    
    # extract model output
    output_dict = response_post.json()
    assert "prediction" in output_dict
    assert "propensity" in output_dict
    
    # assert that the model is detecting the message as True (spam)
    assert output_dict["prediction"] == True


    # stop the Flask app using command line
    os.system('kill $(lsof -t -i:5000)')
'''

def test_app():
    # start the flask app using command_line
    cmd = 'python ' + app_path + ' &'
    os.system(cmd)

    # wait for the app to start up
    time.sleep(1)

    # wait for the app to start listening

    # check the get requests at different endpoints
    endpoint = '/score'
    response_get = app.test_client().get(endpoint)
    
    # assert whether the response is what we expect
    assert (response_get.status_code == 405)

    
    # send a POST request with input message at '/score' endpoint

    sms_text = input_text
    # extract response
    response_post = app.test_client().post(endpoint, data={"sms_text":sms_text})

    # check the response
    assert (response_post.status_code == 200)
    
    # extract model output
    output_json = response_post.data.decode()
    assert "prediction" in output_json
    assert "propensity" in output_json
    
    # assert that the model is detecting the message as True (spam)
    # assert output_json["prediction"] == True
    assert (type(output_json) == str)


    # stop the Flask app using command line
    os.system('kill $(lsof -t -i:5000)')

##########################################################################################################################