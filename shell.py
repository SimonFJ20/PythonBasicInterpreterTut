import basic

while True:
    
    try:
        try:
            text = input('❱❱❱ ')
        except UnicodeEncodeError:
            text = input('>>> ').replace('\n', '', -1)
    except KeyboardInterrupt:
        exit()

    result, error = basic.run('<stdin>', text)

    if error: print(error.as_string())
    elif result: print(repr(result))
