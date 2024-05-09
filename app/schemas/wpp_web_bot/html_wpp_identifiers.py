from enum import Enum


class HtmlWppXpaths(str, Enum):
    QR_CANVAS_XPATH = '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas'
    QR_CANVAS_OR_SIDE_PANEL_XPATH = ('//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas | '
                                     '//div[@id="side"]')
    NOT_FOUND_USER_NOTIFICATION_XPATH = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div'
    CLOCK_MESSAGE_STATE_XPATH = '//*[@id="main"]//*[@data-icon="msg-time"]'
    CLOCK_OR_CHECK_OR_DOUBLE_CHECK_MESSAGE_STATE_XPATH = ('//*[@id="main"]//*[@data-icon="msg-time"] | '
                                                          '//*[@id="main"]//*[@data-icon="msg-dblcheck"] | '
                                                          '//*[@id="main"]//*[@data-icon="msg-check"]')
    IMG_INPUT_BUTTON_XPATH = ('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/span/div/ul/div/div[2]/li/'
                              'div/input')
    VID_INPUT_BUTTON_XPATH = ('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/span/div/ul/div/div[2]/li/'
                              'div/input')
    DOC_INPUT_BUTTON_XPATH = ('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/span/div/ul/div/div[1]/li/'
                              'div/input')
    FILE_CANVA_XPATH = ('//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[2]/div/'
                        'div/div')
    IMG_CAPTION_XPATH = ('//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/'
                         'div/div[2]/div[1]/div[1]')
    DOC_CAPTION_XPATH = ('//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/'
                         'div[2]/div[1]/div[1]')
    VID_CAPTION_XPATH = ('//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/'
                         'div[2]/div[1]/div[1]')
    SEND_BUTTON_XPATH = '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div'

    MESSAGES_CONTAINER = '//*[@id="main"]/div[3]/div/div[2]'


class JavaScriptWppScripts(str, Enum):
    GET_QR_IMG = 'return arguments[0].toDataURL("image/png").substring(22);'
