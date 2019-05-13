from Interpreter.translation import Trans

def interpreter(file_name):
    kcc = Trans(file_name)
    kcc.run()