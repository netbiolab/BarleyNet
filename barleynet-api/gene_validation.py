import config
import re

def validate(user_genes):
	genelist_file = config.GENELIST_FILE
	mloc2gene_file = config.LEGACY_GENE_FILE

	genelist = set( [line.strip() for line in open(genelist_file)] )

	mloc2gene = dict()
	gene2mloc = dict()

	with open(mloc2gene_file) as mloc2gene_f:
		for line in mloc2gene_f:
			mloc, gene = line.split('\t')
			mloc = mloc.strip()
			gene = gene.strip()
			if mloc not in mloc2gene:
				mloc2gene[mloc] = gene
			try:
				gene2mloc[gene].add(mloc)
			except KeyError:
				gene2mloc[gene] = set([mloc])

	# replace to tokenize
	delimeters = [",", "\t", " ", "\n"]
	input_elements = re.split("|".join(delimeters), user_genes)

	valid_genes = list()
	invalid_genes = list()

	for user_gene in input_elements:
		if user_gene in genelist:
			mloc = '' if user_gene not in gene2mloc else ';'.join(gene2mloc[user_gene])
			valid_genes.append( {'geneid': user_gene, 'mloc': mloc} )
		elif user_gene in mloc2gene:
			valid_genes.append( {'geneid': user_gene, 'mloc': mloc2gene[user_gene]} )
		elif user_gene != "":
			invalid_genes.append(user_gene)
	
	return {'valid': valid_genes, 'invalid': invalid_genes}