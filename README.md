# taskweb

Need to save 

```
[Unit]
Description=Minimal Taskwarrior Web Server
After=network.target

[Service]
User=harry
WorkingDirectory=/home/harry/taskweb
# Activate venv and run CLI
ExecStart=/bin/bash -c 'source /home/harry/taskweb/envtaskserve/      bin/activate && exec taskserve'
Restart=always
Environment=PATH=/home/harry/taskweb/envtaskserve/bin:/usr/bin:/      bin

[Install]
WantedBy=multi-user.target
```

in 

`/etc/systemd/system/todo.service`

and run 

```
sudo systemctl daemon-reload
sudo systemctl enable todo.service
sudo systemctl start todo.service
```

on initial set up or 

```
sudo systemctl restart todo.service
```

when I make changes.

## Licence

Released under a non-commercial, MIT-style license. See LICENSE for details.
