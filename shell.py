import basic

while True:
    
    try:
        try:
            text = input('❱❱❱ ')
        except UnicodeEncodeError:
            text = input('>>> ').replace('\n', '')
    except KeyboardInterrupt:
        exit()

    result, error = basic.run('<stdin>', text)

    if error: print(error.as_string())
    elif result: print(result)
