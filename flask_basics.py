from flask import Flask, request, jsonify 

app = Flask(__name__) 

# In-memory data storage 
data_store = [
    {"id": 1, "task": "Learn Flask"},
    {"id": 2, "task": "Build an API"}
]

#  GET / - Welcome message 
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask Basics API!"})

#  GET /data - Return all items 
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_store)

#  POST /data - Add new item 
@app.route('/data', methods=['POST'])
def add_data():
    new_item = request.get_json()
    data_store.append(new_item)
    return jsonify({"message": "Item added successfully", "data": new_item}), 201

#  PUT /data/<id> - Update item 
@app.route('/data/<int:item_id>', methods=['PUT'])
def update_data(item_id):
    updated_values = request.get_json()
    for item in data_store:
        if item['id'] == item_id:
            item.update(updated_values)
            return jsonify({"message": "Item updated", "data": item})
    return jsonify({"error": "Item not found"}), 404

# DELETE /data/<id> - Delete item 
@app.route('/data/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    global data_store
    data_store = [item for item in data_store if item['id'] != item_id]
    return jsonify({"message": f"Item {item_id} deleted"})

if __name__ == '__main__':
    app.run(debug=True)