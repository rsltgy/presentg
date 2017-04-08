from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime
from Group import get_group2
from Group import Group
from Group_member import get_groups_using_user_email
from Group import get_group_using_group_id
from File import get_file_names_using_group_id

home = Blueprint('home',__name__)

@home.route('/')
def home_page():
    if current_user.is_authenticated:
        gr = get_groups_using_user_email(current_user.get_email())      
        gr_names = []
        scroll = False;
        for g in gr:
            gr_names.append(get_group_using_group_id(g.group_id))
        if(len(gr_names)>10):
            scroll = True;   
        return render_template("home.html",groups=gr_names,scroll = scroll)
    else:
        return render_template("home.html")



@home.route('/test/<string:group_id>/<string:file_id>')
@login_required
def test_page(group_id,file_id):
    files = get_file_names_using_group_id('hWNhtlCYFzwEntgf')
    for k in files:
        print(k  + " " + files[k])
    
    return render_template("test.html",group_id=group_id,file_id=file_id)
