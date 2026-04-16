from graphviz import Digraph
from flask import Flask, render_template_string

class GraphVisualizer:
    def __init__(self, domain, subs):
        self.domain = domain
        self.subs = subs
    
    def generate_graph(self, filename):
        dot = Digraph(comment='Subdomain Graph')
        dot.node(self.domain, self.domain, shape='ellipse', color='blue')
        
        for sub in self.subs:
            color = 'green' if sub['score'] > 0.8 else 'orange'
            dot.node(sub['subdomain'], f"{sub['subdomain']}\n{sub['score']:.2f}", color=color)
            dot.edge(self.domain, sub['subdomain'])
        
        dot.render(filename, format='png', cleanup=True)
    
    def start_web_ui(self):
        app = Flask(__name__)
        @app.route('/')
        def index():
            return render_template_string('''
            <h1>SmartSubfinder Results</h1>
            <img src="graph.png" alt="Graph">
            <ul>
            {% for sub in subs %}
                <li>{{ sub.subdomain }} ({{ sub.score }})</li>
            {% endfor %}
            </ul>
            ''', subs=self.subs)
        app.run(debug=True, port=5000)
