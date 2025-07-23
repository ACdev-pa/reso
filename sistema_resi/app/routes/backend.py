from flask import Blueprint, render_template, request, redirect, url_for

from ..models import PuntoVendita, Dipendente, ProceduraReso
from .. import db

bp = Blueprint('backend', __name__, url_prefix='/admin', template_folder='../templates/backend')


@bp.route('/')
def index():
    resi = ProceduraReso.query.order_by(ProceduraReso.data_invio.desc()).all()
    return render_template('index.html', resi=resi)


@bp.route('/reso/<int:reso_id>', methods=['GET', 'POST'])
def reso_detail(reso_id: int):
    reso = ProceduraReso.query.get_or_404(reso_id)
    if request.method == 'POST':
        reso.stato = request.form['stato']
        db.session.commit()
        return redirect(url_for('backend.index'))
    return render_template('reso_detail.html', reso=reso)


# ---- Punti vendita ----
@bp.route('/punti_vendita')
def punti_vendita():
    punti_vendita = PuntoVendita.query.all()
    return render_template('punti_vendita.html', punti_vendita=punti_vendita)


@bp.route('/punti_vendita/nuovo', methods=['GET', 'POST'])
def new_pv():
    if request.method == 'POST':
        pv = PuntoVendita(nome=request.form['nome'])
        db.session.add(pv)
        db.session.commit()
        return redirect(url_for('backend.punti_vendita'))
    return render_template('punto_vendita_form.html')


@bp.route('/punti_vendita/<int:id>/edit', methods=['GET', 'POST'])
def edit_pv(id: int):
    pv = PuntoVendita.query.get_or_404(id)
    if request.method == 'POST':
        pv.nome = request.form['nome']
        db.session.commit()
        return redirect(url_for('backend.punti_vendita'))
    return render_template('punto_vendita_form.html', pv=pv)


@bp.route('/punti_vendita/<int:id>/delete', methods=['POST'])
def delete_pv(id: int):
    pv = PuntoVendita.query.get_or_404(id)
    db.session.delete(pv)
    db.session.commit()
    return redirect(url_for('backend.punti_vendita'))


# ---- Dipendenti ----
@bp.route('/dipendenti')
def dipendenti():
    dipendenti = Dipendente.query.all()
    return render_template('dipendenti.html', dipendenti=dipendenti)


@bp.route('/dipendenti/nuovo', methods=['GET', 'POST'])
def new_dipendente():
    punti = PuntoVendita.query.all()
    if request.method == 'POST':
        d = Dipendente(
            nome=request.form['nome'],
            punto_vendita_id=request.form['punto_vendita_id'],
        )
        db.session.add(d)
        db.session.commit()
        return redirect(url_for('backend.dipendenti'))
    return render_template('dipendente_form.html', punti=punti)


@bp.route('/dipendenti/<int:id>/edit', methods=['GET', 'POST'])
def edit_dipendente(id: int):
    dipendente = Dipendente.query.get_or_404(id)
    punti = PuntoVendita.query.all()
    if request.method == 'POST':
        dipendente.nome = request.form['nome']
        dipendente.punto_vendita_id = request.form['punto_vendita_id']
        db.session.commit()
        return redirect(url_for('backend.dipendenti'))
    return render_template('dipendente_form.html', dipendente=dipendente, punti=punti)


@bp.route('/dipendenti/<int:id>/delete', methods=['POST'])
def delete_dipendente(id: int):
    dipendente = Dipendente.query.get_or_404(id)
    db.session.delete(dipendente)
    db.session.commit()
    return redirect(url_for('backend.dipendenti'))
