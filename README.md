# Whatweb HTML Output

This is just a simple html report generator from the json log from whatweb output.

To generate the report run:

    echo "" > whatweb_out.json #to clear previous runs
    whatweb <arguments> --log-json=whatweb_out.json
    python whatweb_json_to_html.py whatweb_out.json

HTML file will be created in <b>./whatweb_out.html</b>
