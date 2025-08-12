from flask import Blueprint, request, jsonify
import json

helpline_bp = Blueprint('helpline', __name__)

def load_helpline_data():
    with open('data/helpline.json', 'r') as f:
        return json.load(f)

@helpline_bp.route('', methods=['GET'])
@helpline_bp.route('/', methods=['GET'])
def get_helpline_numbers():
    state = request.args.get('state')
    
    if not state:
        return jsonify({'error': 'state parameter is required'}), 400
    
    helpline_data = load_helpline_data()
    helplines = helpline_data.get('helplines', [])
    
    # Filter helplines for the requested state (both Central and State-specific)
    state_helplines = []
    for helpline in helplines:
        if helpline['level'] == 'Central' or (helpline['level'] == 'State' and helpline['state'] == state):
            state_helplines.append(helpline)
    
    if not state_helplines:
        return jsonify({'error': f'Helpline data not available for {state}'}), 404
    
    return jsonify({
        'state': state,
        'helplines': state_helplines
    }), 200 