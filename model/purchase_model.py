import json
import csv
import psycopg2
from config import  Config
from datetime import datetime

class PurchaseModel:
    @staticmethod
    def get_db_connection():
        return psycopg2.connect(Config.DATABASE_URI)
    
    @staticmethod
    def get_purchase_data_with_detail(bill_no):
        
        connection = PurchaseModel.get_db_connection()
        cursor = connection.cursor()

        try:
            query= """
                SELECT p.bill_no, p.bill_date, p.bill_total, pd.medicine_name, pd.quantity, pd.mrp, pd.item_total, pd.expiry_date FROM purchase p 
                LEFT JOIN purchase_details pd ON p.id = pd.purchase_id WHERE p.bill_no = %s;
                """
            
            cursor.execute(query, (bill_no,))
            result = cursor.fetchall()
            return result

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_purchase_detail_data(id,mrp):
        
        connection = PurchaseModel.get_db_connection()
        cursor = connection.cursor()

        try:
            query= """
                UPDATE purchase_details SET mrp = %s WHERE purchase_id = %s returning id;
                """
            cursor.execute(query, (mrp,id))
            
            # result = cursor.fetchone()
            connection.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False

        except Exception as e:
            connection.rollback() 
            print(f"Error occurred: {str(e)}")
            return None
        finally:
            cursor.close()
            connection.close()  


    @staticmethod
    def delete_purchase_detail_data(id):
        
        connection = PurchaseModel.get_db_connection()
        cursor = connection.cursor()

        try:
            query= """
                DELETE FROM purchase_details WHERE id = %s;
                 """
            cursor.execute(query, (id,))
            
            # result = cursor.fetchone()
            connection.commit()
            if cursor.rowcount > 0:
                
                return True
            else:
                
                return False
            

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None
        finally:
            cursor.close()
            connection.close()  

    

    
    @staticmethod
    def insert_purchase_data(bill_no,bill_date,bill_total):
        
        connection = PurchaseModel.get_db_connection()
        cursor = connection.cursor()

        try:
            
            query= """
                INSERT INTO purchase(bill_no,bill_date,bill_total) VALUES (%s,%s,%s) RETURNING id;
                """
            
            cursor.execute(query, (bill_no,bill_date,bill_total))
            purchase_id = cursor.fetchone()[0]
            
            connection.commit()
            
        except Exception as e:
            connection.rollback() 
            print(f"Error occurred: {str(e)}")
            return None
        finally:
            
            cursor.close()
            connection.close()
            return purchase_id

    @staticmethod
    def insert_purchase_detail_data(purchase_id,detail):
        connection = PurchaseModel.get_db_connection()
        cursor = connection.cursor()

        try:
            query= """
                INSERT INTO purchase_details(purchase_id, medicine_name, quantity, mrp, item_total, expiry_date) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id;
                """
            
            cursor.execute(query, (purchase_id,detail['medicine_name'],detail['quantity'],detail['mrp'],detail['item_total'],detail['expiry_date']))
            result = cursor.fetchone()[0]
            connection.commit()
            return result

        except Exception as e:
            connection.rollback() 
            print(f"Error occurred: {str(e)}")
            return None
        finally:
            cursor.close()
            connection.close()

    