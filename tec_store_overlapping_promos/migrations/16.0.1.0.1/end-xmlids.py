import logging

from odoo import SUPERUSER_ID, api


MODEL = "tec_store_overlapping_promos"
ID_XMLID = {
    2: "collaborator_list",
}

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    Pricelist = env["product.pricelist"]
    pricelist_id = Pricelist.env.ref(f"{MODEL}.{ID_XMLID[2]}").id

    cr.execute(
        """
        DELETE FROM ir_model_data
        WHERE model = 'product.pricelist' AND res_id IN %s;
        """,
        (tuple(ID_XMLID),),
    )
    cr.execute(
        """
        UPDATE product_pricelist
        SET active = false
        WHERE id = %s;
        """,
        (pricelist_id,),
    )
    IrModelData = env["ir.model.data"]
    ProductPricelist = env["product.pricelist"]
    rec = ProductPricelist.browse(ID_XMLID.keys())
    xmlids_to_update = []
    xmlids_to_update.append({"xml_id": ".".join([MODEL, ID_XMLID[rec.id]]), "record": rec})
    IrModelData._update_xmlids(xmlids_to_update) 
