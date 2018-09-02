from io import BytesIO

import lxml.html

from seleniumrequests import Chrome

from vgrabber.model import Subject
from vgrabber.model.files import InMemoryFile
from .actionexecutor import ActionExecutor


class TestDownloaderActionExecutor(ActionExecutor):
    __test_css = '''
    /*! CSS Used from: https://vzdelavanie.uniza.sk/moodle3/theme/styles.php/clean/1535358951/all */
    .que.multichoice .answer div.r0,.que.multichoice .answer div.r1{padding:.3em 0 .3em 25px;text-indent:-25px;}
    .que.multichoice .answer div.r0 label,.que.multichoice .answer div.r1 label{text-indent:0;}
    .que.multichoice .answer div.r0 input,.que.multichoice .answer div.r1 input{margin:0 5px;padding:0;width:15px;}
    #page-mod-quiz-review .submitbtns{clear:left;text-align:left;padding-top:1.5em;}
    #page-mod-quiz-review .submitbtns .mod_quiz-next-nav{float:right;}
    table.quizreviewsummary{width:100%;}
    table.quizreviewsummary th.cell{padding:1px .5em 1px 1em;font-weight:700;text-align:right;width:10em;background:#f0f0f0;}
    table.quizreviewsummary td.cell{padding:1px 1em 1px .5em;text-align:left;background:#fafafa;}
    .pull-right{float:right;}
    .empty-region-side-post.used-region-side-pre #region-main.span8{width:74.46808511%;*width:74.41489362%;}
    img.userpicture{margin-right:5px;}
    img.icon{height:16px;vertical-align:text-bottom;width:16px;padding-right:6px;}
    img.iconsmall{height:12px;margin-right:3px;vertical-align:middle;width:12px;}
    #maincontent{display:block;height:1px;overflow:hidden;}
    .accesshide{position:absolute;left:-10000px;font-weight:400;font-size:1em;}
    img.iconsmall{margin:0;padding:.3em;}
    .que{clear:left;text-align:left;margin:0 auto 1.8em auto;}
    .que .info{float:left;width:7em;padding:.5em;margin-bottom:1.8em;background-color:#eee;border:1px solid #dcdcdc;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
    .que h3.no{margin:0;font-size:.8em;line-height:1;}
    .que span.qno{font-size:1.5em;font-weight:700;}
    .que .info>div{font-size:.8em;margin-top:.7em;}
    .que .info .editquestion img,.que .info .questionflag img{vertical-align:bottom;}
    .que .content{margin:0 0 0 8.5em;}
    .que .formulation,.que .outcome,.que .comment{padding:8px 35px 8px 14px;margin-bottom:20px;text-shadow:0 1px 0 rgba(255,255,255,.5);background-color:#fcf8e3;border:1px solid #fbeed5;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;color:#8a6d3b;}
    .que .formulation{background-color:#d9edf7;border-color:#bce8f1;color:#3a87ad;color:#333;}
    .que .comment{background-color:#dff0d8;border-color:#d6e9c6;color:#468847;}
    .que .history{min-height:20px;padding:19px;margin-bottom:20px;background-color:#f5f5f5;border:1px solid #e3e3e3;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-webkit-box-shadow:inset 0 1px 1px rgba(0,0,0,.05);-moz-box-shadow:inset 0 1px 1px rgba(0,0,0,.05);box-shadow:inset 0 1px 1px rgba(0,0,0,.05);border-color:#e3e3e3;}
    .que .ablock{margin:.7em 0 .3em 0;}
    .que .specificfeedback,.que .rightanswer,.que .feedback,.que p{margin:0 0 .5em;}
    .que .qtext{margin-bottom:1.5em;}
    .formulation .correct{background-color:#dff0d8;}
    .formulation .incorrect{background-color:#f2dede;}
    .que .comment,.que .commentlink,.que .history{margin-top:.5em;}
    .que .history table{width:100%;margin:0;}
    .que .history .current{font-weight:700;}
    .que label{display:inline;}
    .clearfix{*zoom:1;}
    .clearfix:before,.clearfix:after{display:table;content:"";line-height:0;}
    .clearfix:after{clear:both;}
    section{display:block;}
    a:focus{outline:thin dotted #333;outline:5px auto -webkit-focus-ring-color;outline-offset:-2px;}
    a:hover,a:active{outline:0;}
    img{vertical-align:middle;border:0;}
    input{margin:0;font-size:100%;vertical-align:middle;}
    input{*overflow:visible;line-height:normal;}
    input::-moz-focus-inner{padding:0;border:0;}
    label,input[type="radio"]{cursor:pointer;}
    a{color:#0070a8;text-decoration:none;}
    a:hover,a:focus{color:#003d5c;text-decoration:underline;}
    [class*="span"]{float:left;min-height:1px;margin-left:20px;}
    .span8{width:620px;}
    .row-fluid [class*="span"]{display:block;width:100%;min-height:30px;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;float:left;margin-left:2.12765957%;*margin-left:2.07446809%;}
    .row-fluid [class*="span"]:first-child{margin-left:0;}
    .row-fluid .span8{width:65.95744681%;*width:65.90425532%;}
    [class*="span"].pull-right,.row-fluid [class*="span"].pull-right{float:right;}
    p{margin:0 0 10px;}
    h3,h4{margin:10px 0;font-family:inherit;font-weight:700;line-height:20px;color:inherit;text-rendering:optimizelegibility;}
    h3{line-height:40px;}
    h3{font-size:24.5px;}
    h4{font-size:17.5px;}
    label,input{font-size:14px;font-weight:400;line-height:20px;}
    input{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;}
    label{display:block;margin-bottom:5px;}
    input{width:206px;}
    input[type="radio"]{margin:4px 0 0;*margin-top:0;margin-top:1px \9;line-height:normal;}
    input[type="radio"]{width:auto;}
    input[type="radio"]:focus{outline:thin dotted #333;outline:5px auto -webkit-focus-ring-color;outline-offset:-2px;}
    input:-moz-placeholder{color:#999;}
    input:-ms-input-placeholder{color:#999;}
    input::-webkit-input-placeholder{color:#999;}
    input{margin-left:0;}
    input[disabled]{cursor:not-allowed;background-color:#eee;}
    input[type="radio"][disabled]{background-color:transparent;}
    input:focus:invalid{color:#b94a48;border-color:#ee5f5b;}
    input:focus:invalid:focus{border-color:#e9322d;-webkit-box-shadow:0 0 6px #f8b9b7;-moz-box-shadow:0 0 6px #f8b9b7;box-shadow:0 0 6px #f8b9b7;}
    table{max-width:100%;background-color:transparent;border-collapse:collapse;border-spacing:0;}
    .pull-right{float:right;}
    h3{font-size:24px;}
    h4{font-size:20px;}
    input[type="radio"]+label{display:inline;padding-left:.2em;}
    input[type="radio"]{margin-top:-4px;margin-right:7px;}
    .generaltable{width:100%;margin-bottom:20px;}
    .generaltable th,.generaltable td{padding:8px;line-height:20px;text-align:left;vertical-align:top;border-top:1px solid #ddd;}
    .generaltable th{font-weight:700;}
    .generaltable thead th{vertical-align:bottom;}
    .generaltable thead:first-child tr:first-child th{border-top:0;}
    .generaltable tbody>tr:nth-child(odd)>td,.generaltable tbody>tr:nth-child(odd)>th{background-color:#f9f9f9;}
    .generaltable tbody tr:hover>td,.generaltable tbody tr:hover>th{background-color:#f5f5f5;}
    .m-l-1{margin-left:14px!important;}
    '''

    def __init__(self, state):
        super().__init__(state)
        self.__state = state

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        model.clear_test_files()

        for test in model.tests:
            browser.get('https://vzdelavanie.uniza.sk/moodle3/mod/quiz/report.php?id={0}'.format(test.moodle_id))

            while True:
                for review_link in browser.find_elements_by_css_selector('a.reviewlink'):
                    email_td = review_link.find_element_by_xpath('./ancestor::tr/td[4]')
                    email = email_td.text

                    student = model.get_student_by_email(email)

                    review_href = review_link.get_attribute('href')
                    review_content = browser.request('GET', review_href).content
                    review_html = lxml.html.parse(BytesIO(review_content))
                    review_element = review_html.xpath('//div[@role="main"]')

                    html_element = lxml.html.Element('html')

                    head_element = lxml.html.Element('head')
                    html_element.append(head_element)
                    meta_element = lxml.html.Element('meta', charset='UTF-8')
                    head_element.append(meta_element)
                    style_element = lxml.html.Element('style')
                    style_element.text = self.__test_css
                    head_element.append(style_element)

                    body_element = lxml.html.Element('body')
                    html_element.append(body_element)
                    body_element.append(review_element[0])
                    serialized_text = lxml.html.tostring(html_element)

                    student.add_test_file(test, InMemoryFile('test.html', serialized_text))

                if not any(browser.find_elements_by_link_text("Ďalší")):
                    break
                browser.find_element_by_link_text("Ďalší").click()
