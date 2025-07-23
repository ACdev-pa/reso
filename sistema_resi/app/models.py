from datetime import datetime
from . import db


class PuntoVendita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    dipendenti = db.relationship('Dipendente', backref='punto_vendita', lazy=True)
    resi = db.relationship('ProceduraReso', backref='punto_vendita', lazy=True)


class Dipendente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    punto_vendita_id = db.Column(db.Integer, db.ForeignKey('punto_vendita.id'), nullable=False)

    resi = db.relationship('ProceduraReso', backref='dipendente', lazy=True)


class ProceduraReso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    motivo = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text)
    stato = db.Column(db.String(20), default='In attesa')
    data_invio = db.Column(db.DateTime, default=datetime.utcnow)

    punto_vendita_id = db.Column(db.Integer, db.ForeignKey('punto_vendita.id'), nullable=False)
    dipendente_id = db.Column(db.Integer, db.ForeignKey('dipendente.id'), nullable=False)
