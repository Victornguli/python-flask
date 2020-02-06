import os
from flask import request, jsonify, abort
from app.models import BucketList

from app import create_app


app = create_app(os.getenv('APP_SETTINGS'))


@app.route('/bucketlists/', methods = ['POST', 'GET'])
def bucketlists():
	if request.method == 'POST':
		name = str(request.data.get('name'))
		if name:
			bucketlist = BucketList(name = name)
			bucketlist.save()
			response = jsonify({
				'id': bucketlist.id,
				'name': bucketlist.name,
				'date_created': bucketlist.date_created,
				'date_modified': bucketlist.date_modified
			})
			response.status_code = 201
			return response
		else:
			bucketlists = BucketList.get_all()
			results = []

			for bucketlist in bucketlists:
				obj = {
					'id': bucketlist.id,
					'name': bucketlist.name,
					'date_created': bucketlist.date_created,
					'date_modified': bucketlist.date_modified
				}
				results.append(obj)
			response = jsonify(results)
			response.status_code = 200
			return response

