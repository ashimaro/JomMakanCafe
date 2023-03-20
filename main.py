from flask import Flask, render_template, request, jsonify
from tableinfo import tableinfo, food, drinks, statuses
from datetime import datetime, timedelta

app = Flask(__name__)

def get_current_dt_string():
  current_dt = datetime.utcnow() + timedelta(hours=8)
  return current_dt.strftime("%d %B %Y, %H:%M:%S")

#front-end paths

@app.route("/")
def database():
  return render_template("dashboard.html", tables=tableinfo)
  
@app.route("/order/<table_id>", methods=["GET", "POST"])
def order(table_id):
  if request.method == "POST":
    new_order = request.form

    tableinfo[table_id]["food"]["itemfood"] = []
    tableinfo[table_id]["food"]["qfood"] = []
    tableinfo[table_id]["drinks"]["itemdrink"] = []
    tableinfo[table_id]["drinks"]["qdrink"] = []
       
    for key, quantity in new_order.items():
      if len(quantity) > 0:
        if key[0] =='f':
          f =  int(key[1:])
          order_food = food[f]
          tableinfo[table_id]["food"]["itemfood"].append(order_food)
          tableinfo[table_id]["food"]["qfood"].append(int(quantity))
        elif key[0]== 'd':
          d = int(key[1:])
          order_drink = drinks[d]
          tableinfo[table_id]["drinks"]["itemdrink"].append(order_drink)
          tableinfo[table_id]["drinks"]["qdrink"].append(int(quantity))

    order_food_length = len(tableinfo[table_id]["food"]["itemfood"])
    order_drinks_length = len(tableinfo[table_id]["drinks"]["itemdrink"])
                     
    # Update status to 'Ordered
    tableinfo[table_id]["status"] = statuses[1]

    # Update time ordered
    tableinfo[table_id]["time"] = get_current_dt_string()

    return render_template ("order_accepted.html",
                             order=tableinfo[table_id], order_food_length=order_food_length,
                             order_drinks_length=order_drinks_length
                           )
  # GET request

  if tableinfo[table_id]["status"] == statuses[0]:
      return render_template("order_new.html", table_id=table_id,                                 food=enumerate(food),drinks=enumerate(drinks))

  return render_template("order_not_allowed.html", table_id=table_id)

#API endpoints
@app.route("/api/table/<table_id>")
def get_table_info(table_id):
    resp = jsonify(tableinfo[table_id])
    resp.status_code = 200
    return resp

@app.route("/api/table/<table_id>/status/<status_id>", methods=["PUT"]
)
def update_table_status(table_id, status_id):
    status_id = int(status_id)
    tableinfo[table_id]["status"] = statuses[status_id]
    tableinfo[table_id]["time"] = get_current_dt_string()
    return f"Updated Table {table_id} status to {statuses[status_id]}"
                        
app.run(host="0.0.0.0", port=8080)
    
            