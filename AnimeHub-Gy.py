from flask import Flask, jsonify, request, render_template
import mongoengine as db
import json

# Flask application object
app= Flask(__name__)

# MongoDB connection setup
client = db.connect('AnimeHub', username='', password='')

# Regions
supported_regions = ['South America', 'Asia', 'North America', 'Africa', 'Europe', 'Guyana', 'Caribbean']
supported_regions_delivery_cost = [125,150,200,100,350, 70, 100]
# Packages
package_price = [400 , 800, 1500, 3000, 1000]

# Data Class for accessing  MongoDB collection
class Order(db.Document):
   customerName = db.StringField()
   customerAddress = db.StringField()
   customerRegion = db.StringField()
   
   customerEmail = db.StringField()
   customerPhoneNo = db.StringField()
   
   packageNo = db.IntField()
   totalPrice = db.IntField()
   
   meta = {'collection': 'Order', 'allow_inheritance': False}

# Data class for package to enter data collection
class Package(db.Document):
   pid = db.IntField()
   name = db.StringField()
   description = db.StringField()
   price = db.IntField()

   meta = {'collection': 'Package', 'allow_inheritance': False}

#http://localhost:5000
@app.route('/', methods = ['GET'])
def view_index(): 
   return render_template('index.html')






# http://localhost:5000/order/list
@app.route('/order/list', methods = ['GET']) # Enable GET and POST
def view_orders():
   return json.loads( Order.objects.to_json())



# http://localhost:5000/package/list
@app.route('/package/list', methods = ['GET']) # Enable GET and POST
def view_packages():
   return json.loads( Package.objects.to_json())


# http://localhost:5000/order/new
@app.route('/order/new', methods = ['GET','POST'])
def place_order():
    
    if (request.method == 'GET'):
       return render_template('index_3.html')
       
   # follow code will be executed for post
   
    customer_name_val = request.form.get('customerName')
    customer_address_val = request.form.get('customerAddress')
    customer_region_val = request.form.get('customerRegion')
    customer_email_val = request.form.get('customerEmail')
    customer_phone_val = request.form.get('customerPhoneNo')
    package_val = request.form.get('packageNo')
    
    #debug
    
    print( customer_name_val)
    print( customer_address_val)
    print( customer_region_val)
    print( customer_email_val, customer_phone_val)
    print( package_val)


    #  calculate total price
    total_monetary_val = 0


    #total_monetary_val += package_price[int(package_val)]

    #need to recieve datat form database
    packages_found = Package.objects(pid=int(package_val))
    # get the first package id from the first package found
    package= packages_found.first()

    print( package, package.pid, package.name, package.price)
    total_monetary_val += package.price

    if customer_region_val == supported_regions[0] :
       total_monetary_val += supported_regions_delivery_cost[0]
    elif customer_region_val == supported_regions[1] :
       total_monetary_val += supported_regions_delivery_cost[1]
    elif customer_region_val == supported_regions[2] :
       total_monetary_val += supported_regions_delivery_cost[2]
    elif customer_region_val == supported_regions[3] :
       total_monetary_val += supported_regions_delivery_cost[3]
    elif customer_region_val == supported_regions[4] :
       total_monetary_val += supported_regions_delivery_cost[4]
    elif customer_region_val == supported_regions[5] :
       total_monetary_val += supported_regions_delivery_cost[5]
    elif customer_region_val == supported_regions[6] :
       total_monetary_val += supported_regions_delivery_cost[6]

    
    print( "Total cost is $", total_monetary_val )

       



    newOrder = Order( customerName=customer_name_val, customerAddress=customer_address_val, customerRegion=customer_region_val, customerEmail=customer_email_val, customerPhoneNo= customer_phone_val, packageNo= package_val, totalPrice= total_monetary_val)
    
    newOrder.save()
    
   # return 'success'
    return 'Order has been placed. The total cost is $'+ str( total_monetary_val) + 'GYD.'
    


   
if __name__=='__main__':
   app.run(debug=True)