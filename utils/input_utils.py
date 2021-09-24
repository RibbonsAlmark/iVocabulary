def input_setting(hint_text, reply_type=str):
    reply = ''
    while reply == '':reply = input(hint_text)
    reply = reply_type(reply)
    return reply


def input_setting_with_default(hint_text, reply_type=str, default_value = None):
    while True:
        try:
            reply = input(hint_text)
            if reply != '':
                reply = reply_type(reply)
            else:
                reply = default_value
            break
        except Exception as e:
            # print(e)
            pass
    return reply


def input_yes_or_no(hint_text, negative_key='n', positive_key='y', default_reply=True):
    reply = ' '

    while not reply in [positive_key, negative_key, '']:reply = input(hint_text).lower()

    if reply == negative_key:
        reply = False
    elif reply == positive_key:
        reply = True
    else:
        reply = default_reply
        
    return reply