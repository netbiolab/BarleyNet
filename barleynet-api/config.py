# REDIS SERVER CONNECTION (REDIS v4.0.x)
REDIS_SERVER = {
	'host': 'localhost',
	'port': 6379,
	'db': 0
}

# GENE VALIDATION
GENELIST_FILE = "../data/gene/barleynet_highconf_gene_list"
LEGACY_GENE_FILE = "../data/gene/mloc_to_horvu_gene"

# GENE NETWORK
# precalculation-random-
CONN_DIST_DIR = "../data/connectivity_distribution"

# GENE CENTRIC
ANNOTATIONS = ['GOBP', 'AT-GOBP', 'OS-GOBP', 'ZM-GOBP']
GENOMECNT = 39734

# GENSET ANALYSIS
GENESETFILE = {
	'GOBP': '../data/geneset/barleynet_gsa_BP',
	'GOCC': '../data/geneset/barleynet_gsa_CC',
	'GOMF': '../data/geneset/barleynet_gsa_MF',
	'AT-GOBP': '../data/extra_gobp_files/bnetv4_arabidopsis_BP_GOtable_for_GSA.tsv',
	'OS-GOBP': '../data/extra_gobp_files/bnetv4_rice_BP_GOtable_for_GSA.tsv',
	'ZM-GOBP': '../data/extra_gobp_files/bnetv4_maize_BP_GOtable_for_GSA.tsv'
}

# FDR Correction Alpha
ADJ_ALPHA = 0.05

# CONTEXT CENTRIC
REGULON = '../data/cah/simple_v4_hubs'
TF = '../data/cah/barley_tf_IBSCv2.txt'


