from flask import Flask, render_template, request, jsonify
from controller import lab_census_system
from controller import verbose

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        school = data.get('school')
        name = data.get('name')
        sample_count = int(data.get('sample_count'))
        filter_cnt = data.get('filter_cnt', '')

        LCS = lab_census_system.LabCensusSystem(school, name, sample_count, filter_cnt)
        verbose_input = LCS.Search()
        res = LCS.Show()

        result = {
            'sample_count': sample_count,
            'graduate_2_years': res[0],
            'graduate_2_3_years': res[1],
            'graduate_3_plus_years': res[2]
        }

        V = verbose.VerboseBooster(name, sample_count, res, verbose_input)
        detailed_data = V.get_data()  # 需要在 verbose.py 中新增此方法
        result['detailed_data'] = detailed_data

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run() 