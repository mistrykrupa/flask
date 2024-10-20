import jwt
import csv
import datetime
from flask import jsonify
from flask import request
from model.purchase_model import PurchaseModel
# from services.auth_service import AuthService
from config import Config
import io


class PurchaseController:
    
    @staticmethod
    def purchase_data(bill_no):
       
        result = PurchaseModel.get_purchase_data_with_detail(bill_no)
        
        if result:
            purchase_data = []
            for row in result:
                purchase_data.append({
                    'bill_no': row[0],
                    'bill_date': row[1],
                    'bill_total': int(row[2]),  
                    'medicine_name': row[3], 
                    'quantity': row[4] ,           
                    'mrp': int(row[5]), 
                    'item_total': int(row[6]),  
                    'expiry_date': row[7]   
                })
           
            return jsonify({'Purchase Data':purchase_data})
        return jsonify({"error": "No purchase found for the provided bill_no"}), 404
    
    @staticmethod
    def update_purchase_detail(id,mrp):
        
        result = PurchaseModel.update_purchase_detail_data(id,mrp)
        

        if result:
            return jsonify({'message':'Updated Purchase Detail Data Succesfully!!'})
        else:
            return jsonify({"error": "No record Updated"}), 404
    
    @staticmethod
    def delete_purchase_detail(id):
        
        result = PurchaseModel.delete_purchase_detail_data(id)
        

        if result:
            return jsonify({'message':'Delete Purchase Detail Data Succesfully!!'})
        return jsonify({"error": "Something went wrong"}), 404
    
    

    @staticmethod
    def fetch_purchase_data_from_csv(file):
        stream = io.StringIO(file.stream.read().decode("UTF8"),newline=None)
        data = []

        reader = csv.DictReader(stream)
        bill_total = 0
        for row in reader:
            row['item_total'] = int(row['quantity']) * int(row['mrp'])
            data.append(row)
            

        for item in data:
            bill_total += item['item_total']

        
        bill_no = data[0]['bill_no']
        bill_date = data[0]['bill_date']
        
        purchase_id=PurchaseModel.insert_purchase_data(bill_no,bill_date,bill_total)
        

        inserted_detail=[]
        for detail in data:
            result = PurchaseModel.insert_purchase_detail_data(purchase_id,detail)

        return data
    
    @staticmethod
    def create_purchase_csv(bill_no):
        result = PurchaseModel.get_purchase_data_with_detail(bill_no)
        
        csv_path = 'purchase.csv'

        with open(csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(['Bill_No', 'Bill_Date', 'Bill_Total', 'Medicine_Name', 
                         'Quantity', 'MRP', 'Item_Total', 'Expiry_Date'])
        
            for row in result:
                writer.writerow(row)

        return csv_path
        