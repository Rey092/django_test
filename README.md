# homework5
homework5 - django

make collect-static - сработает collectstatic
make gunicorn-run - запустится гуникорн(wsgi) сервер

-------------------------------------------------------
# mysite_nginx.conf

    # the upstream component nginx needs to connect to
    upstream django {
        # server unix:///path/to/your/mysite/mysite.sock; # SOCKET
        server 127.0.0.1:8001; # TCP/IP
    }
    
    # configuration of the server
    server {
        # the port site is served on
        listen      8000;
        # the domain name it serve for
        server_name 127.0.0.1; #
        charset     utf-8;
    
        # max upload size
        client_max_body_size 75M;
    
        location /static {
            root /home/roman/GitHub/django_test/static_content;
        }

        location / {
            proxy_pass  http://django;
        }
    }

-------------------------------------------------------