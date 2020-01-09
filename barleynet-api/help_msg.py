def get_help():
	help_text = \
	'''
	<h1>Welcome to BarleyNet API Help</h1>

<hr>


<h2>validate-genes</h2>
	Validation of input genes
	<h4>Request</h4>
	<p>
		URL = /validate-genes<br/>
		Method = POST<br/>
		Content-Type = application/json<br/>
		Body = <br/>
		<pre style="border:1px solid gray">
{
	"genes": "HORVU6Hr1G063490 HORVU4Hr1G014120 HORVU2Hr1G005060 ..."
}</pre>
		* genes are separated any white-spaces or comma<br/>
	</p>

	<h4>Response</h4>
	<p>
		Content-Type = application/json<br/>
		Body =
		<pre style="border:1px solid gray">
{
	"invalid": ["notGeneA", "notGeneB"],
	"valid": [
		{
			"geneid": "HORVU6Hr1G063490",
			"mloc": "MLOC_61720"
		},
		{
			"geneid": "HORVU4Hr1G014120",
			"mloc": "MLOC_61350"
		},
		{
			"geneid": "HORVU2Hr1G005060",
			"mloc": "AK366471"
		},
		{
			"geneid": "HORVU7Hr1G002210",
			"mloc": "MLOC_70480"
		},
		{
			"geneid": "HORVU4Hr1G066860",
			"mloc": "MLOC_15134;MLOC_11890"
		},
		...
	]
}</pre>
	</p>
<br/>
<br/>


<h2>Pathway-centric Search</h2>
	Function of Pathway-centric Search on <a href="https://www.inetbio.org/barleynet/search.php">BarleyNet Search</a>.

	<h4>Request</h4>
	<p>
		URL = /pathway-centric<br/>
		Method = POST<br/>
		Content-Type = application/json<br/>
		Body = <br/>
<pre style="border:1px solid gray">
{
	"species": "hvu",
	"network": "BarleyNet",
	"genes": ["HORVU6Hr1G063490", "HORVU4Hr1G014120", "HORVU2Hr1G005060", "HORVU7Hr1G002210", "HORVU4Hr1G066860", ...]
}
</pre>
		<br/>
		* Submit valid genes only using "validate-genes"<br/>
	</p>

	<h4>Response</h4>
	<p>
		Content-Type = application/json<br/>
		example body =
		<pre style="border:1px solid gray">
{
	"gene-info": [
			{
				"annot": {
					"AT-GOBP": [
						{"desc": "reductive pentose-phosphate cycle", "id": "GO:0019253"},
						{"desc": "glucose metabolic process", "id": "GO:0006006"},
						...
					], 
					"GOBP": [...],
					...
				},
				"desc": "glyceraldehyde-3-phosphate dehydrogenase C2",
				"geneid": "HORVU0Hr1G004830",
				"mloc": "AK248329;AK371539",
				"networks": {
					"AT-CC": 6.8836061955,
					"AT-CX": 25.13629627055,
					"HV-CX": 21.31634096226326,
					"HV-GN": 16.3352201916,
					"OS-CX": 9.01538737136
				},
				"sumlls": 33.17740792142834,
				"type": "candidate"
			},
			...
		],
	"link-info": [
			{
				"genes": ["HORVU1Hr1G007720", "HORVU6Hr1G063490"],
				"lls": 1.3599011680460582,
				"networks": {"MM-CX": 2.12802091418}
			},
			{
				"genes": ["HORVU6Hr1G012010", "HORVU6Hr1G063490"],
				"lls": 1.4583665440111608,
				"networks": {"HS-CX": 2.24699175202}
			},
		],
	...
}</pre><br/>
	</p>
<br/>
<br/>


<h2>Gene-centric Search</h2>
	Function of Gene-centric search on <a href="https://www.inetbio.org/barleynet/search.php">BarleyNet Search</a>.
	<h4>Request</h4>
	<p>
		URL = /gene-centric-search<br/>
		Method = POST<br/>
		Content-Type = application/json<br/>
		Body = 
<pre style="border:1px solid gray">
{
	"species": "hvu",
	"network": "BarleyNet",
	"genes": ["HORVU3Hr1G014120", "HORVU1Hr1G070690", "HORVU7Hr1G082040"]
}
</pre>
		<br/>
		* submit valid genes only using "validate-genes"<br/>
	</p>

	<h4>Response</h4>
	<p>
		Content-Type = application/json<br/>
		Body =
		<pre style="border:1px solid gray">
[
	{
		"gene": {
			"geneid": "HORVU3Hr1G014120",
			"mloc": "AK372454;MLOC_36193",
			"desc": "unknown function",
			"annot": [
				{
					"type": "AT-GOBP",
					"result": [{"desc": "stomatal closure", "id": "GO:0090332"},...]
				},
				...
			]
		},
		"result": [
			{
				"type": "GOBP",
				"gcsResult": [
					{"desc": "ATP hydrolysis coupled proton transport", "id": "GO:0015991", "sumlls": 13.883566314915676},
					{"desc": "response to water", "id": "GO:0009415", "sumlls": 6.691846159297824},
					{"desc": "response to stress", "id": "GO:0006950", "sumlls": 6.691846159297824},
					...
				],
			},
			{
				"type": "AT-GOBP",
				"gcsResult": [
					{"desc": "response to water deprivation", "id": "GO:0009414", "sumlls": 12.059485458031485},
					{"desc": "response to abscisic acid", "id": "GO:0009737", "sumlls": 10.616258635332288},
					{"desc": "hydrogen ion transmembrane transport","id": "GO:1902600", "sumlls": 7.730216432055466},
					...
				]
			},
			...
		]
	},
	{...},
	{...}
]
</pre>
</p>
<br/>
<br/>


<h2>Context-centric Search</h2>
	Function of Context-centric Search on <a href="https://www.inetbio.org/barleynet/search.php">BarleyNet Search</a>.
	<h4>Request</h4>
	<p>
		URL = /context-associated-hubs<br/>
		Method = POST<br/>
		Content-Type = application/json<br/>
		Body = 
<pre style="border:1px solid gray">
{
	"species": "hvu",
	"network": "BarleyNet",
	"genes": ["HORVU3Hr1G040870", "HORVU2Hr1G099820", "HORVU2Hr1G112830", "HORVU3Hr1G080100", "HORVU6Hr1G083960", ...]
}
</pre>
		<br/>
		* submit valid genes only using "validate-genes"<br/>
	</p>

	<h4>Response</h4>
	<p>
		Content-Type = application/json<br/>
		Body =
		<pre style="border:1px solid gray">
{
	"result": [
		{
			"DEG": "False",
			"TF": "False",
			"annot": [
				{"type": "AT-GOBP", "result": [{"desc": "response to cold", "id": "GO:0009409"}, ...]},
				...
			],
			"desc": "RNA-binding protein 1",
			"hub": "HORVU5Hr1G053230",
			"pvalue": 2.800040158694128e-06,
			"qvalue": 0.0005460078309453549
		},
		...
	]
}
</pre>
</p>
<br/>
<br/>


<h2>Geneset Analysis</h2>
	Function of geneset analysis.
	
	<h4>Request</h4>
	<p>
		URL = /geneset-analysis<br/>
		Method = POST<br/>
		Content-Type = application/json<br/>
		Body = 
<pre style="border:1px solid gray">
{
	"geneset-types": ["GOBP"],
	"genes": ["HORVU4Hr1G056070", "HORVU5Hr1G113810", "HORVU1Hr1G076190", "HORVU1Hr1G087070", "HORVU6Hr1G028690"]
}
</pre>
		<br/>
		* submit valid genes only using "validate-genes"<br/>
	</p>

	<h4>Response</h4>
	<p>
		Content-Type = application/json<br/>
		Body =
		<pre style="border:1px solid gray">
[
	{
		"result": [
			{
				"adj-pvalue": 3.342732685826037e-06,
				"desc": "protein metabolic process",
				"id": "GO:0019538",
				"pvalue": 8.356831714565093e-07
			},
			{
				"adj-pvalue": 0.0013417864816530648,
				"desc": "protein processing",
				"id": "GO:0016485",
				"pvalue": 0.0007548308843777163
			},
			{
				"adj-pvalue": 0.0013417864816530648,
				"desc": "response to heat",
				"id": "GO:0009408",
				"pvalue": 0.0010063398612397986
			},
			{
				"adj-pvalue": 0.017990534444161137,
				"desc": "protein folding",
				"id": "GO:0006457",
				"pvalue": 0.017990534444161137
			}
		],
		"type": "GOBP"
	}
]
</pre>
</p>
	'''
	return help_text
