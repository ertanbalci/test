
from flask import Flask,render_template,request,redirect, flash
from flask_login import login_required, current_user, login_user, logout_user
from models import MemberModel,db,login
from my_form import yForm, gForm 
 
app = Flask(__name__)
app.secret_key = 'xyz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_members.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db.init_app(app) # db objesini ana uygulamaya (app objesine)bağlıyoruz.  

login.init_app(app) # login objesini ana uygulamaya bağlıyoruz. 

# kimliği doğrulanmamış kullanıcıların yönlendirileceği sayfa
login.login_view = 'login' 

@app.before_first_request # ilk request'ten önce vt oluşturuyoruz.
def do_before_first_request():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_account', methods = ['POST', 'GET'])
def new_account():
    form = yForm()
    if not form.validate_on_submit():
        return render_template("new_acc.html", form=form)
    else:
        user = form.username.data
        pos  = form.eposta.data
        psw  = form.parola.data
        if MemberModel.query.filter_by(username=user).first():
            flash(user+" kullanıcı adı mevcut! Yeni bir kullanıcı adı seçin.")
            return render_template("new_acc.html", form=form)
        mem = MemberModel(username=user, eposta=pos)
        mem.hash_password(psw)
        db.session.add(mem)
        db.session.commit()
        return redirect("/logout")
        
@app.route('/login', methods = ['POST', 'GET'])
def login():        
    if current_user.is_authenticated:
        return redirect('/members')
    form=gForm() 
    if form.validate_on_submit():
        m_adi  = form.username.data
        m_psw  = form.parola.data
        mem = MemberModel.query.filter_by(username=m_adi).first()
        if mem:
            if mem.control_password(m_psw):
                login_user(mem) 
                return redirect('/members')
        flash( "Hatalı eposta adresi veya parola")
    return render_template("login.html", form=form)

@app.route('/members')
@login_required
def members():
    uyeler = MemberModel.query.all()
    return render_template('member_page.html', mems=uyeler)
 
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == "__main__":
     app.run(debug=True)
