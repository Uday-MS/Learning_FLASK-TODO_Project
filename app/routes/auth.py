from flask import Blueprint,render_template,redirect,request,url_for,flash,session

auth_bp=Blueprint('auth',__name__)

USER_CREDENTIALS={
    'username':'admin',
    'password':'123',

}
@auth_bp.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')

        if username==USER_CREDENTIALS['username'] and password==USER_CREDENTIALS['password']:
            session['user']==username
            flash('Login Succesful','success')
        else:
            flash('invalid username or password ')

    return render_template("login.html")

@auth_bp.route('/logut')

def logout():
    session.pop('user',None)
    flash('Loged out','info')
    return redirect(url_for('auth.login'))
