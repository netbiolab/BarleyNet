import config
from gene_network import GeneNetwork
import operator
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import fdrcorrection as adjust

def gene_centric(species, network, query_genes):
	'''
	Run Gene-centric Search

	:Returns: list of the result of each gene's gene-centric search
	'''
	def run_single(annotation_type, query):
		annot_to_score = dict()
		neighbors = net.get_neighbors(query)
		for neighbor in neighbors:
			link_info = net.get_link_info(neighbor, query)
			for annot in net.get_annot(annotation_type, neighbor):
				if annot not in annot_to_score:
					annot_to_score[annot] = dict()
					annot_to_score[annot]['LLS'] = 0.0
				annot_to_score[annot]['LLS'] += link_info['LLS']

		out = list()
		for annot in annot_to_score:
			out.append({
				'id': annot,
				'desc': net.get_annot_desc(annotation_type, annot),
				'sumlls': annot_to_score[annot]['LLS'],
			})

		out.sort(key=operator.itemgetter('sumlls'), reverse=True)
		return out[:20]

	annotations = config.ANNOTATIONS
	net = GeneNetwork(species, network)
	result = []
	for query_gene in query_genes:
		gi = net.get_gene_info(query_gene)
		gc_result = {
			'gene': {
				'geneid': query_gene,
				'mloc': gi['mloc'] if 'mloc' in gi else '',
				'desc': gi['desc'] if 'desc' in gi else '',
				'annot': [{'type': t, 'result': net.get_annot_dict(t, query_gene)} for t in annotations]
			},
			'result': [{'type': t, 'gcsResult': run_single(annotation_type=t, query=query_gene)} for t in annotations]
		}
		result.append(gc_result)
	return result

def pathway_centric(species, network, query_genes):
	'''
	Run pathway-centric search
	* query_genes: valid query_genes

	:Returns: dict, the result of pathway-centric search 
		the dict has 4 keys and values
			not-in-nw : queried genes not existed in networks
			link-info : result of pathway-centric search
			gene-info : information of genes in 'link-info'
			conn-dist : Within group connectivity distribution of random genes which same number of quried genes
	'''
	net = GeneNetwork(species, network)
	gene_to_scores = dict()
	edgeinfo_out = list()
	notinnw_list = list()
	withingroup_linkcnt = 0

	for query in query_genes:
		if not net.is_in_network(query):
			notinnw_list.append(query)
			continue

		if query not in gene_to_scores:
			gene_to_scores[query] = dict()
			gene_to_scores[query]['LLS'] = float(0)

		for neighbor in net.get_neighbors(query):
			sorted_genes = sorted([neighbor, query])

			redis_out = net.get_link_info(neighbor, query)

			link_info = {k:float(v) for k, v in redis_out.items()}
			
			if neighbor not in gene_to_scores:
				gene_to_scores[neighbor] = dict()

			for evidence, score in link_info.items():
				if evidence not in gene_to_scores[neighbor]:
					gene_to_scores[neighbor][evidence] = float(0)
				gene_to_scores[neighbor][evidence] += score
			
			if neighbor in query_genes:
				withingroup_linkcnt += 1
			
			lls = link_info.pop('LLS')
			edgeinfo_out.append({
				'genes': sorted_genes,
				'lls': lls,
				'networks': link_info
			})
	
	geneinfo_out = list()
	for gene in gene_to_scores:
		sum_of_lls = gene_to_scores[gene].pop("LLS")
		evi_networks = gene_to_scores[gene]
		is_query = "query" if gene in query_genes else "candidate"
		gene_info = net.get_gene_info(gene)

		geneinfo_annot = dict()
		for atype in ['GOBP', 'AT-GOBP', 'OS-GOBP', 'ZM-GOBP']:
			annot_result = net.get_annot_dict(atype, gene)
			if len(annot_result) != 0:
				geneinfo_annot[atype] = annot_result

		geneinfo_out.append({
			'geneid': gene,
			'desc': gene_info['desc'] if 'desc' in gene_info else '',
			'mloc': gene_info['mloc'] if 'mloc' in gene_info else '',
			'sumlls': sum_of_lls,
			'type': is_query,
			'networks': evi_networks,
			'annot': geneinfo_annot
		})
	geneinfo_out.sort(key=operator.itemgetter('sumlls'), reverse=True)
	withingroup_linkcnt >>= 1

	conndist_out = net.get_gene_conn_dist(len(query_genes), withingroup_linkcnt)

	notinnw_out = list()
	for notinnw in notinnw_list:
		gene_info = net.get_gene_info(notinnw)

		notinnw_out.append({
			'geneid': notinnw,
			'desc': gene_info['desc'] if 'desc' in gene_info else '',
			'mloc': gene_info['mloc'] if 'mloc' in gene_info else '',
		})
	
	result = {
		'link-info': edgeinfo_out,
		'gene-info': geneinfo_out,
		'conn-dist': conndist_out,
		'not-in-nw': notinnw_out
	}

	return result

