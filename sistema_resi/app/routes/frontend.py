from flask import Blueprint, render_template, request, redirect, url_for, session

from ..models import PuntoVendita, Dipendente, ProceduraReso
from .. import db

bp = Blueprint(
    'frontend', __name__, template_folder='../templates/frontend'
)


@bp.route('/', methods=['GET'])
def index():
    punti_vendita = PuntoVendita.query.all()
    selected_pv = request.args.get('punto_vendita')
    dipendenti = []
    if selected_pv:
        dipendenti = Dipendente.query.filter_by(punto_vendita_id=selected_pv).all()
    return render_template(
        'home.html',
        punti_vendita=punti_vendita,
        dipendenti=dipendenti,
        selected_pv=selected_pv,
    )


@bp.route('/seleziona_dipendente', methods=['POST'])
def select_dipendente():
    session['punto_vendita_id'] = request.form['punto_vendita_id']
    session['dipendente_id'] = request.form['dipendente_id']
    return redirect(url_for('frontend.dashboard'))


@bp.route('/dashboard')
def dashboard():
    dipendente_id = session.get('dipendente_id')
    if not dipendente_id:
        return redirect(url_for('frontend.index'))
    dipendente = Dipendente.query.get(dipendente_id)
    return render_template('dashboard.html', dipendente=dipendente)


@bp.route('/crea_reso', methods=['GET', 'POST'])
def crea_reso():
    dipendente_id = session.get('dipendente_id')
    punto_vendita_id = session.get('punto_vendita_id')
    if not dipendente_id or not punto_vendita_id:
        return redirect(url_for('frontend.index'))

    if request.method == 'POST':
        motivo = request.form['motivo']
        descrizione = request.form.get('descrizione')
        reso = ProceduraReso(
            motivo=motivo,
            descrizione=descrizione,
            punto_vendita_id=punto_vendita_id,
            dipendente_id=dipendente_id,
        )
        db.session.add(reso)
        db.session.commit()
        return redirect(url_for('frontend.dashboard'))

    return render_template('crea_reso.html')


@bp.route('/stato_reso')
def stato_reso():
    dipendente_id = session.get('dipendente_id')
    if not dipendente_id:
        return redirect(url_for('frontend.index'))

    resi = (
        ProceduraReso.query.filter_by(dipendente_id=dipendente_id)
        .order_by(ProceduraReso.data_invio.desc())
        .all()
    )
    return render_template('stato_reso.html', resi=resi)
