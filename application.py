from flask import Flask, render_template, request, jsonify
from controller import lab_census_system, verbose

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    try:
        data = request.get_json()
        school = data.get('school')
        name = data.get('name', '').strip()
        sample_count = int(data.get('sample_count', 0))
        filter_cnt = int(data.get('filter_cnt', 0))
        departments = data.get('departments', [])

        if not school or not name or sample_count <= 0:
            return jsonify({'error': '請檢查輸入資料'}), 400

        LCS = lab_census_system.LabCensusSystem(str(school), name, sample_count, filter_cnt)
        verbose_input = LCS.Search()
        if not verbose_input:
            return jsonify({'error': '找不到相關資料'}), 404
            
        res = LCS.Show()

        V = verbose.VerboseBooster(name, sample_count, res, verbose_input)
        detailed_results = V.show()

        result = {
            'sample_count': sample_count,
            'graduate_2_years': res[0],
            'graduate_2_3_years': res[1],
            'graduate_3_plus_years': res[2],
            'detailed_results': detailed_results
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'系統錯誤：{str(e)}'}), 500

@app.route('/search', methods=['POST'])
def search():
    return index()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000) 