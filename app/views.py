from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, EnrollmentForm
from .models import User, Temp


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/hello')
@login_required
def hello():
    user = g.user
    return render_template('hello.html', user=user)


@app.route('/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('hello'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(nickname=form.user_nickname.data).first()
        if user is None:
            user = User(nickname=form.user_nickname.data)
            if form.child_user.data:
                user.role = 1
            else:
                user.role = 2
            db.session.add(user)
            db.session.commit()
        if user.related_user1:
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            return redirect(url_for('hello'))
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)
        return redirect(url_for('enrollment'))
    return render_template('login.html', form=form)


@app.route('/enrollment', methods=['GET', 'POST'])
@login_required
def enrollment():
    form = EnrollmentForm()
    if form.validate_on_submit():
        print('enrollment enter')
        user = Temp.query.filter_by(related_phone=form.my_phone.data).first()
        print(user)
        if user:
            print('find user')
            find_user = user.query.get(1)
            print(find_user.user_id, find_user.related_phone)
            partner = User.query.filter_by(id=find_user.user_id).first()
            print('find partner')
            if partner:
                partner.related_user1 = g.user.id
                g.user.related_user1 = partner.id
                g.user.phone = form.my_phone.data
                db.session.add(partner)
                db.session.add(g.user)
                db.session.commit()
            db.session.delete(find_user)
            print('ok?')
            db.session.commit()
            find_user = user.query.get(1)
            if find_user:
                partner = User.query.filter_by(id=find_user.user_id).first()
                if partner:
                    partner.related_user1 = g.user.id
                    g.user.related_user2 = partner.id
                    db.session.add(partner)
                    db.session.add(g.user)
                    db.session.commit()
                db.session.delete(find_user)
                db.session.commit()
        elif form.partner1_phone.data:
            enroll1 = Temp(user_id=g.user.id, related_phone=form.partner1_phone.data)
            db.session.add(enroll1)
        elif form.partner2_phone.data:
            enroll2 = Temp(user_id=g.user.id, related_phone=form.partner2_phone.data)
            db.session.add(enroll2)
        db.session.commit()
        return redirect(url_for('stand_by'))
    return render_template('enrollment.html', form=form, user=g.user)


@app.route('/stand_by')
def stand_by():
    return render_template('stand_by.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
