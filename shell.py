import basic

while True:
    
    try:
        try:
            text = input('❱❱❱ ')
        except UnicodeEncodeError:
            text = input('>>> ').replace('\n', '', -1)
    except KeyboardInterrupt:
        exit()

    if text.strip() == '': continue

    result, error = basic.run('<stdin>', text)

    if error: print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