def geneset_analysis(query_genes, geneset_type):
	total_genecount = config.GENOMECNT
	geneset_file = config.GENESETFILE[geneset_type]
	adj_alpha = config.ADJ_ALPHA

	query_genes = set(query_genes)

	query_cnt = len(query_genes)
	gsa_out = list()
	with open(geneset_file) as geneset_f:
		for line in geneset_f:
			line = line.strip()
			geneset, desc, _, genes = line.split("\t")
			if geneset == 'GO:0008150': # skip GO:0008150 biological_process 
				continue
			member_genes = set(genes.split(","))
			intersection_cnt = len(query_genes & member_genes)

			# taking Overlap > 1  
			if intersection_cnt < 1:
				continue

			contingency_table = [
				[
					intersection_cnt,
					len(member_genes) - intersection_cnt
				], 
				[
					query_cnt - intersection_cnt,
					total_genecount - len(member_genes) - query_cnt + intersection_cnt
				]
			]
			_, pval = fisher_exact(contingency_table, alternative="greater")

			gsa_out.append({
				'id': geneset,
				'desc': desc,
				'pvalue': pval
			})
	pvals = [el['pvalue'] for el in gsa_out]
	rejected, pvals_corr = adjust(pvals, alpha=adj_alpha, method='indep', is_sorted=False)

	del_idx = list()
	for i in range(len(gsa_out)):
		if rejected[i]:
			gsa_out[i]['adj-pvalue'] = pvals_corr[i]
		else:
			del_idx.append(i)

	del_idx = sorted(del_idx, reverse=True)
	for i in del_idx:
		del gsa_out[i]

	gsa_out = sorted(gsa_out, key=lambda idx: idx['pvalue'], reverse=False)
	return gsa_out

def context_associated_hubs(species, network, query_genes):
	def get_annotations(gene):
		return [{'type': a, 'result': net.get_annot_dict(a, gene)} for a in config.ANNOTATIONS]

	REGULON = config.REGULON
	GENOMECNT = config.GENOMECNT
	TF = config.TF

	pval_thres = 0.01
	adj_alpha = config.ADJ_ALPHA

	net = GeneNetwork(species, network)

	query = set(query_genes)
	regulon = dict()
	for line in open(REGULON):
		hub, genes = line.strip().split('\t')
		genes = genes.split(',')
		if len(genes) < 100:
			continue
		regulon[hub] = genes
	
	tf_set = set([line.strip() for line in open(TF)])

	result = []
	for hub in regulon:
		members = set(regulon[hub])
		
		_, pval = fisher_exact([
				[len(query & members), len(members - query)],
				[len(query - members), GENOMECNT - len(members.union(query))]
			], alternative="greater")

		if pval <= pval_thres:
			gene_info = net.get_gene_info(hub)
			result.append({
				'hub':hub,
				'desc': gene_info['desc'] if 'desc' in gene_info else '',
				'annot': get_annotations(hub),
				'pvalue': pval,
				'DEG': str(hub in query),
				'TF': str(hub in tf_set)
			})

	raw_pval = [k['pvalue'] for k in result]
	passed, adj_p = adjust(raw_pval, alpha=adj_alpha, method='indep', is_sorted=False)

	for i in range(len(result)):
		if passed[i]:
			result[i]['qvalue'] = adj_p[i]
	
	result.sort(key = lambda x:x['pvalue'])

	return {"query":sorted(query), "result": result}
