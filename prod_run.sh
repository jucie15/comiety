# 위치 : /home/ubuntu/myproj/prod_run.sh

export BIN_PATH=/home/ubuntu/venv/bin
export DJANGO_HOME=/home/ubuntu/gitComiety/comiety
export DJANGO_SETTINGS_MODULE=comiety.settings.prod

$BIN_PATH/uwsgi --master \
    --die-on-term \
    --processes 1 \
    --enable-threads \
    --socket :8080 \
    --stats  :8081 \
    --harakiri 30 \
    --harakiri-verbose \
    --reload-on-rss 200 \
    --post-buffering-bufsize 8192 \
    --logto /var/log/comiety/uwsgi.log \
    --pythonpath $DJANGO_HOME \
    --wsgi-file $DJANGO_HOME/comiety/wsgi.py \
    --uid www-data --gid www-data \
    --logformat '%(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" %(status) %(size) "%(referer)" "%(uagent)"'
