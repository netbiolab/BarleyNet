from flask import Flask, jsonify, request, url_for
#import json
import gene_validation
import search
import help_msg

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/')
def root():
	return "Welcome to BarleyNet API<br/>please go to <a href=\"" +  url_for('api_help') + "\">help</a> page."

@app.route('/help')
def api_help():
	return help_msg.get_help()

@app.route('/validate-genes', methods=['POST'])
def api_validate_genes():
	request_data = request.get_json()
	result = gene_validation.validate(request_data['genes'])
	return jsonify(result)

@app.route('/search/pathway-centric', methods=['POST'])
def api_search_pathway_centric():
	request_data = request.get_json()
	s = request_data['species']
	n = request_data['network']
	q = request_data['genes']
	
	result = search.pathway_centric(species=s, network=n, query_genes=q)
	return jsonify(result)

@app.route('/search/gene-centric', methods=['POST'])
def api_search_gene_centric():
	request_data = request.get_json()
	s = request_data['species']
	n = request_data['network']
	q = request_data['genes']
	
	result = search.gene_centric(species=s, network=n, query_genes=q)
	return jsonify(result)

@app.route('/search/context-associated-hubs', methods=['POST'])
def search_context_associated_hubs():
	request_data = request.get_json()
	s = request_data['species']
	n = request_data['network']
	q = request_data['genes']
	
	result = search.context_associated_hubs(species=s, network=n, query_genes=q)
	return jsonify(result)

@app.route('/geneset-analysis', methods=['POST'])
def api_geneset_analysis():
	request_data = request.get_json()
	q = request_data['genes']
	types = request_data['geneset-types']

	result = []
	for t in types:
		res = search.geneset_analysis(query_genes=q, geneset_type=t)
		result.append({'type': t, 'result': res})

	return jsonify(result)
