from datetime import datetime

def log_message(msg):
    # The output will be as the following example:
    #   [2020-05-15 17:08:53.508167] Unable to connect
    current_time = datetime.now()
    with open('./log.txt', 'a') as log:
        log.write("[{}] {}\n".format(str(current_time), str(msg)))