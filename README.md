# Service Now Ticket Creator

Script to automate the ticket creation on Service Now

## Instalation
    git clone http://github.com/wagnervaz/sn-creator.git
    cd sn-creator
    pip install -r requirements.txt
    cp sn-creator.cfg.sample sn-creator.cfg

## Configuration
Change the sn-creator.cfg file and put the correct values:

    username: Your Service Now username
    password: Your Service Now password
    requestor_group = The name of requestor group
    assigned_group = The name of the assignee group

## Utilization
    python sn-creator.py --title="Ticket Title" --description="Ticket Description"

## Todo
* List tickets you've opened
