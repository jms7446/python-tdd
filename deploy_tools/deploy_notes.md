Deploy a new version of source
===============================

## Using fabric

    $ git push
    $ source venv/bin/activate
    $ cd deploy_tools
    $ fab deploy:host=user@superlists-staging.myhome.com
    
    # restart gunicorn in server
    server:$ sudo systemctl daemon-reload
    server:$ sudo systemctl restart gunicorn-superlists-staging.myhome.com
    
    # run FT
    $ STAGING_SERVER=superlists-staging.myhome.com python -m pytest ../functional_tests
    
    # for viewing log
    $ sudo journalctl -f -u gunicorn-superlists-staging.myhome.com