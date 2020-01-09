import config
import redis

class GeneNetwork:
	def __init__(self, species, network):
		self.species = species
		self.network = network
		self.redis_connect()

	def redis_connect(self):
		redis_conf = config.REDIS_SERVER

		self.redis_conn = redis.StrictRedis(
			host=redis_conf['host'],
			port=redis_conf['port'],
			db=redis_conf['db'],
			charset='utf-8',
			decode_responses=True
		)
	@staticmethod
	def colon_concat(x):
		return ":".join(x)

	def get_annot(self, annotation_type, gene):
		annots = self.redis_conn.smembers(self.colon_concat([self.species, "gene", "annot", annotation_type, gene]))
		if annotation_type.endswith('GOBP'):
			if 'GO:0008150' in annots:
				annots.remove('GO:0008150') # skip GO:0008150biological_process
		return annots

	def get_annot_dict(self, annotation_type, gene):
		annots = self.get_annot(annotation_type, gene)
		ret = []
		for annot in annots:
			annot_desc = self.get_annot_desc(annotation_type, annot)
			ret.append({'id': annot, 'desc': annot_desc})
		return ret

	def get_annot_desc(self, annotation_type, annotation_id):
		return self.redis_conn.get(self.colon_concat([self.species, "geneset", "desc", annotation_type, annotation_id]))

	def get_gene_info(self, gene):
		gene_key = self.colon_concat([self.species, "gene", "info", gene])
		try:
			return self.redis_conn.hgetall(gene_key)
		except:
			return ""

	def get_gene_symbol(self, gene):
		info = self.get_gene_info(gene)
		return info['symbol']

	def get_link_info(self, g1, g2):
		(g1, g2) = sorted([g1, g2])
		link_key = self.colon_concat([self.species, self.network, "link", g1, g2])
		return {k:float(v) for k, v in self.redis_conn.hgetall(link_key).items()}

	def get_neighbors(self, query):
		nbr_key = self.colon_concat([self.species, self.network, "nbr", query])
		return self.redis_conn.smembers(nbr_key)

	def is_in_network(self, query):
		nbr_key =self.colon_concat([self.species, self.network, "nbr", query])
		return self.redis_conn.exists(nbr_key)

	def get_gene_conn_dist(self, valid_gene_cnt, query_conn_cnt):
		if valid_gene_cnt < 4:
			return {}

		ref_fname = config.CONN_DIST_DIR + "/{net}/{num}.cnt".format(
			net=self.network,
			num=valid_gene_cnt
		)
		first_element = [["", "", {'role': 'annotation'}]]
		conn_occur_list = list()
		match = False
		with open(ref_fname) as referencef:
			for line in referencef:
				conn, occur = line.strip().split('\t')
				if int(conn) != query_conn_cnt:
					conn_occur_list.append([int(conn), int(occur), ""])
				else:
					match = True
					conn_occur_list.append([int(conn), int(occur), 'Guide Genes'])

		conn_occur_list.sort(reverse = True)

		upper_sum = 0
		if match:
			for i, j, _ in conn_occur_list:
				upper_sum += j
				if i == query_conn_cnt:
					break
			pvalue = float(upper_sum) / 10000
			pvalue_str = 'p-value=' + str(pvalue)
		else:
			conn_occur_list.append([int(query_conn_cnt), 0, 'Guide Genes'])
			if query_conn_cnt > conn_occur_list[0][0]:
				pvalue_str = 'p-value<0.0001'
			else:
				for i, j, _ in conn_occur_list:
					upper_sum += j
					if i < query_conn_cnt:
						break
				pvalue = float(upper_sum) / 10000
				pvalue_str = 'p-value<' + str(pvalue)

		final_list = first_element + conn_occur_list

		return {'cnt': query_conn_cnt, 'dist': final_list, 'pvalue': pvalue_str}
