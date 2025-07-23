import os
import sys

BASE_DIR = os.path.join(os.path.dirname(__file__), "sistema_resi")
sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models import PuntoVendita, Dipendente, ProceduraReso


def main():
    app = create_app()
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            os.remove(db_path)
        db.create_all()

        pv_milano = PuntoVendita(nome="Punto Vendita Milano")
        pv_roma = PuntoVendita(nome="Punto Vendita Roma")
        db.session.add_all([pv_milano, pv_roma])
        db.session.commit()

        marco = Dipendente(nome="Marco Rossi", punto_vendita_id=pv_milano.id)
        lucia = Dipendente(nome="Lucia Bianchi", punto_vendita_id=pv_milano.id)
        giovanni = Dipendente(nome="Giovanni Verdi", punto_vendita_id=pv_roma.id)
        elisa = Dipendente(nome="Elisa Neri", punto_vendita_id=pv_roma.id)
        db.session.add_all([marco, lucia, giovanni, elisa])
        db.session.commit()

        reso1 = ProceduraReso(
            motivo="Scarpe difettose",
            stato="In attesa",
            punto_vendita_id=pv_milano.id,
            dipendente_id=marco.id,
        )
        reso2 = ProceduraReso(
            motivo="Cambio numero",
            stato="Accettato",
            punto_vendita_id=pv_roma.id,
            dipendente_id=giovanni.id,
        )
        reso3 = ProceduraReso(
            motivo="Articolo errato",
            stato="Rifiutato",
            punto_vendita_id=pv_roma.id,
            dipendente_id=elisa.id,
        )
        db.session.add_all([reso1, reso2, reso3])
        db.session.commit()

    print("Database popolato con dati di test")


if __name__ == "__main__":
    main()
