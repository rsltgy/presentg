from flask.blueprints import Blueprint
from flask.templating import render_template
from flask import current_app, request
from passlib.apps import custom_app_context as pwd_context
from passlib import hash
import bcrypt
import random
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ctypes.wintypes import BOOLEAN
from sqlalchemy.sql.sqltypes import BINARY
from User import User
from datetime import datetime
from flask_login.utils import current_user
from datetime import datetime
from Group import Group
from Group_member import Group_member
from Group_member import get_group_members_using_group_id
from flask_login import login_required
from Group import get_group_using_group_id
from User import get_username
from File import get_file_names_using_group_id, get_file_using_file_id
import psycopg2
import io
from flask import make_response

Base = declarative_base()    


engine = create_engine('postgresql://postgres:123456@localhost:5432/test')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

''' 
# Insert a Person in the person table
new_person = Users(username='new person',email='ss',name='aa',surname='aa',password='testtt',salt='aa',gender = 'M')
session.add(new_person)
session.commit()
'''

groups  = Blueprint('groups',__name__)
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


@groups.route('/create_new_group', methods=['GET', 'POST'])
def create_group_form_modal():
    if request.method == 'GET':
        return render_template("sign_up.html")
    else:
        group_name = request.form['create_group_name']
        group_id = ""
        for i in range(16):
            group_id = group_id + (random.choice(ALPHABET))   
        creator_email = current_user.get_email()
        creation_date = datetime.now()
        new_group = Group(group_id =group_id, group_name = group_name,creator_email=creator_email,creation_date=creation_date)
        session.add(new_group)
        session.commit()
        new_group_member = Group_member(group_id =group_id,user_email = current_user.get_email(),membership_date=creation_date)
        session.add(new_group_member)                    
        session.commit()
        return render_template("home.html")

    
@groups.route('/<string:group_id>')
@login_required
def groups_page(group_id):
        group = get_group_using_group_id(group_id)
        group_members = get_group_members_using_group_id(group_id)
        members = []
        scroll = False
        for mem in group_members:
            members.append(get_username(mem.user_email))
        if(len(members)>10):
            scroll = True; 
        files = get_file_names_using_group_id(group_id)
        return render_template("groups.html",group = group,group_members=members,files=files)    


@groups.route('/<string:group_id>/<string:file_id>')
@login_required
def groups_page_file(group_id,file_id):
        group = get_group_using_group_id(group_id)
        group_members = get_group_members_using_group_id(group_id)
        members = []
        scroll = False
        for mem in group_members:
            members.append(get_username(mem.user_email))
        if(len(members)>10):
            scroll = True; 
        files = get_file_names_using_group_id(group_id)        
        file = get_file_using_file_id(file_id) 
        response = make_response(file.file)
        response.headers['Content-Type'] = 'application/pdf'
        print("o")
        return response
    
    
@groups.route('/<string:group_id>/add_new_member', methods=['GET', 'POST'])
@login_required
def add_new_member_form_modal(group_id):
    if request.method == 'GET':
        return render_template("sign_up.html")
    else:
        user_email = request.form['add_new_member']
        creator_email = current_user.get_email()
        creation_date = datetime.now()
        new_group_member = Group_member(group_id =group_id,user_email = user_email,membership_date=creation_date)
        session.add(new_group_member)                    
        session.commit()
        return render_template("home.html")   
