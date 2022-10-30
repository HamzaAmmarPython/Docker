import matplotlib 
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file, send_from_directory
from markupsafe import escape
import networkx as nx
from flask_cors import CORS, cross_origin
from PIL import Image


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

number = 0
@app.route('/')
def hello():
    return 'Hello, World!'

G = nx.Graph()
# ERC First Floor (G)
# // Add Nodes
# G_Names = ["A", "B", "C", "D", "E", "F", "G", "H", "Stair", "Elevator", "1001", "1002", "1003", "1004", "1006", "1007", "1009", "1011", "1012", "1012B", "1802", "1902"]
# G_Poses = [(3,4), (4,7.5), (4,8), (4, 10.5), (4, 11.5), (6, 11.5), (8, 11.5), (10, 11.5), (2.5, 3.5), (2.5, 4), (3, 11), (3,10), (3,8), (3,7.5), (6, 10.5), (7, 10.5), (9, 10), (10,9), (10, 13), (8, 13), (4, 13.5), (6, 3.5) ]
G.add_node("A", pos = (3.7,0))
G.add_node("Stair", pos = (2,0))
G.add_node("Elevator", pos = (2,1.5))
G.add_node("1902", pos = (6,0))
G.add_node("B", pos = (3.7,6))
G.add_node("C", pos = (3.7,8))
G.add_node("1004", pos = (3,6))
G.add_node("1003", pos = (3,7))
G.add_node("1002", pos = (3,10))
G.add_node("D", pos = (3.7,10.5))
G.add_node("E", pos = (3.7,11.5))
G.add_node("1001", pos = (3,11))
G.add_node("F", pos = (6,11.5))
G.add_node("G", pos = (8,11.5))
G.add_node("H", pos = (10.5,11.5))
G.add_node("1006", pos = (6,10.5))
G.add_node("1802", pos = (3.5,13.5))
G.add_node("1012", pos = (10.5,14))
G.add_node("1012B", pos = (8,14))
G.add_node("1011", pos = (10,9))
G.add_node("1007", pos = (7,10.5))
G.add_node("1008", pos = (8, 10.5))
G.add_node("1009", pos = (9,10.5))
G.add_node("Cali", pos = (0,0))
G.add_node("Cali2", pos = (12,15))
# // Add edges
G.add_edge("A", "B", weight=1)
G.add_edge("A", "Stair", weight=1)
G.add_edge("A", "Elevator", weight=1)
G.add_edge("A", "1902", weight=1)
G.add_edge("B", "1004", weight=1)
G.add_edge("B", "C", weight=1)
G.add_edge("C", "1003", weight=1)
G.add_edge("C", "D", weight=1)
G.add_edge("D", "1002", weight=1)
G.add_edge("D", "E", weight=1)
G.add_edge("D", "1001", weight=1)
G.add_edge("E", "F", weight=1)
G.add_edge("E", "1001", weight=1)
G.add_edge("E", "1802", weight=1)
G.add_edge("F", "G", weight=1)
G.add_edge("G", "H", weight=1)
G.add_edge("G", "1009", weight=1)
G.add_edge("F", "1007", weight=1)
G.add_edge("F", "1006", weight=1)
G.add_edge("H", "1012", weight=1)
G.add_edge("1012", "1012B", weight=1)
G.add_edge("H", "1011", weight=1)
G.add_edge("G", "1008", weight=1)
# print(G.edges())


pos = nx.get_node_attributes(G, 'pos')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
# print(nx.dijkstra_path(G, "Stair", "1006"))
plt.clf()

@app.route('/<start>/<end>')
def get_route(start, end):
    H = nx.Graph()
    H.clear()
    # // Add Nodes
    for n in G.nodes(data=True):
        print(n)
        if n[0] in nx.dijkstra_path(G, start, end):
            H.add_node(n[0], pos = n[1]['pos'], node_color = 'red')
    for u, v in G.edges():
        if u in H.nodes and v in H.nodes:
            H.add_edge(u, v, weight=3, edge_color = 'black')
    H.add_node("Cali", pos = (0,0))
    H.add_node("Cali2", pos = (12,15))
    nx.draw(H, pos, with_labels=True)
    nx.draw_networkx_nodes(H, pos, nodelist = H.nodes, node_color = 'Red')
    nx.draw_networkx_nodes(H, pos, nodelist=['Cali', 'Cali2'], node_color="None")
    nx.draw_networkx_edge_labels(H, pos, edge_labels=labels)
    nx.draw(H)
    print(H.nodes())
    # os.remove('/abc.png') #prevents the image from being saved twice
    plt.savefig('/abc.png')
    plt.clf()
    H.clear()

    img = Image.open("/abc.png")
    img = img.convert("RGBA")
 
    datas = img.getdata()
 
    newData = []
 
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    
    img.putdata(newData)
    img.save("abc.png", "PNG")
    print("Successful")

    def add_margin(pil_img, top, right, bottom, left, color):
        width, height = pil_img.size
        new_width = width + right + left
        new_height = height + top + bottom
        result = Image.new(pil_img.mode, (new_width, new_height), color)
        result.paste(pil_img, (left, top))
        return result
    with Image.open("abc.png") as im:
        im_new = add_margin(im, -35, 50, -70, 100, (128, 0, 64, 1))
        im_new.save('abc.png', quality=95)
    # str(nx.dijkstra_path(G, start, end)),
    image = open('/abc.png', 'rb')
    print(image)
    return send_from_directory(os.getcwd(), 'abc.png', as_attachment=True)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
