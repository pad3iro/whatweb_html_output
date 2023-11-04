#!/usr/bin/env python

import json, sys

def create_html_report(jsonFile):

    jsonInput = json.load(open(jsonFile))

    IDENT_4 = '\t\t\t\t'
    IDENT_5 = '\t\t\t\t\t'

    html = """<html>
    <head>
        <title> Whatweb Report</title>
    </head>
    <body>
        <div id="all" style="width: 800px; margin: auto; text-align: center;">
            <div id="top">
                <br>
                <h1>Whatweb scan results </h1>
            </div>
            <div id="content" style="margin: auto;">\n"""

    request_config_processed = False
    for element in jsonInput:
        target = element["target"]
        http_status = str(element["http_status"])

        request_config = element["request_config"]
        if not request_config_processed and len(request_config) > 0:
            html += IDENT_4 + '<table style="width:100%; background-color: lightsteelblue; padding-left: 20px; border-collapse: separate; border-spacing: 1em; border: 1px solid black; border-radius: 10px;">\n'
            html += IDENT_5 + '<tr><td style="min-width:300px;"><h3>Request Config</h4></td><td style="min-width:480px;"></td></tr>\n'
            for config in request_config:
                config_name = config
                for config_key in request_config[config]:
                    value = "%s:%s"%(config_key,request_config[config][config_key]) 
                    html += IDENT_5 + '<tr><td><b>%s</b></td><td>%s</td></tr>\n'%(config_name,value)
                    config_name = ''

            html += IDENT_4 + '</table>\n'
            request_config_processed = True
        
        plugins = element["plugins"]

        
        html += IDENT_4 + '<br><br>\n'
        html += IDENT_4 + '<table style="width:100%; background-color: lightskyblue; padding-left: 20px; border-collapse: separate; border-spacing: 1em; border: 1px solid black; border-radius: 10px;">\n'
        html += IDENT_5 + '<tr><td style="min-width:300px;"><h3>Results</h4></td><td style="min-width:480px;"></td></tr>\n'
        html += IDENT_5 + '<tr><td><b>Target</b></td><td><b>%s</b></td></tr>\n'%(target)
        html += IDENT_5 + '<tr><td><b>HTTP Status</b></td><td>[ %s ]</td></tr>\n'%(http_status)

        for plugin in plugins:
            if plugin == "Country": #special case where there is the 2 letter code
                value = [ plugins[plugin]["string"][0] + "["+ plugins[plugin]["module"][0] +"]" ]
            elif plugin == "UncommonHeaders": #special case where the headers come separated by comma instead of in a list
                value = plugins[plugin]["string"][0].split(",")
            else:
                if "string" in plugins[plugin]:
                    value = plugins[plugin]["string"]
                elif "version" in plugins[plugin]:
                    value = plugins[plugin]["version"]
                else:
                    value = [""]

            for textvalue in value:
                html += IDENT_5 + '<tr><td><b>%s</b></td><td>%s</td></tr>\n'%(plugin,textvalue)
                plugin = ''


        html += IDENT_4 + '</table>\n'

    html += """            </div>
        </div>
    </body>
</html>"""

    htmlFilename = jsonFile.split(".json")[0]+".html"
    with open(htmlFilename, 'w', encoding='utf-8') as output_file:
        output_file.write(html)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please provide a json file as input")
        sys.exit()

    jsonFile = sys.argv[1]

    try:
        create_html_report(jsonFile)
    except Exception as e:
        print("Failed to generate html from the json input file due to: " + str(e))
        print("Please provide a valid json whatweb output file [ --log-json=json_file.json ]")