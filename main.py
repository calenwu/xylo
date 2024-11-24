from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import ast
import numpy as np
import pandas as pd
import random
import requests
from pymilvus import (
	connections,
	utility,
	FieldSchema,
	Collection,
	CollectionSchema,
	DataType,
)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Enable CORS for all routes
CORS(app, resources={r'/*': {'origins': '*'}})

def string_to_list(s):
	return ast.literal_eval(s)

def df_to_dict_insert(row):
	row_dict = {}
	for col in row.index:
		if col in 'price':
			row_dict[col] = float(row[col])
		elif col in ['name', 'url', 'description', 'Description', 'description_embedding']:
			row_dict[col] = row[col]
		elif col in ['embedding', 'Embedding']:
			row_dict[col] = string_to_list(row[col]) if isinstance(row[col], str) else []
		else:
			try:
				row_dict[col] = [item.strip() for item in row[col].split(',')] if pd.notna(row[col]) else []
			except Exception:
				print(col)
	return row_dict


connections.connect('default', host='localhost', port='19530')
if not utility.has_collection('clothes'):
	collection = Collection('clothes')
	labels = {
		'Style': [
			'Casual',
			'Formal',
			'Bohemian',
			'Vintage',
			'Sporty',
			'Elegant',
			'Streetwear',
			'Minimalist',
			'Preppy',
			'Chic',
			'Punk',
			'Gothic'
		],
		'Occasion': [
			'Beach',
			'Party',
			'Office',
			'Wedding',
			'Date Night',
			'Casual Outing',
			'Vacation',
			'Festival',
			'Brunch',
			'Evening Gala',
			'Concert',
			'Business Meeting'
		],
		'Season': [
			'Summer',
			'Spring',
			'Autumn',
			'Winter',
			'Transitional',
			'All Seasons',
			'Monsoon',
			'Holiday Season',
			'Festival Season',
			'Rainy Season',
			'Cruise',
			'Desert'
		],
		'Color': [
			'White',
			'Black',
			'Blue',
			'Red',
			'Green',
			'Yellow',
			'Pink',
			'Beige',
			'Grey',
			'Purple',
			'Orange',
			'Brown',
			'Teal',
			'Coral',
			'Navy',
			'Olive',
			'Maroon',
			'Turquoise',
			'Mint',
			'Lavender'
			],
		'Pattern': [
			'Striped',
			'Floral',
			'Solid',
			'Polka Dot',
			'Plaid',
			'Animal Print',
			'Geometric',
			'Abstract',
			'Paisley',
			'Chevron',
			'Houndstooth',
			'Tie-Dye'
		],
		'Material': [
			'Linen',
			'Cotton',
			'Silk',
			'Denim',
			'Knit',
			'Chiffon',
			'Satin',
			'Lace',
			'Wool',
			'Polyester',
			'Velvet',
			'Leather'
		],
		'Fit': [
			'Regular Fit',
			'Slim Fit',
			'Loose Fit',
			'Tailored Fit',
			'Relaxed Fit',
			'Oversized Fit',
			'Skinny Fit',
			'Flowy Fit',
			'Boxy Fit',
			'Bodycon Fit',
			'Straight Fit',
			'Tapered Fit'
		],
		'Length': [
			'Mini',
			'Midi',
			'Maxi',
			'Knee-Length',
			'Ankle-Length',
			'Cropped',
			'Full-Length',
			'Tunic-Length',
			'Thigh-Length',
			'Tea-Length',
			'Calf-Length',
			'Floor-Length'
		],
		'Neckline': [
			'V-Neck',
			'Boat Neck',
			'Round Neck',
			'Square Neck',
			'Scoop Neck',
			'Halter Neck',
			'Off Shoulder',
			'High Neck',
			'Sweetheart Neck',
			'Keyhole Neck',
			'Collared Neck',
			'Cowl Neck'
		],
		'Sleeve Type': [
			'Long Sleeve',
			'Short Sleeve',
			'Sleeveless',
			'Cap Sleeve',
			'Balloon Sleeve',
			'Puff Sleeve',
			'Bell Sleeve',
			'3/4 Sleeve',
			'Flutter Sleeve',
			'Kimono Sleeve',
			'Raglan Sleeve',
			'Dolman Sleeve'
		],
		'Silhouette': [
			'A-Line',
			'Sheath',
			'Fit and Flare',
			'Straight',
			'Mermaid',
			'Empire Waist',
			'Peplum',
			'Wrap',
			'Ball Gown',
			'Shift',
			'Trapeze',
			'Bodycon'
		],
		'Texture': [
			'Smooth',
			'Ribbed',
			'Crinkled',
			'Textured',
			'Matte',
			'Shiny',
			'Quilted',
			'Embroidered',
			'Pleated',
			'Fuzzy',
			'Suede',
			'Sheer'
		],
		'Functionality': [
			'Pockets',
			'Adjustable Straps',
			'Drawstring Waist',
			'Elastic Waistband',
			'Built-in Bra',
			'Convertible',
			'Wrinkle-Resistant',
			'Quick-Dry',
			'Breathable',
			'Water-Resistant',
			'Reversible',
			'UV Protection'
		],
		'Closure Type': [
			'Buttoned',
			'Zippered',
			'Hook and Eye',
			'Tied',
			'Pullover',
			'Snap',
			'Velcro',
			'Lace-Up',
			'Buckle',
			'Magnetic',
			'Toggle',
			'Hidden Zip'
		],
		'Embellishments': [
			'Ruffles',
			'Sequins',
			'Beading',
			'Embroidery',
			'Fringe',
			'Lace',
			'Appliques',
			'Studs',
			'Rhinestones',
			'Tassels',
			'Bows',
			'Pearls'
		],
		'Hemline': [
			'Straight Hem',
			'Curved Hem',
			'Asymmetrical Hem',
			'High-Low Hem',
			'Scalloped Hem',
			'Fringed Hem',
			'Raw Hem',
			'Ruffled Hem',
			'Pleated Hem',
			'Layered Hem',
			'Tapered Hem',
			'Handkerchief Hem'
		], 
		'Clothing Category': [
			'Dress',
			'Skirt',
			'Pants',
			'Shorts',
			'Top',
			'Blouse',
			'Shirt',
			'Jacket',
			'Blazer',
			'Vest',
			'Sweater',
			'Cardigan',
			'Coat',
			'Hoodie',
			'Sweatshirt',
			'Tank Top',
			'Singlet',
			'Camisole',
			'Bodysuit',
			'Jumpsuit',
			'Romper',
			'Leggings',
			'Jeans',
			'Tunic',
			'Cape',
			'Poncho',
			'Scarf',
			'Kimono',
			'Wrap',
			'Polo Shirt',
			'Turtleneck',
			'Henley Shirt'
		]
	}
	categories = list(labels.keys()) + ['Description']
	fields = [
		FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, description='primary id'),
		FieldSchema('name', dtype=DataType.VARCHAR, max_length=1024),
		FieldSchema('url', dtype=DataType.VARCHAR, max_length=1024),
		FieldSchema('price', dtype=DataType.FLOAT),
		FieldSchema('imgs', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=512),
		FieldSchema('description', dtype=DataType.VARCHAR, max_length=1024),
		FieldSchema('style', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('occasion', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('season', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('color', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('pattern', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('material', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('fit', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('length', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('neckline', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('sleeve_types', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('silhouette', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('texture', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('functionality', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('closure_type', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('embellishments', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('hemline', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=32, max_length=128),
		FieldSchema('description_embedding', dtype=DataType.VARCHAR, max_length=4096),
		FieldSchema('embedding', dtype=DataType.FLOAT_VECTOR, dim=4096),
	]
	schema = CollectionSchema(
		fields,
		enable_dynamic_field=True,
	)

	csv_file = 'clothes_data_with_descriptions.csv'
	df = pd.read_csv(csv_file)
	column_mapping = {
		'Description': 'description',
		'Style': 'style',
		'Occasion': 'occasion',
		'Season': 'season',
		'Color': 'color',
		'Pattern': 'pattern',
		'Material': 'material',
		'Fit': 'fit',
		'Length': 'length',
		'Neckline': 'neckline',
		'Sleeve Type': 'sleeve_types',
		'Silhouette': 'silhouette',
		'Texture': 'texture',
		'Functionality': 'functionality',
		'Closure Type': 'closure_type',
		'Embellishments': 'embellishments',
		'Hemline': 'hemline',
		'Clothing Category': 'clothing_category',
		'Description Embedding': 'description_embedding',
		'Embedding': 'embedding'
	}
	df.rename(columns=column_mapping, inplace=True)
	clothes = []
	for i in range(len(df)):
		temp = df_to_dict_insert(df.iloc[i])
		temp['id'] = i
		clothes.append(temp)
	categories = list(labels.keys()) + ['Description']
	collection.flush()
	collection.load()
else:
	print('exists')
	collection = Collection('clothes')
	collection.load()

PREFERENCE_DIM = 4096

def search(query_vector, scalar_filter):
	return collection.search(
		data=[query_vector],
		anns_field='embedding',
		param={},
		output_fields=['id', 'name', 'imgs', 'url', 'description', 'price', 'embedding'],
		limit=1,
		expr=scalar_filter
	)

def generate_scalar_filter(selected_item):
	categories = [
		'style', 'occasion', 'season', 'color', 'pattern', 'material', 'fit',
		'length', 'neckline', 'sleeve_types', 'silhouette', 'texture',
		'functionality', 'closure_type', 'embellishments', 'hemline', 'clothing_category'
	]
	filters = []
	for category in categories:
		values = selected_item.get(category)
		if values:
			chance = random.random()
			if chance < 0.05:
				for value in values:
					filters.append(f'{category} != "{value}"')
			elif chance < 0.50:
				values_str = ', '.join([f'"{value}"' for value in values])
				filters.append(f'{category} in [{values_str}]')
	return ' and '.join(filters) if filters else ''

@app.route('/', methods=['GET'])
def get_my_page():
	preference_vector = [0] * PREFERENCE_DIM
	already_seen = []
	scalar_filter = f'id not in {already_seen}' if already_seen else ''
	results = search(preference_vector, scalar_filter)
	if results:
		result_item = results[0][0].entity
		return jsonify({
			'id': result_item.get('id'),
			'name': result_item.get('name'),
			'buy_link': result_item.get('url'),
			'description': result_item.get('description'),
			'price': result_item.get('price'),
			'image_url': result_item.get('imgs')[0] if result_item.get('imgs') else None
		})
	return jsonify({'error': 'No results found'}), 404

@app.route('/', methods=['POST'])
def update_preferences():
	data = request.json
	like = data.get('like')
	preference = data.get('preference')
	already_seen = data.get('already_seen')
	current_item_id = data.get('item_id')

	if preference is None or current_item_id is None:
		return jsonify({'error': 'Missing required fields'}), 400
	results = search(preference, f'id == {current_item_id}')
	if not results:
		return jsonify({'error': 'Item not found'}), 404
	current_item = results[0][0].entity
	embedding = np.array(current_item.get('embedding'))
	preference = np.array(preference)
	if like:
		preference = preference * 0.9 + 0.1 * embedding
	else:
		preference = preference - 0.1 * embedding
	norm = np.linalg.norm(preference)
	if norm != 0:
		preference = preference / norm
	scalar_filter = generate_scalar_filter(current_item)
	if scalar_filter:
		scalar_filter = f'({scalar_filter}) and id not in {already_seen}'
	else:
		scalar_filter = f'id not in {already_seen}'
	results = search(preference, f'id not in {already_seen}')
	if results:
		result_item = results[0][0].entity
		return jsonify({
			'id': result_item.get('id'),
			'name': result_item.get('name'),
			'description': result_item.get('description'),
			'buy_link': result_item.get('url'),
			'price': result_item.get('price'),
			'image_url': result_item.get('imgs')[0] if result_item.get('imgs') else None,
			'preference': preference.tolist()
		})

	return jsonify({'error': 'No results found'}), 404

@app.route('/proxy-image')
def proxy_image():
	image_url = request.args.get('url')
	if not image_url:
		return 'Missing image URL', 400

	response = requests.get(image_url, stream=True)
	headers = {
		'Access-Control-Allow-Origin': '*',
		'Content-Type': response.headers['Content-Type']
	}
	return Response(response.content, headers=headers, status=response.status_code)

if __name__ == '__main__':
	app.run(debug=True)
