from flask import Blueprint,request,jsonify
from controller.purchase_controller import PurchaseController

purchase_bp = Blueprint('purchase',__name__)


@purchase_bp.route('/get_purchase_data',methods=['POST'])
def get_purchase_data():
    data= request.get_json()
    bill_no = data.get('bill_no')
    if not bill_no:
        return jsonify({"error": "bill_no is required"}), 400

    result = PurchaseController.purchase_data(bill_no)
    return result

@purchase_bp.route('/update_purchase_detail_data',methods=['PUT'])
def update_purchase_detail():
    data= request.get_json()
    id= data.get('id')
    mrp= data.get('mrp')
    if not (id,mrp):
        return jsonify({"error": "id and mrp is required"}), 400

    return PurchaseController.update_purchase_detail(id,mrp)

@purchase_bp.route('/delete_purchase_detail_data',methods=['DELETE'])
def delete_purchase_detail():
    data= request.get_json()
    id= data.get('id')
    
    if id is None:
        return jsonify({"error": "id  is required"}), 400

    return PurchaseController.delete_purchase_detail(id)

@purchase_bp.route('/read_purchase_detail_csv_data',methods=['POST'])
def read_csv():
    if 'file' not in request.files:
        return 'not file'
    file = request.files['file']

    return PurchaseController.fetch_purchase_data_from_csv(file)
@purchase_bp.route('/create_purchase_csv',methods=['POST'])
def create_purchase_csv_data():
    data= request.get_json()
    bill_no = data.get('bill_no')
    if not bill_no:
        return jsonify({"error": "bill_no is required"}), 400
    
    return PurchaseController.create_purchase_csv(bill_no)
